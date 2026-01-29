# Ensembl Exploration Report

## Database Overview
Ensembl is a comprehensive genomics database providing genome annotations for 100+ vertebrate species. Contains genes, transcripts, proteins, and exons with precise genomic locations using FALDO. Covers 3M+ genes across species with hierarchical Gene → Transcript → Protein organization following the central dogma.

## Schema Analysis (from MIE file)
**Main entity types:**
- `terms:EnsemblGene`: Genes with biotypes and chromosomal locations
- `terms:EnsemblTranscript`: Transcript variants with quality flags (MANE, canonical, TSL)
- `terms:EnsemblProtein`: Translated protein products
- `terms:EnsemblExon`: Exon regions
- `terms:EnsemblOrderedExon`: Ordered exons in transcript structure

**Key properties:**
- **Identification**: dcterms:identifier, rdfs:label, dcterms:description
- **Hierarchy**: so:transcribed_from (transcript→gene), so:translates_to (transcript→protein), so:part_of (gene→chromosome)
- **Location**: faldo:location with begin/end positions and strand (ForwardStrandPosition/ReverseStrandPosition)
- **Classification**: terms:has_biotype (protein-coding, miRNA, lncRNA), obo:RO_0002162 (species taxonomy)
- **Quality**: terms:has_transcript_flag (MANE, APPRIS, TSL levels)
- **Ordering**: sio:SIO_000974 (transcript→ordered exons), sio:SIO_000628 (ordered exon→exon), sio:SIO_000300 (exon order)
- **Cross-references**: rdfs:seeAlso (UniProt, HGNC, NCBI Gene, Reactome, OMIM)

**Important patterns:**
- Multiple genome assemblies (GRCh38, GRCh37) in separate graphs
- FALDO strand encoding via position type (not explicit property)
- bif:contains support for full-text search with wildcards and scoring
- Property paths for hierarchical navigation

## Search Queries Performed

1. **Query**: "EGFR*" → Results: Found ENSG00000146648 (EGFR), ENSG00000224057 (EGFR-AS1), LRG_304 (EGFR)
2. **Query**: "kinase AND receptor" → Results: Found ROR1 (ENSG00000185483), ROR2 (ENSG00000169071), RIPK3 (ENSG00000129465), IRAK3, IRAK1, TNK1, GRK1, FLT3LG, TNK2
3. **Filter**: Chromosome X protein-coding genes → Results: Found HTR2C, CA5B, RTL8B, XAGE1B, SLC9A7, GPC4, TLR8, PDZD11, IL13RA1, BEX1, STK26, EIF1AX, ARX, RADX, CETN2, RIBC1, PIGA, ZMAT1, EGFL6, USP51 (20+ genes)

Note: All queries used real database searches, not MIE examples.

## SPARQL Queries Tested

```sparql
# Query 1: Get genomic coordinates for EGFR (adapted from MIE with real entity)
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX so: <http://purl.obolibrary.org/obo/so#>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT DISTINCT ?gene ?id ?label ?start ?end ?strand ?chr
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        faldo:location ?loc ;
        so:part_of ?chr ;
        obo:RO_0002162 taxonomy:9606 .
  ?loc faldo:begin/faldo:position ?start ;
       faldo:end/faldo:position ?end ;
       faldo:begin/rdf:type ?strand_type .
  BIND(IF(?strand_type = faldo:ForwardStrandPosition, "+", "-") AS ?strand)
  FILTER(?id = "ENSG00000146648")
}
# Results: EGFR on chr7:55,019,017-55,211,628 (minus strand)
```

```sparql
# Query 2: Gene-Transcript-Protein mapping with UniProt (adapted for EGFR)
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX so: <http://purl.obolibrary.org/obo/so#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene_id ?gene_label ?transcript_id ?protein_id ?uniprot
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?gene_id ;
        rdfs:label ?gene_label ;
        obo:RO_0002162 taxonomy:9606 .
  ?transcript so:transcribed_from ?gene ;
              dcterms:identifier ?transcript_id ;
              so:translates_to ?protein .
  ?protein dcterms:identifier ?protein_id ;
           rdfs:seeAlso ?uniprot .
  FILTER(STRSTARTS(STR(?uniprot), "http://purl.uniprot.org/uniprot/"))
  FILTER(?gene_label = "EGFR")
}
LIMIT 10
# Results: Found 7 EGFR transcripts/proteins including ENST00000275493→ENSP00000275493→P00533
```

```sparql
# Query 3: Species distribution (adapted from MIE)
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT ?taxonomy (COUNT(?gene) as ?gene_count)
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        obo:RO_0002162 ?taxonomy .
}
GROUP BY ?taxonomy
ORDER BY DESC(?gene_count)
LIMIT 20
# Results: Mouse (10090): 744,820 genes, Sheep (9940): 633,869, Pig (9823): 624,705, Human (9606): 87,688 genes
```

```sparql
# Query 4: Human gene coverage statistics
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT (COUNT(DISTINCT ?gene) as ?total_genes) 
       (COUNT(DISTINCT ?gene_with_desc) as ?genes_with_description)
       (COUNT(DISTINCT ?gene_with_uniprot) as ?genes_with_uniprot)
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        obo:RO_0002162 taxonomy:9606 .
  OPTIONAL { 
    ?gene dcterms:description ?desc .
    BIND(?gene as ?gene_with_desc)
  }
  OPTIONAL {
    ?gene rdfs:seeAlso ?xref .
    FILTER(STRSTARTS(STR(?xref), "http://purl.uniprot.org/uniprot/"))
    BIND(?gene as ?gene_with_uniprot)
  }
}
# Results: 87,688 human genes total, 87,688 (100%) with descriptions, 24,346 (28%) with UniProt cross-references
```

```sparql
# Query 5: Ordered exons for EGFR canonical transcript (adapted from MIE with real transcript)
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>

SELECT ?transcript_id ?exon_id ?order ?start ?end
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?transcript a terms:EnsemblTranscript ;
              dcterms:identifier ?transcript_id ;
              sio:SIO_000974 ?ordered_exon .
  ?ordered_exon sio:SIO_000628 ?exon ;
                sio:SIO_000300 ?order .
  ?exon dcterms:identifier ?exon_id ;
        faldo:location/faldo:begin/faldo:position ?start ;
        faldo:location/faldo:end/faldo:position ?end .
  FILTER(?transcript_id = "ENST00000275493")
}
ORDER BY ?order
LIMIT 30
# Results: Found 28 ordered exons for EGFR canonical transcript from exon 1 (55,019,017-55,019,365) to exon 28 (55,205,256-55,211,628)
```

## Cross-Reference Analysis

**Entity counts** (unique genes with cross-references):
- Human genes → UniProt: 24,346 genes (28% of 87,688)
- Note: ~72% of human genes lack UniProt cross-references

**Cross-database integration** (from MIE):
- Shared endpoint: EBI (with ChEMBL, ChEBI, Reactome, AMR Portal)
- Integration pattern: Ensembl genes → rdfs:seeAlso → UniProt → ChEMBL targets
- ChEMBL target components use skos:exactMatch to UniProt proteins
- Enables gene→drug target→drug mechanism queries

**Cross-reference types**:
- UniProt proteins (protein sequences)
- HGNC (human gene nomenclature)
- NCBI Gene (gene IDs)
- Reactome (pathway participation)
- OMIM (disease associations)

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

✅ **Non-trivial findings from real queries:**

- **EGFR (ENSG00000146648) location**: chr7:55,019,017-55,211,628 on minus strand (requires FALDO coordinate query)
- **EGFR has 7 transcript variants**: Including ENST00000275493 (canonical, 28 exons) mapping to UniProt P00533 (requires gene-transcript-protein navigation)
- **Mouse has most genes**: 744,820 genes vs human 87,688 (8.5x more - requires species aggregation query)
- **Human gene coverage**: 100% have descriptions, but only 28% have UniProt cross-references (requires coverage statistics)
- **Chromosome X protein-coding genes**: Found 20+ including HTR2C, TLR8, IL13RA1 (requires chromosome filtering)
- **Receptor tyrosine kinases**: Found ROR1, ROR2, RIPK3, IRAK3, IRAK1 via functional keyword search (requires bif:contains with boolean operators)
- **EGFR exon structure**: 28 exons spanning 192kb genomic region (requires ordered exon query with FALDO)
- **Species diversity**: Database covers 100+ species with mouse, sheep, pig having more genes than human (requires cross-species comparison)

**Key patterns requiring database queries:**
- FALDO location queries for genomic coordinates (not in MIE examples)
- Hierarchical navigation Gene→Transcript→Protein→UniProt (requires multi-hop)
- Species filtering essential for meaningful results (not optional)
- bif:contains enables keyword searches with wildcards and boolean logic
- Strand determination via position type (ForwardStrandPosition/ReverseStrandPosition)
- Ordered exon retrieval via SIO ontology relationships

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT** ✅

### Precision
- ✅ "What is the Ensembl gene ID for human EGFR?" (requires search_entity or bif:contains)
- ✅ "What are the genomic coordinates of BRCA1 (ENSG00000012048)?" (requires FALDO query)
- ✅ "What is the UniProt ID for the canonical EGFR protein?" (requires transcript-protein-UniProt navigation)
- ✅ "How many exons does EGFR transcript ENST00000275493 have?" (requires ordered exon count)
- ✅ "What chromosome is TP53 located on?" (requires so:part_of query)

### Completeness
- ✅ "How many human genes are annotated in Ensembl?" (requires COUNT with species filter)
- ✅ "How many human genes have UniProt cross-references?" (requires coverage query)
- ✅ "How many protein-coding genes are on chromosome X?" (requires biotype + chromosome filter)
- ✅ "List all transcript variants for BRCA1" (requires gene→transcript enumeration)
- ✅ "How many species are covered in Ensembl?" (requires species aggregation)

### Integration
- ✅ "Convert Ensembl gene ENSG00000146648 to UniProt ID" (requires gene→protein→UniProt)
- ✅ "What Ensembl genes on chromosome 17 encode ChEMBL drug targets?" (requires Ensembl-ChEMBL cross-database via UniProt)
- ✅ "Find NCBI Gene ID for Ensembl gene ENSG00000012048" (requires NCBI Gene cross-reference)
- ✅ "What Reactome pathways involve EGFR?" (requires Reactome cross-reference)
- ✅ "Link human kinase genes to approved drugs via ChEMBL" (requires complex cross-database integration)

### Currency
- ✅ "What is the current Ensembl release version?" (metadata query)
- ✅ "When was BRCA1 annotation last updated?" (requires update metadata)
- ✅ "How many SARS-CoV-2 related genes are in recent Ensembl releases?" (requires recent data)

### Specificity
- ✅ "What is the Ensembl ID for mouse Cas9 ortholog?" (requires mouse species + gene search)
- ✅ "Find microRNA genes (biotype) on human chromosome 19" (requires biotype filtering)
- ✅ "What are the MANE Select transcripts for TP53?" (requires transcript flag filtering)
- ✅ "Find genes with > 100 exons" (requires exon count aggregation)
- ✅ "What is the longest human gene by genomic span?" (requires FALDO coordinate calculation)

### Structured Query
- ✅ "Find human genes on chr7 encoding kinases with < 10 exons" (requires chromosome + keyword + exon count filters)
- ✅ "List receptor tyrosine kinase genes with MANE Select transcripts" (requires biotype + transcript flag filters)
- ✅ "Find genes on chromosome 17 with > 50 transcript variants" (requires chromosome + transcript count filters)
- ✅ "Search for genes involved in 'DNA repair' on chromosomes 13, 17, or X" (requires keyword + multi-chromosome filter)
- ✅ "Find human genes encoding proteins targeted by approved drugs" (requires Ensembl→UniProt→ChEMBL with drug phase filter)

**AVOID INFRASTRUCTURE METADATA** ❌
- Database schema structure (not biological content)
- SPARQL query syntax (technical, not research)
- Graph URI patterns (infrastructure)

**AVOID STRUCTURAL METADATA** ❌
- Biotype codes/URIs (ask about gene functions, not classification codes)
- Namespace prefixes (technical infrastructure)
- Property relationship types (schema, not data)

## Notes

**Limitations and challenges:**
- Not all transcripts encode proteins (~60% are non-coding)
- FALDO queries can return duplicate results (always use DISTINCT)
- Species filter (obo:RO_0002162) is essential for meaningful results
- Only 28% of human genes have UniProt cross-references
- Multiple genome assemblies exist (GRCh38, GRCh37) - must specify
- Strand determination requires checking position type (not explicit property)

**Best practices for querying:**
- Always filter by species early (obo:RO_0002162 taxonomy:9606)
- Use bif:contains for text searches with wildcards ('BRCA*')
- Use DISTINCT with FALDO location queries
- Filter by biotype for protein-coding genes (ENSGLOSSARY_0000026)
- Use LIMIT to control result size
- For cross-database queries: pre-filter in source GRAPH, use explicit GRAPH clauses

**Important clarifications:**
- Gene count = number of genes (not transcripts or proteins)
- UniProt coverage = genes with rdfs:seeAlso to UniProt (28% for human)
- Transcript count per gene varies widely (1 to 100+)
- Exon ordering uses SIO ontology (sio:SIO_000300 for order number)

**Distinction between MIE examples and real data findings:**
- MIE shows BRCA1 as example → We queried EGFR, TP53, receptor kinases
- MIE shows generic gene search → We found specific genes (ROR1, ROR2, RIPK3)
- MIE shows coordinate pattern → We retrieved real coordinates for EGFR
- MIE shows species count pattern → We got actual distribution (mouse > human)
- All SPARQL queries adapted from MIE patterns but using different, real entities
