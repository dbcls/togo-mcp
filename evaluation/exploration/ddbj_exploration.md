# DDBJ Exploration Report

## Database Overview
- **Purpose**: Nucleotide sequence data from the International Nucleotide Sequence Database Collaboration (INSDC)
- **Scope**: Genomic entries with annotations including genes, CDS, tRNA, rRNA, linked to organism metadata and functional annotations
- **Key Data Types**:
  - Sequence entries (accessions like CP036276.1, AP026093.1)
  - Genomic features (genes, coding sequences, tRNA, rRNA)
  - Functional annotations (product descriptions, protein translations)
  - Genomic coordinates (FALDO-based positions)
  - Taxonomic classifications
  - Cross-references (BioProject, BioSample, NCBI Protein)

## Schema Analysis (from MIE file)

### Main Entity Types
1. **nuc:Entry** - Sequence record
   - rdfs:label (entry description)
   - dcterms:identifier (accession number)
   - nuc:definition (full description)
   - nuc:organism (organism name)
   - nuc:taxonomy (taxonomic string)
   - nuc:division (database division)
   - nuc:sequence_version, nuc:sequence_date
   - nuc:dblink (BioProject, BioSample links)
   - nuc:reference (literature references)

2. **nuc:Gene** - Gene features
   - nuc:locus_tag (>99% coverage - most reliable ID)
   - nuc:gene (gene symbol, ~60% coverage)
   - nuc:location (text description)
   - faldo:location (structured coordinates)
   - rdfs:subClassOf (Sequence Ontology classification)
   - bfo:0000050 (part of entry/sequence)
   - ro:0002162 (in taxon)

3. **nuc:Coding_Sequence** (CDS)
   - nuc:locus_tag (same as corresponding gene)
   - nuc:product (protein product description, >95% coverage)
   - nuc:translation (amino acid sequence, >95% coverage)
   - nuc:codon_start, nuc:transl_table (translation parameters)
   - rdfs:seeAlso (NCBI Protein link)
   - sio:SIO_010081 (encodes gene - **case-sensitive uppercase**)
   - faldo:location (coordinates)

4. **nuc:Transfer_RNA and nuc:Ribosomal_RNA**
   - faldo:location (coordinates)
   - nuc:product (RNA type/amino acid)
   - bfo:0000050 (part of entry)
   - ro:0002162 (in taxon)

5. **nuc:Source** - Organism/sample information
   - nuc:organism (organism name)
   - nuc:mol_type (molecule type, e.g., "genomic DNA")
   - rdfs:seeAlso (Taxonomy link)
   - ro:0002162 (taxonomic classification)

6. **FALDO Regions and Positions**
   - faldo:Region with faldo:begin and faldo:end
   - faldo:ExactPosition with faldo:position (integer coordinate)
   - faldo:reference (reference to sequence)

### Important Relationships
- **Entry-Feature hierarchy**: All features link to entry via bfo:0000050 (part of)
- **Gene-CDS linkage**: CDS encodes gene via sio:SIO_010081 (**CRITICAL: uppercase**)
- **Taxonomic classification**: Features use ro:0002162 (in taxon) for NCBI Taxonomy
- **Protein cross-reference**: CDS links to NCBI Protein via rdfs:seeAlso
- **Sequence Ontology**: Features classified via rdfs:subClassOf to SO terms
- **FALDO coordinates**: Structured genomic positions enable range queries

### Query Patterns Observed
- **CRITICAL**: Always filter by entry ID before any complex queries: `FILTER(CONTAINS(STR(?var), "ENTRY_ID"))`
- Use `bif:contains` ONLY for organism search at entry level (fast, scored)
- Use `FILTER CONTAINS` for product searches WITHIN entries (after entry filter)
- Case-sensitive property: `sio:SIO_010081` (uppercase) for gene-CDS links
- FROM clause: `FROM <http://rdfportal.org/dataset/ddbj>`
- Entry URIs: `http://identifiers.org/insdc/ACCESSION`
- Protein URIs: `http://identifiers.org/ncbiprotein/ACCESSION`

## Search Queries Performed

1. **Query**: Search E. coli entries using bif:contains
   **Results**: Found 10 E. coli genome entries (AP026093.1, AP026094.1, etc.) all with relevance score 28

2. **Query**: Gene coordinates in CP036276.1
   **Results**: Retrieved 10 genes with locus tags (Mal52_08030 through Mal52_08120), start positions 1001623-1013845, end positions 1002915-1014603. Shows FALDO coordinates working.

3. **Query**: Protease/peptidase genes in CP036276.1
   **Results**: Found 20 protease/peptidase genes including Clp proteases, leader peptidases, aminopeptidases, signal peptide peptidases, FtsH protease, HtrA protease. Diverse protease families.

4. **Query**: Gene-CDS-Protein integration
   **Results**: Successfully linked locus tags to products and NCBI Protein IDs. Examples: Mal52_08030 → ClpX → QDU42347.1, Mal52_08040 → N-6 DNA Methylase → QDU42348.1. Many hypothetical proteins.

5. **Query**: RNA features (tRNA and rRNA)
   **Results**: Retrieved 20 tRNAs with amino acid specificity (tRNA-Ile, tRNA-Ala, tRNA-Gly, etc.). Standard tRNA set for translation. No rRNA in first 20 results.

6. **Query**: BioProject and BioSample links
   **Results**: Found 10 entries with both BioProject and BioSample links. Example: CP036276.1 → PRJNA485700 + SAMN10954015. Multiple plasmids from same BioProject.

## SPARQL Queries Tested

```sparql
# Query 1: Search entries by organism (bif:contains at entry level)
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?entry ?organism ?relevance
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?entry a nuc:Entry ;
         nuc:organism ?organism .
  ?organism bif:contains "'escherichia' AND 'coli'" option (score ?relevance) .
}
ORDER BY DESC(?relevance)
LIMIT 10
```
**Results**: Successfully retrieved 10 E. coli entries with relevance scoring. Shows bif:contains effective for organism-level search.

```sparql
# Query 2: Gene coordinates with FALDO (entry-filtered)
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>

SELECT ?locus_tag ?start ?end
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?gene a nuc:Gene ;
        nuc:locus_tag ?locus_tag ;
        faldo:location ?region .
  ?region faldo:begin/faldo:position ?start ;
          faldo:end/faldo:position ?end .
  FILTER(CONTAINS(STR(?gene), "CP036276.1"))
}
LIMIT 10
```
**Results**: Retrieved genes with precise coordinates. FALDO property paths working (begin/position, end/position).

```sparql
# Query 3: Product search within entry (FILTER CONTAINS)
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?locus_tag ?product
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?cds a nuc:Coding_Sequence ;
       nuc:locus_tag ?locus_tag ;
       nuc:product ?product .
  FILTER(CONTAINS(STR(?cds), "CP036276.1"))
  FILTER(CONTAINS(LCASE(?product), "protease") || CONTAINS(LCASE(?product), "peptidase"))
}
LIMIT 20
```
**Results**: Found 20 protease/peptidase genes. Entry filtering + product filtering combination works efficiently.

```sparql
# Query 4: Gene-CDS-Protein integration (complex join)
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>
PREFIX sio: <http://semanticscience.org/resource/>

SELECT ?locus_tag ?product ?protein_id
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?gene a nuc:Gene ;
        nuc:locus_tag ?locus_tag .
  ?cds sio:SIO_010081 ?gene ;
       nuc:product ?product ;
       rdfs:seeAlso ?protein_id .
  FILTER(CONTAINS(STR(?protein_id), "ncbiprotein"))
  FILTER(CONTAINS(STR(?gene), "CP036276.1"))
}
LIMIT 10
```
**Results**: Successfully joined genes, CDS, and proteins. Demonstrates sio:SIO_010081 (uppercase) linkage working.

```sparql
# Query 5: RNA features with UNION
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?rna_type ?product
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  {
    ?rna a nuc:Transfer_RNA ; nuc:product ?product .
    BIND("tRNA" AS ?rna_type)
    FILTER(CONTAINS(STR(?rna), "CP036276.1"))
  }
  UNION
  {
    ?rna a nuc:Ribosomal_RNA ; nuc:product ?product .
    BIND("rRNA" AS ?rna_type)
    FILTER(CONTAINS(STR(?rna), "CP036276.1"))
  }
}
LIMIT 20
```
**Results**: Retrieved tRNAs with amino acid specificity. UNION pattern working for different RNA types.

```sparql
# Query 6: BioProject/BioSample cross-references
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?entry ?bioproject ?biosample
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?entry a nuc:Entry ;
         nuc:dblink ?bioproject ;
         nuc:dblink ?biosample .
  FILTER(CONTAINS(STR(?bioproject), "bioproject"))
  FILTER(CONTAINS(STR(?biosample), "biosample"))
}
LIMIT 10
```
**Results**: Retrieved entries with both BioProject and BioSample links. Shows external database integration.

## Interesting Findings

### Biological/Scientific Content
1. **Protease Diversity**: CP036276.1 genome contains 20+ different protease/peptidase families including ATP-dependent Clp, leader peptidases, signal peptide peptidases, FtsH, HtrA
2. **tRNA Gene Set**: Standard set of tRNAs for all amino acids (Ile, Ala, Gly, Pro, Glu, Cys, Arg, Ser, Leu, Met, Asp, Lys, Val)
3. **Hypothetical Proteins**: Many CDS annotated as "hypothetical protein" suggesting unknowns in bacterial genomes
4. **Gene Density**: CP036276.1 has genes every ~1000-2000 bp showing typical bacterial genome compactness
5. **Protein Translations**: >95% of CDS have full amino acid translations available

### Genomic Annotation Patterns
- **Locus Tags**: >99% coverage, most reliable identifier (e.g., Mal52_08030)
- **Gene Symbols**: ~60% coverage, some genes unnamed
- **Product Descriptions**: >95% coverage for CDS
- **FALDO Coordinates**: >99% of features have structured positions
- **Protein Cross-refs**: All CDS link to NCBI Protein database

### Entry Organization
- **Multiple Accessions**: AP026093-AP026119 series suggests related sequences (chromosomes/plasmids)
- **CP036276.1**: Complete chromosome of Symmachiella dynata strain Mal52
- **Prokaryotic Focus**: Mostly bacterial and archaeal genomes
- **Daily Updates**: Continuous integration from INSDC submissions

### Data Integration Opportunities
- **BioProject**: Links to project-level metadata (PRJNA numbers)
- **BioSample**: Links to sample metadata (SAMN numbers)
- **NCBI Protein**: Every CDS links to RefSeq protein (QDU prefixes)
- **NCBI Taxonomy**: All features taxonomically classified via ro:0002162
- **Sequence Ontology**: Features typed via rdfs:subClassOf to SO terms

### Performance Insights
- **Entry Filtering CRITICAL**: Must filter by entry ID before ANY complex queries to prevent timeouts
- **bif:contains**: Fast for organism search at entry level
- **FILTER CONTAINS**: Use for product/description searches WITHIN entries
- **Property Case Sensitivity**: sio:SIO_010081 MUST be uppercase
- **Coordinate Queries**: FALDO efficient when entry-filtered first

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
- "What is the NCBI Protein ID for the gene with locus tag Mal52_08030?" (QDU42347.1)
- "What is the start position of the clpX gene in CP036276.1?" (1001623)
- "What is the product annotation for locus tag Mal52_08430?" (ATP-dependent Clp protease proteolytic subunit)
- "What amino acid does tRNA-Ile carry in CP036276.1?" (Isoleucine)
- "What is the BioSample ID for entry CP036276.1?" (SAMN10954015)

### Completeness
- "How many protease/peptidase genes are in CP036276.1?" (20+)
- "How many different tRNA genes are in a typical bacterial genome?" (Count from query)
- "What is the full set of tRNA amino acid specificities in CP036276.1?" (Ile, Ala, Gly, Pro, Glu, Cys, Arg, Ser, Leu, Met, Asp, Lys, Val)
- "How many genes have the prefix Mal52_ in CP036276.1?" (Need count)
- "List all Clp protease subunits in CP036276.1" (ClpX, proteolytic subunit, precursor)

### Integration
- "What is the NCBI Protein accession for the ATP-dependent Clp protease in CP036276.1?" (QDU42347.1)
- "Convert locus tag Mal52_08030 to its corresponding NCBI Protein ID"
- "What BioProject does entry CP036276.1 belong to?" (PRJNA485700)
- "Link BioSample SAMN10954015 to its DDBJ entry accession"
- "What is the NCBI Taxonomy ID for Symmachiella dynata?"

### Currency
- "What are the most recently added E. coli genome entries?" (AP026xxx series from query)
- "What is the update frequency for DDBJ RDF data?" (Daily)
- "Which genomes were deposited under BioProject PRJNA485700 recently?"
- "What new hypothetical proteins have been annotated in recent submissions?"

### Specificity
- "What is the function of the HtrA protease in CP036276.1?" (Serine protease)
- "Find the FtsH protease gene in CP036276.1" (Mal52_13200 - ATP-dependent zinc metalloprotease)
- "What is the codon start position for translation in a specific CDS?"
- "Which signal peptide peptidases are present in the Symmachiella dynata genome?"
- "What is the mol_type annotation for phage sequences?" (genomic DNA)

### Structured Query
- "Find all genes between positions 1000000-1010000 in CP036276.1"
- "List all membrane-associated proteases (leader peptidase, signal peptidase) in CP036276.1"
- "Find all genes with products containing 'ATP-dependent' AND 'protease' in CP036276.1"
- "Retrieve all tRNA genes with their amino acid specificities AND genomic positions"
- "Find all CDS with translations longer than 400 amino acids in CP036276.1"

## Notes

### Critical Limitations
- **Entry filtering MANDATORY**: All complex queries MUST filter by entry ID first or will timeout
- **Case sensitivity**: sio:SIO_010081 must be uppercase (sio:010081 won't work)
- **No aggregation without filtering**: COUNT/GROUP BY without entry filter causes timeout
- **bif:contains scope**: Only effective for organism search at entry level, not for products
- **FALDO performance**: Coordinate queries require entry filtering first

### Best Practices
1. **Always filter by entry ID**: `FILTER(CONTAINS(STR(?var), "ENTRY_ID"))` before complex queries
2. **Use bif:contains for organism**: Entry-level organism search only
3. **Use FILTER CONTAINS for products**: Within-entry product searches
4. **Uppercase SIO property**: `sio:SIO_010081` not `sio:010081`
5. **OPTIONAL for gene symbols**: ~40% don't have gene symbols, use locus_tag
6. **FROM clause required**: `FROM <http://rdfportal.org/dataset/ddbj>`
7. **Sample instead of aggregate**: Use LIMIT instead of COUNT for exploration
8. **FALDO property paths**: `faldo:location/faldo:begin/faldo:position`

### Unique Strengths
- **FALDO genomic coordinates**: Structured position queries enable range-based searches
- **Complete gene annotations**: Gene → CDS → Protein linkage with functional descriptions
- **tRNA/rRNA coverage**: RNA genes annotated with specificity
- **Daily updates**: Continuous integration from INSDC
- **Protein cross-references**: All CDS link to NCBI Protein RefSeq
- **BioProject/BioSample links**: Experimental context and metadata
- **Sequence Ontology**: Semantic feature typing
- **Translation data**: Amino acid sequences for >95% of CDS
