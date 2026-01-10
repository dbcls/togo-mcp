# NCBI Gene Database Exploration Report

## Database Overview
- **Purpose**: Comprehensive gene database across all organisms
- **Scope**: 57M+ entries covering protein-coding genes, ncRNAs, pseudogenes, tRNAs, rRNAs
- **Key entities**: Genes with symbols, descriptions, chromosomal locations, types, synonyms, cross-references
- **Integration**: Links to Ensembl, HGNC, OMIM, NCBI Taxonomy, orthology relationships

## Schema Analysis (from MIE file)

### Main Properties
- `rdfs:label`: Gene symbol (e.g., "TP53", "INS", "BRCA1")
- `dct:identifier`: Numeric gene ID
- `dct:description`: Full gene name (e.g., "tumor protein p53", "insulin")
- `ncbio:typeOfGene`: Gene type (protein-coding, ncRNA, tRNA, rRNA, pseudo)
- `insdc:gene_synonym`: Synonyms/alternative names
- `dct:alternative`: Alternative full names
- `insdc:chromosome`: Chromosome location
- `insdc:map`: Chromosomal map position (e.g., "17p13.1")
- `ncbio:taxid`: Taxonomic classification (link to NCBI Taxonomy)
- `insdc:dblink`: IRI-based external links (Ensembl, HGNC, OMIM)
- `insdc:db_xref`: String-based cross-references
- `orth:hasOrtholog`: Orthologous genes in other species
- `ncbio:nomenclatureStatus`: Official/provisional/discontinued
- `dct:modified`: Last modification date

### Important Relationships
- **Taxonomic**: `ncbio:taxid` links to NCBI Taxonomy
- **Orthology**: `orth:hasOrtholog` for comparative genomics
- **External databases**: `insdc:dblink` (IRIs) and `insdc:db_xref` (strings)
- **Hierarchical**: None (flat gene database)

### Query Patterns Observed
- **RECOMMENDED**: Use `ncbi_esearch` BEFORE SPARQL for gene discovery
- Use `bif:contains` for text search, not REGEX or FILTER
- ALWAYS filter by `ncbio:taxid` early (57M+ genes!)
- Use `FROM <http://rdfportal.org/dataset/ncbigene>` clause
- Label = gene symbols (short), description = full names (long)
- Add LIMIT clauses for orthology queries
- Use OPTIONAL for properties with variable coverage

## Search Queries Performed

1. **Query**: "BRCA1 AND human[organism]" (ncbi_esearch)
   - **Results**: Found 1,563 matching genes
     - Gene ID 7157: TP53 (top result - not BRCA1!)
     - Note: Search returned broader results including related genes
   - First 5 Gene IDs: 7157, 1956, 3569, 7422, 7040

2. **Query**: Detailed metadata for TP53, INS, TGFB1 (ncbi_esummary)
   - **TP53 (Gene ID 7157)**:
     - Description: "tumor protein p53"
     - Chromosome: 17, Map: 17p13.1
     - Synonyms: BCC7, BMFS5, LFS1, P53, TRP53
     - OMIM: 191170
     - Comprehensive summary about tumor suppressor function
   
   - **INS (Gene ID 3630)**:
     - Description: "insulin"
     - Chromosome: 11, Map: 11p15.5
     - Synonyms: IDDM, IDDM1, IDDM2, ILPR, IRDN, MODY10, PNDM4
     - OMIM: 176730
     - Summary about carbohydrate/lipid metabolism regulation
   
   - **TGFB1 (Gene ID 7040)**:
     - Description: "transforming growth factor beta 1"
     - Chromosome: 19, Map: 19q13.2
     - Synonyms: CAEND1, CED, DPD1, etc.
     - OMIM: 190180

3. **Query**: Gene metadata via SPARQL (Gene ID 7157)
   - **Results**: Retrieved TP53 data
     - Label: "TP53"
     - Description: "tumor protein p53"
     - Type: "protein-coding"
   - Demonstrates SPARQL access to RDF data

## SPARQL Queries Tested

```sparql
# Query 1: Basic gene info by ID
PREFIX insdc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>
PREFIX ncbio: <https://dbcls.github.io/ncbigene-rdf/ontology.ttl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?label ?description ?type
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  <http://identifiers.org/ncbigene/7157> rdfs:label ?label ;
    ncbio:typeOfGene ?type .
  OPTIONAL { <http://identifiers.org/ncbigene/7157> dct:description ?description }
}

# Results: TP53, tumor protein p53, protein-coding
# Demonstrates direct gene ID lookup
```

## Interesting Findings

### Specific Entities for Questions
- **TP53 (Gene ID 7157)**: Tumor suppressor, chr 17p13.1, OMIM:191170
- **INS (Gene ID 3630)**: Insulin, chr 11p15.5, OMIM:176730
- **TGFB1 (Gene ID 7040)**: Growth factor, chr 19q13.2, OMIM:190180
- **Multiple synonyms**: TP53 has 5+, INS has 7+ synonyms

### Unique Properties
- **57,768,578 total genes**: Massive database across all organisms
- **Best coverage**: Human, mouse, rat (model organisms)
- **Gene types**: protein-coding (46M), ncRNA (3.5M), tRNA (3M), pseudo (2.7M), rRNA (1M)
- **Orthology**: Average 150 orthologs per gene
- **Cross-references**: Average 1.8 external links per gene
- **Two reference systems**: IRI-based (dblink) and string-based (db_xref)

### Connections to Other Databases
- **Ensembl**: Gene annotations and detailed features
- **HGNC**: Human gene nomenclature (official symbols)
- **OMIM**: Disease associations and phenotypes
- **NCBI Taxonomy**: Organism classification
- **AllianceGenome**: Integrated genomics resources
- **Orthology**: Internal cross-species gene relationships

### Verifiable Facts
- 57,768,578 total gene entries
- 46,105,590 protein-coding genes (80%)
- 3,476,823 ncRNA genes
- 3,030,346 tRNA genes
- 2,731,789 pseudogenes
- Average 2.5 synonyms per gene
- Average 1.8 external links per gene
- Average 150 orthologs per gene (for genes with orthology data)
- Best curated for human (Homo sapiens, taxid:9606)

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Biological IDs and gene properties**
- "What is the NCBI Gene ID for human TP53?"
- "What is the chromosomal location of the INS gene?"
- "What is the OMIM ID for TGFB1?"
- "What is the full name/description of gene ID 7157?"
- "What type of gene is BRCA1 (protein-coding, ncRNA, etc.)?"

❌ Avoid: "What database version is this?" "When was the database updated?"

### Completeness
✅ **Counts and comprehensive lists of genes**
- "How many total genes are in NCBI Gene?"
- "How many protein-coding genes exist in the database?"
- "List all synonyms for the TP53 gene"
- "How many genes are on chromosome 17?"
- "How many human genes have OMIM associations?"

❌ Avoid: "How many database tables exist?" "What is the storage capacity?"

### Integration
✅ **Cross-database gene entity linking**
- "Convert NCBI Gene ID 7157 to its Ensembl ID"
- "What is the HGNC ID for the INS gene?"
- "Find the OMIM ID associated with TP53"
- "What is the NCBI Taxonomy ID for the organism of gene 3630?"
- "Link gene ID 7157 to UniProt via TogoID"

❌ Avoid: "What databases connect to this endpoint?" "List all integration APIs"

### Currency
✅ **Recent gene annotations and updates**
- "When was the TP53 gene entry last modified?"
- "What genes were recently updated in the human genome?"
- "Has the nomenclature status of BRCA1 changed recently?"
- "What is the most recent annotation release for human genes?"

❌ Avoid: "What is the current database version?" "When was the server updated?"

### Specificity
✅ **Specific genes and rare organisms**
- "What is the gene ID for SHOX (a gene on both X and Y chromosomes)?"
- "Find genes specific to hyperthermophilic archaea"
- "What is the gene type for ACTG1P14 (pseudogene)?"
- "Find genes with 'discontinued' nomenclature status"
- "What are the orthologs of human INS in mouse and rat?"

❌ Avoid: "What is the most common query?" "Which gene type is most popular?"

### Structured Query
✅ **Complex gene queries with multiple criteria**
- "Find all human protein-coding genes on chromosome 17 with OMIM IDs"
- "List genes with 'insulin' in the description AND located on chromosome 11"
- "Find all pseudogenes in the human genome"
- "Which genes have more than 5 synonyms AND are tumor-related?"
- "Find orthologs of TP53 in non-human primates"

❌ Avoid: "Find databases updated after 2024" "List all server configurations"

## Notes

### Limitations and Challenges
- **Massive size**: 57M+ genes require careful filtering
- **Variable coverage**: Best for model organisms, sparse for rare species
- **Orthology completeness**: Not all genes have ortholog data
- **Two reference systems**: IRI-based (dblink) vs string-based (db_xref) can be confusing
- **Search ambiguity**: ncbi_esearch may return broader results than expected

### Best Practices for Querying
1. **Use ncbi_esearch FIRST**: More efficient for gene discovery than SPARQL
2. **Always filter by organism**: Use `ncbio:taxid <http://identifiers.org/taxonomy/9606>` early
3. **Use bif:contains for search**: Much faster than REGEX or FILTER
4. **Include FROM clause**: `FROM <http://rdfportal.org/dataset/ncbigene>`
5. **Label vs description**: label=symbols (TP53), description=full names (tumor protein p53)
6. **Add LIMIT clauses**: Essential for orthology and broad queries
7. **Use OPTIONAL**: Many properties have variable coverage
8. **Direct ID lookups**: Fast when you have the Gene ID
9. **Combine ncbi_esearch + SPARQL**: Best of both worlds

### Data Quality Notes
- 100% have typeOfGene
- 95% have descriptions (higher for well-curated organisms)
- 80% have chromosomal locations
- 70% have external links
- 40% have orthology data
- Best curated: human, mouse, rat, zebrafish
- Coverage decreases for non-model organisms
- Orthology most complete between closely related species
- Official nomenclature status indicates curation level
- Modification dates track currency of annotations
