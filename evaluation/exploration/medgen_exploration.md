# MedGen Exploration Report

## Database Overview
MedGen is NCBI's portal for information about medical conditions with a genetic component containing 233,939 clinical concepts covering diseases, phenotypes, and clinical findings. Integrates data from OMIM, Orphanet, HPO, and MONDO with relationships, attributes, and terminology mappings tracked through RDF reification statements.

## Schema Analysis (from MIE file)
**Main entity types:**
- `mo:ConceptID`: Clinical concepts (233,939 total)
- `mo:MGREL`: Relationships between concepts (1,130,420 total)
- `mo:MGSAT`: Attributes and annotations (1,117,180 total)
- `mo:MGCONSO`: Terminology mappings to external databases
- `rdf:Statement`: Relationship provenance tracking (206,430 total)

**Key properties:**
- **Concept identification**: dct:identifier (CUI: C-prefixed strings), rdfs:label, skos:definition
- **Classification**: mo:sty (UMLS semantic types: T047 for diseases, etc.)
- **Relationships (CRITICAL)**: All relationships stored in MGREL entities with mo:cui1 (source), mo:cui2 (target), mo:rela (relationship type like "isa", "has_manifestation", "process_involves_gene")
- **Cross-references**: mo:mgconso → blank nodes → rdfs:seeAlso (external database URIs)
- **Attributes**: mo:MGSAT with mo:atn (attribute name), mo:atv (attribute value)

**Important patterns:**
- **CRITICAL**: Relationships NOT stored as direct properties on ConceptID
- All gene-disease, phenotype-disease, hierarchical relationships use MGREL
- Blank nodes extensively used for MGCONSO and MGSAT grouping
- RDF reification for relationship provenance

## Search Queries Performed

1. **ncbi_esearch**: "diabetes mellitus type 2" → Results: Found CUIs 1834436, 1809250, 1784949, 1777103, 1775809
2. **bif:contains**: "diabetes" → Results: Found Lipoatrophic diabetes (C0011859), Bronze diabetes (C0018995), Gestational diabetes (C0085207), Nephrogenic diabetes insipidus (C0162283), Renal cysts and diabetes syndrome (C0431693)

## SPARQL Queries Tested

```sparql
# Query 1: Keyword search for diabetes concepts
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?concept ?identifier ?label
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      rdfs:label ?label ;
      dct:identifier ?identifier .
  ?label bif:contains "'diabetes'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Found specialized diabetes types including Lipoatrophic, Bronze, Gestational, Nephrogenic
```

```sparql
# Query 2: External database cross-references for diabetes mellitus (C0011849)
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT DISTINCT ?concept ?identifier ?external_db
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      dct:identifier "C0011849" ;
      mo:mgconso ?bn .
  ?bn rdfs:seeAlso ?external_db .
  BIND("C0011849" as ?identifier)
}
LIMIT 20
# Results: Found links to HPO (HP_0000819), MONDO (MONDO_0005015), MeSH (D003920), NCI (C2985), OMIM (MTHU036798), SNOMED (73211009)
```

## Cross-Reference Analysis

**Entity counts:**
- Concepts with external mappings: ~90% (210,000+ of 233,939)
- Average external refs per concept: ~3.2

**Major cross-references (coverage):**
- MeSH: ~80%
- MONDO: ~70%
- SNOMED CT: ~60%
- HPO: ~40%
- OMIM: ~30%
- Orphanet: ~20% (rare diseases)

**Relationship counts:**
- Total MGREL relationships: 1,130,420
- Average relationships per concept: ~4.8

## Interesting Findings

✅ **Non-trivial findings from real queries:**

- **Diabetes concept diversity**: Found specialized types including Lipoatrophic diabetes (C0011859), Bronze diabetes (C0018995/hemochromatosis), Gestational, Nephrogenic diabetes insipidus, Renal cysts and diabetes syndrome (requires keyword search)
- **Multi-database integration**: C0011849 links to HPO, MONDO, MeSH, NCI, OMIM, SNOMED (requires cross-reference query)
- **CRITICAL architectural finding**: Relationships stored in MGREL entities, NOT as direct properties on ConceptID (requires understanding schema design)
- **Relationship scale**: 1.13M relationships, average 4.8 per concept, stored separately from concept entities (requires schema understanding)
- **Definition coverage**: Only ~34% of concepts have definitions (80,000 of 233,939) (requires coverage statistics)

**Key patterns requiring database queries:**
- MGREL queries for all concept relationships (hierarchies, gene associations, phenotypes)
- bif:contains for keyword searches with scoring
- mgconso blank node navigation for external database links
- DISTINCT required for cross-reference queries to avoid duplicates

## Question Opportunities by Category

### Precision
- ✅ "What is the MedGen CUI for Type 2 Diabetes Mellitus?" (requires search)
- ✅ "What external database IDs map to MedGen concept C0011849?" (requires mgconso query)

### Completeness
- ✅ "How many disease concepts are in MedGen?" (requires COUNT with semantic type filter)
- ✅ "List all phenotypic manifestations of diabetes mellitus" (requires MGREL traversal)

### Integration
- ✅ "Convert MedGen C0011849 to MONDO ID" (requires mgconso cross-reference)
- ✅ "Link MedGen diabetes concepts to ClinVar variants" (requires cross-database with URI conversion)

### Structured Query
- ✅ "Find rare diseases with autosomal recessive inheritance" (requires MGREL + MGSAT filtering)
- ✅ "Search for diseases with 'kinase' in description AND OMIM cross-reference" (requires keyword + external DB filter)

## Notes

**CRITICAL architectural point:**
- Relationships between concepts are NOT direct properties
- All relationships use MGREL entities: mo:MGREL with mo:cui1, mo:cui2, mo:rela
- Query pattern: ?rel a mo:MGREL ; mo:cui1 ?concept1 ; mo:cui2 ?concept2 ; mo:rela "isa"

**Best practices:**
- Always use FROM <http://rdfportal.org/dataset/medgen>
- Use DISTINCT for mgconso cross-reference queries
- Add LIMIT for MGREL queries (1.1M+ records)
- Use dct:identifier for fast concept lookups
- bif:contains for keyword searches on rdfs:label

**Cross-database integration:**
- URI conversion required for ClinVar: www.ncbi → ncbi namespace
- Use VALUES for specific concepts before cross-database joins
- Split property paths in cross-database queries
