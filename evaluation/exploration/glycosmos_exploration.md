# GlyCosmos Exploration Report

## Database Overview
- **Purpose**: Comprehensive glycoscience portal integrating glycan structures, glycoproteins, glycosylation sites, glycogenes, and glycoepitopes
- **Scope**: Multi-species glycobiology data (100+ named graphs)
- **Key data types**: 
  - 117,864 glycans (GlyTouCan)
  - 153,178 glycoproteins
  - 414,798 glycosylation sites
  - 423,164 glycogenes
  - 173 glycoepitopes
  - 739 lectins

## Schema Analysis (from MIE file)

### Main Properties Available
- **Glycans**: `glytoucan:has_primary_id`, `glycan:has_Resource_entry`
- **Glycoproteins**: `rdfs:label`, `glycan:has_taxon`, `glycoconjugate:glycosylated_at`
- **Glycosylation Sites**: `sio:SIO_000772` (protein reference), `faldo:location/faldo:position`
- **Glycogenes**: `rdfs:label`, `dcterms:description`, `rdfs:seeAlso`
- **Glycoepitopes**: `rdfs:label`, `skos:altLabel`, `glycoepitope:has_antibody`, `glycoepitope:tissue`

### Important Relationships
- Glycoproteins → Glycosylation sites via `glycoconjugate:glycosylated_at`
- Sites → Proteins via `sio:SIO_000772`
- Sites → Sequence positions via `faldo:location/faldo:position`
- Glycans → External databases via `glycan:has_Resource_entry`
- All entities → External databases via `rdfs:seeAlso`

### Query Patterns Observed
1. **CRITICAL**: Always use `FROM <graph_uri>` to specify which graph (100+ graphs available)
2. **Full-text search**: Use `bif:contains` with `option (score ?sc)` for label searches
3. **Early filtering**: Filter by taxonomy first for performance on large datasets
4. **Pagination**: Essential for 414K+ glycosylation sites - always include LIMIT
5. **Multi-graph queries**: Explicitly specify FROM for each graph involved

## Search Queries Performed

### Query 1: Epitope Search with Full-Text
**Query**: Lewis epitopes
**Method**: SPARQL with bif:contains
**Results**: 20 Lewis-type epitopes found including:
- EP0007 (Lewis a)
- EP0008 (Sialyl Lewis a)
- EP0010 (Lewis b)
- EP0011 (Lewis x)
- EP0012 (Sialyl Lewis x)
- Multiple sulfated and modified variants

### Query 2: Glycoprotein Distribution by Species
**Query**: Count of glycoproteins per species
**Results**:
- Human (9606): 16,604 glycoproteins
- Mouse (10090): 10,713
- Rat (10116): 2,576
- Arabidopsis (3702): 2,251
- C. elegans (6239): 1,447
- Top 5 species account for majority of data

### Query 3: Human Glycosylation Sites
**Query**: Human proteins with glycosylation site positions
**Results**: Found diverse proteins including:
- HLA class I (position 110)
- Platelet glycoprotein Ib (positions 65, 66, 83)
- Membrane cofactor protein (multiple sites at position 83)
- Shows multiple sites per protein are common

### Query 4: Glycogene Function Search
**Query**: Genes with "transferase" in description
**Results**: 15+ glycosyltransferases found including:
- FUT1, FUT2, FUT3, FUT6 (fucosyltransferases)
- MGAT4A (N-acetylglucosaminyltransferase)
- ST3GAL2 (sialyltransferase)
- B4GALNT2 (galactosaminyltransferase)

### Query 5: Glycan Cross-References
**Query**: Glycans with multiple database entries
**Results**: Many glycans have 2 external database entries, showing good cross-referencing to structure and chemical databases

## SPARQL Queries Tested

```sparql
# Query 1: Epitope tissue and antibody data
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX glycoepitope: <http://www.glycoepitope.jp/epitopes/glycoepitope.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?epitope ?label ?antibody ?tissue
FROM <http://rdf.glycoinfo.org/glycoepitope>
WHERE {
  ?epitope a glycan:Glycan_epitope ;
    rdfs:label ?label .
  OPTIONAL { ?epitope glycoepitope:has_antibody ?antibody }
  OPTIONAL { ?epitope glycoepitope:tissue ?tissue }
}
LIMIT 10
# Results: HNK-1 epitope found in brain, glial cells, natural killer cells, neurons, spinal cord
```

```sparql
# Query 2: Species distribution of glycoproteins
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>

SELECT ?taxon (COUNT(DISTINCT ?protein) as ?count)
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    glycan:has_taxon ?taxon .
}
GROUP BY ?taxon
ORDER BY DESC(?count)
LIMIT 10
# Results: Top 10 species ranging from 16K (human) to 766 (S. cerevisiae) glycoproteins
```

```sparql
# Query 3: Glycogene functional annotations
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene ?symbol ?description
FROM <http://rdf.glycosmos.org/glycogenes>
WHERE {
  ?gene a glycan:Glycogene ;
    rdfs:label ?symbol ;
    dcterms:description ?description .
  FILTER(CONTAINS(LCASE(?description), "transferase"))
}
LIMIT 15
# Results: Identified key glycosyltransferases with detailed functional descriptions
```

## Interesting Findings

### Specific Entities for Questions
1. **Lewis antigens**: Well-characterized epitopes (EP0007-EP0018) with known tissue distributions
2. **Blood group antigens**: FUT1, FUT2, FUT3 genes encode H and Lewis blood group transferases
3. **Human glycoproteome**: 16,604 glycoproteins with 414K+ glycosylation sites
4. **Site multiplicity**: Some proteins (e.g., P15529) have 20+ glycosylation sites at same position
5. **HNK-1 epitope**: Neural-specific epitope with multiple antibodies and tissue locations

### Unique Properties
- Multi-graph architecture (100+ named graphs) requiring explicit FROM clauses
- FALDO coordinates for precise glycosylation site positions
- Full-text indexing via bif:contains with relevance scoring
- Cross-species coverage (human, mouse, model organisms, plants)
- Integration of structural (glycans), functional (proteins), and genetic (genes) data

### Connections to Other Databases
- **UniProt**: 139K protein cross-references
- **NCBI Gene**: 423K gene cross-references
- **PubChem**: 32K compound and substance links
- **ChEBI**: 11K chemical entity cross-references
- **KEGG**: 10K pathway/compound links, 381K gene references
- **PDB**: 6K structure cross-references

### Verifiable Facts
1. Human has exactly 16,604 glycoproteins in GlyCosmos
2. Lewis a epitope ID is EP0007
3. FUT3 gene encodes fucosyltransferase 3 (Lewis blood group)
4. Total of 173 glycoepitopes catalogued
5. HNK-1 (EP0001) is found in brain, neurons, glial cells, NK cells, spinal cord

## Question Opportunities by Category

### Precision
✅ **Biological IDs and measurements**:
- "What is the epitope ID for Lewis a in GlyCosmos?" (EP0007)
- "What is the gene symbol for fucosyltransferase 3?" (FUT3)
- "How many glycoepitopes are catalogued in GlyCosmos?" (173)
- "At which position is the glycosylation site in platelet glycoprotein Ib beta chain?" (positions 65, 66, 83)

❌ Avoid: Database version numbers, server configurations

### Completeness
✅ **Counts of biological entities**:
- "How many human glycoproteins are in GlyCosmos?" (16,604)
- "How many glycosylation sites exist across all species?" (414,798)
- "How many Lewis-type epitopes are defined?" (20+)
- "Count glycogenes with 'transferase' function" (~15+ in sample)

❌ Avoid: "How many database updates?", "How many graphs?"

### Integration
✅ **Cross-database biological linking**:
- "Convert GlyCosmos protein P02763 to UniProt ID"
- "Which NCBI Gene IDs correspond to glycogene FUT1?"
- "Link glycan G00051MO to PubChem Compound"
- "Find UniProt entries for human glycoproteins"

❌ Avoid: "Which databases link to GlyCosmos server?"

### Currency
✅ **Recent biological discoveries**:
- "What tissue distributions are documented for HNK-1 epitope?" (current annotations)
- "How many glycosylation sites are annotated for human proteins as of 2024?" (subset of 414K)
- "Which antibodies recognize the Lewis a epitope?" (current list)

❌ Avoid: "What is the current database release version?"

### Specificity
✅ **Niche glycobiology topics**:
- "What is the epitope ID for Sialyl 6-Sulfo Lewis x?" (EP0015)
- "Which tissues express the HNK-1 glycan epitope?" (brain, neurons, glial, NK cells, spinal cord)
- "What antibody recognizes the dimeric Lewis x epitope?" (specific antibody IDs)
- "Which genes encode fucosyltransferases in the H blood group system?" (FUT1, FUT2)

❌ Avoid: Infrastructure metadata

### Structured Query
✅ **Complex biological queries**:
- "Find human glycoproteins with more than 10 glycosylation sites"
- "List glycogenes that are transferases AND located in human genome"
- "Which epitopes are found in both brain AND spinal cord tissue?"
- "Find glycoproteins from mouse with N-glycosylation sites at positions < 100"

❌ Avoid: "Find databases updated after date X"

## Notes

### Limitations
- **Label coverage variable**: Glycans <1%, proteins 17%, genes 32%
- **Performance-critical**: Must use FROM clause and early filters for queries on 414K+ sites
- **bif:contains limitation**: Only works well on rdfs:label, use FILTER for other properties
- **Multi-graph complexity**: Requires understanding which data is in which graph

### Best Practices
1. **Always specify FROM graph**: Critical for performance (10-100x speedup)
2. **Use bif:contains for labels**: Full-text index + relevance scoring
3. **Filter early by taxonomy**: Essential for glycoprotein/site queries
4. **Always paginate**: Use LIMIT on large datasets (glycosylation sites, glycogenes)
5. **Nested SELECT for aggregations**: Better performance on complex queries
6. **Prefer IDs over labels**: GlyTouCan IDs, gene symbols more reliable than labels
7. **Use rdfs:seeAlso**: For external database cross-references when labels missing

### Data Quality Notes
- **GlyTouCan ID pattern**: G[0-9]{5}[A-Z]{2}
- **Coverage**: 86% glycans have external database entries
- **Position data**: >90% glycosylation sites have FALDO positions
- **Multi-site proteins**: Some proteins have 20+ sites (often at same position - isoforms?)
- **Cross-reference richness**: Strong links to UniProt (139K), NCBI Gene (423K), chemical databases
