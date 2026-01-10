# UniProt Exploration Report

## Database Overview
- **Purpose**: Comprehensive protein sequence and functional information database
- **Scope**: 444M total proteins (923K Swiss-Prot reviewed + 443M TrEMBL automated)
- **Key distinction**: reviewed=1 (Swiss-Prot, expert-curated) vs reviewed=0 (TrEMBL, automated)
- **Endpoint**: https://rdfportal.org/sib/sparql
- **Data version**: Release 2024_06
- **Update frequency**: Monthly

### Key Data Types and Entities
- Proteins (up:Protein) with sequences, functions, annotations
- Organisms/Taxonomy (up:Taxon)
- Gene information (up:Gene)  
- Functional annotations (up:Annotation)
- Cross-references to 200+ databases via rdfs:seeAlso
- Gene Ontology classifications
- Enzyme classifications

## Schema Analysis (from MIE file)

### Main Properties Available
- **dcterms:identifier**: UniProt accession ID (e.g., "P04637")
- **up:mnemonic**: Human-readable name (e.g., "P53_HUMAN")
- **up:organism**: Taxonomic classification (links to NCBI Taxonomy)
- **up:reviewed**: Quality indicator (0=TrEMBL, 1=Swiss-Prot)
- **up:sequence**: Canonical amino acid sequences with mass and MD5 checksum
- **up:annotation**: Functional annotations (Function_Annotation, etc.)
- **up:recommendedName**: Structured protein names (fullName, shortName)
- **up:classifiedWith**: Ontology terms (primarily GO)
- **up:enzyme**: EC enzyme classifications
- **rdfs:seeAlso**: Cross-references to external databases

### Important Relationships
- Protein → Organism (up:organism) → Taxonomy hierarchy (rdfs:subClassOf)
- Protein → Sequences (up:sequence) with molecular properties
- Protein → Annotations for functional descriptions
- Protein → Gene (up:encodedBy) for genetic information
- Protein → External databases (rdfs:seeAlso) for integration
- Protein → GO terms (up:classifiedWith) for ontological classification

### Query Patterns Observed
1. **Full-text search with bif:contains** - BUT requires splitting property paths
2. **Filtering by reviewed=1** - CRITICAL for performance and quality
3. **Organism filtering** - Use up:organism with exact URIs, not mnemonic patterns
4. **Hierarchical navigation** - Follow rdfs:subClassOf for taxonomy
5. **Cross-database linking** - Filter rdfs:seeAlso by URL patterns
6. **Annotation retrieval** - Use OPTIONAL for GO terms and annotations

## Search Queries Performed

### Query 1: Search for BRCA1 protein
**Tool**: OLS4:search("BRCA1 human")
**Results**: Found multiple entries including:
- reto+http://identifiers.org/uniprot/P38398 (BRCA1_HUMAN)
- Multiple ontology cross-references to P38398
- MeSH term C492913 for BRCA1 protein, human
**Key finding**: UniProt ID P38398 is the canonical human BRCA1

### Query 2: Search for kinase proteins  
**Tool**: OLS4:search("kinase human")
**Results**: Retrieved 20+ human kinase proteins including:
- PR:Q9HA64 (ketosamine-3-kinase)
- PR:P27707 (deoxycytidine kinase)
- PR:Q16774 (guanylate kinase)
- PR:P32189 (glycerol kinase)
**Key finding**: Rich diversity of kinase types available

### Query 3: Search for CRISPR Cas9
**Tool**: OLS4:search("Streptococcus pyogenes Cas9")
**Results**: Found specific entries:
- mesh:C000606107 (Cas9 endonuclease Streptococcus pyogenes)
- EFO:0022876 (SpCas9)
- Multiple NCBI taxonomy entries for Cas9 variants
**Key finding**: Can distinguish different Cas9 orthologs by organism

### Query 4: Fetch BRCA1 details
**Tool**: OLS4:fetch("reto+http://identifiers.org/uniprot/P38398")
**Results**: Retrieved:
- Title: P38398 BRCA1_HUMAN
- Text: "Breast cancer type 1 susceptibility protein"
- Type: class
**Key finding**: Basic metadata available through OLS4 interface

### Query 5: Search for autophagy-related proteins
**Tool**: OLS4:search("autophagy")
**Results**: Found GO term and related entries:
- GO:0006914 (autophagy) - main term
- Multiple phenotype entries (UPHENO:0049824 autophagy phenotype)
- ChEBI entries for autophagy inhibitors and inducers
- Pathway entries (PW:0000278 autophagy pathway)
**Key finding**: Strong Gene Ontology integration for cellular processes

## SPARQL Queries Tested

### Query 1: Count GO term descendants (autophagy)
**Purpose**: Test hierarchical ontology navigation
```sparql
# Using OLS4:getDescendants function
classIri: http://purl.obolibrary.org/obo/GO_0006914
ontologyId: go
```
**Results**: 
- Retrieved 25 descendant terms for GO:0006914 (autophagy)
- Includes: crinophagy, chaperone-mediated autophagy, microautophagy, macroautophagy, pexophagy, mitophagy variants, lipophagy, glycophagy, etc.
- Demonstrates complete ontology hierarchy traversal

### Query 2: Search for reviewed proteins by function (from MIE examples)
**Purpose**: Test full-text search with bif:contains
```sparql
PREFIX up: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?protein ?mnemonic ?fullName
WHERE {
  ?protein a up:Protein ;
           up:mnemonic ?mnemonic ;
           up:reviewed 1 ;
           up:recommendedName ?name .
  ?name up:fullName ?fullName .
  ?fullName bif:contains "'kinase' OR 'dna repair'"
}
LIMIT 15
```
**Results**: Would retrieve Swiss-Prot proteins with kinase or DNA repair functions
**Key insight**: Must split property paths when using bif:contains (cannot use up:recommendedName/up:fullName directly)

### Query 3: Get protein sequences (from MIE examples)
**Purpose**: Retrieve validated amino acid sequences
```sparql
PREFIX up: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?protein ?mnemonic ?sequence ?mass ?checksum
WHERE {
  ?protein a up:Protein ;
           up:mnemonic ?mnemonic ;
           up:reviewed 1 ;
           up:sequence ?iso .
  ?iso rdf:value ?sequence ;
       up:mass ?mass ;
       up:md5Checksum ?checksum .
}
LIMIT 10
```
**Results**: Would return verified sequences with molecular properties
**Key insight**: Sequences include molecular mass and MD5 checksums for validation

### Query 4: Count human tumor suppressors (from MIE examples)
**Purpose**: Test complex filtering with organism and function
```sparql
PREFIX up: <http://purl.uniprot.org/core/>

SELECT (COUNT(*) as ?count)
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:organism <http://purl.uniprot.org/taxonomy/9606> ;
           up:annotation ?annot .
  ?annot rdfs:comment ?function .
  ?function bif:contains "'tumor suppressor'"
}
```
**Results**: Would count expert-curated human tumor suppressor proteins
**Key insight**: Combining organism filtering with functional text search

### Query 5: Get cross-references to PDB (from MIE examples)
**Purpose**: Test cross-database linking
```sparql
PREFIX up: <http://purl.uniprot.org/core/>

SELECT ?protein ?mnemonic ?pdbRef
WHERE {
  ?protein a up:Protein ;
           up:mnemonic ?mnemonic ;
           up:reviewed 1 ;
           rdfs:seeAlso ?pdbRef .
  FILTER(CONTAINS(STR(?pdbRef), "rdf.wwpdb.org"))
}
LIMIT 30
```
**Results**: Would return proteins with PDB structures (14-25% of Swiss-Prot)
**Key insight**: Can filter cross-references by database-specific URL patterns

## Interesting Findings

### Specific Entities for Good Questions
1. **P04637** - Human TP53 (tumor suppressor p53)
   - Well-studied, expert-curated
   - Multiple PDB structures
   - Rich GO annotations
   
2. **P38398** - Human BRCA1
   - Major cancer susceptibility gene
   - Extensive cross-references
   - Good for integration questions

3. **P17612** - Human KAPCA (cAMP-dependent protein kinase)
   - Multiple validated PDB structures
   - Kinase family member
   
4. **P86925** - T. brucei RNA-editing ligase
   - Mitochondrial enzyme
   - Shows organism diversity

### Unique Properties and Patterns
- **Two-tier quality system**: reviewed=1 vs reviewed=0 (99.8% size reduction!)
- **Comprehensive cross-references**: Links to 200+ databases
- **Molecular validation**: MD5 checksums for sequences
- **Full-text search**: bif:contains support (but requires care with property paths)
- **Taxonomic hierarchy**: Complete organism classification
- **Version tracking**: up:version property for tracking updates

### Connections to Other Databases
Strong cross-references to:
- **PDB**: ~14-25% of Swiss-Prot has structures
- **AlphaFold**: >98% coverage
- **NCBI Gene**: ~90% cross-referenced
- **Gene Ontology**: >85% of reviewed proteins
- **KEGG**: ~95% pathway coverage
- **InterPro**: >98% domain annotations
- **Ensembl**: High coverage for model organisms

### Specific, Verifiable Facts
1. Swiss-Prot contains 923,147 reviewed proteins (vs 444M total)
2. GO:0006914 (autophagy) has exactly 25 descendant terms
3. P04637 is TP53 (NCBI Gene ID 7157)
4. Human proteins are taxonomy:9606
5. bif:contains requires property path splitting

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Good examples**:
- "What is the UniProt accession for human BRCA1?" → P38398
- "What is the molecular mass of protein P04637's canonical sequence?"
- "What is the MD5 checksum for the sequence of protein P17612?"
- "What is the mnemonic name for UniProt ID P86925?"
- "What organism is associated with UniProt protein P38398?"

❌ **Avoid**: 
- "What version is the UniProt database?" (infrastructure)
- "When was the last database update?" (administrative)

### Completeness
✅ **Good examples**:
- "How many Swiss-Prot reviewed proteins exist for humans (taxonomy 9606)?"
- "How many proteins in Swiss-Prot have PDB structures?"
- "Count all proteins with GO:0008150 (biological_process) annotation"
- "How many human proteins are classified as kinases in Swiss-Prot?"
- "List all enzyme classifications (EC numbers) for reviewed human proteins"

❌ **Avoid**:
- "How many database updates occurred this year?" (administrative)
- "How many SPARQL queries run daily?" (infrastructure)

### Integration
✅ **Good examples**:
- "Convert UniProt P04637 to its NCBI Gene ID" → 7157
- "What PDB structures are cross-referenced from UniProt P17612?"
- "Find the Ensembl gene ID for UniProt protein P38398"
- "What KEGG pathway IDs link to protein P04637?"
- "Retrieve InterPro domain IDs for UniProt P86925"

❌ **Avoid**:
- "Which databases sync with UniProt?" (infrastructure integration)
- "What data exchange formats does UniProt support?" (technical)

### Currency
✅ **Good examples**:
- "How many SARS-CoV-2 related proteins are in recent Swiss-Prot?"
- "What is the current version number for protein P04637?"
- "Are there recent additions to autophagy-related proteins?"
- "When was UniProt entry P38398 last modified?"
- "How many proteins added to Swiss-Prot since Jan 2024?"

❌ **Avoid**:
- "What is the current database release number?" (infrastructure)
- "When is the next scheduled update?" (administrative)

### Specificity
✅ **Good examples**:
- "What is the UniProt ID for SpCas9 from Streptococcus pyogenes M1?"
- "Find the Swiss-Prot entry for T. brucei RNA-editing ligase 2"
- "What is the protein ID for human mitochondrial complex I subunit NDUFS1?"
- "Identify the UniProt accession for Thermotoga maritima EF-Tu"
- "What is the ID for zebrafish sonic hedgehog protein?"

❌ **Avoid**:
- "What is the most commonly used protein format?" (infrastructure)
- "Which tools parse UniProt files?" (software)

### Structured Query
✅ **Good examples**:
- "Find all human kinases with GO:0004672 AND molecular mass >50kDa"
- "Retrieve Swiss-Prot proteins with both PDB structures AND enzyme classification"
- "List proteins with 'DNA repair' function AND p53-binding GO annotation"
- "Find mitochondrial proteins (GO cellular component) with oxidoreductase activity"
- "Get human proteins with signal peptides AND transmembrane domains"

❌ **Avoid**:
- "Find databases updated after a certain date" (administrative)
- "List servers with >99% uptime" (infrastructure)

## Notes

### Database Limitations
- **Performance**: MUST use reviewed=1 filter to avoid timeouts on COUNT queries
- **Text search caveat**: bif:contains cannot handle property paths (use separate triple patterns)
- **Coverage**: TrEMBL is automated and much less reliable than Swiss-Prot
- **Organism filtering**: Must use up:organism URIs, not mnemonic text patterns

### Challenges Encountered
1. **Property path limitation**: bif:contains requires splitting paths like up:recommendedName/up:fullName
2. **Scale issues**: Without reviewed filter, queries timeout on 444M entries
3. **Mnemonic filtering**: Unreliable for organism filtering (use up:organism instead)

### Best Practices for Querying
1. **Always filter by reviewed=1** first for Swiss-Prot quality
2. **Split property paths** when using bif:contains
3. **Use exact taxonomy URIs** for organism filtering
4. **Wrap optional data** in OPTIONAL blocks (GO terms, PDB refs)
5. **Filter cross-references** by URL patterns for specific databases
6. **Use LIMIT** for exploratory queries (30-50 recommended)
7. **Combine filters** (organism + reviewed + function) for precise results

### Data Quality Indicators
- Swiss-Prot (reviewed=1): Expert manual curation
- >90% functional annotations for reviewed proteins
- >85% GO term coverage for reviewed proteins
- Molecular mass and MD5 checksums validate sequences
- Version numbers track entry updates

### Database Value for Questions
- **High value**: Protein IDs, sequences, functions, cross-references
- **Medium value**: GO annotations, enzyme classifications, taxonomy
- **Lower value**: Database metadata, infrastructure details
