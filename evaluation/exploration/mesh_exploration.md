# MeSH (Medical Subject Headings) Exploration Report

## Database Overview
MeSH is the National Library of Medicine's controlled vocabulary thesaurus for biomedical literature indexing:
- **2.5 million total entities**
- **30,248 topical descriptors** (subject headings)
- **250,445 supplementary chemical records**
- **869,536 terms** (synonyms and variants)
- **466,976 concepts**
- **16 hierarchical categories** (A-Z tree structure)
- Used for indexing PubMed and other NLM databases
- Annual updates with comprehensive cross-references

## Schema Analysis (from MIE file)

### Main Properties Available
- **TopicalDescriptors**: Labels, identifiers (D codes), tree numbers, broader descriptors, annotations
- **Supplementary Chemical Records**: Labels, identifiers (C codes), CAS registry numbers
- **Concepts**: Preferred terms for synonym management
- **Terms**: Preferred labels (use meshv:prefLabel, NOT rdfs:label)
- **Tree Numbers**: Hierarchical alphanumeric codes (A-Z categories)
- **Qualifiers**: Allowable subheadings for descriptor combinations
- **Annotations**: Scope notes and indexing guidance (~40% of descriptors)
- **Cross-References**: 916K total via thesaurusID (FDA SRS/UNII, OMIM, ChEBI, SNOMED CT)

### Important Relationships
- **meshv:broaderDescriptor** - Parent-child hierarchy (CRITICAL: not meshv:broader)
- **meshv:treeNumber** - Hierarchical classification codes
- **meshv:annotation** - Scope notes (CRITICAL: not meshv:scopeNote)
- **meshv:preferredConcept** - Links descriptor to concept
- **meshv:preferredTerm** - Links concept to term
- **meshv:allowableQualifier** - Permitted subheadings
- **meshv:thesaurusID** - External database cross-references
- **meshv:registryNumber** - CAS registry numbers for chemicals
- **meshv:identifier** - MeSH unique identifiers (D/C codes)

### Query Patterns Observed
- **CRITICAL**: Use `meshv:broaderDescriptor` (NOT meshv:broader)
- **CRITICAL**: Use `meshv:annotation` (NOT meshv:scopeNote)
- **CRITICAL**: Terms use `meshv:prefLabel` (NOT rdfs:label)
- **Keyword search**: Use `bif:contains` with relevance scoring
- **Hierarchical queries**: Use `broaderDescriptor+` from specific descriptors
- **Tree categories**: Use SUBSTR or STRSTARTS on tree number labels
- **FROM clause required**: `FROM <http://id.nlm.nih.gov/mesh>`

## Search Queries Performed

1. **Query: "diabetes"** → Results: 10 diabetes-related terms including rare subtypes (6q24-Related Transient Neonatal Diabetes, ADH-Resistant Diabetes Insipidus, etc.)
2. **Query: "Erdheim-Chester"** → Results: 1 result - Erdheim-Chester Disease (rare histiocytic disorder)
3. **Topical descriptors for "diabetes mellitus"** → Results: 5 main descriptors (D003920-D003924)
4. **Tree numbers for Type 2 Diabetes** → Results: C18.452.394.750.149 and C19.246.300
5. **Insulin chemicals** → Results: 10 insulin variants and combinations (no CAS numbers in sample)

## SPARQL Queries Tested

```sparql
# Query 1: Search topical descriptors for diabetes mellitus
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?descriptor ?label
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?descriptor a meshv:TopicalDescriptor ;
    rdfs:label ?label .
  ?label bif:contains "'diabetes mellitus'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: D003920 (Diabetes Mellitus), D003921 (Experimental), D003922 (Type 1),
# D003923 (Lipoatrophic), D003924 (Type 2)
```

```sparql
# Query 2: Get annotations and tree numbers for Type 2 Diabetes
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?annotation ?treeNumber
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  mesh:D003924 rdfs:label ?label .
  OPTIONAL { mesh:D003924 meshv:annotation ?annotation }
  OPTIONAL { 
    mesh:D003924 meshv:treeNumber ?tree .
    ?tree rdfs:label ?treeNumber
  }
}
# Results: "Diabetes Mellitus, Type 2" with tree numbers C18.452.394.750.149 and C19.246.300
# Note: No annotation found (only ~40% have annotations)
```

```sparql
# Query 3: Find insulin chemical records
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?chemical ?label ?registryNumber
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?chemical a meshv:SCR_Chemical ;
    rdfs:label ?label .
  OPTIONAL { ?chemical meshv:registryNumber ?registryNumber }
  ?label bif:contains "'insulin'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Various insulin combinations and derivatives (labels only, registry numbers sparse in results)
```

## Interesting Findings

### Specific Entities for Questions
- **D003924**: Diabetes Mellitus, Type 2 - major disease descriptor
- **D003920**: Diabetes Mellitus - general term
- **T459455**: Erdheim-Chester Disease - rare disease example
- **C codes**: Chemical supplementary records (insulin variants)
- **Tree numbers**: C18.452.394.750.149 (Type 2 Diabetes classification)

### Unique Properties
- **Three-level structure**: Descriptor → Concept → Term for synonym management
- **Hierarchical tree codes**: Alphanumeric classification (e.g., C18.452...)
- **Allowable qualifiers**: Constrain valid descriptor-subheading combinations
- **Scope notes**: Indexing guidance in ~40% of descriptors
- **Annual updates**: Comprehensive yearly revisions
- **16 major categories**: A-Z tree structure (Anatomy, Organisms, Diseases, etc.)
- **Average 2.7 tree numbers** per descriptor (multiple classifications)

### Connections to Other Databases
- **FDA SRS/UNII**: 22.6K pharmaceutical substance identifiers
- **OMIM**: 12.5K genetic disorder cross-references
- **ChEBI**: 2.5K chemical entity links
- **SNOMED CT**: 800+ clinical terminology mappings
- **INN**: 8.8K International Nonproprietary Names
- **FMA**: 1.1K Foundational Model of Anatomy links
- **GHR**: 3.8K Genetics Home Reference links

### Specific Verifiable Facts
- **2,456,909 total entities**
- **30,248 topical descriptors**
- **250,445 chemical records**
- **D003924**: MeSH descriptor for Type 2 Diabetes
- **Tree C18.452.394.750.149**: Classification path for Type 2 Diabetes
- **~99.6% descriptors** have broaderDescriptor relationships
- **~40% descriptors** have annotations
- **Average 22 qualifiers** per descriptor

## Question Opportunities by Category

### Precision
- "What is the MeSH descriptor ID for Diabetes Mellitus, Type 2?" → D003924
- "What is the MeSH ID for Erdheim-Chester disease?" → T459455
- "What are the tree numbers for Type 2 Diabetes?" → C18.452.394.750.149, C19.246.300
- "What is the MeSH term for general Diabetes Mellitus?" → D003920
- "How many tree numbers does D003924 have?" → 2

### Completeness
- "How many topical descriptors are in MeSH?" → 30,248
- "How many chemical records exist?" → 250,445
- "How many total entities in MeSH?" → 2.5 million
- "How many diabetes-related MeSH terms exist?" → Count from search
- "How many descriptors have annotations?" → ~40% (need count)

### Integration
- "What is the OMIM ID linked to MeSH descriptor X?" → Via thesaurusID
- "Find ChEBI IDs for MeSH chemical records" → Cross-reference query
- "Link MeSH D003924 to FDA UNII codes" → Via thesaurusID
- "What SNOMED CT codes map to diabetes descriptor?" → Cross-references
- "Convert MeSH tree numbers to descriptor IDs" → Tree query

### Currency
- "How many MeSH terms were added in 2024?" → Annual update info
- "What are the newest disease descriptors?" → Recent additions
- "Find recently updated chemical records" → Update tracking
- "What COVID-19 related MeSH terms exist?" → Recent disease additions

### Specificity
- "What is the annotation for rare disease X?" → Scope note query
- "Find MeSH terms for Japanese rare diseases" → Specific niche
- "What allowable qualifiers exist for descriptor Y?" → Qualifier query
- "Find chemicals with specific CAS registry numbers" → Chemical lookup
- "What is the tree classification for rare enzyme deficiency?" → Niche disease

### Structured Query
- "Find disease descriptors in tree category C18 with annotations" → Category + property
- "List all Type 2 Diabetes related terms with their broader descriptors" → Hierarchy
- "Find chemical records with both CAS numbers AND FDA UNII codes" → Multiple xrefs
- "Search for cancer descriptors with >3 tree numbers" → Complex filter
- "Find descriptors in categories C18 AND C19" → Multiple category filter

## Notes

### Critical Property Names
**MUST USE CORRECT PROPERTIES** (common errors):
1. **meshv:broaderDescriptor** (NOT meshv:broader) - for hierarchy
2. **meshv:annotation** (NOT meshv:scopeNote or skos:scopeNote) - for scope notes
3. **meshv:prefLabel** for Terms (NOT rdfs:label) - term preferred labels
4. **FROM <http://id.nlm.nih.gov/mesh>** - required in all queries

### Limitations
- **Annotations sparse**: Only ~40% of descriptors have annotations (use OPTIONAL)
- **Chemical CAS numbers**: Not all chemical records have registry numbers
- **No broader for chemicals**: SCR_Chemical records lack hierarchical structure
- **Complex synonym structure**: Three-level Descriptor→Concept→Term requires navigation
- **Large dataset**: 2.5M entities require careful filtering and LIMIT clauses

### Best Practices
1. **ALWAYS use bif:contains** for keyword searches (with option (score ?sc))
2. **ALWAYS use meshv:broaderDescriptor** (not meshv:broader)
3. **ALWAYS use meshv:annotation** (not meshv:scopeNote)
4. **ALWAYS include FROM clause**: `FROM <http://id.nlm.nih.gov/mesh>`
5. **Use OPTIONAL** for annotations and registry numbers
6. **Start transitive queries** from specific descriptors
7. **Filter by entity type** first (TopicalDescriptor, SCR_Chemical)
8. **Add LIMIT** to prevent timeouts (50-100 for exploration)
9. **ORDER BY DESC(?sc)** for relevance-ranked results

### Performance Notes
- bif:contains label searches: Very fast with relevance ranking
- Tree number filtering: Efficient with STRSTARTS or SUBSTR
- Transitive broaderDescriptor+: Works well from specific starting points
- Full descriptor scans: Require careful filtering and LIMIT
- Cross-reference queries: Fast when filtering by specific database (OMIM, ChEBI)
- Recommend LIMIT 50 for exploratory queries
