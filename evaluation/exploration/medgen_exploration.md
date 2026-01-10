# MedGen Exploration Report

## Database Overview
- **Purpose**: NCBI's portal for medical genetics information linking clinical concepts to genetic components
- **Scope**: 233,939 clinical concepts (ConceptID entities) covering diseases, phenotypes, and clinical findings
- **Key data types**:
  - 233,939 ConceptID (clinical concepts with UMLS CUI identifiers)
  - 1,130,420 MGREL (relationships between concepts)
  - 1,117,180 MGSAT (attributes like inheritance patterns)
  - 206,430 RDF reification statements (relationship provenance)

## Schema Analysis (from MIE file)

### Main Properties Available
- **ConceptID**: `dct:identifier` (CUI), `rdfs:label`, `mo:sty` (semantic type), `skos:definition`
- **MGREL**: `mo:cui1`, `mo:cui2`, `mo:rela` (relationship type), `dct:source`
- **MGSAT**: `mo:atui`, `mo:cui`, `mo:atn` (attribute name), `mo:atv` (attribute value)
- **MGCONSO**: `rdfs:seeAlso` (external database cross-references via blank nodes)

### Important Relationships
**CRITICAL ARCHITECTURAL NOTE**: All relationships between concepts are stored in MGREL entities, NOT as direct properties on ConceptID. This is a fundamental design pattern in MedGen.

- Relationships via `mo:MGREL` with `mo:rela` types: "isa", "inverse_isa", "has_manifestation", "manifestation_of", "gene" associations
- External mappings via `mo:mgconso` blank nodes containing `rdfs:seeAlso` to MONDO, HPO, MeSH, OMIM, Orphanet
- Provenance tracking via RDF reification statements with `dct:source` attribution

### Query Patterns Observed
1. **Identifier lookup**: Very fast (<1 sec) using `dct:identifier`
2. **Keyword search**: Use `bif:contains` with relevance scoring
3. **Relationships**: MUST query `mo:MGREL` entities, NOT direct properties
4. **Cross-references**: Always use DISTINCT to avoid duplicates from MGCONSO
5. **Large datasets**: Always LIMIT queries on MGREL, MGSAT, rdf:Statement (>1M records each)
6. **Graph specification**: Always include `FROM <http://rdfportal.org/dataset/medgen>`

## Search Queries Performed

### Query 1: E-utilities Search for Diabetes
**Method**: ncbi_esearch
**Query**: "diabetes mellitus"
**Results**: 1,399 total concepts found
- Top concepts include specific diabetes subtypes
- C6012785: Congenital malabsorptive diarrhea with diabetes
- C6007960: Finding about diabetes medication dosing
- C6010364: Diabetes due to chronic pancreatitis

### Query 2: Concept Details via E-utilities
**Method**: ncbi_esummary for C6012785, C6007960, C6010364
**Results**: Retrieved full concept metadata including:
- Semantic types (T047: Disease, T033: Finding)
- OMIM cross-references (604882)
- SNOMED CT codes
- Preferred names and definitions

### Query 3: Fabry Disease Keyword Search
**Method**: SPARQL with bif:contains
**Results**: 4 Fabry-related concepts found:
- C0002986: Fabry disease (primary)
- C1970820: Fabry disease, cardiac variant
- C5395738: Autonomic neuropathy due to Fabry disease
- C5438969: Glomerular disease due to Fabry disease

### Query 4: Diabetes External Cross-References
**Method**: SPARQL on MGCONSO for C0011849
**Results**: Found 9 external database references:
- MONDO:0011849 (disease ontology)
- MeSH: D003920
- OMIM: multiple entries
- SNOMED CT codes
- Orphanet, NCI Thesaurus

### Query 5: Diabetes Relationships
**Method**: SPARQL on MGREL
**Results**: 20+ relationships including:
- Child types (isa): Lipoatrophic diabetes, Gestational diabetes
- Manifestations (has_manifestation): Ataxia-telangiectasia, Friedreich ataxia, MELAS syndrome, Werner syndrome
- Shows complex disease-syndrome associations

## SPARQL Queries Tested

```sparql
# Query 1: Basic concept lookup
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concept ?identifier ?label ?sty ?definition
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      dct:identifier "C0011849" ;
      rdfs:label ?label ;
      mo:sty ?sty .
  BIND("C0011849" as ?identifier)
  OPTIONAL { ?concept skos:definition ?definition }
}
LIMIT 10
# Results: Diabetes mellitus (T047), "A group of abnormalities characterized by hyperglycemia and glucose intolerance."
```

```sparql
# Query 2: External database cross-references (CRITICAL: Use DISTINCT)
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT DISTINCT ?concept ?identifier ?external_db
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      dct:identifier "C0002986" ;
      mo:mgconso ?bn .
  ?bn rdfs:seeAlso ?external_db .
  BIND("C0002986" as ?identifier)
}
LIMIT 20
# Results: Fabry disease links to MONDO, MeSH, OMIM, Orphanet, SNOMED CT, etc.
```

```sparql
# Query 3: Relationship navigation via MGREL (CRITICAL pattern)
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?disease ?disease_label ?related ?related_label ?rel_type
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?disease a mo:ConceptID ;
      dct:identifier "C0011849" ;
      rdfs:label ?disease_label .
  ?rel a mo:MGREL ;
      mo:cui1 ?disease ;
      mo:cui2 ?related ;
      mo:rela ?rel_type .
  ?related rdfs:label ?related_label .
  FILTER(CONTAINS(LCASE(?rel_type), "gene") || CONTAINS(LCASE(?rel_type), "manifestation") || CONTAINS(LCASE(?rel_type), "isa"))
  FILTER(?disease != ?related)
}
LIMIT 20
# Results: Found hierarchical (isa) and phenotypic (has_manifestation) relationships for diabetes
```

## Interesting Findings

### Specific Entities for Questions
1. **C0011849 (Diabetes mellitus)**: Well-connected concept with multiple relationships and cross-references
2. **C0002986 (Fabry disease)**: Rare disease with OMIM (301500, 300644), MONDO (0010526), Orphanet (324) links
3. **Semantic types**: T047 (Disease), T033 (Finding), T191 (Neoplasm) provide classification
4. **Relationship types**: "isa", "inverse_isa", "has_manifestation", "manifestation_of" enable hierarchy navigation
5. **Gestational diabetes (C0085207)**: Example of isa relationship to diabetes mellitus

### Unique Properties
- **UMLS integration**: Uses CUI identifiers and semantic types (STY)
- **Relationship architecture**: MGREL entities (not direct properties) - CRITICAL design pattern
- **Provenance tracking**: RDF reification statements track relationship sources
- **Blank node pattern**: MGCONSO uses blank nodes for grouping external references
- **Multi-source integration**: OMIM, HPO, MONDO, MeSH, Orphanet, SNOMED CT

### Connections to Other Databases
- **MONDO**: ~70% coverage (disease ontology)
- **MeSH**: ~80% coverage (medical subject headings)
- **OMIM**: ~30% coverage (genetic disorders)
- **HPO**: ~40% coverage (phenotypes)
- **Orphanet**: ~20% coverage (rare diseases)
- **SNOMED CT**: ~60% coverage (clinical terminology)
- **ClinVar**: Direct links for genetic variants
- **NCBI Gene**: Gene associations via MGREL

### Verifiable Facts
1. MedGen contains exactly 233,939 clinical concepts
2. Fabry disease CUI is C0002986 with OMIM ID 301500
3. Diabetes mellitus (C0011849) has semantic type T047 (Disease or Syndrome)
4. Total of 1,130,420 relationships stored in MGREL
5. ~34% of concepts have formal definitions (skos:definition)

## Question Opportunities by Category

### Precision
✅ **Specific medical concept IDs**:
- "What is the MedGen CUI for Fabry disease?" (C0002986)
- "What is the OMIM ID for Fabry disease in MedGen?" (301500, 300644)
- "What semantic type is assigned to diabetes mellitus?" (T047)
- "What is the definition of acute myeloid leukemia in MedGen?" (from skos:definition)

❌ Avoid: Database version, update schedules

### Completeness
✅ **Counts of medical entities**:
- "How many clinical concepts are in MedGen?" (233,939)
- "How many relationships are stored in MGREL?" (1,130,420)
- "How many Fabry disease variants are in MedGen?" (4 found)
- "Count diabetes-related concepts" (1,399 from esearch)

❌ Avoid: Infrastructure counts

### Integration
✅ **Cross-database medical concept linking**:
- "Convert MedGen C0002986 to MONDO identifier" (MONDO:0010526)
- "What OMIM IDs correspond to Fabry disease in MedGen?" (301500, 300644)
- "Link MedGen diabetes concept to MeSH" (D003920)
- "Find Orphanet ID for Fabry disease" (324)

❌ Avoid: Server infrastructure links

### Currency
✅ **Current medical knowledge**:
- "What syndromes have diabetes as a manifestation according to MedGen?" (current list)
- "How many diabetes subtypes are currently defined?" (from recent isa relationships)
- "What are the latest rare disease associations in MedGen?" (requires date filtering)

❌ Avoid: Database release versions

### Specificity
✅ **Rare diseases and specific phenotypes**:
- "What is the MedGen ID for Fabry disease cardiac variant?" (C1970820)
- "Find autonomic neuropathy due to Fabry disease" (C5395738)
- "What is glomerular disease due to Fabry in MedGen?" (C5438969)
- "Identify MELAS syndrome manifestations" (via MGREL relationships)

❌ Avoid: Generic infrastructure

### Structured Query
✅ **Complex medical queries**:
- "Find all diseases with 'isa' relationship to diabetes mellitus"
- "List genetic syndromes that have diabetes as manifestation"
- "Which MedGen concepts map to both OMIM AND Orphanet?"
- "Find diseases classified as T047 semantic type with MONDO cross-references"

❌ Avoid: Technical infrastructure queries

## Notes

### Limitations
- **Definition coverage**: Only ~34% of concepts have skos:definition
- **Relationship architecture**: MUST use MGREL entities - direct properties on ConceptID don't exist for relationships
- **Duplicate cross-references**: MGCONSO queries return duplicates - always use DISTINCT
- **Large datasets**: MGREL (1.1M), MGSAT (1.1M), rdf:Statement (206K) require LIMIT
- **No labels on some entities**: Some referenced concepts may lack rdfs:label

### Best Practices
1. **For identifier lookup**: Use `dct:identifier` (fast, indexed)
2. **For keyword search**: Use `bif:contains` with relevance scoring
3. **For relationships**: MUST query `mo:MGREL` with `mo:cui1`, `mo:cui2`, `mo:rela`
4. **For cross-references**: Use DISTINCT on MGCONSO queries
5. **Always LIMIT**: On MGREL, MGSAT, rdf:Statement queries
6. **Graph specification**: Always include `FROM <http://rdfportal.org/dataset/medgen>`
7. **Relationship types**: Filter `mo:rela` for "isa", "has_manifestation", "gene" etc.

### Critical Architectural Understanding
**THE MOST IMPORTANT PATTERN**: MedGen does NOT use direct relationship properties like `mo:disease_has_associated_gene` or `mo:isa` on ConceptID entities. ALL relationships are stored in separate MGREL entities with the pattern:
```sparql
?rel a mo:MGREL ;
    mo:cui1 ?concept1 ;
    mo:cui2 ?concept2 ;
    mo:rela ?relationship_type .
```
This is fundamentally different from many other RDF databases and is the primary cause of empty results if not understood correctly.
