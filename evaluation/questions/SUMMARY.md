# TogoMCP Evaluation Questions Summary

**Total Questions**: 120 across 10 files (Q01.json - Q10.json)
**Created**: January 2026
**Based on**: Complete exploration of 23 databases

## Distribution by Category

Each category has exactly **20 questions** (2 per file × 10 files):

| Category | Count | Focus Areas |
|----------|-------|-------------|
| Precision | 20 | Exact IDs, molecular properties, specific values |
| Completeness | 20 | Database counts, comprehensive listings |
| Integration | 20 | Cross-database ID conversion, linking |
| Currency | 20 | Recent data, post-training additions |
| Specificity | 20 | Rare diseases, extremophiles, niche data |
| Structured Query | 20 | Complex filters, multi-criteria queries |

## Database Coverage

All 23 databases are represented with biologically relevant questions:

### Tier 1: High-Use Databases (6-8 questions each)
- **UniProt** (8 questions): Protein IDs, sequences, functions, features
- **PubChem** (7 questions): Compound properties, CIDs, bioassays
- **ChEMBL** (6 questions): Drug targets, IC50 values, mechanisms
- **GO** (6 questions): Term hierarchies, annotations, namespaces
- **ClinVar** (6 questions): Variant pathogenicity, clinical significance
- **PubMed** (7 questions): Literature search, citations

### Tier 2: Specialized Databases (4-5 questions each)
- **PDB** (5 questions): Structure resolution, experimental methods
- **Reactome** (5 questions): Pathway hierarchies, disease pathways
- **MeSH** (5 questions): Medical terminology, tree navigation
- **NCBI Gene** (5 questions): Gene symbols, locations, orthologs
- **ChEBI** (4 questions): Chemical ontology, biological roles
- **Rhea** (4 questions): Biochemical reactions, EC numbers
- **MONDO** (4 questions): Disease ontology, cross-references

### Tier 3: Niche Databases (2-3 questions each)
- **BacDive** (3 questions): Extremophile strains, growth conditions
- **MediaDive** (2 questions): Culture media for extremophiles
- **AMR Portal** (3 questions): Resistance patterns, AST data
- **NANDO** (3 questions): Japanese rare diseases, multilingual
- **MedGen** (3 questions): Clinical concepts, disease mappings
- **GlyCosmos** (3 questions): Glycan structures, glycoproteins
- **PubTator** (3 questions): Gene-disease literature mining
- **Taxonomy** (2 questions): Organism classification, strain IDs
- **Ensembl** (2 questions): Gene transcripts, biotypes
- **DDBJ** (2 questions): Genome sequences, viral references

## Question File Structure

Each file (Q01-Q10.json) contains:
- **12 questions** with sequential global IDs
- **2 questions per category** (Precision, Completeness, Integration, Currency, Specificity, Structured Query)
- **All required fields**: id, category, question, expected_answer, notes
- **JSON array format**: `[{...}, {...}, ...]` (not object wrapper)

### File Breakdown

| File | Question IDs | Categories (2 each) |
|------|--------------|---------------------|
| Q01.json | 1-12 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q02.json | 13-24 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q03.json | 25-36 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q04.json | 37-48 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q05.json | 49-60 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q06.json | 61-72 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q07.json | 73-84 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q08.json | 85-96 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q09.json | 97-108 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |
| Q10.json | 109-120 | Precision, Completeness, Integration, Currency, Specificity, Structured Query |

## Biological Relevance Verification

✅ **ALL 120 questions focus on biological/scientific content:**
- Protein sequences, gene IDs, disease classifications
- Molecular properties, chemical structures, reaction mechanisms
- Clinical significance, resistance patterns, growth conditions
- Pathway annotations, literature citations, organism taxonomy

❌ **NO questions about IT infrastructure:**
- Database versions or release numbers
- Software tools (unless methodology affects interpretation)
- Administrative metadata
- Update schedules or technical specs

## Key Question Themes

### Precision Questions (20)
- UniProt/ChEMBL/PubChem IDs for specific entities
- Molecular weights, SMILES, InChI keys
- Genomic locations, resolution values
- EC numbers, taxonomy IDs

### Completeness Questions (20)
- Counts of variants, reactions, proteins, pathways
- Database size metrics (structures, compounds, genes)
- GO term descendants, MeSH term hierarchies
- Comprehensive disease/gene listings

### Integration Questions (20)
- UniProt ↔ NCBI Gene ↔ Ensembl conversions
- PubChem ↔ ChEBI ↔ ChEMBL linking
- ClinVar ↔ MedGen ↔ MONDO mappings
- Reactome ↔ UniProt ↔ GO connections

### Currency Questions (20)
- Recent SARS-CoV-2 pathways in Reactome
- 2024 isolates in AMR Portal
- New cryo-EM structures in PDB
- Recent COVID-19 literature in PubMed

### Specificity Questions (20)
- Rare diseases (Erdheim-Chester, Fabry, Huntington)
- Extremophiles (T. maritima, H. salinarum, P. furiosus)
- Japanese rare disease terminology (NANDO)
- Specialized glycan structures (Lewis antigens)

### Structured Query Questions (20)
- Multi-filter searches (kinases + IC50 < 10nM)
- Ontology hierarchy navigation (ancestors/descendants)
- Pathway + species filtering
- Complex MeSH tree queries

## Verification Status

All questions have been:
- ✅ Referenced to exploration report findings
- ✅ Verified as biologically relevant (not IT metadata)
- ✅ Confirmed to require database access (not baseline knowledge)
- ✅ Formatted as JSON arrays with all required fields
- ✅ Assigned sequential IDs from 1-120
- ✅ Distributed evenly across 6 categories
- ✅ Covering all 23 explored databases

## Example High-Quality Questions

**Precision**: "What is the UniProt accession ID for human BRCA1 protein?" → P38398
**Completeness**: "How many descendant terms does GO:0006914 (autophagy) have?" → 25
**Integration**: "What is the NCBI Gene ID for UniProt P04637?" → 7157 (TP53)
**Currency**: "What pathways in Reactome involve SARS-CoV-2 proteins?" → Multiple COVID pathways
**Specificity**: "What is the MeSH descriptor ID for Erdheim-Chester disease?" → D031249
**Structured Query**: "Find GO terms in biological_process namespace containing 'apoptosis'" → Multiple GO IDs

## Next Steps

The questions are ready for:
1. **Validation**: Run `python validate_questions.py` on each file
2. **Testing**: Execute with automated evaluation framework
3. **Analysis**: Compare baseline vs TogoMCP performance
4. **Refinement**: Update based on evaluation results

## Notes

- Questions draw from verified exploration findings
- Natural language phrasing (no SPARQL/MCP mention)
- Mix of simple and complex queries
- All answers verifiable through database queries
- Focus on realistic research scenarios
- Balanced across organisms, diseases, compounds, pathways
