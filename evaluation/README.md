# TogoMCP Evaluation Framework

Comprehensive evaluation suite for testing TogoMCP's biological database query capabilities across 22 specialized databases.

---

## 🎯 Quick Start

```bash
# 1. Setup
cd scripts
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"

# 2. Run evaluation on a question set
python automated_test_runner.py ../questions/Q01.json

# 3. Analyze costs and results
python compute_costs.py evaluation_results.csv
python results_analyzer.py evaluation_results.csv -v
python generate_dashboard.py evaluation_results.csv --open
```

**New here?** → Read the [5-minute overview](#5-minute-overview) below.

---

## 📖 Table of Contents

- [5-Minute Overview](#5-minute-overview)
- [Project Structure](#project-structure)
- [The Evaluation Suite](#the-evaluation-suite)
  - [120 Test Questions](#120-test-questions)
  - [22 Biological Databases](#22-biological-databases)
  - [6 Question Categories](#6-question-categories)
- [Getting Started](#getting-started)
- [Common Use Cases](#common-use-cases)
- [Documentation Guide](#documentation-guide)
- [Cost Analysis](#cost-analysis)
- [Understanding Results](#understanding-results)
- [Project Status](#project-status)
- [Contributing](#contributing)

---

## 5-Minute Overview

### What Is This?

This evaluation framework systematically tests how well TogoMCP (Model Context Protocol for biological databases) improves Claude's ability to answer life sciences research questions.

**The Test Design**: Ask Claude the same question twice:
1. **Baseline**: Without access to any database tools
2. **TogoMCP**: With access to 22 biological databases via MCP

**The Goal**: Quantify the improvement when Claude can query real-time biological databases.

### What's Been Done?

✅ **Phase 1: Database Exploration** (100% complete)
- Explored all 22 biological databases
- Documented capabilities, tested queries, identified opportunities
- 279 KB of detailed exploration reports

✅ **Phase 2: Question Generation** (100% complete)  
- Created 120 evaluation questions across 6 categories
- Complete coverage of all 22 databases
- Verified answers based on exploration findings

🔄 **Phase 3: Automated Evaluation** (20% complete)
- 24/120 questions evaluated (Q01-Q02)
- 96 questions ready to run (Q03-Q10)
- Automated tooling complete and tested

📊 **Phase 4: Analysis & Reporting** (Pending)
- Awaiting full evaluation completion
- Analysis tools ready and tested

**See**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for detailed progress tracking.

### Key Statistics

| Metric | Value |
|--------|-------|
| **Databases Covered** | 22/22 (100%) |
| **Questions Created** | 120 |
| **Questions Evaluated** | 24 (20%) |
| **Questions Pending** | 96 (80%) |
| **Documentation Size** | 279 KB |
| **Estimated Full Cost** | ~$6.50 (Claude Sonnet 4.5) |

---

## 📁 Project Structure

```
evaluation/
├── README.md                      # This file - start here
├── PROJECT_STATUS.md              # Current progress and timeline
├── QUESTION_DESIGN_GUIDE.md       # How to create evaluation questions
│
├── questions/                     # 120 evaluation questions
│   ├── Q01.json                  # Questions 1-12
│   ├── Q02.json                  # Questions 13-24
│   ├── Q03.json → Q10.json       # Questions 25-120
│   └── SUMMARY.md                # Complete question overview
│
├── exploration/                   # Database capability reports
│   ├── 00_SUMMARY.md             # Overview of all 22 databases
│   ├── uniprot_exploration.md    # UniProt detailed report
│   ├── pubchem_exploration.md    # PubChem detailed report
│   └── [20 more database reports]
│
├── scripts/                       # Automated evaluation tools
│   ├── README.md                 # Complete script documentation
│   ├── QUICK_REFERENCE.md        # Quick command reference
│   ├── automated_test_runner.py  # Run evaluations
│   ├── compute_costs.py          # Calculate API costs
│   ├── results_analyzer.py       # Analyze results
│   ├── generate_dashboard.py     # Create visualizations
│   ├── validate_questions.py     # Validate question format
│   └── requirements.txt          # Python dependencies
│
└── results/                       # Evaluation outputs
    ├── Q01_out.csv               # Results for Q01
    ├── Q02_out.csv               # Results for Q02
    ├── results.csv               # Combined results
    └── combine_csv.py            # CSV merging utility
```

### Quick Navigation

| I want to... | Go to |
|--------------|-------|
| **Run an evaluation** | [`scripts/README.md`](scripts/README.md) |
| **Create questions** | [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md) |
| **Calculate costs** | [Cost Analysis](#cost-analysis) section below |
| **Check progress** | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| **Understand questions** | [`questions/SUMMARY.md`](questions/SUMMARY.md) |
| **Learn about databases** | [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) |
| **Quick commands** | [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md) |

---

## The Evaluation Suite

### 120 Test Questions

Questions are organized into **10 JSON files** (Q01-Q10), each containing **12 questions** with balanced representation from all 6 categories.

**Distribution by Category** (20 questions each):

| Category | Tests | Example Question |
|----------|-------|------------------|
| **Precision** | Exact IDs, specific values | "What is the UniProt ID for human BRCA1?" |
| **Completeness** | Counts, exhaustive lists | "How many GO terms are descendants of autophagy?" |
| **Integration** | Cross-database linking | "Convert UniProt P04637 to NCBI Gene ID" |
| **Currency** | Recent/updated data | "When was BRCA1 variant c.5266dup last updated?" |
| **Specificity** | Niche, specialized topics | "What is the MeSH ID for Erdheim-Chester disease?" |
| **Structured Query** | Complex multi-criteria | "Find ChEMBL kinases with IC50 < 100nM" |

**See**: [`questions/SUMMARY.md`](questions/SUMMARY.md) for complete question catalog.

### 22 Biological Databases

**Molecular Biology Core** (6 databases)
- UniProt (444M proteins), PDB (204K structures), NCBI Gene (57M genes)
- Ensembl (100+ species), DDBJ (genomic sequences), Taxonomy (3M taxa)

**Chemical & Drug Resources** (4 databases)
- ChEBI (217K entities), ChEMBL (2.4M compounds), PubChem (119M compounds), Rhea (17K reactions)

**Pathways & Systems** (2 databases)
- Reactome (22K pathways), GO (48K terms)

**Clinical & Genetics** (4 databases)
- ClinVar (3.5M variants), MedGen (233K concepts), MONDO (30K diseases), NANDO (2,777 rare diseases)

**Literature & Terminology** (3 databases)
- MeSH (2.5M entities), PubMed (literature), PubTator (text mining)

**Specialized** (3 databases)
- BacDive (97K strains), MediaDive (3,289 media), GlyCosmos (glycans)

**See**: [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) for database capabilities.

### 6 Question Categories

Each category tests a different aspect of database access:

#### 1. Precision Questions (20)
**Purpose**: Test exact data retrieval
- Specific database IDs (UniProt accessions, PubChem CIDs)
- Molecular properties (molecular weight, formula)
- Measurement values (PDB resolution, temperature ranges)

**Example**: "What is the UniProt accession for SpCas9 from S. pyogenes?" → `Q99ZW2`

#### 2. Completeness Questions (20)
**Purpose**: Test comprehensive result retrieval
- Entity counts ("How many variants in ClinVar?")
- Exhaustive lists ("All descendants of GO:0006914")
- Systematic enumeration ("Count FDA-approved drugs")

**Example**: "How many descendant terms does GO:0006914 have?" → `25`

#### 3. Integration Questions (20)
**Purpose**: Test cross-database linking
- ID conversion (UniProt ↔ NCBI Gene)
- Cross-references (PubChem ↔ ChEBI)
- Multi-database workflows (ClinVar → MedGen → MONDO)

**Example**: "Convert UniProt P04637 to NCBI Gene ID" → `7157` (TP53)

#### 4. Currency Questions (20)
**Purpose**: Test access to recent/updated data
- Last update timestamps
- Recent additions (post-training cutoff)
- Current status/classifications

**Example**: "When was BRCA1 c.5266dup last updated in ClinVar?" → `2025-05-25`

#### 5. Specificity Questions (20)
**Purpose**: Test niche/specialized information
- Rare diseases (NANDO, MONDO)
- Specialized organisms (BacDive extremophiles)
- Uncommon compounds or specialized terminology

**Example**: "What is the MeSH ID for Erdheim-Chester disease?" → `D031249`

#### 6. Structured Query Questions (20)
**Purpose**: Test complex filtering and multi-step queries
- Multiple criteria (IC50 < 100nM AND kinase target)
- Logical operators (AND, OR, NOT)
- Complex SPARQL-like queries

**Example**: "Find ChEMBL molecules with IC50 < 100nM against kinases" → List of compounds

---

## Getting Started

### Prerequisites

- Python 3.8+
- Anthropic API key
- ~30 minutes for small evaluation (12 questions)
- ~6-8 hours for full evaluation (120 questions)

### Installation

```bash
# 1. Navigate to scripts directory
cd scripts

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 4. Verify installation
python -c "import anthropic; print('Ready!')"

# 5. Test with example questions
python automated_test_runner.py example_questions.json
```

### First Evaluation

Run your first evaluation on the smallest question set:

```bash
# Run evaluation on Q01 (12 questions)
python automated_test_runner.py ../questions/Q01.json

# This will:
# - Test each question twice (baseline + TogoMCP)
# - Output results to evaluation_results.csv
# - Take approximately 15-20 minutes
# - Cost approximately $0.65

# Calculate costs
python compute_costs.py evaluation_results.csv

# Analyze results
python results_analyzer.py evaluation_results.csv -v

# Generate dashboard
python generate_dashboard.py evaluation_results.csv --open
```

**See**: [`scripts/README.md`](scripts/README.md) for complete documentation.

---

## Common Use Cases

### Run an Evaluation

```bash
cd scripts

# Validate questions first
python validate_questions.py ../questions/Q03.json --estimate-cost

# Run evaluation
python automated_test_runner.py ../questions/Q03.json -o ../results/Q03_out.csv

# Calculate costs
python compute_costs.py ../results/Q03_out.csv

# Analyze results
python results_analyzer.py ../results/Q03_out.csv -v

# Generate dashboard
python generate_dashboard.py ../results/Q03_out.csv --open
```

**Time**: ~30 minutes for 12 questions  
**Cost**: ~$0.65 (Claude Sonnet 4.5)

### Create New Questions

```bash
# 1. Read the guide
cat QUESTION_DESIGN_GUIDE.md

# 2. Study existing examples
cat questions/Q01.json | jq

# 3. Create your question file
cat > my_questions.json << 'EOF'
[
  {
    "id": 121,
    "category": "Precision",
    "question": "Your question here",
    "expected_answer": "Expected result",
    "notes": "Why this tests database access"
  }
]
EOF

# 4. Validate format
cd scripts
python validate_questions.py my_questions.json

# 5. Test it
python automated_test_runner.py my_questions.json
```

**See**: [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md) for detailed guidance.

### Calculate API Costs

```bash
cd scripts

# Basic cost analysis
python compute_costs.py ../results/results.csv

# With different model
python compute_costs.py results.csv --model claude-opus-4-20250514

# Export detailed report
python compute_costs.py results.csv --export cost_report.json

# With custom pricing
python compute_costs.py results.csv --pricing custom_pricing.json
```

**See**: [Cost Analysis](#cost-analysis) section below for details.

### Analyze Results

```bash
cd scripts

# View statistics
python results_analyzer.py evaluation_results.csv

# Verbose output (show individual questions)
python results_analyzer.py evaluation_results.csv -v

# Export markdown report
python results_analyzer.py evaluation_results.csv --export ../analysis_report.md

# Generate interactive dashboard
python generate_dashboard.py evaluation_results.csv --open
```

### Understand the Questions

```bash
# Question overview and statistics
cat questions/SUMMARY.md

# Detailed look at specific questions
cat questions/Q01.json | jq

# Database capabilities reference
cat exploration/00_SUMMARY.md

# Deep dive on specific database
cat exploration/uniprot_exploration.md
```

### Check Project Status

```bash
# Overall progress
cat PROJECT_STATUS.md

# Current evaluation status
ls -lh results/

# Question coverage
grep -c "^  {" questions/*.json
```

---

## Documentation Guide

### Primary Documents

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **README.md** (this file) | Quick start, overview | First visit |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | Current progress, timeline | Check status |
| **[QUESTION_DESIGN_GUIDE.md](QUESTION_DESIGN_GUIDE.md)** | Create questions | Adding questions |
| **[scripts/README.md](scripts/README.md)** | Complete script guide | Running evaluations |
| **[scripts/QUICK_REFERENCE.md](scripts/QUICK_REFERENCE.md)** | Quick commands | Daily use |
| **[questions/SUMMARY.md](questions/SUMMARY.md)** | All 120 questions | Question reference |
| **[exploration/00_SUMMARY.md](exploration/00_SUMMARY.md)** | Database capabilities | Database reference |

### Learning Path

**New Users** (90 minutes total):
1. Read this README (10 min)
2. Review [`PROJECT_STATUS.md`](PROJECT_STATUS.md) (5 min)
3. Browse [`questions/SUMMARY.md`](questions/SUMMARY.md) (10 min)
4. Read [`scripts/README.md`](scripts/README.md) (20 min)
5. Run first evaluation (30 min)
6. Analyze results (15 min)

**Question Creators**:
1. Read [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md) (20 min)
2. Study [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) (15 min)
3. Review existing questions in [`questions/SUMMARY.md`](questions/SUMMARY.md) (15 min)
4. Create and test questions (variable)

**Database Researchers**:
1. Start with [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) (15 min)
2. Read specific database reports in `exploration/` (5-10 min each)
3. Test queries documented in reports (variable)

---

## Cost Analysis

### Understanding Costs

The evaluation system uses **isolated sessions** for optimal cache efficiency:

```
Q1: CREATE cache (system + tools) + READ cache → Answer
Q2: CREATE cache (system + tools) + READ cache → Answer  ← Fresh session
Q3: CREATE cache (system + tools) + READ cache → Answer  ← Fresh session
```

**Benefits**:
- Stable, predictable costs per question
- No exponential cache growth
- ~46% cheaper than conversation accumulation
- Each question independent

### Cost Breakdown (Claude Sonnet 4.5)

**Per Question**:
- Baseline: ~$0.002 (no caching)
- TogoMCP: ~$0.053 (includes cache creation + reads)
- **Total**: ~$0.055 per question

**Evaluation Sizes**:
- 12 questions: ~$0.65
- 24 questions: ~$1.30
- 120 questions: ~$6.50

### Using compute_costs.py

```bash
# Basic cost analysis
python compute_costs.py evaluation_results.csv

# Output includes:
# - Baseline costs (input/output tokens)
# - TogoMCP costs (input/output + cache creation/read)
# - Breakdown by category
# - Breakdown by value-add level
# - Per-question averages

# Specify different model
python compute_costs.py results.csv --model claude-opus-4-20250514

# Export detailed JSON
python compute_costs.py results.csv --export cost_report.json
```

### Supported Models

| Model | Input | Output | Cache Create | Cache Read |
|-------|-------|--------|--------------|------------|
| Sonnet 4.5 (default) | $3.00/MTok | $15.00/MTok | $3.75/MTok | $0.30/MTok |
| Opus 4 | $15.00/MTok | $75.00/MTok | $18.75/MTok | $1.50/MTok |
| Haiku 4.5 | $0.80/MTok | $4.00/MTok | $1.00/MTok | $0.08/MTok |
| Sonnet 3.5 | $3.00/MTok | $15.00/MTok | $3.75/MTok | $0.30/MTok |

### Example Output

```
================================================================================
COST ANALYSIS FOR TOGOMCP EVALUATION
================================================================================
Model: Claude Sonnet 4.5
Total questions evaluated: 12

BASELINE COSTS (No Tools)
--------------------------------------------------------------------------------
  Input tokens:         780
  Output tokens:        1,400
  Total cost:           $0.0234

TOGOMCP COSTS (With MCP Tools)
--------------------------------------------------------------------------------
  Input tokens:         108
  Output tokens:        4,600
  Cache creation:       98,011 tokens
  Cache read:           644,288 tokens
  Total cost:           $0.6308

TOTAL EVALUATION COST: $0.6542
```

**See**: [`scripts/README.md`](scripts/README.md#cost-analysis) for more details.

---

## Understanding Results

### Output Metrics

Each evaluation produces a CSV with these key columns:

| Metric | Description |
|--------|-------------|
| **baseline_has_expected** | Did baseline answer include expected result? |
| **togomcp_has_expected** | Did TogoMCP answer include expected result? |
| **tools_used** | Which MCP tools were called? |
| **value_add** | CRITICAL/VALUABLE/MARGINAL/REDUNDANT |
| **cache_creation_tokens** | Tokens created in cache |
| **cache_read_tokens** | Tokens read from cache |

### Success Patterns

| Pattern | Baseline | TogoMCP | Interpretation |
|---------|----------|---------|----------------|
| **Both have expected** | ✅ | ✅ | Question may be too easy |
| **Only baseline** | ✅ | ❌ | TogoMCP failed (check config) |
| **Only TogoMCP** | ❌ | ✅ | **Clear value-add!** ⭐ |
| **Neither** | ❌ | ❌ | Question needs revision |

### Value-Add Categories

Questions are automatically scored:

- **CRITICAL** (15-18 points): Essential improvement, use for benchmarks
- **VALUABLE** (9-14 points): Significant improvement, include in evaluation  
- **MARGINAL** (4-8 points): Minor improvement, consider revising
- **REDUNDANT** (0-3 points): No improvement, exclude

**Goal**: Identify CRITICAL questions that clearly demonstrate TogoMCP's value.

### Analyzing Results

```bash
cd scripts

# View overall statistics
python results_analyzer.py evaluation_results.csv

# See individual question details
python results_analyzer.py evaluation_results.csv -v

# Generate interactive dashboard
python generate_dashboard.py evaluation_results.csv --open

# Export detailed report
python results_analyzer.py evaluation_results.csv --export report.md
```

**See**: [`scripts/README.md`](scripts/README.md#understanding-results) for interpretation guide.

---

## Project Status

### Current Phase: Automated Evaluation (20% complete)

| Phase | Status | Progress |
|-------|--------|----------|
| **1. Database Exploration** | ✅ Complete | 22/22 databases (100%) |
| **2. Question Generation** | ✅ Complete | 120/120 questions (100%) |
| **3. Automated Evaluation** | 🔄 In Progress | 24/120 questions (20%) |
| **4. Analysis & Reporting** | 📊 Pending | Awaiting full evaluation |

### Completed

✅ All 22 databases explored and documented (279 KB reports)  
✅ 120 evaluation questions created across 6 categories  
✅ Q01-Q02 evaluated (24 questions)  
✅ Automated tooling complete and tested  
✅ Cost analysis tools ready

### In Progress

🔄 Q03-Q10 evaluation (96 questions remaining)  
🔄 Cost tracking and optimization

### Next Steps

1. Complete Q03-Q10 evaluation (~6-8 hours)
2. Calculate total costs and analyze spending
3. Run comprehensive analysis across all 120 questions
4. Generate final dashboard and reports
5. Identify benchmark questions (CRITICAL category)
6. Document findings and insights

**See**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for detailed timeline and metrics.

---

## Contributing

### Adding Questions

1. Read [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)
2. Follow format in existing `questions/*.json` files
3. Validate with `scripts/validate_questions.py`
4. Ensure expected answers are verifiable
5. Test with `scripts/automated_test_runner.py`

### Improving Documentation

1. Keep README.md concise (entry point only)
2. Put details in specific docs (scripts/README.md, QUESTION_DESIGN_GUIDE.md)
3. Update PROJECT_STATUS.md when progress changes
4. Add examples to help users understand concepts

### Reporting Issues

- **Missing database functionality?** → Document in exploration reports
- **Question problems?** → Note in questions/SUMMARY.md
- **Script bugs?** → See scripts/README.md troubleshooting
- **Cost discrepancies?** → Check compute_costs.py output

---

## FAQ

### How much does a full evaluation cost?

**Claude Sonnet 4.5** (default):
- 12 questions: ~$0.65
- 24 questions: ~$1.30
- 120 questions: ~$6.50

Use `scripts/validate_questions.py --estimate-cost` before running.

### Why is evaluation only 20% complete?

The full evaluation requires:
- 240 API calls (120 questions × 2 tests each)
- 6-8 hours of runtime
- ~$6.50 in API costs

We completed Q01-Q02 as validation. Q03-Q10 are ready to run.

### How do I add my own questions?

1. Read [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)
2. Create JSON file following the format
3. Validate: `python validate_questions.py my_questions.json`
4. Run: `python automated_test_runner.py my_questions.json`

### What's the cache efficiency strategy?

**Isolated sessions** design:
- Each question gets a fresh Claude client
- Only system prompt + tools are cached
- Cache reads stay constant per question
- **46% cheaper** than accumulating conversations
- No cross-question contamination

### Can I use different Claude models?

Yes! Supported models:
- `claude-sonnet-4-5-20250929` (default, Sonnet 4.5)
- `claude-sonnet-4-20250514` (Sonnet 4)
- `claude-opus-4-20250514` (Opus 4)
- `claude-haiku-4-5-20251001` (Haiku 4.5)
- `claude-sonnet-3-5-20241022` (Sonnet 3.5)

Specify with: `--model claude-opus-4-20250514`

### Where can I find example questions?

- `questions/Q01.json` through `questions/Q10.json` (120 questions)
- `scripts/example_questions.json` (simple examples)
- [`questions/SUMMARY.md`](questions/SUMMARY.md) (complete catalog)

---

## Support

**For Running Evaluations**: [`scripts/README.md`](scripts/README.md)  
**For Creating Questions**: [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)  
**For Cost Analysis**: [Cost Analysis](#cost-analysis) section above  
**For Quick Commands**: [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md)  
**For Database Info**: [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md)  
**For Project Status**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md)

---

## License

This evaluation tooling follows the same license as the main TogoMCP project.

---

**Last Updated**: 2025-12-22  
**Version**: 3.0 (Comprehensive Documentation Update)  
**Status**: Foundation Complete ✅ | Evaluation In Progress 🔄 (20%)

**Ready to evaluate?** → Start with [`scripts/README.md`](scripts/README.md)  
**Ready to create questions?** → Start with [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)  
**Need quick commands?** → See [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md)
