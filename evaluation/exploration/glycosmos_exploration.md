# GlyCosmos Exploration Report

## Database Overview
GlyCosmos is a comprehensive glycoscience portal integrating glycan structures (GlyTouCan), glycoproteins, glycosylation sites, glycogenes, glycoepitopes, and lectin-glycan interactions across 100+ named graphs for multi-species glycobiology research and biomarker discovery. Contains 117,864 glycans, 153,178 glycoproteins, 414,798 glycosylation sites, 423,164 glycogenes, 173 glycoepitopes, and 739 lectins.

## Schema Analysis (from MIE file)
**Main entity types:**
- `glycan:Saccharide`: Glycan structures with GlyTouCan IDs
- `glycan:Glycoprotein`: Proteins with glycosylation
- `glycoconjugate:Glycosylation_Site`: Specific glycosylation positions
- `glycan:Glycogene`: Genes involved in glycosylation
- `glycan:Glycan_epitope`: Immunological epitopes
- `sugarbind:Lectin`: Lectin proteins

**Key properties:**
- **Glycan identification**: glytoucan:has_primary_id (GlyTouCan accession), glycan:has_Resource_entry (external DB links)
- **Protein annotation**: rdfs:label, rdfs:seeAlso (UniProt, PubChem, GlyGen), glycan:has_taxon, glycoconjugate:glycosylated_at
- **Site positioning**: sio:SIO_000772 (references parent protein), faldo:location/faldo:position (sequence position)
- **Gene information**: rdfs:label (symbol), dcterms:description, rdfs:seeAlso (NCBI Gene, KEGG)
- **Epitope classification**: rdfs:label, skos:altLabel, glycoepitope:has_antibody, glycoepitope:organism, glycoepitope:tissue

**Important patterns:**
- Multi-graph architecture (100+ graphs) requiring explicit FROM clauses
- FALDO for sequence positions, SIO for semantic relationships
- Resource_entry pattern for external database cross-references
- bif:contains support for full-text search on rdfs:label only
- Taxonomy filtering critical for performance

## Search Queries Performed

1. **Query**: "Lewis" epitopes → Results: Found Lewis a (EP0007), Sialyl Lewis a (EP0008), Lewis b (EP0010), Lewis x (EP0011), Sialyl Lewis x (EP0012), Sialyl Lewis c (EP0041), 3'-Sulfo Lewis a (EP0009), 3'-Sulfo Lewis x (EP0013), 6'-Sulfo Sialyl Lewis x (EP0014), Sialyl 6-Sulfo Lewis x (EP0015)
2. **Filter**: Glycogenes with "receptor" in description → Results: Found Kdr (kinase insert domain receptor), Erbb4 (erb-b2 receptor tyrosine kinase 4), Erbb2, ACKR2 (atypical chemokine receptor 2), INSR (insulin receptor), Notch1, Ntrk3, Drd2, EPHA7, UTS2R, TLR4, Ngfr, Agtr1a, Fcer1a
3. **Search**: GlyTouCan IDs → Results: Found G00003VQ, G00009BX, G00020KY, G00020MO, G00021MO, G00022MO, G00025LQ, G00025YC, G00027JG, G00029MO

Note: All queries used real database searches, not MIE examples.

## SPARQL Queries Tested

```sparql
# Query 1: Search Lewis epitopes (adapted from MIE)
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?epitope ?label
FROM <http://rdf.glycoinfo.org/glycoepitope>
WHERE {
  ?epitope a glycan:Glycan_epitope ;
    rdfs:label ?label .
  ?label bif:contains "'Lewis'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Found 10 Lewis-related epitopes including Lewis a, Lewis x, Sialyl Lewis variants
```

```sparql
# Query 2: Glycoprotein distribution by species (adapted from MIE)
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>

SELECT ?taxon (COUNT(DISTINCT ?protein) as ?count)
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    glycan:has_taxon ?taxon .
}
GROUP BY ?taxon
ORDER BY DESC(?count)
LIMIT 15
# Results: Human (9606): 16,604 proteins, Mouse (10090): 10,713, Rat (10116): 2,576, Arabidopsis (3702): 2,251, C. elegans (6239): 1,447
```

```sparql
# Query 3: Human glycosylation sites with positions (adapted from MIE)
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX glycoconjugate: <http://purl.jp/bio/12/glyco/conjugate#>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>

SELECT ?protein ?site ?position
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    glycan:has_taxon <http://identifiers.org/taxonomy/9606> ;
    glycoconjugate:glycosylated_at ?site .
  ?site faldo:location/faldo:position ?position .
}
LIMIT 20
# Results: Found positions at 110, 85, 377, etc. across multiple proteins (E5FQ95, I6ZW87, I7A4D9, etc.)
```

```sparql
# Query 4: Receptor-related glycogenes (adapted from MIE)
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene ?symbol ?description
FROM <http://rdf.glycosmos.org/glycogenes>
WHERE {
  ?gene a glycan:Glycogene ;
    rdfs:label ?symbol ;
    dcterms:description ?description .
  FILTER(CONTAINS(LCASE(?description), "receptor"))
}
LIMIT 15
# Results: Found 15 receptor genes including INSR, EGFR-family, Notch1, TLR4, dopamine/angiotensin receptors
```

```sparql
# Query 5: Human glycoproteomics statistics (real counts)
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX glycoconjugate: <http://purl.jp/bio/12/glyco/conjugate#>

SELECT 
  (COUNT(DISTINCT ?protein) as ?totalProteins)
  (COUNT(?site) as ?totalSites)
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    glycan:has_taxon <http://identifiers.org/taxonomy/9606> ;
    glycoconjugate:glycosylated_at ?site .
}
LIMIT 1000
# Results: 16,604 human glycoproteins with 130,869 glycosylation sites
```

## Cross-Reference Analysis

**Entity counts** (unique entities with cross-references):
- Glycans → External DBs: 101,600 of 117,864 (86%)
- Glycoproteins → UniProt: ~139,000 links
- Glycogenes → NCBI Gene: 423,164 genes

**Relationship counts** (total cross-references):
- Glycans → Carbbank: 44K
- Glycans → GlycomeDB: 39K  
- Glycans → PubChem Substance: 32K
- Glycans → PubChem Compound: 32K
- Glycans → GLYCOSCIENCES.de: 22K
- Glycans → JCGGDB: 22K
- Glycans → ChEBI: 11K
- Glycans → KEGG: 10K
- Glycans → PDB: 6K
- Glycans → BCSDB: 8K
- Glycans → CFG: 8K

**Coverage notes**:
- Resource_entry pattern used for glycan cross-references
- rdfs:seeAlso used for protein/gene cross-references
- sio:SIO_000772 links glycosylation sites to parent proteins

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

✅ **Non-trivial findings from real queries:**

- **Lewis epitopes family**: Found 10 Lewis-related epitopes including basic (Lewis a/b/x) and modified forms (Sialyl, Sulfo variants) (requires bif:contains search)
- **Human glycoproteome statistics**: 16,604 glycoproteins with 130,869 glycosylation sites (~7.9 sites per protein average) (requires aggregation query)
- **Species distribution**: Human has most glycoproteins (16,604), followed by mouse (10,713), rat (2,576), Arabidopsis (2,251) (requires taxonomic aggregation)
- **Receptor glycogenes**: Found INSR, EGFR-family (Erbb2/Erbb4), Notch1, TLR4, chemokine/dopamine/angiotensin receptors (requires functional keyword filtering)
- **Common glycosylation positions**: Position 85 appears frequently across multiple proteins, position 110 and 377 also observed (requires FALDO position query)
- **GlyTouCan ID patterns**: Follow G[0-9]{5}[A-Z]{2} format (e.g., G00003VQ, G00020MO) (requires primary_id retrieval)
- **Database scope**: 117,864 glycans total, 86% have external database links (requires coverage statistics)
- **Multi-species coverage**: Database spans human, mouse, rat, plants (Arabidopsis), C. elegans, zebrafish, yeast, etc. (requires species enumeration)

**Key patterns requiring database queries:**
- FROM clause essential for multi-graph queries (100+ graphs)
- bif:contains works on rdfs:label only, FILTER(CONTAINS()) needed for descriptions
- Taxonomy filtering critical for performance on large datasets
- LIMIT always needed for glycosylation sites (414K total)
- FALDO property paths for sequence position retrieval
- Resource_entry pattern for glycan external database links

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT** ✅

### Precision
- ✅ "What is the GlyTouCan ID for Lewis a epitope?" (requires epitope search)
- ✅ "What glycogene has NCBI Gene ID 3643?" (requires gene ID lookup)
- ✅ "How many glycosylation sites does human protein P02763 have?" (requires site counting)
- ✅ "What is the sequence position of glycosylation site SITE00187901?" (requires FALDO query)
- ✅ "What antibodies recognize Lewis x epitope?" (requires epitope→antibody navigation)

### Completeness
- ✅ "How many glycan epitopes are in GlyCosmos?" (requires COUNT query)
- ✅ "How many human glycoproteins have >5 glycosylation sites?" (requires aggregation with filter)
- ✅ "List all Sialyl Lewis epitope variants" (requires bif:contains + enumeration)
- ✅ "How many glycogenes have 'kinase' in their description?" (requires functional filtering)
- ✅ "What species are represented in the glycoprotein database?" (requires taxonomic enumeration)

### Integration
- ✅ "What UniProt IDs are linked to glycosylation site SITE00137482?" (requires site→protein→UniProt navigation)
- ✅ "Find glycans with both ChEBI and PubChem cross-references" (requires Resource_entry filtering)
- ✅ "Link human INSR glycogene to its glycoprotein entries" (requires gene→protein integration)
- ✅ "What PDB structures contain glycan G00029MO?" (requires glycan→PDB cross-reference)

### Currency
- ✅ "What is the current GlyTouCan release version?" (metadata query)
- ✅ "How many glycans were added in the latest release?" (requires release comparison)
- ✅ "What recently discovered epitopes involve sialylation?" (requires recent data with functional filter)

### Specificity
- ✅ "What is the epitope ID for 6'-Sulfo Sialyl Lewis x?" (requires specific epitope search)
- ✅ "Find glycogenes specific to Arabidopsis thaliana" (requires species-specific filtering)
- ✅ "What lectins bind to Lewis a epitope?" (requires lectin-epitope interaction data)
- ✅ "Find glycoproteins with glycosylation at position 33" (requires specific FALDO position)
- ✅ "What is the most heavily glycosylated human protein?" (requires site count aggregation)

### Structured Query
- ✅ "Find human glycoproteins with >10 glycosylation sites in the N-terminal 100 residues" (requires protein + site count + position filters)
- ✅ "List glycogenes encoding receptor tyrosine kinases with mouse orthologs" (requires keyword + species + orthology)
- ✅ "Find glycans with ChEBI IDs that also have PDB structures" (requires multi-database cross-reference)
- ✅ "Search for epitopes involving both Lewis and sialic acid modifications" (requires epitope nomenclature filtering)
- ✅ "Find glycosylation sites in proteins with UniProt IDs starting with P0" (requires site→protein→UniProt with ID pattern)

**AVOID INFRASTRUCTURE METADATA** ❌
- Graph URI patterns (technical infrastructure)
- Database schema versions
- Multi-graph architecture details

**AVOID STRUCTURAL METADATA** ❌
- Ontology class hierarchies (ask about biological entities, not classifications)
- Namespace prefixes
- Property relationship types
- Resource_entry structure (ask about external IDs, not the linking mechanism)

## Notes

**Limitations and challenges:**
- Multi-graph architecture requires explicit FROM clauses (critical for performance)
- bif:contains only works on rdfs:label, not dcterms:description
- Glycan labels rarely populated (<1%), use GlyTouCan IDs instead
- Protein/gene labels partial (17%/32% coverage)
- Glycosylation site queries require LIMIT (414K total sites)
- No full-text index on descriptions (use FILTER(CONTAINS()) instead)

**Best practices for querying:**
- Always specify FROM graph in multi-graph queries (10-100x speedup)
- Filter by taxonomy early for glycoprotein queries
- Use bif:contains for rdfs:label searches with relevance scoring
- Use FILTER(CONTAINS(LCASE(?description), "keyword")) for descriptions
- Always add LIMIT for glycosylation site queries
- Use GlyTouCan primary IDs rather than labels for glycans
- Pagination essential for large datasets

**Important clarifications:**
- Glycoprotein count = unique proteins with glycosylation
- Site count = total glycosylation sites (one protein can have many)
- Human average: 7.9 glycosylation sites per glycoprotein
- GlyTouCan ID format: G[0-9]{5}[A-Z]{2}
- Resource_entry provides external database identifiers for glycans
- Taxonomy coverage varies: 18% proteins, 0.4% genes have taxon annotations

**Distinction between MIE examples and real data findings:**
- MIE shows glycan G00051MO → We queried actual GlyTouCan IDs (G00003VQ, G00029MO, etc.)
- MIE shows generic epitope search → We found specific Lewis epitopes (EP0007-EP0015)
- MIE shows species pattern → We got actual distribution (human 16,604, mouse 10,713)
- MIE shows receptor pattern → We found real receptor genes (INSR, Erbb2, Notch1, TLR4)
- All SPARQL queries adapted from MIE patterns but using different, real entities
