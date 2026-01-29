# AMR Portal Exploration Report

## Database Overview
AMR Portal integrates antimicrobial resistance surveillance data from NCBI Pathogen Detection, PATRIC, and CABBAGE. Contains 1.7M phenotypic resistance test results and 1.1M genotypic AMR features from bacterial isolates worldwide.

## Schema Analysis
**Main entity types:**
- `PhenotypeMeasurement`: Resistance test results with MIC values and disk diffusion
- `GenotypeFeature`: AMR genes, mutations, and resistance elements

**Key properties:**
- Phenotype: organism, antibioticName, resistancePhenotype, bioSample, collectionYear, country, laboratoryTypingMethod
- Genotype: amrClass, geneSymbol, bioSample, elementType, regionStart/End, evidenceType

**Important patterns:**
- BioSample IRI links phenotype and genotype data from same isolate
- Geographic hierarchy: region → subregion → country → ISO code
- Temporal coverage: 1911-2025 with 92 distinct collection years
- Resistance phenotypes: resistant, susceptible, intermediate, non-susceptible

## Search Queries Performed
N/A - AMR Portal uses SPARQL keyword search via `bif:contains`

## SPARQL Queries Tested

```sparql
# Query 1: Top organisms with resistant measurements
SELECT ?organism (COUNT(*) as ?resistantCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism ?organism .
  ?s amr:resistancePhenotype "resistant" .
}
GROUP BY ?organism
ORDER BY DESC(?resistantCount)
LIMIT 10
# Results: M. tuberculosis (62,371), K. pneumoniae (54,237), E. coli (46,158)
```

```sparql
# Query 2: Antibiotics with resistance in K. pneumoniae
SELECT ?antibiotic (COUNT(*) as ?resistanceCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Klebsiella pneumoniae" .
  ?s amr:antibioticName ?antibiotic .
  ?s amr:resistancePhenotype "resistant" .
}
GROUP BY ?antibiotic
ORDER BY DESC(?resistanceCount)
LIMIT 10
# Results: ampicillin (3,897), ceftazidime (3,398), ciprofloxacin (3,098)
```

```sparql
# Query 3: AMR gene classes distribution
SELECT ?amrClass (COUNT(*) as ?featureCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:GenotypeFeature .
  ?s amr:amrClass ?amrClass .
}
GROUP BY ?amrClass
ORDER BY DESC(?featureCount)
LIMIT 15
# Results: BETA-LACTAM (243,389), AMINOGLYCOSIDE (187,430), EFFLUX (180,406)
```

```sparql
# Query 4: Geographic distribution of measurements
SELECT ?region (COUNT(*) as ?measurements)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:geographicalRegion ?region .
}
GROUP BY ?region
# Results: Americas (790,139), Europe (249,017), Asia (245,560)
```

```sparql
# Query 5: Beta-lactam resistance genes
SELECT ?geneSymbol (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:GenotypeFeature .
  ?s amr:geneSymbol ?geneSymbol .
  ?s amr:amrClass "BETA-LACTAM" .
}
GROUP BY ?geneSymbol
ORDER BY DESC(?count)
LIMIT 10
# Results: penA (22,039), blaC (20,858), bla_1 (19,467)
```

## Cross-Reference Analysis

**Entity counts** (from MIE documentation):
- BioSample: ~1.4M unique samples linked
- SRA: ~870K SRA accessions
- INSDC/GenBank: ~890K assembly identifiers
- NCBI Taxonomy: All genotype features linked via obo:RO_0002162

**Integration patterns:**
- Phenotype-genotype linkage via bioSample IRI
- ChEMBL integration via antibiotic name matching (requires LCASE normalization)
- PubMed citations via dct:references
- ARO ontology for antibiotic classification

## Interesting Findings

**Resistance prevalence:**
- Mycobacterium tuberculosis has most resistance measurements (62,371)
- Top resistance mechanisms: BETA-LACTAM (243K features), AMINOGLYCOSIDE (187K), EFFLUX (180K)
- Americas region has 46% of all phenotype measurements

**Genotype-phenotype linkage:**
- ~65% of phenotype samples have genotype data
- ~35% of genotype features have antibiotic names
- BioSample serves as primary linkage key

**Laboratory methods:**
- Broth dilution: 56% of tests
- Agar dilution: 8%
- Disk diffusion: 7%

**Geographic coverage:**
- 150+ countries across all continents
- Geographic hierarchy enables multi-level spatial analysis

**Query performance notes:**
- Queries filtering on single antibiotic complete in <5 seconds
- Organism + phenotype combined filtering causes timeout (requires two-stage approach)
- Cross-database queries require reverse join order (ChEMBL → AMR) or two-stage aggregation

## Question Opportunities by Category

### Precision (Specific measurements for real organisms/antibiotics)
- ✅ "How many resistance measurements exist for Mycobacterium tuberculosis?"
- ✅ "How many K. pneumoniae isolates are resistant to ciprofloxacin?"
- ✅ "What is the most common beta-lactam resistance gene?"

### Completeness (Entity counts, comprehensive analysis)
- ✅ "How many phenotype measurements are from the Americas region?"
- ✅ "How many genotype features have beta-lactam resistance class?"
- ✅ "How many organisms have >10,000 resistance measurements?"

### Integration (Cross-database linking)
- ✅ "Link ciprofloxacin resistance data to ChEMBL compound properties" (requires two-stage query)
- ✅ "Find isolates with both phenotype and genotype data for same bioSample"
- ✅ "Which NCBI Taxonomy IDs have >1000 genotype features?"

### Currency (Temporal patterns)
- ✅ "How many resistance measurements were collected in 2020?"
- ✅ "What is the temporal trend of ciprofloxacin resistance?"

### Specificity (Rare resistance, niche mechanisms)
- ✅ "How many isolates have glycopeptide resistance genes?"
- ✅ "Find measurements from African countries with <100 samples"
- ✅ "Which organisms have fosfomycin resistance?"

### Structured Query (Complex filtering, multiple criteria)
- ✅ "Find K. pneumoniae isolates resistant to both ceftazidime and ciprofloxacin"
- ✅ "Count efflux pump genes in Neisseria gonorrhoeae"
- ✅ "Find beta-lactam genes with evidence type 'HMM'"

### Performance-aware questions
- ✅ "Which 5 organisms have the most resistance measurements?" (simple aggregation)
- ⚠️ "Find all biosamples with both phenotype and genotype data" (requires careful query design)

## Notes

**Query optimization critical:**
- Two-stage aggregation pattern required for cross-database analytics
- Reverse join order (small → large) for cross-database queries
- LIMIT clauses essential for exploratory queries
- SAMPLE() aggregate for representative data

**Data quality considerations:**
- Inconsistent capitalization in isolation sources
- Geographic hierarchy incomplete for some records
- Not all genotype features have antibiotic names (~35%)

**Performance characteristics:**
- 1.7M phenotype + 1.1M genotype records = large dataset
- Single antibiotic filters work well
- Combined organism + phenotype filtering causes timeout
