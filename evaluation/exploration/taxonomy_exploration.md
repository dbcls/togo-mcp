# NCBI Taxonomy Exploration Report

## Database Overview
- **Purpose**: Comprehensive biological taxonomic classification for all organisms
- **Scope**: 2.7M+ taxa covering bacteria, archaea, fungi, plants, and animals
- **Key entities**: Taxa (organisms), Ranks (taxonomic levels), Genetic codes
- **Integration**: Links to UniProt, OBO ontologies, multiple taxonomic databases

## Schema Analysis (from MIE file)

### Main Properties
- `rdfs:label`: Organism name (e.g., "Homo sapiens")
- `dcterms:identifier`: Numeric taxon ID (e.g., "9606")
- `tax:rank`: Taxonomic rank (Species, Genus, Family, Order, Class, Phylum, Kingdom)
- `tax:scientificName`: Official scientific name with authority
- `tax:commonName`: Common names (e.g., "human", "E. coli")
- `tax:synonym`: Alternative names
- `tax:geneticCode`: Nuclear genetic code
- `tax:geneticCodeMt`: Mitochondrial genetic code
- `rdfs:subClassOf`: Parent taxon (hierarchical relationship)
- `owl:sameAs`: Cross-database identifiers (5 per taxon average)
- `rdfs:seeAlso`: Links to UniProt Taxonomy

### Important Relationships
- **Hierarchy**: `rdfs:subClassOf` creates taxonomic tree (species → genus → family → ... → root)
- **Identity**: `owl:sameAs` provides equivalences across ontology systems
- **Integration**: `rdfs:seeAlso` links to protein databases (UniProt)
- **Classification**: 47 different taxonomic ranks available

### Query Patterns Observed
- Use `bif:contains` for efficient full-text search with relevance scoring
- Always include `FROM <http://rdfportal.org/ontology/taxonomy>` clause
- Use `rdfs:subClassOf*` for lineage queries (with caution - can be slow)
- Filter by `tax:rank` to improve performance
- Start transitive queries from specific taxa, not all taxa
- Add `LIMIT` clauses to prevent timeouts

## Search Queries Performed

1. **Query**: "Streptococcus pyogenes" (ncbi_esearch)
   - **Results**: Found taxID 1314, species rank, division firmicutes
   - Scientific name verified, no common name
   - Modified: 2018/11/23

2. **Query**: Multiple taxa summary (9606, 1314, 562)
   - **Results**: Retrieved detailed metadata for human, S. pyogenes, E. coli
   - All active status, different divisions (primates, firmicutes, enterobacteria)
   - Modification dates range from 2018-2024

3. **Query**: "thermophile" (SPARQL bif:contains)
   - **Results**: Found 2 thermophilic organisms
   - "anaerobic thermophile IC-BH" (taxID 44257)
   - "Gram-positive thermophile ODP159-02" (taxID 307125)

4. **Query**: "Pyrococcus furiosus" (ncbi_esearch)
   - **Results**: Found taxID 2261
   - Hyperthermophilic archaeon commonly used in research

5. **Query**: Cross-references for human (taxID 9606)
   - **Results**: 5 owl:sameAs identifiers found:
     - OBO NCBITaxon, DDBJ, NCBI Web, OBO OWL, Berkeley BOP
   - Demonstrates comprehensive cross-database linking

## SPARQL Queries Tested

```sparql
# Query 1: Full-text search for thermophiles
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?taxon ?id ?label
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  ?taxon a tax:Taxon ;
    rdfs:label ?label ;
    dcterms:identifier ?id .
  ?label bif:contains "'thermophile'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10

# Results: Found 2 thermophilic organisms with relevance scoring
```

```sparql
# Query 2: Complete lineage for humans
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX taxon: <http://identifiers.org/taxonomy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?ancestor ?rank ?label ?id
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  taxon:9606 rdfs:subClassOf* ?ancestor .
  ?ancestor a tax:Taxon ;
    tax:rank ?rank ;
    rdfs:label ?label ;
    dcterms:identifier ?id .
}
ORDER BY DESC(?id)
LIMIT 20

# Results: Retrieved 20 ancestral taxa including:
# - Species: Homo sapiens (9606)
# - Subfamily: Homininae (207598)
# - Family: Hominidae (9604 - not shown but implied)
# - Superfamily: Hominoidea (314295)
# - Order, Class (Mammalia 40674), Phylum, Kingdom (Metazoa 33208)
# - Root: cellular organisms (131567)
```

```sparql
# Query 3: Genera with most species (biodiversity analysis)
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?genus ?genus_label (COUNT(?species) AS ?count)
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  ?species a tax:Taxon ;
    tax:rank tax:Species ;
    rdfs:subClassOf ?genus .
  ?genus tax:rank tax:Genus ;
    rdfs:label ?genus_label .
}
GROUP BY ?genus ?genus_label
ORDER BY DESC(?count)
LIMIT 20

# Results: Top genera by species count:
# 1. Cortinarius (fungi): 2,030 species
# 2. Astragalus (plants): 1,580 species
# 3. Megaselia (insects): 1,308 species
# 4. Inocybe (fungi): 1,231 species
# 5. Russula (fungi): 1,209 species
# 6. Streptomyces (bacteria): 1,141 species
# Demonstrates wide taxonomic coverage across kingdoms
```

```sparql
# Query 4: Cross-database identifiers for human
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX taxon: <http://identifiers.org/taxonomy/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?sameAs
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  taxon:9606 owl:sameAs ?sameAs .
}

# Results: 5 equivalent identifiers:
# - OBO: NCBITaxon_9606
# - DDBJ: taxonomy/9606
# - NCBI Web: ncbi.nlm.nih.gov/taxonomy/9606
# - OBO OWL: NCBITaxon#9606
# - Berkeley BOP: NCBITaxon#9606
```

## Interesting Findings

### Specific Entities for Questions
- **Human (9606)**: Complete lineage, multiple common names, extensive cross-refs
- **E. coli (562)**: Model organism, well-documented
- **S. pyogenes (1314)**: Pathogenic bacterium
- **Pyrococcus furiosus (2261)**: Hyperthermophilic archaeon
- **Cortinarius genus (34451)**: Most species-rich genus (2,030 species)
- **Streptomyces genus (1883)**: Important bacterial genus (1,141 species)

### Unique Properties
- **47 taxonomic ranks**: Far more granular than traditional Linnaean taxonomy
- **Genetic codes**: Both nuclear and mitochondrial codes specified
- **5 cross-references per taxon**: Comprehensive identifier mapping
- **100% coverage**: Scientific names, owl:sameAs, UniProt links
- **Hierarchical structure**: Complete tree from root to species

### Connections to Other Databases
- **UniProt Taxonomy**: 100% coverage via rdfs:seeAlso
- **OBO NCBITaxon**: Ontology representation
- **TogoID**: Separate graphs for cross-database conversion
- **DDBJ**: DNA sequence database integration
- **Multiple ontologies**: OWL, Berkeley BOP representations

### Verifiable Facts
- Genus Cortinarius has 2,030 species (most species-rich)
- Human lineage includes 20+ major taxonomic ranks
- Streptomyces genus has 1,141 species
- All taxa have 5 owl:sameAs identifiers on average
- Database contains 2,698,386 total taxa

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Biological IDs and classifications**
- "What is the NCBI Taxonomy ID for Pyrococcus furiosus?"
- "What is the scientific name and authority for taxID 1314?"
- "What genetic code does E. coli (taxID 562) use?"
- "What is the taxonomic rank of Hominidae?"

❌ Avoid: "What database version is this?" "When was the database last updated?"

### Completeness
✅ **Counts and comprehensive lists of biological entities**
- "How many species are in the genus Streptomyces?"
- "List all taxonomic ranks in the lineage of Homo sapiens"
- "How many genera have more than 1,000 species?"
- "How many ancestor taxa does human have from species to root?"

❌ Avoid: "How many database tables exist?" "What is the total storage size?"

### Integration
✅ **Cross-database biological entity linking**
- "Convert NCBI Taxonomy ID 9606 to its OBO NCBITaxon identifier"
- "What is the UniProt Taxonomy link for Streptococcus pyogenes?"
- "Find the owl:sameAs identifiers for E. coli"
- "What are all equivalent identifiers for taxID 2261?"

❌ Avoid: "What databases link to this server?" "List all API endpoints"

### Currency
✅ **Recent taxonomic updates and classifications**
- "When was the Homo sapiens taxonomy entry last modified?"
- "What are recently added species in genus Streptomyces?" (if recent)
- "Has the classification of Pyrococcus been updated?" (check modification date)

❌ Avoid: "What is the current database version number?" "When was the server last restarted?"

### Specificity
✅ **Rare organisms and specialized taxa**
- "What is the taxonomy ID for the hyperthermophile Pyrococcus furiosus?"
- "Find the taxonomic classification of anaerobic thermophile IC-BH"
- "What species exist in the rare fungal genus Cortinarius?"
- "What is the genetic code for mitochondria in taxID 2261?"

❌ Avoid: "What is the most popular database query?" "Which data format is used?"

### Structured Query
✅ **Complex biological queries with multiple criteria**
- "Find all species in phylum Chordata with more than 2 common names"
- "List genera in kingdom Fungi that have over 1,000 species"
- "Find all bacterial species (rank=Species) in division Firmicutes"
- "Which taxa have both nuclear genetic code 1 AND mitochondrial code 2?"

❌ Avoid: "Find databases updated after date X" "List all server configurations"

## Notes

### Limitations and Challenges
- **Performance**: Transitive queries (rdfs:subClassOf*) can timeout on deep lineages
- **Size**: 2.7M+ taxa require careful query design with LIMIT clauses
- **Complexity**: 47 different ranks make filtering complex
- **Lineage depth**: Some organisms have very deep hierarchies

### Best Practices for Querying
1. **Always use FROM clause**: `FROM <http://rdfportal.org/ontology/taxonomy>`
2. **Use bif:contains for search**: Much faster than FILTER(CONTAINS())
3. **Start from specific taxa**: Don't query all taxa with transitive properties
4. **Add LIMIT clauses**: Prevent timeouts, especially for exploratory queries
5. **Filter by rank**: Improves performance significantly
6. **Use specific taxon IDs**: e.g., `taxon:9606` rather than ?taxon
7. **Avoid unbounded traversal**: rdfs:subClassOf* on all taxa will timeout

### Data Quality Notes
- Scientific names: 99%+ complete
- Common names: ~30% complete (higher for vertebrates, lower for microbes)
- Cross-references: 100% coverage for owl:sameAs and rdfs:seeAlso
- Genetic codes: 100% specified where applicable
- Modification dates: Track when taxonomy was last updated
