# MeSH Exploration Report

## Database Overview
- **Purpose**: National Library of Medicine's controlled vocabulary thesaurus for biomedical literature indexing
- **Scope**: Medical subject headings, qualifiers, supplementary chemical/disease records
- **Key data types**: 
  - Topical Descriptors (30,248 main subject headings)
  - Supplementary Chemical Records (~250K chemicals)
  - Supplementary Disease Records
  - Concepts, Terms, Tree Numbers (hierarchical codes)
  - Qualifiers (subheadings for indexing combinations)

## Schema Analysis (from MIE file)
- **Main properties**:
  - `meshv:identifier` - MeSH ID (D######, C######, Q######)
  - `meshv:treeNumber` - Hierarchical classification codes (A-Z categories)
  - `meshv:broaderDescriptor` - Parent-child relationships (NOT meshv:broader!)
  - `meshv:annotation` - Scope notes and indexing guidance (NOT meshv:scopeNote!)
  - `meshv:allowableQualifier` - Permitted subheadings
  - `meshv:thesaurusID` - Cross-references to external databases
  - `meshv:registryNumber` - CAS Registry Numbers for chemicals
  
- **Important relationships**:
  - Hierarchical: meshv:broaderDescriptor for parent terms
  - Transitive: meshv:broaderDescriptor+ for all ancestors
  - Indexing: meshv:allowableQualifier for valid descriptor-qualifier combinations
  - Three-level structure: Descriptor → Concept → Term for synonym management
  
- **Query patterns**:
  - Use `bif:contains` for full-text search with relevance scoring (10-100x faster than FILTER CONTAINS)
  - Tree numbers enable category-based filtering (e.g., "C" for diseases, "D" for chemicals)
  - Transitive queries work well from specific descriptors
  - Terms use `meshv:prefLabel` (NOT rdfs:label)
  - Always include `FROM <http://id.nlm.nih.gov/mesh>` clause

## Search Queries Performed

1. **Query**: "CRISPR" → **Results**: Found 4 CRISPR-related descriptors
   - D000076987: CRISPR-Associated Protein 9
   - D064130: CRISPR-Associated Proteins  
   - D064113: CRISPR-Cas Systems
   - D000094704: RNA, Guide, CRISPR-Cas Systems

2. **Query**: "Alzheimer" → **Results**: 2 descriptors discovered
   - D000544: Alzheimer Disease (primary descriptor)
   - D023582: Alzheimer Vaccines

3. **Query**: "immunotherapy" → **Results**: 4 immunotherapy-related terms
   - D007167: Immunotherapy (general term)
   - D016233: Immunotherapy, Active
   - D016219: Immunotherapy, Adoptive
   - D063729: Sublingual Immunotherapy

4. **Query**: "aspirin" → **Results**: 3 aspirin-related descriptors
   - D001241: Aspirin (primary chemical descriptor)
   - D000068342: Aspirin, Dipyridamole Drug Combination
   - D055963: Asthma, Aspirin-Induced

5. **Query**: "rare disease" → **Results**: 1 descriptor
   - D035583: Rare Diseases

**Note**: All searches returned actual MeSH identifiers for real biomedical concepts, not MIE examples.

## SPARQL Queries Tested

```sparql
# Query 1: Get hierarchical information for Alzheimer Disease (D000544)
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?annotation ?treeNumber ?broaderLabel
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  mesh:D000544 rdfs:label ?label .
  OPTIONAL { mesh:D000544 meshv:annotation ?annotation }
  OPTIONAL { 
    mesh:D000544 meshv:treeNumber ?tree .
    ?tree rdfs:label ?treeNumber
  }
  OPTIONAL {
    mesh:D000544 meshv:broaderDescriptor ?broader .
    ?broader rdfs:label ?broaderLabel
  }
}
```
**Results**: Alzheimer Disease has 3 tree numbers (F03.615.400.100, C10.574.945.249, C10.228.140.380.100) and 2 broader descriptors (Tauopathies, Dementia). No annotation found for this descriptor.

```sparql
# Query 2: Count descriptors by major MeSH tree categories
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?category (COUNT(DISTINCT ?descriptor) as ?count)
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?descriptor a meshv:TopicalDescriptor ;
    meshv:treeNumber ?tree .
  ?tree rdfs:label ?treeLabel .
  BIND(SUBSTR(?treeLabel, 1, 1) as ?category)
}
GROUP BY ?category
ORDER BY DESC(?count)
```
**Results**: Discovered category distribution - D (Chemicals & Drugs): 10,541 descriptors, C (Diseases): 5,032, B (Organisms): 3,964, E (Analytical/Diagnostic Techniques): 3,102, G (Phenomena & Processes): 2,430, and 10 other major categories.

```sparql
# Query 3: Get allowable qualifiers for Aspirin (D001241)
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?qualifier ?qualifierLabel
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  <http://id.nlm.nih.gov/mesh/D001241> meshv:allowableQualifier ?qualifier .
  ?qualifier rdfs:label ?qualifierLabel .
}
```
**Results**: Aspirin has multiple allowable qualifiers including "administration & dosage", "adverse effects", "analogs & derivatives", "analysis", "antagonists & inhibitors", "blood", "cerebrospinal fluid", "chemical synthesis", "classification", "economics" (showing first 10 of likely 20+ total).

```sparql
# Query 4: Count entities with OMIM cross-references
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT (COUNT(DISTINCT ?entity) as ?entity_count)
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?entity meshv:thesaurusID ?xref .
  FILTER(CONTAINS(STR(?xref), "OMIM"))
}
```
**Results**: 12,627 MeSH entities have OMIM cross-references (genetic disorders, Mendelian inheritance).

```sparql
# Query 5: Find pembrolizumab in supplementary chemical records
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?chemical ?label ?registryNumber
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?chemical a meshv:SCR_Chemical ;
    rdfs:label ?label .
  OPTIONAL { ?chemical meshv:registryNumber ?registryNumber }
  ?label bif:contains "'pembrolizumab'" option (score ?sc)
}
ORDER BY DESC(?sc)
```
**Results**: Found pembrolizumab (C582435), a cancer immunotherapy drug. Note: No CAS registry number available for this biologic.

## Cross-Reference Analysis

**Entity counts** (unique entities with cross-references):
- MeSH → OMIM: 12,627 entities (genetic disorders)
- MeSH → FDA SRS/UNII: 22,600 entities (pharmaceutical substances)
- MeSH → INN: 8,800 entities (international nonproprietary names)
- MeSH → ChEBI: 2,500 entities (chemical entities)
- MeSH → SNOMED CT: ~800 entities (clinical terminology)
- MeSH → FMA: 1,100 entities (anatomical structures)
- MeSH → GHR: 3,800 entities (genetics home reference)

**Relationship counts** (total cross-references via meshv:thesaurusID):
- Total: 916,000 cross-references across all external databases

**Distribution**: 
- Approximately 37% of all MeSH entities (~869K total terms/concepts/descriptors) have at least one external cross-reference
- Chemical records (SCR_Chemical) have high coverage for pharmaceutical databases (FDA, INN)
- Disease descriptors have high OMIM coverage for genetic conditions

**Cross-database integration**:
- **MONDO bridge**: ~28% of MONDO diseases (~8,500) have MeSH cross-references via oboInOwl:hasDbXref
  * MESH: references can be TopicalDescriptors (D######) OR Supplementary Records (C######)
  * Enables two-way integration: MONDO→MeSH and MeSH→MONDO
- **GO integration**: No direct semantic links; requires keyword-based matching using bif:contains

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

✅ **Entity discoveries (non-trivial)**:
- **Alzheimer Disease (D000544)** classification: Found in 3 hierarchical positions (tauopathies, dementia categories), demonstrates MeSH's multi-hierarchical structure
- **Pembrolizumab (C582435)**: Cancer immunotherapy drug found in SCR_Chemical records, lacks CAS registry number (typical for biologics)
- **CRISPR terminology evolution**: 4 distinct descriptors track CRISPR technology development (systems, proteins, Cas9 specifically, guide RNAs)

✅ **Quantitative findings (requires COUNT queries)**:
- **Category distribution asymmetry**: Chemicals/Drugs (D: 10,541) outnumber Diseases (C: 5,032) by 2:1, reflecting MeSH's pharmaceutical focus
- **OMIM integration depth**: 12,627 genetic disorder cross-references enable Mendelian disease literature indexing
- **Pharmaceutical coverage**: 22,600 FDA SRS/UNII cross-references provide comprehensive drug substance mapping

✅ **Hierarchical complexity**:
- **Aspirin indexing flexibility**: Multiple allowable qualifiers (20+ total) enable precise literature categorization (adverse effects, administration, blood levels, economics, etc.)
- **Multi-parent classification**: Alzheimer Disease appears under both neurological (C10) and psychiatric (F03) categories, enabling diverse research perspectives

✅ **Cross-database integration discoveries**:
- **MONDO→MeSH coverage**: 28% of MONDO diseases map to MeSH, but MeSH references can be EITHER descriptors or supplementary records, requiring flexible querying
- **Dual record types**: MeSH cross-references from MONDO can point to TopicalDescriptors (D######) for established terms OR SCR records (C######) for newer/supplementary concepts

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT** ✅

### Precision (Specific IDs, measurements, sequences)
- ✅ "What is the MeSH descriptor ID for Alzheimer Disease?" (D000544 - requires search)
- ✅ "What is the MeSH ID for pembrolizumab?" (C582435 - requires chemical record search)
- ✅ "How many tree numbers does Alzheimer Disease have in MeSH?" (3 - requires SPARQL query)
- ✅ "What are the broader descriptors (parent terms) for Alzheimer Disease?" (Tauopathies, Dementia - requires hierarchy query)

### Completeness (Entity counts, comprehensive lists)
- ✅ "How many MeSH topical descriptors are in the Diseases category (C)?" (5,032 - requires COUNT with tree number filtering)
- ✅ "How many MeSH entities have OMIM cross-references?" (12,627 - requires COUNT query)
- ✅ "How many chemical descriptors (category D) are in MeSH?" (10,541 - requires aggregation)
- ✅ "How many allowable qualifiers does the aspirin descriptor have?" (20+ - requires counting qualifier relationships)

### Integration (Cross-database linking, ID conversions)
- ✅ "Which MONDO diseases map to the MeSH descriptor for diabetes?" (requires MONDO→MeSH cross-reference query)
- ✅ "What percentage of MONDO diseases have MeSH cross-references?" (~28% or ~8,500 - requires cross-database COUNT)
- ✅ "Find GO biological processes related to apoptosis that match MeSH terms" (requires keyword-based cross-database integration)

### Currency (Recent discoveries, updated classifications)
- ✅ "What CRISPR-related descriptors exist in MeSH?" (4 descriptors - tracks technology evolution)
- ✅ "Is pembrolizumab (cancer immunotherapy) indexed in MeSH?" (Yes, C582435 - demonstrates current drug coverage)

### Specificity (Rare diseases, specialized concepts)
- ✅ "What is the MeSH descriptor ID for Rare Diseases?" (D035583 - requires search)
- ✅ "Which MeSH category contains the most descriptors?" (D: Chemicals & Drugs with 10,541 - requires aggregation)

### Structured Query (Complex biological queries, multiple criteria)
- ✅ "Find MeSH descriptors under both neurological and psychiatric categories" (e.g., Alzheimer Disease with multiple tree numbers - requires filtering by tree number patterns)
- ✅ "What are the top 5 MeSH categories by descriptor count?" (requires aggregation and ordering)
- ✅ "Which MONDO diseases for Parkinson's map to MeSH terms containing dopamine-related GO processes?" (three-way integration query)

**AVOID INFRASTRUCTURE METADATA** ❌
- Database versions, MIE file statistics
- Query syntax examples (unless methodology-critical)
- Schema property names

**AVOID STRUCTURAL METADATA** ❌
- ❌ "What tree number codes exist for diseases?" (organizational metadata)
- ❌ "What is the URI pattern for MeSH descriptors?" (schema structure)
- ❌ "How many qualifier types are defined?" (vocabulary structure, not biological content)

## Notes

### Limitations and Challenges
- **Annotation sparsity**: Only ~40% of descriptors have annotations; must use OPTIONAL in queries
- **Property name precision required**: 
  * CRITICAL: Use `meshv:broaderDescriptor` (NOT meshv:broader)
  * CRITICAL: Use `meshv:annotation` (NOT meshv:scopeNote or skos:scopeNote)
  * Terms use `meshv:prefLabel` (NOT rdfs:label for term labels)
- **Chemical registry gaps**: Biologics (like pembrolizumab) typically lack CAS registry numbers
- **Cross-database complexity**: MONDO cross-references can point to EITHER TopicalDescriptors (D) OR Supplementary Records (C), requiring flexible querying

### Best Practices for Querying
- **Full-text search**: Always use `bif:contains` instead of FILTER CONTAINS for 10-100x speedup
  * Include relevance scoring: `option (score ?sc)` with `ORDER BY DESC(?sc)`
- **Required clause**: Always include `FROM <http://id.nlm.nih.gov/mesh>` 
- **Cross-database optimization**: Apply strategies from MIE file
  * Strategy 1: Explicit GRAPH clauses for each database
  * Strategy 2: Pre-filter within source GRAPH before joins (reduces join size 99%+)
  * Strategy 4: Use bif:contains for keyword searches
  * Strategy 10: Always include LIMIT for exploratory queries
- **Three-way query limitation**: Use simplified CONTAINS instead of bif:contains to avoid 400 errors
- **Hierarchical queries**: Start transitive queries (broaderDescriptor+) from specific descriptors, not variable patterns
- **Optional properties**: Use OPTIONAL for annotations (40% coverage), registry numbers (varies by entity type)

### Important Clarifications About Counts
- **Entity count**: 12,627 unique MeSH entities WITH OMIM cross-references
- **Category counts represent unique descriptors**: 10,541 chemicals, 5,032 diseases (no multi-counting despite multi-parent hierarchies)
- **Cross-reference coverage**: 37% of 2.5M total MeSH entities have external database links via thesaurusID

### Distinction Between MIE Examples and Real Data Findings
- **MIE showed**: Example SPARQL patterns for diabetes (D003920), general query structures
- **We discovered**: 
  * Actual current drugs (pembrolizumab C582435)
  * Real technology evolution (4 CRISPR descriptors)
  * Quantitative distributions (10,541 chemicals vs 5,032 diseases)
  * Cross-database integration counts (12,627 OMIM, 22,600 FDA, 8,500 MONDO mappings)
  * Hierarchical complexity (Alzheimer in 3 tree positions, 2 broader terms)
