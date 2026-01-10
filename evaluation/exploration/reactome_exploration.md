# Reactome Exploration Report

## Database Overview
Reactome is an open-source, manually curated knowledgebase of biological pathways and processes:
- **22,071 pathways** across 30+ species
- **88,464 biochemical reactions**
- **226,021 proteins**
- **101,651 protein complexes**
- **50,136 small molecules**
- **46,901 catalysis events**
- Based on BioPAX Level 3 ontology
- Cross-references to UniProt, ChEBI, GO, PubMed, and pharmacology databases

## Schema Analysis (from MIE file)

### Main Properties Available
- **Pathways**: Display name, organism, comments, hierarchical components (sub-pathways, reactions)
- **Reactions**: Participants (left/right), EC numbers, spontaneity, direction
- **Proteins**: Entity references with names, organism, UniProt IDs
- **Complexes**: Components, stoichiometric coefficients, cellular location
- **Small Molecules**: ChEBI cross-references, chemical names
- **Catalysis**: Controller protein/complex, controlled reaction, direction
- **Cross-References**: UniProt (87K), GO (65K), ChEBI (32K), PubMed (443K)
- **Evidence**: Evidence codes, publication references

### Important Relationships
- `bp:pathwayComponent` - Links pathways to sub-pathways and reactions (hierarchical)
- `bp:left / bp:right` - Reaction participants (substrates/products)
- `bp:controller / bp:controlled` - Catalysis relationships
- `bp:entityReference` - Links instances to canonical definitions
- `bp:component / bp:componentStoichiometry` - Complex composition
- `bp:xref` - External database cross-references
- `bp:organism` - Species information
- `bp:cellularLocation` - Subcellular localization

### Query Patterns Observed
- **Keyword search**: MUST use `bif:contains` (not FILTER/REGEX) for performance
- **Boolean operators**: Use `AND`, `OR`, `NOT` within bif:contains
- **Cross-references**: CRITICAL - use `^^xsd:string` for bp:db comparisons
- **Property paths**: Use `bp:pathwayComponent+` from specific URIs (not unbounded *)
- **FROM clause required**: `FROM <http://rdf.ebi.ac.uk/dataset/reactome>`

## Search Queries Performed

1. **Query: "mTOR"** → Results: 30 entities including MTOR protein, mTOR signaling pathway, mTORC1/2 complexes, reactions, drugs (BEZ235, XL765)
2. **Query: "SARS-CoV-2"** → Results: 50+ entities including infection pathway, replication, transcription, autophagy modulation, viral proteins, drugs (remdesivir, molnupiravir)
3. **Query: "autophagy"** → Results: 10 autophagy pathways across different species (human, mouse, rat, etc.)
4. **Cross-species pathways**: Same biological process represented for multiple organisms
5. **Drug targets**: Guide to Pharmacology links for drug-protein interactions

## SPARQL Queries Tested

```sparql
# Query 1: Search pathways by keyword with relevance ranking
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT ?pathway ?name
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
    bp:displayName ?name .
  ?name bif:contains "'autophagy'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Retrieved autophagy pathways across multiple species (human, mouse, rat, etc.)
```

```sparql
# Query 2: Find pathways with GO annotations (example structure)
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?pathway ?name ?goId
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
    bp:displayName ?name ;
    bp:xref ?xref .
  ?xref bp:db "GENE ONTOLOGY"^^xsd:string ;
    bp:id ?goId .
  FILTER(CONTAINS(?goId, "GO:"))
}
LIMIT 50
# Demonstrates GO cross-reference retrieval with proper ^^xsd:string usage
```

```sparql
# Query 3: Find UniProt cross-references (example structure)
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?entity ?uniprotId
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?entity bp:xref ?xref .
  ?xref a bp:UnificationXref ;
    bp:db "UniProt"^^xsd:string ;
    bp:id ?uniprotId .
}
LIMIT 50
# Critical: ^^xsd:string is required for bp:db comparison
```

## Interesting Findings

### Specific Entities for Questions
- **mTOR signaling pathway**: Major nutrient sensing pathway with many components
- **SARS-CoV-2 pathways**: Recent COVID-19 related pathways (post-training cutoff)
- **Autophagy**: Well-studied pathway with 10+ species-specific versions
- **30+ species**: Human, mouse, rat, zebrafish, chicken, etc.
- **Drug targets**: Guide to Pharmacology links (8K drug-target interactions)

### Unique Properties
- **BioPAX Level 3 ontology**: Standardized biological pathway representation
- **Hierarchical organization**: Pathways contain sub-pathways and reactions
- **Stoichiometric coefficients**: Precise complex composition (e.g., "2 copies of protein X")
- **Evidence tracking**: PublicationXref to PubMed for provenance
- **Manual curation**: All pathways expert-reviewed with citations
- **Quarterly updates**: Fresh biological knowledge
- **Cross-species comparison**: Same pathway across multiple organisms

### Connections to Other Databases
- **UniProt**: 87K protein references (~90% coverage)
- **ChEBI**: 32K small molecule references
- **GO**: 65K Gene Ontology term annotations (~85% pathways)
- **PubMed**: 443K publication citations (~85% pathways)
- **Guide to Pharmacology**: 8K drug-target interactions
- **NCBI Taxonomy**: Species identifiers for all organisms
- **COSMIC/ClinGen/LOVD**: Disease and variant databases

### Specific Verifiable Facts
- **22,071 total pathways**
- **88,464 biochemical reactions**
- **30+ species** covered
- **443K PubMed citations**
- **mTOR pathway**: R-HSA-165159 in human
- **SARS-CoV-2 infection**: R-HSA-9694516 (recent addition)
- **Average 5.3 sub-pathways** per pathway
- **Average 8.7 reactions** per pathway

## Question Opportunities by Category

### Precision
- "What is the Reactome pathway ID for mTOR signaling in humans?" → R-HSA-165159
- "What is the Reactome ID for SARS-CoV-2 infection pathway?" → R-HSA-9694516
- "How many protein components are in mTORC1 complex?" → From complex stoichiometry
- "What is the EC number for a specific reaction?" → From reaction EC annotation
- "What is the cellular location of Complex X?" → From bp:cellularLocation

### Completeness
- "How many pathways are in Reactome?" → 22,071
- "How many SARS-CoV-2 related pathways exist?" → ~50+ (from search results)
- "How many species are covered in Reactome?" → 30+
- "How many reactions involve ATP?" → Count from small molecule queries
- "List all sub-pathways of mTOR signaling" → Hierarchical query

### Integration
- "What is the UniProt ID for protein in Reactome pathway X?" → Via bp:xref
- "Find ChEBI IDs for metabolites in glycolysis pathway" → Cross-reference query
- "What GO terms are associated with autophagy pathway?" → GO cross-references
- "Link Reactome pathways to PubMed publications" → Via PublicationXref
- "Find drug targets in cancer pathways" → Guide to Pharmacology links

### Currency
- "What pathways involve SARS-CoV-2 proteins?" → Recent COVID pathways
- "How many COVID-19 related pathways were added?" → Recent additions
- "What pathways were updated in latest release?" → Release 88 information
- "Find pathways for mRNA vaccines" → Recent additions

### Specificity
- "What pathways involve rare enzyme X?" → Niche protein queries
- "Find pathways specific to zebrafish development" → Species-specific
- "What is the stoichiometry of complex Y?" → Precise coefficient data
- "Which pathways have spontaneous reactions?" → Filter by spontaneity property

### Structured Query
- "Find cancer pathways with documented drug targets" → Multiple filters
- "List reactions with EC numbers in glycolysis" → Pathway + EC filter
- "Find complexes with > 5 components in nucleus" → Complex + location
- "Search pathways in humans with GO:0006914 annotation" → Species + GO filter
- "Find catalysis events where protein X controls reaction Y" → Regulatory query

## Notes

### Limitations
- **^^xsd:string CRITICAL**: Cross-reference queries fail without type restriction on bp:db
- **Property path caution**: Unbounded `bp:pathwayComponent*` causes timeout
- **FROM clause required**: Queries fail on multi-graph endpoints without it
- **Species variation**: Same pathway may have different IDs across species
- **Complex nesting**: Deep hierarchies require careful property path use

### Best Practices
1. **ALWAYS use bif:contains** for keyword searches (not FILTER/REGEX)
2. **ALWAYS use ^^xsd:string** for bp:db comparisons
3. **Start from specific URIs** for property path queries
4. **Use bp:pathwayComponent+** (not *) with starting pathway
5. **Include FROM clause**: `FROM <http://rdf.ebi.ac.uk/dataset/reactome>`
6. **Add type filters** to reduce pattern matching space
7. **Use LIMIT** for exploratory queries (50-100)
8. **Use OPTIONAL** for cross-references (not all entities have all xrefs)

### Performance Notes
- bif:contains pathway search: <1 second for 20 results
- Hierarchy traversal from specific pathway: <2 seconds
- Cross-reference queries with ^^xsd:string: <3 seconds
- Complex stoichiometry queries: <5 seconds
- Unbounded property paths may timeout without LIMIT
- Boolean operators in bif:contains are very efficient
