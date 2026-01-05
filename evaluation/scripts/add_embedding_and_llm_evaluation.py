#!/usr/bin/env python3
"""
Add Embedding-Based and LLM-Based Evaluation to Existing Results

This script reads existing evaluation results CSV files and adds:
1. Semantic similarity scores using embeddings (Ollama with nomic-embed-text model)
2. LLM-based evaluation using a generative model to judge if texts discuss the same topic (Ollama with llama3.2)

Usage:
    python add_embedding_and_llm_evaluation.py Q01_out.csv
    python add_embedding_and_llm_evaluation.py Q01_out.csv -o Q01_with_embeddings.csv
    python add_embedding_and_llm_evaluation.py Q01_out.csv --threshold 0.75
    python add_embedding_and_llm_evaluation.py Q01_out.csv --llm-model llama3.2
    python add_embedding_and_llm_evaluation.py ../results/*.csv  # Process multiple files

Requirements:
    pip install ollama scikit-learn numpy pandas
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import re

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Install with: pip install pandas")
    sys.exit(1)

try:
    import ollama
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SEMANTIC_AVAILABLE = True
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install ollama scikit-learn numpy")
    sys.exit(1)


class EmbeddingEvaluator:
    """Evaluates semantic similarity using embeddings.
    
    NOTE: Currently using chunking for long texts because available embedding models
    (nomic-embed-text, etc) have a context limit of ~8K tokens.
    
    TODO: Consider using a long-context embedding model when available
    
    Chunking works but may lose semantic coherence for very long responses.
    A model with 32K+ token context would be preferable for full-text embeddings.
    """
    
    def __init__(self, model: str = "nomic-embed-text", threshold: float = 0.75):
        """
        Initialize embedding evaluator.
        
        Args:
            model: Ollama embedding model name
            threshold: Cosine similarity threshold for semantic match (0.0-1.0)
        """
        self.model = model
        self.threshold = threshold
        self._cache: Dict[str, np.ndarray] = {}
        self._max_chars = 6000  # Safe limit for nomic-embed-text (~8K tokens)
        self._chunk_size = 4000  # Chunk size for long texts
        
    def _get_embedding_single(self, text: str) -> Optional[np.ndarray]:
        """Get embedding for a single text chunk."""
        try:
            response = ollama.embed(model=self.model, input=text)
            if hasattr(response, 'embeddings'):
                return np.array(response.embeddings[0])
            elif isinstance(response, dict) and 'embeddings' in response:
                return np.array(response['embeddings'][0])
            elif isinstance(response, dict) and 'embedding' in response:
                return np.array(response['embedding'])
            return None
        except Exception as e:
            print(f"  Warning: Embedding failed: {e}")
            return None
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks for long text embedding.
        
        Strategy: Extract beginning, middle, and end of text to capture
        key information. First chunk is weighted more heavily since
        LLM responses typically put the main answer at the beginning.
        
        TODO: A long-context embedding model (32K+ tokens) would eliminate
        the need for chunking and provide more accurate semantic similarity.
        """
        chunks = []
        # First chunk: beginning (usually has the main answer)
        chunks.append(text[:self._chunk_size])
        
        # Middle chunks if text is very long
        if len(text) > self._chunk_size * 2:
            mid_start = len(text) // 2 - self._chunk_size // 2
            chunks.append(text[mid_start:mid_start + self._chunk_size])
        
        # Last chunk: end (may have conclusions)
        if len(text) > self._chunk_size:
            chunks.append(text[-self._chunk_size:])
        
        return chunks
        
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding vector for text using Ollama with caching.
        
        For short texts (<6000 chars): embeds directly.
        For long texts: uses chunking and weighted average of embeddings.
        
        NOTE: Chunking is a workaround for the 8K token limit of current models.
        Consider switching to a long-context embedding model when available.
        """
        if not text or not text.strip():
            return None
            
        # Check cache
        cache_key = text.lower().strip()[:500]  # Use first 500 chars as cache key
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Short text: embed directly
        if len(text) <= self._max_chars:
            embedding = self._get_embedding_single(text)
            if embedding is not None:
                self._cache[cache_key] = embedding
            return embedding
        
        # Long text: chunk and average embeddings
        # TODO: Replace with long-context embedding model (32K+ tokens) when available
        print(f"(long text: {len(text)} chars, using chunking)", end=" ")
        chunks = self._chunk_text(text)
        embeddings = []
        
        for chunk in chunks:
            emb = self._get_embedding_single(chunk)
            if emb is not None:
                embeddings.append(emb)
        
        if not embeddings:
            return None
        
        # Average all chunk embeddings (weighted: first chunk gets more weight)
        # First chunk weighted 2x because LLM responses typically start with the answer
        weights = [2.0] + [1.0] * (len(embeddings) - 1)
        weighted_sum = sum(w * e for w, e in zip(weights, embeddings))
        avg_embedding = weighted_sum / sum(weights)
        
        self._cache[cache_key] = avg_embedding
        return avg_embedding
    
    def compute_similarity(self, response_text: str, expected_answer: str) -> Dict[str, Any]:
        """
        Compute semantic similarity between response and expected answer.
        
        Returns:
            Dict with:
                - semantic_similarity: float (0.0-1.0)
                - semantic_found: bool (similarity >= threshold)
                - error: Optional[str]
        """
        result = {
            "semantic_similarity": 0.0,
            "semantic_found": False,
            "error": None
        }
        
        if not response_text or not expected_answer:
            result["error"] = "Empty text"
            return result
        
        # Get embeddings
        emb_response = self._get_embedding(response_text)
        emb_expected = self._get_embedding(expected_answer)
        
        if emb_response is None or emb_expected is None:
            result["error"] = "Failed to get embeddings"
            return result
        
        # Compute cosine similarity
        try:
            similarity = cosine_similarity(
                emb_expected.reshape(1, -1),
                emb_response.reshape(1, -1)
            )[0][0]
            
            result["semantic_similarity"] = float(similarity)
            result["semantic_found"] = similarity >= self.threshold
            
        except Exception as e:
            result["error"] = str(e)
        
        return result


class LLMEvaluator:
    """Evaluates if two texts discuss the same topic using a generative LLM.
    
    Uses Ollama with a generative model (e.g., llama3.2, mistral) to determine
    if the response text contains the expected answer or discusses the same topic.
    """
    
    def __init__(self, model: str = "llama3.2"):
        """
        Initialize LLM evaluator.
        
        Args:
            model: Ollama generative model name (e.g., llama3.2, mistral, gemma2)
        """
        self.model = model
    
    def evaluate_match(self, response_text: str, expected_answer: str) -> Dict[str, Any]:
        """
        Use LLM to evaluate if response contains or discusses the expected answer.
        
        Args:
            response_text: The LLM response to evaluate
            expected_answer: The expected answer to find
            
        Returns:
            Dict with:
                - llm_match: bool (True if LLM judges it as a match)
                - llm_confidence: str ('high', 'medium', 'low')
                - llm_explanation: str (brief explanation)
                - error: Optional[str]
        """
        result = {
            "llm_match": False,
            "llm_confidence": "low",
            "llm_explanation": "",
            "error": None
        }
        
        if not response_text or not expected_answer:
            result["error"] = "Empty text"
            return result
        
        # Build prompt for LLM evaluation
        prompt = f"""You are an expert evaluator. Your task is to determine if a RESPONSE text contains or discusses the same information as an EXPECTED ANSWER.

    EXPECTED ANSWER:
    {expected_answer}

    RESPONSE TEXT:
    {response_text}

    Analyze if the RESPONSE contains the key information from the EXPECTED ANSWER. The response may have additional details, but the core information should match.

    Respond in this EXACT format (nothing else):
    MATCH: [YES/NO]
    CONFIDENCE: [HIGH/MEDIUM/LOW]
    REASON: [One brief sentence explaining why]

    Rules:
    - MATCH=YES if the response contains the expected information (even if phrased differently)
    - MATCH=NO if the response doesn't address the expected answer or gives wrong information
    - CONFIDENCE=HIGH if you're very sure, MEDIUM if somewhat sure, LOW if uncertain"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}  # Low temperature for consistent evaluation
            )
            
            # Parse response
            llm_output = response.get('message', {}).get('content', '')
            
            # Extract MATCH
            match_line = re.search(r'MATCH:\s*(YES|NO)', llm_output, re.IGNORECASE)
            if match_line:
                result["llm_match"] = match_line.group(1).upper() == "YES"
            
            # Extract CONFIDENCE
            conf_line = re.search(r'CONFIDENCE:\s*(HIGH|MEDIUM|LOW)', llm_output, re.IGNORECASE)
            if conf_line:
                result["llm_confidence"] = conf_line.group(1).lower()
            
            # Extract REASON
            reason_line = re.search(r'REASON:\s*(.+)', llm_output, re.IGNORECASE)
            if reason_line:
                result["llm_explanation"] = reason_line.group(1).strip()[:200]  # Limit length
                
        except Exception as e:
            result["error"] = str(e)
        
        return result


def evaluate_row(row: Dict, embedding_evaluator: 'EmbeddingEvaluator', llm_evaluator: Optional['LLMEvaluator'] = None) -> Dict[str, Any]:
    """
    Evaluate a single row from the results CSV.
    
    Args:
        row: Dictionary containing CSV row data
        embedding_evaluator: EmbeddingEvaluator for semantic similarity
        llm_evaluator: Optional LLMEvaluator for generative model evaluation
        
    Returns:
        Dict with new columns to add:
            - baseline_semantic_similarity
            - baseline_semantic_found
            - togomcp_semantic_similarity  
            - togomcp_semantic_found
            - combined_baseline_found (token OR semantic)
            - combined_togomcp_found (token OR semantic)
            - baseline_llm_match (if llm_evaluator provided)
            - baseline_llm_confidence (if llm_evaluator provided)
            - togomcp_llm_match (if llm_evaluator provided)
            - togomcp_llm_confidence (if llm_evaluator provided)
    """
    expected = row.get('expected_answer', '')
    baseline_text = row.get('baseline_text', '')
    togomcp_text = row.get('togomcp_text', '')
    
    # Evaluate baseline response
    baseline_result = embedding_evaluator.compute_similarity(baseline_text, expected)
    
    # Evaluate togomcp response  
    togomcp_result = embedding_evaluator.compute_similarity(togomcp_text, expected)
    
    # Combine with existing token-based results
    baseline_token_found = str(row.get('baseline_has_expected', 'False')).lower() == 'true'
    togomcp_token_found = str(row.get('togomcp_has_expected', 'False')).lower() == 'true'
    
    result = {
        "baseline_semantic_similarity": baseline_result["semantic_similarity"],
        "baseline_semantic_found": baseline_result["semantic_found"],
        "togomcp_semantic_similarity": togomcp_result["semantic_similarity"],
        "togomcp_semantic_found": togomcp_result["semantic_found"],
        "combined_baseline_found": baseline_token_found or baseline_result["semantic_found"],
        "combined_togomcp_found": togomcp_token_found or togomcp_result["semantic_found"],
        "baseline_max_confidence": max(
            float(row.get('baseline_confidence', 0)), 
            baseline_result["semantic_similarity"]
        ),
        "togomcp_max_confidence": max(
            float(row.get('togomcp_confidence', 0)), 
            togomcp_result["semantic_similarity"]
        )
    }
    
    # Add LLM evaluation if evaluator is provided
    if llm_evaluator is not None:
        baseline_llm = llm_evaluator.evaluate_match(baseline_text, expected)
        togomcp_llm = llm_evaluator.evaluate_match(togomcp_text, expected)
        
        result.update({
            "baseline_llm_match": baseline_llm["llm_match"],
            "baseline_llm_confidence": baseline_llm["llm_confidence"],
            "baseline_llm_explanation": baseline_llm["llm_explanation"],
            "togomcp_llm_match": togomcp_llm["llm_match"],
            "togomcp_llm_confidence": togomcp_llm["llm_confidence"],
            "togomcp_llm_explanation": togomcp_llm["llm_explanation"],
            # Combined with LLM: token OR semantic OR llm
            "full_combined_baseline_found": (
                baseline_token_found or 
                baseline_result["semantic_found"] or 
                baseline_llm["llm_match"]
            ),
            "full_combined_togomcp_found": (
                togomcp_token_found or 
                togomcp_result["semantic_found"] or 
                togomcp_llm["llm_match"]
            )
        })
    
    return result


def process_csv(
    input_path: Path, 
    output_path: Optional[Path], 
    evaluator: EmbeddingEvaluator,
    llm_evaluator: Optional[LLMEvaluator] = None,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Process a CSV file and add embedding evaluation columns.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file (None = modify in place)
        evaluator: EmbeddingEvaluator instance
        llm_evaluator: Optional LLMEvaluator for generative model evaluation
        verbose: Print progress
        
    Returns:
        DataFrame with added columns
    """
    if verbose:
        print(f"\nProcessing: {input_path}")
    
    # Read CSV
    df = pd.read_csv(input_path)
    
    if verbose:
        print(f"  Found {len(df)} rows")
    
    # New columns to add
    new_columns = {
        "baseline_semantic_similarity": [],
        "baseline_semantic_found": [],
        "togomcp_semantic_similarity": [],
        "togomcp_semantic_found": [],
        "combined_baseline_found": [],
        "combined_togomcp_found": [],
        "baseline_max_confidence": [],
        "togomcp_max_confidence": []
    }
    
    # Add LLM columns if evaluator provided
    if llm_evaluator is not None:
        new_columns.update({
            "baseline_llm_match": [],
            "baseline_llm_confidence": [],
            "baseline_llm_explanation": [],
            "togomcp_llm_match": [],
            "togomcp_llm_confidence": [],
            "togomcp_llm_explanation": [],
            "full_combined_baseline_found": [],
            "full_combined_togomcp_found": []
        })
    
    # Process each row
    for idx, row in df.iterrows():
        if verbose:
            question_id = row.get('question_id', idx)
            print(f"  Evaluating Q{question_id}...", end=" ")
        
        result = evaluate_row(row.to_dict(), evaluator, llm_evaluator)
        
        for col, value in result.items():
            if col in new_columns:
                new_columns[col].append(value)
        
        if verbose:
            baseline_sim = result["baseline_semantic_similarity"]
            togomcp_sim = result["togomcp_semantic_similarity"]
            msg = f"baseline={baseline_sim:.3f}, togomcp={togomcp_sim:.3f}"
            if llm_evaluator:
                baseline_llm = result.get("baseline_llm_match", False)
                togomcp_llm = result.get("togomcp_llm_match", False)
                msg += f" | LLM: base={baseline_llm}, togo={togomcp_llm}"
            print(msg)
    
    # Add new columns to DataFrame
    for col, values in new_columns.items():
        df[col] = values
    
    # Save to output
    save_path = output_path or input_path
    df.to_csv(save_path, index=False)
    
    if verbose:
        print(f"  Saved to: {save_path}")
    
    return df


def print_summary(df: pd.DataFrame, filename: str):
    """Print evaluation summary statistics."""
    print(f"\n{'='*60}")
    print(f"Summary for {filename}")
    print(f"{'='*60}")
    
    total = len(df)
    
    # Baseline metrics
    baseline_token = df['baseline_has_expected'].sum() if 'baseline_has_expected' in df.columns else 0
    baseline_semantic = df['baseline_semantic_found'].sum()
    baseline_combined = df['combined_baseline_found'].sum()
    baseline_avg_sim = df['baseline_semantic_similarity'].mean()
    
    # TogoMCP metrics
    togomcp_token = df['togomcp_has_expected'].sum() if 'togomcp_has_expected' in df.columns else 0
    togomcp_semantic = df['togomcp_semantic_found'].sum()
    togomcp_combined = df['combined_togomcp_found'].sum()
    togomcp_avg_sim = df['togomcp_semantic_similarity'].mean()
    
    print(f"\nBaseline Results (n={total}):")
    print(f"  Token-based matches:    {baseline_token:3d} ({100*baseline_token/total:.1f}%)")
    print(f"  Semantic matches:       {baseline_semantic:3d} ({100*baseline_semantic/total:.1f}%)")
    print(f"  Combined matches:       {baseline_combined:3d} ({100*baseline_combined/total:.1f}%)")
    print(f"  Avg semantic similarity: {baseline_avg_sim:.3f}")
    
    print(f"\nTogoMCP Results (n={total}):")
    print(f"  Token-based matches:    {togomcp_token:3d} ({100*togomcp_token/total:.1f}%)")
    print(f"  Semantic matches:       {togomcp_semantic:3d} ({100*togomcp_semantic/total:.1f}%)")
    print(f"  Combined matches:       {togomcp_combined:3d} ({100*togomcp_combined/total:.1f}%)")
    print(f"  Avg semantic similarity: {togomcp_avg_sim:.3f}")
    
    # LLM metrics if available
    if 'baseline_llm_match' in df.columns:
        baseline_llm = df['baseline_llm_match'].sum()
        togomcp_llm = df['togomcp_llm_match'].sum()
        baseline_full = df['full_combined_baseline_found'].sum() if 'full_combined_baseline_found' in df.columns else baseline_combined
        togomcp_full = df['full_combined_togomcp_found'].sum() if 'full_combined_togomcp_found' in df.columns else togomcp_combined
        
        print(f"\nLLM-Based Evaluation:")
        print(f"  Baseline LLM matches:   {baseline_llm:3d} ({100*baseline_llm/total:.1f}%)")
        print(f"  TogoMCP LLM matches:    {togomcp_llm:3d} ({100*togomcp_llm/total:.1f}%)")
        print(f"\nFull Combined (Token OR Semantic OR LLM):")
        print(f"  Baseline full combined: {baseline_full:3d} ({100*baseline_full/total:.1f}%)")
        print(f"  TogoMCP full combined:  {togomcp_full:3d} ({100*togomcp_full/total:.1f}%)")

def main():
    parser = argparse.ArgumentParser(
        description="Add embedding-based and LLM-based evaluation to existing results CSV files"
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        help="Input CSV file(s) to process"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output CSV file (only valid for single input file)"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.75,
        help="Semantic similarity threshold (default: 0.75)"
    )
    parser.add_argument(
        "-m", "--model",
        default="nomic-embed-text",
        help="Ollama embedding model (default: nomic-embed-text)"
    )
    parser.add_argument(
        "--llm-model",
        default=None,
        help="Ollama generative model for LLM evaluation (e.g., llama3.2, mistral, gemma2). If not set, LLM evaluation is skipped."
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Modify input files in place (default behavior if no -o specified)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Don't print summary statistics"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.output and len(args.input_files) > 1:
        print("Error: Cannot use -o with multiple input files")
        sys.exit(1)
    
    # Initialize evaluators
    print(f"Initializing embedding evaluator...")
    print(f"  Embedding model: {args.model}")
    print(f"  Threshold: {args.threshold}")
    
    evaluator = EmbeddingEvaluator(model=args.model, threshold=args.threshold)
    
    # Initialize LLM evaluator if specified
    llm_evaluator = None
    if args.llm_model:
        print(f"  LLM model: {args.llm_model}")
        llm_evaluator = LLMEvaluator(model=args.llm_model)
    else:
        print(f"  LLM evaluation: disabled (use --llm-model to enable)")
    
    # Process each file
    all_dfs = []
    for input_file in args.input_files:
        input_path = Path(input_file)
        
        if not input_path.exists():
            print(f"Warning: File not found: {input_path}")
            continue
        
        output_path = Path(args.output) if args.output else None
        
        df = process_csv(
            input_path, 
            output_path, 
            evaluator,
            llm_evaluator,
            verbose=not args.quiet
        )
        all_dfs.append((input_path.name, df))
    
    # Print summaries
    if not args.no_summary:
        for filename, df in all_dfs:
            print_summary(df, filename)
    
    print(f"\n✓ Processing complete!")


if __name__ == "__main__":
    main()
