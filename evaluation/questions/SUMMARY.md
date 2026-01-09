# TogoMCP Evaluation Questions - Summary

## Overview
- **Total Questions**: 120
- **Files**: 10 (Q01.json through Q10.json)
- **Questions per file**: 12
- **Format**: JSON array (not object wrapper)

## Category Distribution

Each category has exactly **20 questions** (2 per file):

| Category | Count | Description |
|----------|-------|-------------|
| **Precision** | 20 | Exact IDs, specific values, precise measurements |
| **Completeness** | 20 | Counts, exhaustive lists, comprehensive enumeration |
| **Integration** | 20 | Cross-database ID conversion, entity linking |
| **Currency** | 20 | Recent updates, current classifications, temporal data |
| **Specificity** | 20 | Rare diseases, niche organisms, specialized data |
| **Structured Query** | 20 | Complex filters, multi-step queries, Boolean logic |

## Database Coverage

All 23 databases from the exploration phase are represented:

### Tier 1 - High Coverage (8-12 questions each)
- **UniProt** (12 questions) - Protein sequences and annotations
- **PubChem** (10 questions) - Chemical compounds and properties
- **ChEMBL** (10 questions) - Bioactive molecules and drug discovery
- **GO** (10 questions) - Gene ontology hierarchy
- **ClinVar** (10 questions) - Genetic variants and clinical significance
- **AMR Portal** (10 questions) - Antimicrobial resistance surveillance ✨
- **PDB** (8 questions) - 3D protein structures
- **Reactome** (8 questions) - Biological pathways

### Tier 2 - Moderate Coverage (4-6 questions each)
- **NANDO** (6 questions) - Japanese rare diseases
- **Rhea** (2+ questions) - Biochemical reactions
- **ChEBI** (3+ questions) - Chemical entities
- **MeSH** (3+ questions) - Medical terminology
- **NCBI Gene** (4+ questions) - Gene database
- **MONDO** (3+ questions) - Disease ontology

### Tier 3 - Supporting Coverage (1-3 questions each)
- **BacDive** (2 questions) - Bacterial strains
- **EMDB**, **PubMed**, **DrugBank**, **KEGG**, **HGNC**, **OMIM**, **Ensembl**
- All represented through integration questions

## Question ID Distribution

- **Q01.json**: Questions 1-12
- **Q02.json**: Questions 13-24
- **Q03.json**: Questions 25-36
- **Q04.json**: Questions 37-48
- **Q05.json**: Questions 49-60
- **Q06.json**: Questions 61-72
- **Q07.json**: Questions 73-84
- **Q08.json**: Questions 85-96
- **Q09.json**: Questions 97-108
- **Q10.json**: Questions 109-120

## Format Verification

✅ **All files comply with requirements:**
- Root element is JSON array `[...]`
- Each question has all 5 recommended fields: `id`, `category`, `question`, `expected_answer`, `notes`
- Categories match exactly (case-sensitive): "Precision", "Completeness", "Integration", "Currency", "Specificity", "Structured Query"
- IDs are sequential 1-120 globally
- Each file has exactly 12 questions
- Each file has exactly 2 questions from each category

## Sample Questions by Category

### Precision
- Q1: "What is the UniProt accession ID for SpCas9 from Streptococcus pyogenes M1?" → Q99ZW2
- Q13: "What is the molecular weight of PubChem compound CID2244?" → 180.16

### Completeness
- Q3: "How many descendant terms does GO:0006914 (autophagy) have?" → 25
- Q15: "How many protein structure entries in PDB used electron microscopy?" → 15,032

### Integration
- Q5: "What is the NCBI Gene ID for UniProt P04637?" → 7157 (TP53)
- Q17: "Convert PubChem CID2244 to its ChEBI identifier." → CHEBI:15365

### Currency
- Q7: "When was BRCA1 variant c.5266dup last updated in ClinVar?" → 2025-05-25
- Q20: "What is the most recent collection year in AMR Portal?" → 2025

### Specificity
- Q9: "What is the NANDO identifier for Parkinson's disease?" → NANDO:1200010
- Q21: "What is the MeSH descriptor ID for Erdheim-Chester disease?" → D031249

### Structured Query
- Q11: "Find ChEMBL molecules with IC50 < 100 nM against kinases"
- Q24: "Count resistance phenotypes by antibiotic for P. aeruginosa in AMR Portal"

## Key Features

### Biologically Realistic
- All questions derived from actual research use cases
- Natural phrasing without technical jargon
- Questions researchers would genuinely ask

### Testable Distinction
- Require database access, not training knowledge
- Specific IDs, current counts, temporal data
- Post-training cutoff information

### Appropriate Complexity
- Range from single-fact lookups to multi-step queries
- None impossibly broad or trivially simple
- Balanced difficulty across categories

### Clear Success Criteria
- All have verifiable expected answers
- Answers confirmed during exploration phase
- Specific enough for automated validation

## Verification

All questions have been:
1. ✅ Derived from verified exploration report findings
2. ✅ Formatted according to QUESTION_FORMAT.md
3. ✅ Designed per QUESTION_DESIGN_GUIDE.md principles
4. ✅ Referenced to specific exploration report sections
5. ✅ Given expected answers from exploration data
6. ✅ Distributed evenly across categories and databases

## Next Steps

1. Run automated evaluation using `automated_test_runner.py`
2. Analyze results with `results_analyzer.py`
3. Refine questions based on CRITICAL vs REDUNDANT classification
4. Generate evaluation report and dashboard

## Files Created

```
/Users/arkinjo/work/GitHub/togo-mcp/evaluation/questions/
├── Q01.json  (12 questions, IDs 1-12)
├── Q02.json  (12 questions, IDs 13-24)
├── Q03.json  (12 questions, IDs 25-36)
├── Q04.json  (12 questions, IDs 37-48)
├── Q05.json  (12 questions, IDs 49-60)
├── Q06.json  (12 questions, IDs 61-72)
├── Q07.json  (12 questions, IDs 73-84)
├── Q08.json  (12 questions, IDs 85-96)
├── Q09.json  (12 questions, IDs 97-108)
└── Q10.json  (12 questions, IDs 109-120)
```

---

**Created**: January 2026  
**Total Questions**: 120  
**Status**: ✅ Complete and verified
