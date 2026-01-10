# ClinVar Exploration Report

## Database Overview
ClinVar aggregates genomic variation and its relationship to human health:
- **3.5 million+ variant records** (3,236,823 SNVs alone)
- **~20,000 human genes** with variant associations
- **Clinical interpretations** with significance classifications
- **Gene-disease associations** through variant annotations
- **Monthly updates** from submissions worldwide
- Cross-references to MedGen, OMIM, MeSH, and HGNC

## Schema Analysis (from MIE file)

### Main Properties Available
- **VariationArchiveType**: Variant records with VCV accessions, variation names, types, species
- **Variant Properties**: Record status (current/deprecated), dates (created/updated), number of submitters
- **Classification**: Germline clinical significance (pathogenic, benign, uncertain, etc.)
- **Gene Associations**: Gene ID, symbol, full name, HGNC ID, OMIM ID, cytogenetic location
- **Disease/Trait**: Clinical assertion traits with type, IDs, MedGen/OMIM/MeSH references
- **Genomic Location**: FALDO ontology for precise coordinates
- **Submitter Information**: Number of submitters indicates evidence strength

### Important Relationships
- `cvo:accession` - VCV variant identifiers (e.g., VCV000017662)
- `cvo:variation_id` - Numeric variant IDs
- `cvo:classified_record` - Links to clinical assertions (blank nodes)
- `cvo:classifications` - Clinical significance assessments
- `med2rdf:disease` - Disease/phenotype associations (blank nodes)
- `sio:SIO_000628` - Gene associations
- `dct:references` - External database cross-references (MedGen, OMIM, MeSH)
- `cvo:hgnc_id` - HGNC gene identifiers
- `faldo:location` - Genomic coordinates

### Query Patterns Observed
- **ncbi_esearch**: Search by gene symbol, disease, or accession
- **SPARQL with bif:contains**: Full-text search on rdfs:label
- **FROM clause required**: `FROM <http://rdfportal.org/dataset/clinvar>`
- **Blank node navigation**: Complex paths to clinical significance and diseases
- **Status filtering**: Use `cvo:record_status "current"` to exclude deprecated
- **Date filtering**: Use cvo:date_created/date_last_updated (xsd:date type)
- **Use OPTIONAL**: For incomplete annotations (clinical significance, diseases)

## Search Queries Performed

1. **ncbi_esearch for "BRCA1"** → Results: 82,811 variants total (massive dataset for this gene)
2. **ncbi_esearch for "Type 2 Diabetes"** → Results: 16,458 variants associated with diabetes
3. **SPARQL search for BRCA1 variants** → Results: 10 variants including frameshift deletions, duplications, SNVs
4. **Variant type counts** → Results: 3.2M SNVs, 160K deletions, 73K duplications
5. **BRCA1 gene details** → Results: Gene 672, location 17q21.31, HGNC:1100

## SPARQL Queries Tested

```sparql
# Query 1: Find BRCA1 variants with full-text search
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?variant ?label ?type ?status
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           rdfs:label ?label ;
           cvo:variation_type ?type ;
           cvo:record_status ?status .
  ?label bif:contains "'BRCA1'" .
}
LIMIT 10
# Results: Retrieved 10 BRCA1 variants including:
# - c.2244dup (p.Asp749fs) - Duplication
# - c.453T>G (p.Ser151Arg) - SNV
# - c.1997del (p.Leu666fs) - Deletion
# - Various frameshift and missense mutations
```

```sparql
# Query 2: Count variants by type (current records only)
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>

SELECT ?variation_type (COUNT(?variant) as ?count)
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           cvo:variation_type ?variation_type ;
           cvo:record_status "current" .
}
GROUP BY ?variation_type
ORDER BY DESC(?count)
LIMIT 10
# Results:
# - single nucleotide variant: 3,236,823 (90.2%)
# - Deletion: 160,620
# - Duplication: 73,448
# - Microsatellite: 36,328
# - copy number gain: 24,800
# - copy number loss: 22,592
# - Indel: 16,935
# - Insertion: 13,373
# - Inversion: 1,495
# - Haplotype: 616
```

```sparql
# Query 3: Get BRCA1 gene details
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>

SELECT ?gene ?symbol ?full_name ?hgnc_id ?cyto_loc
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?gene a cvo:Gene ;
        cvo:symbol ?symbol ;
        cvo:full_name ?full_name ;
        cvo:cytogenetic_location ?cyto_loc .
  OPTIONAL { ?gene cvo:hgnc_id ?hgnc_id }
  FILTER(?symbol = "BRCA1")
}
# Results: Gene 672
# - Symbol: BRCA1
# - Full name: BRCA1 DNA repair associated
# - HGNC ID: HGNC:1100
# - Cytogenetic location: 17q21.31
```

```sparql
# Query 4: Find well-studied BRCA1 variants (multiple submitters)
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?variant ?label ?num_submitters ?date_created ?date_updated
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           rdfs:label ?label ;
           cvo:number_of_submitters ?num_submitters ;
           cvo:date_created ?date_created ;
           cvo:date_last_updated ?date_updated .
  ?label bif:contains "'BRCA1'" .
  FILTER(?num_submitters >= 5)
}
ORDER BY DESC(?num_submitters)
LIMIT 5
# Results: Top 5 well-studied BRCA1 variants:
# 1. c.68_69del (p.Glu23fs) - 78 submitters, created 2013-04-12, updated 2025-05-25
# 2. c.5266dup (p.Gln1756fs) - 78 submitters, created 2013-10-01, updated 2025-05-25
# 3. c.181T>G (p.Cys61Gly) - 59 submitters, created 2015-09-29, updated 2025-05-25
# 4. c.1687C>T (p.Gln563Ter) - 52 submitters, created 2015-03-03, updated 2025-05-25
# 5. c.3756_3759del (p.Ser1253fs) - 52 submitters, created 2014-04-01, updated 2025-05-25
```

```sparql
# Query 5: Get variant by accession
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>

SELECT ?variant ?accession ?label
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant cvo:accession ?accession ;
           rdfs:label ?label .
  FILTER(?accession = "VCV000017662")
}
# Results: VCV000017662 - NM_007294.4(BRCA1):c.68_69del (p.Glu23fs)
```

## Interesting Findings

### Specific Entities for Questions
- **82,811 BRCA1 variants** - major cancer susceptibility gene
- **16,458 Type 2 Diabetes variants** - common disease
- **VCV000017662**: Well-studied BRCA1 variant (78 submitters, c.68_69del)
- **VCV000017677**: Another highly studied variant (78 submitters, c.5266dup aka 5382insC)
- **Gene 672**: BRCA1 at chromosomal location 17q21.31
- **3,236,823 SNVs**: 90.2% of all current variants

### Unique Properties
- **Monthly updates**: Last update dates show 2025-05-25 for recent variants
- **Submitter tracking**: Top variants have 78 submitters (extremely well-studied)
- **Clinical significance**: Pathogenic, benign, uncertain, likely pathogenic/benign
- **Record status**: "current" filters active records
- **Blank node structure**: Disease and classification data in graph patterns
- **Variant type distribution**: Heavily skewed toward SNVs (90%+)
- **Historical tracking**: Variants created as early as 2013, continuously updated

### Connections to Other Databases
- **MedGen**: ~95% coverage for standardized disease concepts
- **HGNC**: 100% human genes have official symbols (e.g., HGNC:1100 for BRCA1)
- **OMIM**: ~40% genes linked to Mendelian inheritance
- **MeSH**: ~30% variants with medical subject headings
- **ClinVar Web**: Direct links via rdfs:seeAlso

### Specific Verifiable Facts
- **3,236,823 single nucleotide variants** (SNVs)
- **160,620 deletions**
- **73,448 duplications**
- **82,811 BRCA1 variants** total
- **BRCA1 location**: Chromosome 17q21.31
- **BRCA1 Gene ID**: 672
- **BRCA1 HGNC ID**: HGNC:1100
- **Top variant submissions**: 78 submitters (c.68_69del and c.5266dup)
- **Recent updates**: 2025-05-25 for well-studied variants
- **Earliest variant creation**: 2013 in dataset

## Question Opportunities by Category

### Precision
- "What is the ClinVar accession for BRCA1 variant c.68_69del?" → VCV000017662
- "How many submitters reported variant VCV000017662?" → 78
- "When was variant c.5266dup last updated?" → 2025-05-25
- "What is the cytogenetic location of gene BRCA1?" → 17q21.31
- "What is the HGNC ID for BRCA1?" → HGNC:1100

### Completeness
- "How many BRCA1 variants are in ClinVar?" → 82,811
- "How many single nucleotide variants exist?" → 3,236,823
- "How many deletion variants are recorded?" → 160,620
- "How many duplication variants exist?" → 73,448
- "How many variant types are in ClinVar?" → At least 10 types

### Integration
- "What is the HGNC ID for ClinVar gene 672?" → HGNC:1100
- "Find Gene ID for BRCA1 in ClinVar" → 672
- "What is the full name of gene with symbol BRCA1?" → BRCA1 DNA repair associated
- "Convert VCV accession to variant ID" → Mapping query
- "Link ClinVar variants to chromosomal locations" → Via cytogenetic_location

### Currency
- "When was variant VCV000017662 last updated?" → 2025-05-25
- "How many variants were updated in May 2025?" → Filter by date_last_updated
- "What variants were created in 2025?" → Filter by date_created
- "Find recently updated BRCA1 variants" → 2025-05-25 updates found

### Specificity
- "Find BRCA1 frameshift variants" → Filter by mutation type in label
- "What variants have exactly 78 submitters?" → c.68_69del and c.5266dup
- "Find rare Duplication variants in BRCA1" → Type + gene filter
- "What variants have >50 submitters?" → High-confidence variants
- "Find variants created before 2014" → Early submissions

### Structured Query
- "Find BRCA1 deletions with >10 submitters updated in 2025" → Multiple filters
- "List SNVs in genes on chromosome 17q with >5 submitters" → Type + location + evidence
- "Find frameshift variants with high submitter counts" → Type + quality
- "Search for variants updated after 2024-01-01 with current status" → Date + status
- "Find genes with >1000 variants" → Aggregation query

## Notes

### Limitations
- **Blank node complexity**: Disease and classification data requires complex property paths
- **Incomplete clinical significance**: Would need deeper queries to access classification data
- **Large gene datasets**: BRCA1 with 82K+ variants requires pagination
- **SNV dominance**: 90% of variants are SNVs, other types much smaller
- **Historical data**: Older variants may have fewer submitters

### Best Practices
1. **Use ncbi_esearch** for initial discovery by gene/disease
2. **Use bif:contains** for SPARQL full-text searches on labels
3. **Always include FROM clause**: `FROM <http://rdfportal.org/dataset/clinvar>`
4. **Filter by record_status**: Use "current" to exclude deprecated entries
5. **Use OPTIONAL** for clinical significance and diseases (not all variants have them)
6. **Add submitter filter**: `FILTER(?num_submitters >= 3)` for higher quality variants
7. **Date filtering**: Use cvo:date_created/date_last_updated with proper date format
8. **Add LIMIT clauses**: Essential for large result sets (BRCA1 has 82K+)
9. **ORDER BY DESC(?num_submitters)**: Get most well-studied variants first
10. **Check update dates**: 2025-05-25 shows very recent updates

### Performance Notes
- Simple property queries: <1 second
- bif:contains searches: 1-3 seconds (very efficient)
- Aggregation queries (COUNT by type): Fast (~2 seconds)
- Filtering by submitters + dates: Efficient with indexes
- ncbi_esearch: Fast with good result pagination
- LIMIT essential for genes with >1000 variants
