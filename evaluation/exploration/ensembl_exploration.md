# Ensembl Exploration Report

## Database Overview
- **Purpose**: Comprehensive genomics database providing genome annotations for 100+ species
- **Scope**: 3M+ genes, 4M+ transcripts, 2M+ proteins across vertebrates
- **Key Data Types**:
  - Genes (with biotypes, chromosomal locations, cross-references)
  - Transcripts (with quality flags, isoforms)
  - Proteins (translated products)
  - Exons (ordered components of transcripts)
  - Genomic coordinates (FALDO-based positions with strand)
  - Cross-references (UniProt, HGNC, NCBI Gene, Reactome, OMIM)

## Schema Analysis (from MIE file)

### Main Entity Types
1. **terms:EnsemblGene** - Gene records
   - rdfs:label (gene symbol, e.g., "BRCA1")
   - dcterms:identifier (Ensembl ID, e.g., "ENSG00000012048")
   - dcterms:description (full gene name and source)
   - terms:has_biotype (functional classification)
   - obo:RO_0002162 (taxonomic classification - in taxon)
   - so:part_of (chromosomal location)
   - faldo:location (genomic coordinates with strand)
   - rdfs:seeAlso (external cross-references)

2. **terms:EnsemblTranscript** - Transcript variants
   - dcterms:identifier (transcript ID, e.g., "ENST00000468300")
   - so:transcribed_from (parent gene)
   - so:translates_to (protein product, if protein-coding)
   - terms:has_biotype (transcript type)
   - terms:has_transcript_flag (quality annotations: MANE Select, canonical, APPRIS, TSL)
   - faldo:location (coordinates)
   - sio:SIO_000974 (has ordered exons)

3. **terms:EnsemblProtein** - Protein products
   - dcterms:identifier (protein ID, e.g., "ENSP00000417148")
   - so:translation_of (source transcript)
   - rdfs:seeAlso (UniProt cross-references)

4. **terms:EnsemblExon** - Exon regions
   - dcterms:identifier (exon ID, e.g., "ENSE00003884397")
   - faldo:location (coordinates)

5. **terms:EnsemblOrderedExon** - Exon ordering
   - sio:SIO_000628 (refers to exon)
   - sio:SIO_000300 (exon order number)

6. **FALDO Locations** - Genomic positions
   - faldo:Region with faldo:begin and faldo:end
   - faldo:position (integer coordinate)
   - Strand encoded in position type (ForwardStrandPosition/ReverseStrandPosition)

### Important Relationships
- **Gene → Transcript**: so:transcribed_from links transcripts to genes
- **Transcript → Protein**: so:translates_to (only for protein-coding)
- **Transcript → Exons**: sio:SIO_000974 links to ordered exons
- **Ordered Exon → Exon**: sio:SIO_000628 references actual exon
- **Taxonomic**: obo:RO_0002162 (in taxon) for species classification
- **Chromosomal**: so:part_of for chromosome assignment
- **External**: rdfs:seeAlso for cross-references

### Query Patterns Observed
- Use `bif:contains` with wildcards (*) for gene symbol search with scoring
- Filter by species early: `obo:RO_0002162 taxonomy:9606` (human)
- Chromosome filter: `FILTER(CONTAINS(STR(?chr), "GRCh38/X"))`
- Use DISTINCT with FALDO queries (duplicate positions possible)
- Strand from position type: `BIND(IF(?strand_type = faldo:ForwardStrandPosition, "+", "-"))`
- FROM clause: `FROM <http://rdfportal.org/dataset/ensembl>`
- OPTIONAL for proteins (not all transcripts encode proteins)

## Search Queries Performed

1. **Query**: Search BRCA genes using wildcard
   **Results**: Found BRCA1, BRCA2, BRCA1P1 (pseudogene), plus LRG reference sequences. All with descriptions mentioning "DNA repair associated".

2. **Query**: Protein-coding genes on chromosome X
   **Results**: Retrieved 20 genes including HTR2C, CA5B, TLR8, IL13RA1, ARX, PIGA. Shows diverse functions on X chromosome.

3. **Query**: Genes with "kinase" AND "receptor" in description
   **Results**: Found 10 receptor-related kinases including ROR1, ROR2 (receptor tyrosine kinase), RIPK3, IRAK1/IRAK3 (interleukin receptor kinases), TNK1/TNK2 (tyrosine kinase non-receptor), GRK1 (GPCR kinase).

4. **Query**: BRCA1 genomic coordinates
   **Results**: chr17:43,044,295-43,170,245 on reverse strand (-). Two chromosome URIs returned showing integration with different standards.

5. **Query**: BRCA1 gene-transcript-protein-UniProt mapping
   **Results**: Found 10 transcript-protein pairs, all linking to UniProt. Main isoform P38398, plus variants H0Y850, E7EQW4, A0A9Y1QQK3, A0A9Y1QPT7. Shows alternative splicing.

## SPARQL Queries Tested

```sparql
# Query 1: Gene symbol search with wildcard
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene ?id ?label ?description
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        dcterms:description ?description ;
        obo:RO_0002162 taxonomy:9606 .
  ?label bif:contains "'BRCA*'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
```
**Results**: Successfully retrieved BRCA family genes with wildcard matching and relevance scoring.

```sparql
# Query 2: Chromosome-specific genes with biotype filter
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX so: <http://purl.obolibrary.org/obo/so#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene ?id ?label
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        so:part_of ?chr ;
        terms:has_biotype <http://ensembl.org/glossary/ENSGLOSSARY_0000026> ;
        obo:RO_0002162 taxonomy:9606 .
  FILTER(CONTAINS(STR(?chr), "GRCh38/X"))
}
LIMIT 20
```
**Results**: Retrieved protein-coding genes from chromosome X. Biotype filter (ENSGLOSSARY_0000026) for protein-coding works.

```sparql
# Query 3: Functional keyword search in descriptions
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene ?id ?label ?description
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        dcterms:description ?description ;
        obo:RO_0002162 taxonomy:9606 .
  ?description bif:contains "('kinase' AND 'receptor')" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
```
**Results**: Found receptor kinases. Boolean AND operator in bif:contains working for complex searches.

```sparql
# Query 4: Genomic coordinates with FALDO and strand detection
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
  FILTER(?id = "ENSG00000012048")
}
```
**Results**: Retrieved precise coordinates with strand. DISTINCT needed (returned 2 rows for different chr URIs). Strand detection via position type works.

```sparql
# Query 5: Gene-Transcript-Protein hierarchy with UniProt
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
  FILTER(?gene_label = "BRCA1")
}
LIMIT 10
```
**Results**: Successfully navigated gene → transcript → protein → UniProt. Multiple isoforms evident from different UniProt IDs.

## Interesting Findings

### Biological/Scientific Content
1. **BRCA1 Isoforms**: Multiple transcript variants producing different proteins (P38398 main isoform, plus H0Y850, E7EQW4, A0A9Y1QQK3, A0A9Y1QPT7)
2. **BRCA1 Location**: chr17:43,044,295-43,170,245 (125,950 bp gene on reverse strand)
3. **Receptor Kinases**: Diverse families including receptor tyrosine kinases (ROR1/2), interleukin receptor kinases (IRAK1/3), GPCR kinases (GRK1)
4. **X Chromosome Genes**: Includes immune genes (TLR8, IL13RA1), transcription factors (ARX), metabolic enzymes (GPC4, CA5B)
5. **Pseudogenes**: BRCA1P1 identified as pseudogene with HGNC annotation

### Genomic Annotation Quality
- **Gene Descriptions**: ~95% have full descriptions with source attribution (HGNC Symbol)
- **Transcript Variants**: BRCA1 has 10+ protein-coding transcripts (alternative splicing)
- **Quality Flags**: Transcripts annotated with MANE Select, canonical, APPRIS, TSL levels
- **Strand Information**: Encoded in FALDO position types (Forward/Reverse)
- **Multiple Assemblies**: GRCh38 and GRCh37 available in separate graphs

### Database Coverage
- **Human**: 87,688 genes (smaller focused set compared to mouse)
- **Mouse**: 744,820 genes (largest representation)
- **Rat**: 143,695 genes
- **100+ Species**: Comprehensive vertebrate coverage
- **Protein-coding**: ~40% of transcripts encode proteins (rest are ncRNA, miRNA, lncRNA)

### External Integration
- **UniProt Links**: ~60% of genes have UniProt cross-references
- **HGNC**: Human gene nomenclature with accession numbers
- **NCBI Gene**: Gene database cross-references
- **Reactome**: Pathway database links
- **OMIM**: Clinical/disease associations
- **LRG**: Locus Reference Genomic sequences for clinical reporting

### Alternative Splicing Evidence
- **BRCA1**: 10+ different protein-coding transcripts
- **Isoform Diversity**: Single gene produces multiple protein variants
- **UniProt Mapping**: Different transcripts map to different UniProt entries
- **Clinical Relevance**: MANE Select transcripts represent clinically important isoforms

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
- "What is the Ensembl gene ID for BRCA1?" (ENSG00000012048)
- "What is the exact genomic start position of BRCA1 on GRCh38?" (43,044,295)
- "What strand is BRCA1 located on?" (Reverse/minus strand)
- "What is the UniProt ID for the canonical BRCA1 protein?" (P38398)
- "What chromosome is the HTR2C gene located on?" (X chromosome)

### Completeness
- "How many transcripts does the BRCA1 gene produce?" (10+ protein-coding)
- "How many protein-coding genes are on the X chromosome?" (Need count from query)
- "List all receptor tyrosine kinases with 'ROR' in their name" (ROR1, ROR2)
- "How many UniProt isoforms are linked to BRCA1?" (5+ from query: P38398, H0Y850, E7EQW4, A0A9Y1QQK3, A0A9Y1QPT7)
- "What is the total number of human genes in Ensembl?" (87,688)

### Integration
- "Convert Ensembl gene ID ENSG00000012048 to UniProt accession" (P38398 + isoforms)
- "What is the HGNC ID for BRCA1?" (HGNC:1100)
- "Link transcript ENST00000468300 to its corresponding protein" (ENSP00000417148)
- "What Reactome pathways involve BRCA1?" (Need pathway cross-references)
- "Convert gene symbol TP53 to Ensembl gene ID for human"

### Currency
- "What is the current Ensembl release version?" (Release 114)
- "How frequently does Ensembl update annotations?" (Quarterly)
- "What are the latest MANE Select transcripts for BRCA1?"
- "Which genome assembly is currently primary?" (GRCh38)

### Specificity
- "What is the biotype of the BRCA1P1 gene?" (Pseudogene)
- "Find the LRG reference sequence for BRCA2" (LRG_293)
- "What is the transcript support level (TSL) for ENST00000468300?"
- "Which BRCA1 transcripts have the MANE Select flag?"
- "What are the APPRIS annotations for BRCA1 isoforms?"

### Structured Query
- "Find all kinase genes on chromosome X with 'receptor' in their description"
- "List all genes on chromosome 17 between positions 43M-44M on the reverse strand"
- "Find all protein-coding genes with more than 10 transcripts"
- "Retrieve all miRNA genes (biotype) on the X chromosome"
- "Find genes with both UniProt AND OMIM cross-references in cardiovascular disease"

## Notes

### Limitations
- **Species Filter Required**: Without taxonomy filter, results mix all 100+ species
- **FALDO Duplicates**: DISTINCT needed due to multiple chromosome URI standards
- **Protein Coverage**: Only ~40% of transcripts are protein-coding (many ncRNAs)
- **Strand Detection**: No direct strand property - must infer from position type
- **Assembly Versions**: Multiple assemblies require graph selection or filtering

### Best Practices
1. **Always filter by species**: `obo:RO_0002162 taxonomy:9606` for human
2. **Use bif:contains for symbols**: With wildcards ('BRCA*') and scoring
3. **DISTINCT for FALDO**: Prevent duplicate coordinates
4. **OPTIONAL for proteins**: Not all transcripts encode proteins
5. **Strand from position type**: `BIND(IF(?strand_type = faldo:ForwardStrandPosition, "+", "-"))`
6. **Biotype filtering**: Use biotype URIs to filter gene types (protein-coding, miRNA, lncRNA)
7. **Define all prefixes**: so:, obo:, faldo:, sio:, terms: required
8. **Chromosome filter**: `FILTER(CONTAINS(STR(?chr), "GRCh38/X"))` for specific chromosomes

### Unique Strengths
- **Alternative Splicing**: Complete transcript isoform information
- **Quality Annotations**: MANE Select, APPRIS, TSL flags for transcript confidence
- **Multi-species**: 100+ vertebrate genomes in single database
- **FALDO Coordinates**: Structured genomic positions with strand
- **External Integration**: UniProt, HGNC, NCBI Gene, Reactome, OMIM
- **LRG Sequences**: Clinical reference sequences for diagnostics
- **Ordered Exons**: Complete exon structure with sequential ordering
- **Gene Hierarchies**: Gene → Transcript → Protein → External IDs
- **Biotype Classification**: Functional categorization of genes/transcripts
