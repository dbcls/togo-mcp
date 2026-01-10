# ChEMBL Exploration Report

## Database Overview
ChEMBL is a manually curated database of bioactive molecules with drug-like properties containing:
- **2.4 million+ compounds**
- **1.6 million assays**
- **20 million bioactivity measurements**
- **13,000 targets** (proteins, protein complexes, protein families)
- Cross-references to UniProt, PDB, PubChem, DrugBank, and other databases
- Drug development phases, mechanisms of action, and disease indications

## Schema Analysis (from MIE file)

### Main Properties Available
- **Molecules**: ChEMBL ID, name, ATC classification, development phase, substance type, cross-references
- **Activities**: Standard type (IC50, EC50, Ki), values, units, pChembl scores
- **Assays**: Assay type, organism name, target relationships
- **Targets**: Target type (single protein, complex, family), organism, UniProt links
- **Drug Mechanisms**: Mechanism of action (inhibitor, agonist, etc.), target relationships
- **Drug Indications**: MeSH disease terms, EFO ontology, development phase

### Important Relationships
- `cco:hasMolecule` - Links activities to molecules
- `cco:hasAssay` - Links activities to assays
- `cco:hasTarget` - Links assays/mechanisms to targets
- `cco:hasTargetComponent` - Links targets to protein components
- `skos:exactMatch` - Links target components to UniProt
- `cco:moleculeXref` - External database cross-references
- `cco:hasMesh` - Links indications to MeSH disease terms
- `bibo:pmid` - Links to PubMed literature

### Query Patterns Observed
- **Keyword search**: Use `bif:contains` for fast full-text search with Boolean operators
- **FROM clause mandatory**: Always specify `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
- **Unit checking critical**: Always filter by `cco:standardUnits` when comparing activity values
- **Target filtering**: Start with specific target types (cco:SingleProtein) for efficiency
- **Development phase**: Filter by `cco:highestDevelopmentPhase` (0-4, where 4=marketed)

## Search Queries Performed

1. **Query: "aspirin"** → Results: CHEMBL25 (aspirin), CHEMBL5314595 (aspirin trelamine), 52 total hits
2. **Query: "EGFR"** → Results: CHEMBL203 (human EGFR), CHEMBL3608 (mouse EGFR), 20 total including protein interactions
3. **Query: "imatinib"** → Results: CHEMBL941 (imatinib), CHEMBL1642 (imatinib mesylate), 5 total
4. **Query: "kinase"** → Results: 1,632 kinase targets across species
5. **Marketed drugs (phase 4)** → Results: Cetirizine, pentazocine, tolmetin, bromfenac, etc.

## SPARQL Queries Tested

```sparql
# Query 1: Get human protein targets
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>

SELECT ?target ?label ?targetType
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?target a cco:SingleProtein ;
          rdfs:label ?label ;
          cco:targetType ?targetType ;
          cco:organismName "Homo sapiens" .
}
LIMIT 10
# Results: Retrieved human proteins including alpha-glucosidase, alcohol dehydrogenase, 
# AMP deaminase, serum albumin, etc.
```

```sparql
# Query 2: Get bioactivity data for aspirin (CHEMBL25)
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>

SELECT ?activity ?type ?value ?units
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?activity a cco:Activity ;
            cco:hasMolecule <http://rdf.ebi.ac.uk/resource/chembl/molecule/CHEMBL25> ;
            cco:standardType ?type .
  OPTIONAL { ?activity cco:standardValue ?value }
  OPTIONAL { ?activity cco:standardUnits ?units }
}
LIMIT 10
# Results: Multiple activity types - IC50 (270000 nM, 90000 nM, 100000 nM, 5000 nM), 
# ED30 (30 mg/kg), Inhibition (15%, 30%, 38.3%), Survival (105%)
```

```sparql
# Query 3: Find marketed drugs (development phase 4)
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>

SELECT ?molecule ?label ?phase
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule a cco:SmallMolecule ;
            rdfs:label ?label ;
            cco:highestDevelopmentPhase ?phase .
  FILTER(?phase = 4)
}
LIMIT 10
# Results: CETIRIZINE, PENTAZOCINE, TOLMETIN, BROMFENAC, ROPIVACAINE, 
# TIZANIDINE, DIBUCAINE, MESORIDAZINE, INDACATEROL, IMIPRAMINE
```

## Interesting Findings

### Specific Entities for Questions
- **CHEMBL25**: Aspirin - has multiple bioactivity measurements
- **CHEMBL203**: Human EGFR - major drug target with many inhibitors
- **CHEMBL941**: Imatinib - blockbuster cancer drug
- **Marketed drugs**: Over 2,000 phase 4 (marketed) drugs
- **1,632 kinase targets**: Large family for structured queries

### Unique Properties
- **Development phase tracking**: 0-4 scale (0=research, 4=marketed)
- **Standardized bioactivity**: pChembl scores normalize different measurement types
- **Mechanism of action**: Explicit drug-target mechanism relationships
- **Disease indications**: MeSH and EFO disease ontology links
- **bif:contains optimization**: Virtuoso-specific full-text search with Boolean operators
- **ATC classification**: Anatomical Therapeutic Chemical codes for drugs

### Connections to Other Databases
- **UniProt**: 85% of targets have UniProt mappings via TargetComponent
- **PubChem**: 90% of molecules cross-referenced
- **DrugBank**: 8,400 drug cross-references
- **MeSH**: 51,000 drug indications
- **PubMed**: 88,000 document references
- **ChEBI**: 35,000 chemical ontology links
- **PDB**: 64,000 structure links

### Specific Verifiable Facts
- **2.4 million molecules** total
- **20 million bioactivity measurements**
- **13,000 targets** (proteins, complexes, families)
- **1,632 kinase targets** across all species
- **52 aspirin-related molecules**
- **20 EGFR-related targets**
- Activity values range from picomolar to millimolar

## Question Opportunities by Category

### Precision
- "What is the ChEMBL ID for aspirin?" → CHEMBL25
- "What is the ChEMBL ID for human EGFR?" → CHEMBL203
- "What is the development phase of imatinib?" → Phase 4 (marketed)
- "What is the target type for CHEMBL203?" → SINGLE PROTEIN
- "What is the ChEMBL ID for imatinib mesylate?" → CHEMBL1642

### Completeness
- "How many molecules are in ChEMBL?" → 2.4 million
- "How many bioactivity measurements are recorded?" → 20 million
- "How many kinase targets are in ChEMBL?" → 1,632
- "How many marketed drugs (phase 4) are there?" → ~2,000+
- "How many aspirin-related molecules exist?" → 52

### Integration
- "What is the UniProt ID for ChEMBL target CHEMBL203?" → Via TargetComponent
- "Find DrugBank IDs for ChEMBL molecules" → Via moleculeXref
- "Link ChEMBL CHEMBL25 to PubChem" → Via cross-references
- "What MeSH disease terms are associated with imatinib?" → Via drug indications
- "Convert ChEMBL targets to UniProt accessions" → Via skos:exactMatch

### Currency
- "How many COVID-19 related molecules are in ChEMBL?" → Search recent additions
- "What are the newest drug indications added?" → Recent indication data
- "How many molecules are in clinical trials?" → Phase 1-3 counts
- "What kinase inhibitors entered phase 3 recently?" → Recent development updates

### Specificity
- "What is the IC50 of imatinib against BCR-ABL?" → Specific bioactivity
- "Find molecules with nanomolar potency against rare kinases" → Niche targets
- "What is the mechanism of action for drug X?" → Specific mechanism
- "Find inhibitors of CHEMBL203 with IC50 < 10 nM" → Highly specific query

### Structured Query
- "Find kinase inhibitors with IC50 < 100 nM" → Activity + target + threshold
- "List marketed drugs (phase 4) that target human proteins AND have DrugBank IDs" → Multiple filters
- "Find molecules with IC50 < 50 nM against EGFR in humans" → Complex criteria
- "Search for agonists (not inhibitors) of GPCRs" → Mechanism + target type
- "Find molecules in phase 3 trials for cancer indications" → Phase + disease filter

## Notes

### Limitations
- **FROM clause required**: Queries fail without `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
- **Activity units vary**: Must always check cco:standardUnits (nM, uM, %, mg/kg)
- **Not all molecules have activities**: ~80% coverage
- **UniProt mapping incomplete**: ~85% for human, lower for other organisms
- **Development phase**: Most complete for marketed drugs, sparse for early research

### Best Practices
1. **Use bif:contains** for keyword searches (faster than FILTER/REGEX)
2. **Always include FROM clause**: `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
3. **Check units**: Filter by `cco:standardUnits` when comparing activity values
4. **Start with specific types**: Use `cco:SingleProtein` not just generic targets
5. **Use Boolean operators**: `bif:contains` supports AND, OR, NOT
6. **Add ORDER BY DESC(?sc)** for relevance-ranked results with bif:contains
7. **Filter development phase**: Use `cco:highestDevelopmentPhase` for drug status

### Performance Notes
- Simple lookups: <1s for 100 results
- Activity queries with filters: 2-5s
- bif:contains keyword search: Very fast with relevance ranking
- Cross-database joins: Fast for specific IDs, slower for broad queries
- Always use LIMIT to prevent timeouts
