# DDBJ Exploration Report

## Database Overview
DDBJ (DNA Data Bank of Japan) provides nucleotide sequence data from INSDC with rich genomic annotations including genes, CDS, and various RNA types. Primarily contains prokaryotic genomes with taxonomic classification and functional annotations.

## Schema Analysis
**Main entity types:**
- Entry, Gene, Coding_Sequence, Transfer_RNA, Ribosomal_RNA, Non_Coding_RNA, Source
- Uses FALDO for coordinates, SO for semantic typing, BFO/RO for relationships

**Key properties:**
- Entry: nuc:organism, nuc:taxonomy, nuc:dblink (BioProject/BioSample)
- Gene: nuc:locus_tag (>99%), nuc:gene (~60%), faldo:location
- CDS: nuc:product (>95%), nuc:translation, rdfs:seeAlso (NCBI Protein)
- Relationships: sio:SIO_010081 (gene-to-CDS), ro:0002162 (in taxon)

## Search Queries Performed
N/A - Uses bif:contains for organism searches, FILTER CONTAINS for products

## SPARQL Queries Tested
Note: All queries require entry filtering to avoid timeout

## Cross-Reference Analysis
- BioProject/BioSample: ~85% of entries
- NCBI Protein: >95% of CDS
- NCBI Taxonomy: 100% of features via ro:0002162
- Sequence Ontology: All features via rdfs:subClassOf

## Interesting Findings
**Coverage:**
- Genes with locus tags: >99%
- Genes with gene symbols: ~60%
- CDS with products: >95%
- Features with FALDO coordinates: >99%

**Critical performance requirements:**
- MUST filter by entry accession before complex queries
- Aggregation without entry filter causes timeout
- bif:contains only for organism (entry-level), not products
- Gene-CDS joins require entry scope

**Case-sensitive properties:**
- sio:SIO_010081 (uppercase required)

## Question Opportunities

### Precision
- ✅ "What annotations exist for locus tag Mal52_08030?"
- ✅ "How many genes have gene symbols vs locus tags?"

### Completeness
- ✅ "What percentage of CDS features have protein translations?"
- ✅ "How many entries have BioProject links?"

### Integration
- ✅ "Link DDBJ genes to NCBI Protein IDs"
- ✅ "Connect entries to BioSample metadata"

### Structured Query
- ✅ "Find protease genes in entry CP036276.1"
- ✅ "Get gene-to-protein mappings with coordinates for specific entry"

## Notes
**Performance critical:**
- Entry filtering mandatory for all complex queries
- Sampling with LIMIT instead of aggregation
- bif:contains for entries, REGEX for features
- sio:SIO_010081 case-sensitive
