# AMR Portal Exploration Report

## Database Overview
- **Purpose**: Antimicrobial resistance (AMR) surveillance data integration from NCBI Pathogen Detection, PATRIC, and CABBAGE
- **Scope**: 1.7M+ phenotypic antimicrobial susceptibility test (AST) results and 1.1M+ genotypic AMR features from bacterial isolates worldwide
- **Key data types**: 
  - PhenotypeMeasurement: Antibiotic susceptibility testing results with MIC values, disk diffusion
  - GenotypeFeature: AMR genes, mutations with genomic coordinates
  - Geographic, temporal, and epidemiological metadata

## Schema Analysis (from MIE file)

### Main Properties Available

**PhenotypeMeasurement:**
- Organism identification: organism, species, genus
- Antibiotic testing: antibioticName, antibioticOntologyId (ARO links), resistancePhenotype
- Quantitative measurements: measurementValue, measurementSign, measurementUnits
- Sample metadata: bioSample, assemblyId, sraAccession
- Geographic data: country, geographicalRegion, geographicalSubregion, isoCountryCode
- Temporal data: collectionYear (1911-2025)
- Clinical metadata: isolateId, isolationSource, isolationCategory, host
- Methods: laboratoryTypingMethod, astStandard, platform
- References: dct:references (PubMed links)

**GenotypeFeature:**
- AMR classification: amrClass, amrSubclass, amrElementSymbol, geneSymbol
- Genomic location: region, regionStart, regionEnd, strand
- Element types: elementType, elementSubtype
- Evidence: evidenceType (HMM), evidenceAccession, evidenceDescription, evidenceLink
- Taxonomy: obo:RO_0002162 (in taxon) links to NCBI Taxonomy
- Sample linkage: bioSample (connects to phenotype data)

### Important Relationships
- **Phenotype-Genotype linkage**: via shared bioSample IRI enables correlation studies
- **Geographic hierarchy**: region → subregion → country → ISO code for spatial analysis
- **Cross-database references**: BioSample, SRA, INSDC assemblies, PubMed, ARO ontology, NCBI Taxonomy
- **Temporal tracking**: collectionYear for trend analysis (92 distinct years, 1911-2025)

### Query Patterns Observed
1. **Keyword search**: Use `bif:contains` for flexible organism/text matching with scoring
2. **Filtering**: Always specify organism or antibiotic before aggregations to avoid timeouts
3. **Geographic analysis**: Multi-level spatial filtering (region/country/ISO)
4. **Temporal trends**: Year-based resistance tracking with conditional aggregation
5. **Genotype-phenotype correlation**: JOIN on bioSample for same isolate analysis
6. **Multi-drug resistance**: GROUP BY with HAVING for complex resistance profiling

## Search Queries Performed

### Query 1: E. coli resistance patterns
**Query**: Keyword search for Escherichia coli phenotype data
**Results**: Found diverse resistance/susceptibility patterns - ampicillin (resistant), ciprofloxacin (resistant), nitrofurantoin (susceptible), etc. Demonstrates comprehensive AST data.

### Query 2: P. aeruginosa resistance by antibiotic
**Query**: Count resistant phenotypes by antibiotic for Pseudomonas aeruginosa
**Results**: Top resistances - ciprofloxacin (813), meropenem (741), ceftazidime (604), levofloxacin (542). Shows prevalence of quinolone and carbapenem resistance.

### Query 3: Geographic distribution of ciprofloxacin-resistant E. coli
**Query**: Country-level analysis of ciprofloxacin resistance in E. coli
**Results**: USA leads (1,041), UK (790), Norway (313), Vietnam (101), Thailand (91). Demonstrates global surveillance capability.

### Query 4: AMR gene class distribution
**Query**: Count genotype features by AMR class
**Results**: BETA-LACTAM (243,389), AMINOGLYCOSIDE (187,430), EFFLUX (180,406), TETRACYCLINE (89,420). Shows major resistance mechanism categories.

### Query 5: Temporal trend of ampicillin resistance in E. coli
**Query**: Year-by-year resistance tracking (2010-2023)
**Results**: Variable resistance rates - 2010: 134/206 (65%), 2019: 567/2002 (28%), 2023: 184/211 (87%). Demonstrates temporal trend analysis capability.

### Query 6: Carbapenem resistance genotype-phenotype linkage
**Query**: Beta-lactam genes in carbapenem-resistant isolates
**Results**: bla_1 (2,066 isolates), ampC (1,891), blaNDM-1 variants (258+207+204). Shows successful phenotype-genotype correlation.

### Query 7: Multi-drug resistant isolates
**Query**: Isolates resistant to 5+ antibiotics
**Results**: Found extreme MDR - Proteus mirabilis (33 drugs), K. pneumoniae (32 drugs), E. coli (30 drugs). Highlights public health concern.

### Query 8: Quantitative MIC measurements
**Query**: MIC values for Klebsiella pneumoniae
**Results**: Found measurements like ceftriaxone >32 mg/L, gentamicin >8 mg/L, imipenem ≤1 mg/L. About 30% of phenotypes have quantitative data.

### Query 9: Isolation sources
**Query**: Count phenotypes by isolation source
**Results**: Stool (189,939), urine (123,939), blood (81,333), sputum (55,428). Note: inconsistent capitalization (Stool/stool, Blood/blood).

### Query 10: N. gonorrhoeae AMR genes
**Query**: Genotype features for Neisseria gonorrhoeae
**Results**: mdtK efflux pumps (multiple), tet(M) tetracycline resistance, bla beta-lactamase. All with HMM evidence and descriptions.

## SPARQL Queries Tested

```sparql
# Query 1: Laboratory typing methods distribution
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?laboratoryTypingMethod (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:laboratoryTypingMethod ?laboratoryTypingMethod .
}
GROUP BY ?laboratoryTypingMethod
ORDER BY DESC(?count)
LIMIT 20
```
**Results**: Broth dilution (959,895 - 76%), agar dilution (142,476 - 11%), disk diffusion (120,901 - 10%), E-test (33,937 - 3%). Shows method distribution.

```sparql
# Query 2: Organism distribution in phenotype data
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?organism (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism ?organism .
}
GROUP BY ?organism
ORDER BY DESC(?count)
LIMIT 30
```
**Results**: Top organisms - Salmonella enterica (443,249), E. coli (364,276), M. tuberculosis (331,449), K. pneumoniae (133,136), N. gonorrhoeae (95,195). 20+ bacterial species represented.

```sparql
# Query 3: PubMed citations by frequency
PREFIX amr: <http://example.org/ebiamr#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT DISTINCT ?pubmed (COUNT(*) as ?citationCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s dct:references ?pubmed .
}
GROUP BY ?pubmed
ORDER BY DESC(?citationCount)
LIMIT 10
```
**Results**: Top cited - PMID:35944069 (157,331 citations), PMID:38052776 (108,358), PMID:35780211 (99,144). Shows data provenance.

```sparql
# Query 4: Antibiotic Resistance Ontology (ARO) linkage
PREFIX amr: <http://example.org/ebiamr#>

SELECT ?s ?antibioticName ?antibioticOntologyId
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:antibioticName ?antibioticName .
  ?s amr:antibioticOntologyId ?antibioticOntologyId .
}
LIMIT 20
```
**Results**: ARO terms like ARO_3004024 (trimethoprim-sulfamethoxazole), ARO_0000062 (ceftriaxone), ARO_0000051 (tetracycline). Standardized antibiotic classification.

```sparql
# Query 5: Host organisms
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?host (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:host ?host .
}
GROUP BY ?host
ORDER BY DESC(?count)
```
**Results**: Homo sapiens (828,750 - 73%), "other (non-clinical isolate)" (309,699 - 27%). Mix of clinical and environmental/food isolates.

```sparql
# Query 6: S. aureus beta-lactam resistance genes
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?geneSymbol (COUNT(DISTINCT ?bioSample) as ?isolateCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:GenotypeFeature .
  ?s amr:organism "Staphylococcus aureus" .
  ?s amr:geneSymbol ?geneSymbol .
  ?s amr:amrClass "BETA-LACTAM" .
  ?s amr:bioSample ?bioSample .
}
GROUP BY ?geneSymbol
ORDER BY DESC(?isolateCount)
LIMIT 15
```
**Results**: blaI (3,755), blaZ (3,741), mecR1 (2,436), mecA variants (2,006+1,642+1,014). Shows MRSA-relevant genes including mecA.

```sparql
# Query 7: M. tuberculosis drug resistance
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?antibiotic (COUNT(*) as ?resistantCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Mycobacterium tuberculosis" .
  ?s amr:antibioticName ?antibiotic .
  ?s amr:resistancePhenotype "resistant" .
}
GROUP BY ?antibiotic
ORDER BY DESC(?resistantCount)
LIMIT 15
```
**Results**: Isoniazid (14,770), rifampin (12,616), ethambutol (5,990). MDR-TB and XDR-TB relevant. Fluoroquinolones (moxifloxacin: 3,203, levofloxacin: 3,063) indicating second-line resistance.

## Interesting Findings

### Specific Entities for Good Questions

1. **Extreme MDR isolates**: SAMN07602702 (Proteus mirabilis - 33 drugs), SAMN07602916 (K. pneumoniae - 32 drugs)
2. **Specific resistance genes**: blaNDM-1 (New Delhi metallo-beta-lactamase), mecA (methicillin resistance), tet(M) (tetracycline)
3. **Geographic hotspots**: USA (1,041 ciprofloxacin-resistant E. coli), UK (790), Norway (313)
4. **Temporal patterns**: Ampicillin resistance in E. coli varying 28%-87% across years
5. **Organism-specific**: M. tuberculosis (331,449 AST results), S. enterica (443,249 - largest dataset)

### Unique Properties

- **Quantitative MIC data**: ~30% of phenotypes have measurementValue/Sign/Units (e.g., ">32 mg/L", "≤1 mg/L")
- **Evidence annotations**: 65% of genotypes have HMM evidence with detailed descriptions
- **Geographic hierarchy**: Four-level classification (region/subregion/country/ISO) for 150+ countries
- **Laboratory methods**: Four distinct AST methods with method-specific distribution
- **Database provenance**: "database" field tracks source (PATRIC, CABBAGE_PubMed_data, NCBI)

### Connections to Other Databases

- **BioSample**: ~1.4M unique samples linking phenotype-genotype data
- **SRA**: ~870K sequence read archive accessions for raw data
- **INSDC/GenBank**: ~890K assembly identifiers (GCA/ERZ accessions)
- **PubMed**: Multiple publications per study (top: 157K citations)
- **ARO**: Antibiotic Resistance Ontology terms for standardized antibiotic classification
- **NCBI Taxonomy**: obo:RO_0002162 links for all genotype features

### Specific, Verifiable Facts

1. **Beta-lactam genes dominate**: 243,389 features (21% of all genotypes)
2. **Geographic coverage**: 150+ countries, all continents represented
3. **Temporal span**: 92 distinct years (1911-2025), concentrated post-2000
4. **Resistance distribution**: 18% resistant, 61% susceptible, 2% intermediate
5. **Clinical vs environmental**: 73% human isolates, 27% non-clinical
6. **Top isolation source**: Stool (189,939 - 17% of all phenotypes)
7. **Largest organism dataset**: Salmonella enterica (443,249 AST results)

## Question Opportunities by Category

### Precision
- "What is the BioSample ID for the Proteus mirabilis isolate resistant to 33 antibiotics?"
- "What is the exact MIC value for meropenem resistance in BioSample SAMN18874760?"
- "What is the ARO ontology ID for ciprofloxacin?"
- "What gene symbol represents New Delhi metallo-beta-lactamase in the AMR Portal?"

### Completeness
- "How many phenotypic measurements are available for Mycobacterium tuberculosis in AMR Portal?"
- "How many beta-lactam resistance genes are detected across all isolates?"
- "List all AMR gene classes present in Neisseria gonorrhoeae genomes"
- "How many countries have reported ciprofloxacin-resistant E. coli?"

### Integration
- "What PubMed IDs are cited most frequently in AMR Portal phenotype data?"
- "Link BioSample SAMEA1569508 phenotype data with its genotype features"
- "What ARO ontology terms are used for beta-lactam antibiotics?"
- "Find SRA accessions for isolates with both meropenem resistance phenotype and blaNDM-1 genotype"

### Currency
- "What is the most recent collection year for Klebsiella pneumoniae isolates in AMR Portal?"
- "How has ciprofloxacin resistance in Pseudomonas aeruginosa changed from 2010 to 2023?"
- "What newly identified MDR isolates are in the most recent data updates?"

### Specificity
- "What percentage of Campylobacter jejuni isolates carry the tet(O) resistance gene?"
- "What isolation sources are specific to food-borne Salmonella surveillance?"
- "Which geographic subregions in Asia have the highest carbapenem resistance rates?"
- "What evidence type is used for AMR gene prediction in genotype data?" (Answer: HMM - 65%)

### Structured Query
- "Find all E. coli isolates from Southeast Asia resistant to both ciprofloxacin and ceftriaxone collected after 2020"
- "Identify isolates with blaNDM-1 gene AND meropenem resistance phenotype from the same BioSample"
- "Search for multi-drug resistant Klebsiella pneumoniae (5+ drugs) with beta-lactam genes from Europe"
- "Find Staphylococcus aureus isolates with mecA gene collected from blood with MIC >32 mg/L for any beta-lactam"

## Notes

### Limitations and Challenges

1. **Performance**: Large dataset requires careful query design
   - MUST use LIMIT clauses (timeout at 60 seconds)
   - MUST filter by organism or antibiotic before aggregations
   - Geographic/temporal filters significantly improve performance

2. **Data quality issues**:
   - Inconsistent capitalization (Stool/stool, Blood/blood, Urine/urine)
   - Geographic hierarchy incomplete for some records (~20% missing)
   - Not all bioSamples have both phenotype AND genotype (~65% linkage)
   - MIC quantitative data only ~30% of phenotypes

3. **Schema considerations**:
   - Blank nodes only (no direct URIs for records)
   - BioSample IRI is primary linkage key
   - Antibiotic names are free text (use ARO links for standardization)

### Best Practices for Querying

1. **Always specify FROM clause**: `FROM <http://rdfportal.org/dataset/amrportal>`
2. **Use bif:contains for text search**: Handles variations, case differences, scores results
3. **Filter before aggregating**: Organism + antibiotic filters prevent timeouts
4. **Use LIMIT liberally**: Start with LIMIT 10-100 for exploration
5. **Check coverage first**: Verify data exists before complex queries (use COUNT)
6. **Phenotype-genotype joins**: Filter to specific bioSamples for targeted analysis
7. **Geographic queries**: Multi-level filtering (region → country) for spatial analysis
8. **Temporal queries**: Add year range filters (FILTER(?year >= X && ?year <= Y))

### Key Anti-patterns to Avoid

❌ **Don't query without organism filter**:
```sparql
SELECT ?antibiotic (COUNT(*) as ?count)
WHERE { ?s amr:antibioticName ?antibiotic . }
GROUP BY ?antibiotic
```

✅ **Do filter by organism**:
```sparql
SELECT ?antibiotic (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE { 
  ?s amr:organism "Escherichia coli" .
  ?s amr:antibioticName ?antibiotic .
}
GROUP BY ?antibiotic
LIMIT 50
```

❌ **Don't use exact string matching**:
```sparql
WHERE { ?s amr:organism "E. coli" . }
```

✅ **Do use keyword search**:
```sparql
WHERE { 
  ?s amr:organism ?organism .
  ?organism bif:contains "'coli'" option (score ?sc) .
}
ORDER BY DESC(?sc)
```

### Data Statistics Summary

- **Total records**: 1.7M phenotypes + 1.1M genotypes
- **Unique samples**: ~1.4M BioSamples
- **Organisms**: 20+ bacterial species (largest: Salmonella 443K)
- **Countries**: 150+ across all continents
- **Years**: 92 (1911-2025), concentrated post-2000
- **Resistance rate**: 18% resistant, 61% susceptible, 2% intermediate
- **Clinical vs non-clinical**: 73% human, 27% environmental/food
- **Methods**: Broth dilution (76%), agar dilution (11%), disk diffusion (10%), E-test (3%)
- **Phenotype-genotype linkage**: ~65% of samples have both
- **Quantitative MIC data**: ~30% of phenotypes
- **Evidence annotations**: 65% of genotypes with HMM evidence
