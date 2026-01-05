#!/usr/bin/env python3
"""
Add Embedding-Based Evaluation to Existing Results

This script reads existing evaluation results CSV files and adds semantic
similarity scores using embeddings (Ollama with nomic-embed-text model).

Usage:
    python add_embedding_evaluation.py Q01_out.csv
    python add_embedding_evaluation.py Q01_out.csv -o Q01_with_embeddings.csv
    python add_embedding_evaluation.py Q01_out.csv --threshold 0.75
    python add_embedding_evaluation.py ../results/*.csv  # Process multiple files

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
    """Evaluates semantic similarity using embeddings."""
    
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
        
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding vector for text using Ollama with caching."""
        if not text or not text.strip():
            return None
            
        # Check cache
        cache_key = text.lower().strip()
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            response = ollama.embed(model=self.model, input=text)
            # Handle both old and new ollama API response formats
            if hasattr(response, 'embeddings'):
                embedding = np.array(response.embeddings[0])
            elif isinstance(response, dict) and 'embeddings' in response:
                embedding = np.array(response['embeddings'][0])
            elif isinstance(response, dict) and 'embedding' in response:
                embedding = np.array(response['embedding'])
            else:
                return None
            
            # Cache the result
            self._cache[cache_key] = embedding
            return embedding
            
        except Exception as e:
            print(f"  Warning: Embedding failed: {e}")
            return None
    
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
    
    def evaluate_row(self, row: Dict) -> Dict[str, Any]:
        """
        Evaluate a single row from the results CSV.
        
        Args:
            row: Dictionary containing CSV row data
            
        Returns:
            Dict with new columns to add:
                - baseline_semantic_similarity
                - baseline_semantic_found
                - togomcp_semantic_similarity  
                - togomcp_semantic_found
                - combined_baseline_found (token OR semantic)
                - combined_togomcp_found (token OR semantic)
        """
        expected = row.get('expected_answer', '')
        baseline_text = row.get('baseline_text', '')
        togomcp_text = row.get('togomcp_text', '')
        
        # Evaluate baseline response
        baseline_result = self.compute_similarity(baseline_text, expected)
        
        # Evaluate togomcp response  
        togomcp_result = self.compute_similarity(togomcp_text, expected)
        
        # Combine with existing token-based results
        baseline_token_found = str(row.get('baseline_has_expected', 'False')).lower() == 'true'
        togomcp_token_found = str(row.get('togomcp_has_expected', 'False')).lower() == 'true'
        
        return {
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


def process_csv(
    input_path: Path, 
    output_path: Optional[Path], 
    evaluator: EmbeddingEvaluator,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Process a CSV file and add embedding evaluation columns.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file (None = modify in place)
        evaluator: EmbeddingEvaluator instance
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
    
    # Process each row
    for idx, row in df.iterrows():
        if verbose:
            question_id = row.get('question_id', idx)
            print(f"  Evaluating Q{question_id}...", end=" ")
        
        result = evaluator.evaluate_row(row.to_dict())
        
        for col, value in result.items():
            new_columns[col].append(value)
        
        if verbose:
            baseline_sim = result["baseline_semantic_similarity"]
            togomcp_sim = result["togomcp_semantic_similarity"]
            print(f"baseline={baseline_sim:.3f}, togomcp={togomcp_sim:.3f}")
    
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
    
    # Improvement analysis
    improvement = togomcp_combined - baseline_combined
    print(f"\nImprovement Analysis:")
    print(f"  TogoMCP advantage (combined): {improvement:+d} questions")
    print(f"  Relative improvement: {100*(togomcp_combined - baseline_combined)/max(1, baseline_combined):+.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description="Add embedding-based evaluation to existing results CSV files"
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
    
    # Initialize evaluator
    print(f"Initializing embedding evaluator...")
    print(f"  Model: {args.model}")
    print(f"  Threshold: {args.threshold}")
    
    evaluator = EmbeddingEvaluator(model=args.model, threshold=args.threshold)
    
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
