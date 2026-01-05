# Embedding-Based Evaluation Guide

This guide explains how to use the `add_embedding_evaluation.py` script to add semantic similarity scores to existing evaluation results.

## Prerequisites

### 1. Install Ollama

Ollama is required to generate embeddings locally.

**Windows:**
```powershell
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Or download directly from: https://ollama.com/download

### 2. Start Ollama Server

After installation, ensure Ollama is running:

```bash
ollama serve
```

On Windows, Ollama typically starts automatically after installation.

### 3. Download the Embedding Model

Pull the `nomic-embed-text` model (recommended for semantic similarity):

```bash
ollama pull nomic-embed-text
```

This model is ~274MB and provides high-quality embeddings for text similarity tasks.

### 4. Install Python Dependencies

```bash
pip install ollama scikit-learn numpy pandas
```

## Usage

### Basic Usage

Process a single CSV file and save with embeddings:

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv -o ../results/Q01_with_embeddings.csv
```

### Modify In-Place

Update the original file directly:

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv --inplace
```

### Process Multiple Files

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv ../results/Q02_out.csv ../results/Q11_out.csv
```

### Custom Threshold

Adjust the semantic similarity threshold (default: 0.75):

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv -t 0.6
```

### Use Different Model

Use an alternative Ollama embedding model:

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv -m mxbai-embed-large
```

### Quiet Mode (No Progress Output)

```bash
python add_embedding_evaluation.py ../results/Q01_out.csv -q
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output CSV file path (only for single input) |
| `-t, --threshold` | Semantic similarity threshold (0.0-1.0, default: 0.75) |
| `-m, --model` | Ollama embedding model (default: nomic-embed-text) |
| `--inplace` | Modify input files in place |
| `-q, --quiet` | Suppress progress output |
| `--no-summary` | Don't print summary statistics |

## Output Columns

The script adds the following columns to the CSV:

| Column | Description |
|--------|-------------|
| `baseline_semantic_similarity` | Cosine similarity between baseline response and expected answer (0.0-1.0) |
| `baseline_semantic_found` | True if similarity >= threshold |
| `togomcp_semantic_similarity` | Cosine similarity between TogoMCP response and expected answer (0.0-1.0) |
| `togomcp_semantic_found` | True if similarity >= threshold |
| `combined_baseline_found` | True if token-based OR semantic match found for baseline |
| `combined_togomcp_found` | True if token-based OR semantic match found for TogoMCP |
| `baseline_max_confidence` | Maximum of token confidence and semantic similarity |
| `togomcp_max_confidence` | Maximum of token confidence and semantic similarity |

## Example Output

```
Initializing embedding evaluator...
  Model: nomic-embed-text
  Threshold: 0.75

Processing: Q01_out.csv
  Found 12 rows
  Evaluating Q1... baseline=0.565, togomcp=0.554
  Evaluating Q2... baseline=0.438, togomcp=0.432
  ...
  Saved to: Q01_with_embeddings.csv

============================================================
Summary for Q01_out.csv
============================================================

Baseline Results (n=12):
  Token-based matches:      6 (50.0%)
  Semantic matches:         0 (0.0%)
  Combined matches:         6 (50.0%)
  Avg semantic similarity: 0.524

TogoMCP Results (n=12):
  Token-based matches:     10 (83.3%)
  Semantic matches:         0 (0.0%)
  Combined matches:        10 (83.3%)
  Avg semantic similarity: 0.541

Improvement Analysis:
  TogoMCP advantage (combined): +4 questions
  Relative improvement: +66.7%

✓ Processing complete!
```

## Troubleshooting

### "Failed to connect to Ollama"

Ensure Ollama is running:
```bash
ollama serve
```

Or on Windows, check if Ollama is in your PATH:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
ollama --version
```

### Model Not Found

Pull the required model:
```bash
ollama pull nomic-embed-text
```

### Low Semantic Similarity Scores

- The default threshold (0.75) may be too high for short expected answers
- Try lowering with `-t 0.6` or `-t 0.5`
- Short answers like IDs (e.g., "Q99ZW2") may not benefit from semantic matching

## Alternative Models

Other embedding models available in Ollama:

| Model | Size | Notes |
|-------|------|-------|
| `nomic-embed-text` | 274MB | Default, good balance of quality/speed |
| `mxbai-embed-large` | 670MB | Higher quality, slower |
| `all-minilm` | 46MB | Lightweight, faster |
| `snowflake-arctic-embed` | 335MB | Good for retrieval tasks |

List available models:
```bash
ollama list
```
