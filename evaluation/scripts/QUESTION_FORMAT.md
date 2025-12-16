# Question File Format Specification

## Overview

TogoMCP evaluation questions are stored in JSON format as an array of question objects.

---

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TogoMCP Evaluation Questions",
  "description": "Question set for evaluating TogoMCP capabilities",
  "type": "array",
  "minItems": 1,
  "items": {
    "type": "object",
    "required": ["question"],
    "properties": {
      "id": {
        "type": ["integer", "string"],
        "description": "Unique identifier for the question"
      },
      "category": {
        "type": "string",
        "enum": [
          "Precision",
          "Completeness",
          "Integration",
          "Currency",
          "Specificity",
          "Structured Query"
        ],
        "description": "Question category based on evaluation rubric"
      },
      "question": {
        "type": "string",
        "minLength": 10,
        "maxLength": 500,
        "description": "The actual question text to ask Claude"
      },
      "expected_answer": {
        "type": "string",
        "description": "Expected answer or outcome (for verification)"
      },
      "notes": {
        "type": "string",
        "description": "Additional context, rationale, or testing notes"
      },
      "mcp_servers": {
        "type": "object",
        "description": "Optional: Override default MCP server configuration for this question",
        "additionalProperties": {
          "type": "object",
          "properties": {
            "type": {
              "type": "string",
              "enum": ["http", "stdio"]
            },
            "url": {
              "type": "string",
              "format": "uri"
            }
          }
        }
      }
    }
  }
}
```

---

## Field Definitions

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `question` | string | The question to evaluate (10-500 characters) |

### Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer or string | Unique identifier (e.g., 1, 2, 3 or "Q001") |
| `category` | string | One of the 6 evaluation categories |
| `expected_answer` | string | What you expect the answer to be |
| `notes` | string | Why you're asking this, what it tests |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `mcp_servers` | object | Override MCP configuration for this question |

---

## Categories

Valid category values:

1. **Precision** - Questions requiring exact, verifiable data
   - Database IDs, sequences, molecular properties
   - Example: "What is the UniProt ID for human BRCA1?"

2. **Completeness** - Questions requiring exhaustive/systematic data
   - "List all...", "How many...", complete sets
   - Example: "How many human genes are in GO term 'DNA repair'?"

3. **Integration** - Questions requiring cross-database linking
   - ID conversions, relationship mapping
   - Example: "Convert UniProt P04637 to NCBI Gene ID"

4. **Currency** - Questions benefiting from up-to-date database info
   - Recent additions, current classifications
   - Example: "What Reactome pathways involve SARS-CoV-2 proteins?"

5. **Specificity** - Questions about niche/specialized information
   - Rare diseases, specific organisms, unusual compounds
   - Example: "What is the MeSH ID for Erdheim-Chester disease?"

6. **Structured Query** - Questions requiring database querying
   - Complex filters, SPARQL-like queries
   - Example: "Find all kinase inhibitors with IC50 < 10nM"

---

## Examples

### Minimal Example (Required Fields Only)

```json
[
  {
    "question": "What is the UniProt ID for human BRCA1?"
  }
]
```

**Valid but not recommended** - Missing context and verification info.

---

### Basic Example (Recommended Fields)

```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398",
    "notes": "Test basic UniProt ID lookup"
  }
]
```

**Recommended minimum** - Has all information for proper evaluation.

---

### Complete Example (All Common Fields)

```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398",
    "notes": "Test basic UniProt ID lookup. Should use search_uniprot_entity tool."
  },
  {
    "id": 2,
    "category": "Integration",
    "question": "Convert UniProt ID P04637 to its corresponding NCBI Gene ID.",
    "expected_answer": "7157 (TP53)",
    "notes": "Tests ID conversion using TogoID. Verifies cross-database linking."
  },
  {
    "id": 3,
    "category": "Completeness",
    "question": "How many human genes are annotated with the GO term 'DNA repair' (GO:0006281)?",
    "expected_answer": "Check actual count in GO database",
    "notes": "Tests ability to query and count GO annotations. Answer may change over time."
  }
]
```

---

### Advanced Example (With MCP Override)

```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "Find recent publications about BRCA1.",
    "expected_answer": "List of recent PMIDs",
    "notes": "Test PubMed MCP server specifically",
    "mcp_servers": {
      "pubmed": {
        "type": "http",
        "url": "https://pubmed.mcp.claude.com/mcp"
      }
    }
  }
]
```

**Use case:** When you want to test a specific MCP server for this question.

---

## Validation

Use the validator to check your question file:

```bash
# Basic validation
python validate_questions.py questions.json

# With recommendations
python validate_questions.py questions.json --recommendations

# Estimate costs
python validate_questions.py questions.json --estimate-cost

# Strict mode (warnings become errors)
python validate_questions.py questions.json --strict
```

---

## Common Validation Errors

### ❌ Invalid JSON
```json
[
  {
    "question": "What is the UniProt ID for BRCA1?"
    "category": "Precision"  // Missing comma!
  }
]
```

**Fix:** Add comma after each field (except the last)

---

### ❌ Missing Required Field
```json
[
  {
    "id": 1,
    "category": "Precision"
    // Missing "question" field!
  }
]
```

**Fix:** Add `"question"` field

---

### ❌ Invalid Category
```json
[
  {
    "question": "What is the UniProt ID for BRCA1?",
    "category": "Database Lookup"  // Not a valid category!
  }
]
```

**Fix:** Use one of the 6 valid categories

---

### ⚠️ Missing Recommended Fields
```json
[
  {
    "question": "What is the UniProt ID for BRCA1?"
    // Missing id, category, expected_answer, notes
  }
]
```

**Warning, not error** - Will work but makes tracking harder

---

## Best Practices

### ✅ Do

**Provide all recommended fields:**
```json
{
  "id": 1,
  "category": "Precision",
  "question": "What is the UniProt ID for human BRCA1?",
  "expected_answer": "P38398",
  "notes": "Basic UniProt lookup test"
}
```

**Use descriptive IDs:**
```json
{
  "id": "precision_001",
  "category": "Precision",
  ...
}
```

**Write clear questions:**
```json
{
  "question": "What is the UniProt ID for human BRCA1?"  // Clear, specific
}
```

**Add helpful notes:**
```json
{
  "notes": "Tests search_uniprot_entity tool. Should return P38398. Human-specific to avoid ambiguity."
}
```

---

### ❌ Don't

**Vague questions:**
```json
{
  "question": "Tell me about BRCA1"  // Too broad
}
```

**Missing context:**
```json
{
  "question": "What is the ID?"  // ID of what? Which database?
}
```

**Duplicate questions:**
```json
[
  {"question": "What is the UniProt ID for BRCA1?"},
  {"question": "What's the UniProt ID for BRCA1?"}  // Duplicate!
]
```

---

## File Naming Conventions

Recommended naming patterns:

- `questions.json` - Generic question set
- `brca1_questions.json` - Entity-specific questions
- `precision_questions.json` - Category-specific questions
- `pilot_questions.json` - Initial test questions
- `benchmark_v1.json` - Versioned benchmark set

---

## Integration with Tools

### Question Generator
```bash
# Generates valid JSON automatically
python question_generator.py --entity BRCA1 --batch 5
```

Output is already in the correct format!

### Validator
```bash
# Checks format compliance
python validate_questions.py questions.json
```

Catches format errors before evaluation.

### Test Runner
```bash
# Expects this exact format
python automated_test_runner.py questions.json
```

Won't work with invalid format!

---

## Version History

- **v1.0** (2025-12-16): Initial schema definition
  - Required: `question`
  - Recommended: `id`, `category`, `expected_answer`, `notes`
  - Optional: `mcp_servers`

---

## See Also

- `example_questions.json` - Working examples
- `validate_questions.py` - Format validator
- `question_generator.py` - Generates valid questions
- `USAGE_GUIDE.md` - Complete workflow

---

## Quick Reference

**Minimal valid file:**
```json
[{"question": "What is the UniProt ID for human BRCA1?"}]
```

**Recommended structure:**
```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398",
    "notes": "Basic test"
  }
]
```

**Validate it:**
```bash
python validate_questions.py questions.json --recommendations
```
