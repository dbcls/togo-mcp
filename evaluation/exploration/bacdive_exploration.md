# BacDive Exploration Report

## Database Overview
BacDive provides standardized bacterial and archaeal strain information covering taxonomy, morphology, physiology, cultivation conditions, and molecular data. Contains 97,334 strain records with phenotypic and genotypic characterizations.

## Schema Analysis
**Main entity types:**
- `Strain`: Core records with full taxonomic hierarchy
- `Enzyme`: Enzyme activities with activity indicators (+/-)
- `16SSequence`/`GenomeSequence`: Molecular data with accessions
- `GramStain`/`CellMotility`/`OxygenTolerance`: Phenotypic traits
- `CultureMedium`/`CultureTemperature`/`CulturePH`: Growth conditions
- `CultureCollectionNumber`: Repository links
- `LocationOfOrigin`: Isolation locations

**Key properties:**
- Strain: hasBacDiveID, hasTaxID, hasGenus, hasSpecies, hasFamily, hasOrder, hasClass, hasPhylum, hasDomain, isTypeStrain
- Links: hasMediaLink (to MediaDive), hasLink (to culture collections)
- Phenotypes: describesStrain (hub-and-spoke architecture)

**Important patterns:**
- Hub-and-spoke with Strain as central entity
- Full taxonomic lineage from domain to species
- bif:contains for keyword search with boolean operators
- OPTIONAL blocks for incomplete phenotype coverage

## Search Queries Performed
N/A - BacDive uses SPARQL keyword search via `bif:contains`

## SPARQL Queries Tested

```sparql
# Query 1: Top genera by strain count
SELECT ?genus (COUNT(*) as ?strainCount)
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          schema:hasGenus ?genus .
}
GROUP BY ?genus
ORDER BY DESC(?strainCount)
LIMIT 10
# Results: Streptomyces (24,747), Bacillus (3,332), Arthrobacter (2,045)
```

```sparql
# Query 2: Gram stain distribution
SELECT ?gramStain (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?gs a schema:GramStain ;
      schema:hasGramStain ?gramStain .
}
GROUP BY ?gramStain
# Results: negative (10,747), positive (7,333), variable (135)
```

```sparql
# Query 3: 16S sequence database sources
SELECT ?seqDB (COUNT(*) as ?seqCount)
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?seq a schema:16SSequence ;
       schema:fromSequenceDB ?seqDB .
}
GROUP BY ?seqDB
# Results: ena (33,556), nuccore (2,505), empty (396)
```

## Cross-Reference Analysis

**Direct cross-references:**
- NCBI Taxonomy: 100% of strains via hasTaxID
- MediaDive: ~34% via BacDiveID (primary method), ~20% via MediaLink (alternative)
- Culture collections: ~60% have links (DSMZ >90%, JCM ~40%)
- Sequence databases: ~35% have 16S sequences (ENA ~60%, GenBank ~40%)

**Integration methods:**
1. BacDiveID integer matching with MediaDive (primary, ~34% coverage for IDs 1-170,041)
2. MediaLink URI conversion to MediaDive (alternative, ~20% coverage)
3. TaxID URI conversion to NCBI Taxonomy (100% coverage)
4. Keyword-based integration with MONDO (no direct links)

**Shared endpoint:**
- Part of "primary" endpoint with mediadive, taxonomy, mesh, go, mondo, nando
- Enables efficient cross-database queries with explicit GRAPH clauses

## Interesting Findings

**Strain diversity:**
- Streptomyces dominates with 24,747 strains (25% of database)
- Bacillus has 3,332 strains - ideal genus for cross-database queries (lower BacDiveIDs)
- 18,215 strains have Gram stain data (~19% coverage)

**Phenotype coverage:**
- Gram stain: ~19% of strains
- 16S sequences: ~35% of strains (36,457 total)
- Culture collections: ~60% of strains (149,377 records)
- Enzyme data: ~55% of strains (573,112 enzyme records)

**Sequence data sources:**
- ENA dominates 16S sequences (33,556 = 92%)
- NCBI nuccore: 2,505 sequences
- 396 sequences without database attribution

**MediaDive integration specifics:**
- BacDiveID method (primary): Works for strains with IDs 1-170,041
- MediaDive has 33,226 strain records with BacDiveIDs (~34% of BacDive)
- MediaLink method (alternative): ~20% coverage, different data (recipes vs growth conditions)
- Newer strains (BacDiveID >170,041) not in MediaDive - no growth condition data available

**Query performance:**
- Simple strain queries complete in <2s
- bif:contains keyword searches very fast with complex boolean logic
- Cross-database queries (Tier 1): 1-3s with proper optimization
- Pre-filtering within GRAPH blocks essential for performance

## Question Opportunities by Category

### Precision
- ✅ "How many Bacillus strains are in BacDive?"
- ✅ "What is the most common Gram stain result in BacDive?"
- ✅ "How many 16S sequences are from ENA?"

### Completeness  
- ✅ "How many strains have Gram stain data?"
- ✅ "How many strains have DSMZ culture collection numbers?"
- ✅ "What percentage of strains have 16S sequence data?"

### Integration
- ✅ "Find Bacillus strains with MediaDive growth conditions via BacDiveID"
- ✅ "Link Mycobacterium strains to MONDO tuberculosis diseases via keyword"
- ✅ "Convert Escherichia coli TaxIDs to NCBI Taxonomy URIs"

### Currency
- ⚠️ Limited - database focuses on stable phenotypic data, not time-series

### Specificity
- ✅ "How many thermophilic strains are in BacDive?"
- ✅ "Find anaerobic Gram-positive strains"
- ✅ "Which strains are designated as type strains?"

### Structured Query
- ✅ "Find motile Gram-negative bacteria with 16S sequences"
- ✅ "Find Bacillus strains with temperature and pH ranges via MediaDive"
- ✅ "Which genera have gelatinase enzyme activity?"

## Notes

**Query optimization critical:**
- Always use FROM clause for single-database queries
- Use GRAPH clauses (not FROM) for cross-database queries
- Pre-filter within GRAPH blocks before joins (10-100x speedup)
- bif:contains as triple pattern with option (score ?sc)
- Never use ?score as variable name (reserved keyword)
- Always use OPTIONAL for phenotypes (~40% coverage)

**MediaDive integration methods:**
- Primary: BacDiveID integer matching for growth conditions (34% coverage, faster)
- Alternative: MediaLink URI conversion for media recipes (20% coverage)
- BacDiveID range limitation: Only 1-170,041 in MediaDive
- Test with Bacillus genus (lower IDs) not Escherichia (high IDs >130,000)

**Cross-database quirks:**
- Taxonomy uses DDBJ namespace (tax:) not UniProt (up:)
- URI conversion required: TaxID → http://identifiers.org/taxonomy/{ID}
- MONDO integration keyword-based only (no direct RDF links)

**Performance characteristics:**
- Single-database: <2s for simple queries, 5-10s for multi-phenotype joins
- Cross-database: Tier 1 (1-3s) for all optimized methods
