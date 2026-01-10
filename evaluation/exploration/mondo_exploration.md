# MONDO (Monarch Disease Ontology) Exploration Report

## Database Overview
- **Purpose**: Comprehensive disease ontology integrating multiple disease databases
- **Scope**: 30,000+ disease classes covering genetic disorders, infectious diseases, cancers, and rare diseases
- **Key entities**: Disease classes with hierarchical classification, definitions, synonyms, cross-references
- **Integration**: Maps to 39+ external databases (OMIM, Orphanet, DOID, MeSH, ICD, UMLS, etc.)

## Schema Analysis (from MIE file)

### Main Properties
- `rdfs:label`: Disease name (e.g., "Fabry disease", "type 1 diabetes mellitus")
- `oboInOwl:id`: MONDO identifier (e.g., "MONDO:0010526")
- `IAO:0000115`: Disease definition/description
- `rdfs:subClassOf`: Parent disease class (hierarchical classification)
- `oboInOwl:hasExactSynonym`: Exact synonym (semantically equivalent)
- `oboInOwl:hasRelatedSynonym`: Related synonym (broader/narrower meaning)
- `oboInOwl:hasDbXref`: Cross-references to external databases
- `owl:deprecated`: Deprecation status (obsolete terms)

### Important Relationships
- **Hierarchical**: `rdfs:subClassOf` for disease classification tree
- **Cross-references**: `oboInOwl:hasDbXref` links to 39+ external databases
- **Synonyms**: Exact and related synonyms for alternative disease names
- **OBO Foundry compliant**: Standard ontology structure

### Query Patterns Observed
- Use `bif:contains` for efficient full-text search with relevance scoring
- Always include `FROM <http://rdfportal.org/ontology/mondo>` clause
- Use `FILTER(isIRI(?parent))` to exclude blank nodes in hierarchy queries
- Use `STRSTARTS(?xref, "OMIM:")` for efficient prefix filtering on cross-references
- Add `LIMIT` clauses to prevent timeouts (30K+ classes)
- Start transitive queries from specific disease classes

## Search Queries Performed

1. **Query**: "Fabry disease" (OLS4 searchClasses)
   - **Results**: Found MONDO:0010526
     - Definition: "Progressive, inherited, multisystemic lysosomal storage disease"
     - 17 direct ancestors shown (sphingolipidosis, lysosomal storage disease, inherited lipid metabolism disorder, hereditary disease, etc.)
     - Complete hierarchical classification from molecular to high-level
   - Also found related diseases (7,368 total search results)

2. **Query**: "cancer" (SPARQL bif:contains)
   - **Results**: 10 cancer-related diseases ranked by relevance
     - MONDO:0011361: prostate cancer/brain cancer susceptibility (top ranked)
     - MONDO:0004992: cancer (general term)
     - MONDO:0000952: cancer of long bone of lower limb
     - MONDO:0021317: cancer of cerebellum
     - MONDO:0045054: cancer-related condition
     - Demonstrates comprehensive cancer classification

3. **Query**: Diseases with OMIM cross-references
   - **Results**: 20 diseases with OMIM IDs
     - Includes: B-cell chronic lymphocytic leukemia (OMIM:151400)
     - Type 2 diabetes mellitus (OMIM:125853)
     - Colorectal cancer (OMIM:114500)
     - Duchenne muscular dystrophy (OMIM:310200)
     - Shows wide range of disease types with genetic component

4. **Query**: Disease counts by parent category (aggregation)
   - **Results**: Top 15 disease categories
     - Hereditary disease: 1,921 diseases (largest category)
     - Syndromic disease: 1,164 diseases
     - Multiple congenital anomalies with ID: 338
     - Inherited disease susceptibility: 285
     - Demonstrates distribution across disease types

## SPARQL Queries Tested

```sparql
# Query 1: Search diseases by keyword with bif:contains
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?disease ?mondoId ?label
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    rdfs:label ?label ;
    oboInOwl:id ?mondoId .
  ?label bif:contains "'cancer'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10

# Results: 10 cancer-related diseases ranked by relevance
# Top result: prostate cancer/brain cancer susceptibility
# Demonstrates efficient keyword search with scoring
```

```sparql
# Query 2: Find diseases with OMIM cross-references
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?disease ?label ?xref
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    rdfs:label ?label ;
    oboInOwl:hasDbXref ?xref .
  FILTER(STRSTARTS(?xref, "OMIM:"))
}
LIMIT 20

# Results: 20 diseases with OMIM identifiers
# Includes common genetic diseases (diabetes, muscular dystrophy)
# Demonstrates cross-database integration
```

```sparql
# Query 3: Count diseases by parent category
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?parentLabel (COUNT(?disease) as ?count)
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    rdfs:subClassOf ?parent .
  ?parent rdfs:label ?parentLabel .
  FILTER(isIRI(?parent))
}
GROUP BY ?parentLabel
ORDER BY DESC(?count)
LIMIT 15

# Results: Top categories:
# - Hereditary disease: 1,921 diseases
# - Syndromic disease: 1,164 diseases
# - Multiple congenital anomalies: 338 diseases
# Demonstrates aggregation and disease distribution
```

## Interesting Findings

### Specific Entities for Questions
- **Fabry disease (MONDO:0010526)**: Lysosomal storage disease, 17+ ancestors
- **Cancer (MONDO:0004992)**: General cancer classification
- **Type 2 diabetes mellitus (MONDO:0005148)**: OMIM:125853
- **Duchenne muscular dystrophy (MONDO:0010679)**: OMIM:310200
- **Huntington disease (MONDO:0007739)**: Orphanet:399, OMIM:143100
- **Achondroplasia (MONDO:0000003)**: OMIM:100800, Orphanet:15

### Unique Properties
- **30,304 total disease classes**: 28,500 active (excluding obsolete)
- **90% have cross-references**: Average 6.5 references per disease
- **75% have definitions**: Comprehensive disease descriptions
- **85% have synonyms**: Average 2.8 synonyms per disease
- **39+ external databases**: Comprehensive cross-referencing

### Connections to Other Databases
- **Genetic databases**: OMIM (33%), Orphanet (34%), GARD (35%)
- **Clinical databases**: UMLS (70%), MEDGEN (70%), MESH (28%)
- **Classification systems**: ICD-9 (19%), ICD-10 (9%), ICD-11 (14%)
- **Phenotype**: EFO (8%), HP (2%)
- **Japanese**: NANDO (8%)
- **Oncology**: ICDO (3%), ONCOTREE (2%)

### Verifiable Facts
- 30,304 total disease classes
- 1,921 hereditary diseases (largest category)
- 1,164 syndromic diseases
- Average 6.5 cross-references per disease
- Average 2.8 synonyms per disease
- 90% of diseases have external cross-references
- 75% have formal definitions
- OMIM coverage: 33% of diseases

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Biological IDs and disease classifications**
- "What is the MONDO ID for Fabry disease?"
- "What is the OMIM identifier for Duchenne muscular dystrophy?"
- "What is the exact definition of achondroplasia in MONDO?"
- "What is the Orphanet ID for Huntington disease?"
- "How many cross-references does type 2 diabetes have in MONDO?"

❌ Avoid: "What database version is this?" "When was the ontology released?"

### Completeness
✅ **Counts and comprehensive lists of diseases**
- "How many total disease classes are in MONDO?"
- "How many diseases are classified as hereditary diseases?"
- "List all ancestor classes of Fabry disease"
- "How many diseases have OMIM cross-references?"
- "How many cancer-related diseases are in MONDO?"

❌ Avoid: "How many database tables exist?" "What is the storage capacity?"

### Integration
✅ **Cross-database disease entity linking**
- "Convert MONDO:0010526 to its OMIM identifier"
- "What is the Orphanet ID for Fabry disease in MONDO?"
- "Find all ICD-10 codes associated with type 2 diabetes"
- "What MESH ID corresponds to Duchenne muscular dystrophy?"
- "Link MONDO:0007739 to NANDO (Japanese rare disease database)"

❌ Avoid: "What databases link to this server?" "List all API endpoints"

### Currency
✅ **Recent disease classifications and updates**
- "What new rare diseases were added to MONDO in 2024?"
- "Has the classification of COVID-19 been updated in MONDO?"
- "What diseases were recently reclassified as hereditary?"
- "Are there any newly obsoleted disease terms?"

❌ Avoid: "What is the current database version number?" "When was the server last updated?"

### Specificity
✅ **Rare diseases and specialized classifications**
- "What is the MONDO ID for Fabry disease (rare lysosomal storage disorder)?"
- "Find the classification of ichthyosis-intellectual disability-dwarfism-renal impairment syndrome"
- "What is the definition of Tangier disease?"
- "What rare diseases are classified as sphingolipidoses?"
- "Find all diseases with both OMIM and Orphanet references"

❌ Avoid: "What is the most common database query?" "Which format is most popular?"

### Structured Query
✅ **Complex disease queries with multiple criteria**
- "Find all hereditary diseases with OMIM references AND ICD-10 codes"
- "List syndromic diseases that affect the nervous system"
- "Find all cancers with OMIM identifiers"
- "Which diseases are both hereditary AND have Orphanet cross-references?"
- "Find all lysosomal storage diseases with definitions"

❌ Avoid: "Find databases updated after 2024" "List all server configurations"

## Notes

### Limitations and Challenges
- **Large dataset**: 30K+ classes require careful query design with LIMIT clauses
- **Blank nodes**: Must use FILTER(isIRI()) to exclude OWL restrictions
- **Variable cross-reference coverage**: Ranges from 3% (ICDO) to 70% (UMLS)
- **Deprecated terms**: Need to check owl:deprecated status
- **Hierarchy complexity**: Some diseases have many ancestors

### Best Practices for Querying
1. **Always use FROM clause**: `FROM <http://rdfportal.org/ontology/mondo>`
2. **Use bif:contains for search**: Much faster than FILTER(CONTAINS())
3. **Filter blank nodes**: Add `FILTER(isIRI(?parent))` in hierarchy queries
4. **Use STRSTARTS for xrefs**: Efficient prefix filtering for cross-references
5. **Add LIMIT clauses**: Prevent timeouts, recommend LIMIT 50 for exploratory queries
6. **Start transitive queries from specific disease**: Don't query all diseases with rdfs:subClassOf*
7. **Use OLS4:searchClasses for simple searches**: More efficient than raw SPARQL
8. **Order by score**: `ORDER BY DESC(?sc)` for relevance ranking

### Data Quality Notes
- Definitions: 75% completeness (high-quality when present)
- Cross-references: 90% coverage, average 6.5 per disease (up to 50+ for some)
- Synonyms: 85% coverage, average 2.8 per disease
- Hierarchical structure: Well-defined with rdfs:subClassOf
- Deprecated terms: Properly marked with owl:deprecated
- OBO Foundry compliant: Follows standard ontology best practices
- Integration quality: Comprehensive mapping to major disease databases
- Coverage varies by database: UMLS (70%), Orphanet (34%), OMIM (33%), ICD-10 (9%)
