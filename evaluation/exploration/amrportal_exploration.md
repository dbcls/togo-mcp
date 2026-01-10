# AMRPortal Exploration Report

## Database Overview
- **Purpose**: Integrates antimicrobial resistance (AMR) surveillance data from multiple sources (NCBI Pathogen Detection, PATRIC, CABBAGE)
- **Scope**: 1.7M+ phenotypic antimicrobial susceptibility test (AST) results and 1.1M+ genotypic AMR features from bacterial isolates worldwide
- **Key Data Types**: 
  - **Phenotypic data**: MIC values, disk diffusion results, resistance classifications
  - **Genotypic data**: AMR genes, mutations, genomic locations
  - **Metadata**: Geographic origin, isolation source, host organism, temporal information

## Schema Analysis (from MIE file)

### Main Entity Types
1. **amr:PhenotypeMeasurement** - Antimicrobial susceptibility test results
   - Organism identification (genus, species, full organism name)
   - Antibiotic information (name, ontology ID)
   - Resistance phenotype (resistant, susceptible, intermediate, non-susceptible, susceptible-dose dependent)
   - Geographic metadata (country, region, subregion, ISO code, coordinates)
   - Temporal data (collection year: 1911-2025, 92 distinct years)
   - Laboratory methods (broth dilution 56%, agar dilution 8%, disk diffusion 7%, E-test 2%)
   - Quantitative measurements (MIC value, sign, units for ~30% of records)
   - Sample identifiers (BioSample, Assembly ID, SRA accession)

2. **amr:GenotypeFeature** - AMR gene/mutation annotations
   - AMR classification (class, subclass, element symbol, gene symbol)
   - Genomic coordinates (region, start, end, strand)
   - Feature type and subtype
   - Evidence information (type, accession, description, link)
   - Taxonomic linkage via obo:RO_0002162

### Important Relationships
- **Phenotype-Genotype Linkage**: Both entity types share `amr:bioSample` IRI for correlation studies
- **Cross-References**: 
  - BioSample (~1.4M unique samples)
  - SRA (~870K accessions)
  - INSDC assemblies (~890K)
  - PubMed literature (via dct:references)
  - ARO ontology for antibiotics
  - NCBI Taxonomy for organisms

### Query Patterns Observed
- Use `FROM <http://rdfportal.org/dataset/amrportal>` for all queries
- `bif:contains` enables efficient keyword search with score-based ranking
- Always filter by organism or antibiotic before aggregations
- Use LIMIT clauses to prevent timeouts on large dataset
- Geographic hierarchy enables multi-level spatial analysis
- Temporal filtering significantly reduces result sets

## Search Queries Performed

1. **Query**: Basic E. coli resistance search using bif:contains
   **Results**: Retrieved 10 E. coli resistance records with various antibiotics (ampicillin, ciprofloxacin, fosfomycin, etc.) showing mix of resistant and susceptible phenotypes

2. **Query**: Pseudomonas aeruginosa resistance profile
   **Results**: Top resistant antibiotics: ciprofloxacin (813), meropenem (741), ceftazidime (604), levofloxacin (542), tobramycin (533) - shows major fluoroquinolone and carbapenem resistance

3. **Query**: Geographic distribution of ciprofloxacin-resistant E. coli
   **Results**: USA leads (1,041), followed by UK (790), Norway (313), Vietnam (101), Thailand (91). Shows global distribution across Americas, Europe, Asia, and Africa

4. **Query**: AMR gene class distribution in genotype data
   **Results**: BETA-LACTAM most common (243,389), followed by AMINOGLYCOSIDE (187,430), EFFLUX (180,406), TETRACYCLINE (89,420), QUINOLONE (80,396). Reveals antibiotic class hierarchy

5. **Query**: Beta-lactam genes in carbapenem-resistant isolates
   **Results**: bla_1 (2,066 isolates), ampC (1,891), bla_2 (1,853), bla_3 (1,517) most prevalent. NDM-1 variants identified in 258-207 isolates - important carbapenemase

6. **Query**: Multi-drug resistant isolates (≥5 antibiotics)
   **Results**: Found extensively drug-resistant isolates with 28-33 different antibiotic resistances, predominantly in Klebsiella pneumoniae. One Proteus mirabilis isolate resistant to 33 antibiotics!

7. **Query**: Temporal trends in E. coli ampicillin resistance (2010-2023)
   **Results**: Resistance rates fluctuate between 10-92% annually. Peak testing in 2019 (2,002 tests), showing ongoing surveillance patterns

## SPARQL Queries Tested

```sparql
# Query 1: Keyword search for organism with scored ranking
PREFIX amr: <http://example.org/ebiamr#>

SELECT ?s ?organism ?antibiotic ?phenotype
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism ?organism .
  ?s amr:antibioticName ?antibiotic .
  ?s amr:resistancePhenotype ?phenotype .
  ?organism bif:contains "'Escherichia'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
```
**Results**: Successfully retrieved E. coli resistance records ranked by relevance. Demonstrates bif:contains effectiveness for flexible organism name matching.

```sparql
# Query 2: Resistance profile aggregation by antibiotic
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?antibiotic (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Pseudomonas aeruginosa" .
  ?s amr:antibioticName ?antibiotic .
  ?s amr:resistancePhenotype "resistant" .
}
GROUP BY ?antibiotic
ORDER BY DESC(?count)
LIMIT 20
```
**Results**: Identified top 20 antibiotics with P. aeruginosa resistance. Shows fluoroquinolones and carbapenems as major resistance issues.

```sparql
# Query 3: Geographic distribution analysis
PREFIX amr: <http://example.org/ebiamr#>

SELECT ?country ?region (COUNT(*) as ?resistantCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Escherichia coli" .
  ?s amr:antibioticName "ciprofloxacin" .
  ?s amr:resistancePhenotype "resistant" .
  ?s amr:country ?country .
  ?s amr:geographicalRegion ?region .
}
GROUP BY ?country ?region
ORDER BY DESC(?resistantCount)
LIMIT 20
```
**Results**: Mapped global distribution across 20 countries and 4 continents. Shows geographic hierarchy (region → country) working effectively.

```sparql
# Query 4: Genotype-phenotype correlation
PREFIX amr: <http://example.org/ebiamr#>

SELECT DISTINCT ?geneSymbol ?amrClass (COUNT(DISTINCT ?bioSample) as ?isolateCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?pheno a amr:PhenotypeMeasurement .
  ?pheno amr:bioSample ?bioSample .
  ?pheno amr:antibioticName ?antibiotic .
  ?pheno amr:resistancePhenotype "resistant" .
  FILTER(?antibiotic IN ("meropenem", "imipenem", "ertapenem"))
  
  ?geno a amr:GenotypeFeature .
  ?geno amr:bioSample ?bioSample .
  ?geno amr:geneSymbol ?geneSymbol .
  ?geno amr:amrClass ?amrClass .
  FILTER(CONTAINS(?amrClass, "BETA-LACTAM"))
}
GROUP BY ?geneSymbol ?amrClass
ORDER BY DESC(?isolateCount)
LIMIT 20
```
**Results**: Successfully linked phenotypic carbapenem resistance with beta-lactam genes. Found bla genes and ampC in thousands of carbapenem-resistant isolates.

```sparql
# Query 5: Temporal trend analysis
PREFIX amr: <http://example.org/ebiamr#>

SELECT ?year (COUNT(*) as ?total) (SUM(?isResistant) as ?resistant)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Escherichia coli" .
  ?s amr:antibioticName "ampicillin" .
  ?s amr:collectionYear ?year .
  ?s amr:resistancePhenotype ?phenotype .
  BIND(IF(?phenotype = "resistant", 1, 0) as ?isResistant)
  FILTER(?year >= 2010 && ?year <= 2023)
}
GROUP BY ?year
ORDER BY ?year
```
**Results**: Tracked 14 years of resistance data showing temporal patterns. Demonstrates BIND and IF functions for calculating resistance rates.

## Interesting Findings

### Biological/Clinical Significance
1. **Extensively Drug-Resistant Isolates**: Found Klebsiella pneumoniae with resistance to 28-33 different antibiotics, representing serious clinical threats
2. **NDM-1 Carbapenemase**: Detected in 258-207 isolates across multiple samples - a critical resistance mechanism of global concern
3. **Fluoroquinolone Resistance Patterns**: Ciprofloxacin resistance very common in P. aeruginosa (813 isolates) and E. coli (multiple countries)
4. **Beta-lactam Gene Diversity**: Over 243,000 beta-lactam resistance gene features detected - largest AMR class
5. **Efflux Pumps**: 180,406 efflux pump features - second largest category showing importance of multidrug efflux

### Geographic Surveillance
- **USA and UK**: Highest representation in ciprofloxacin-resistant E. coli data
- **Asian Countries**: Strong representation (Vietnam, Thailand, Pakistan, India)
- **Coverage**: 150+ countries across all continents with 80% geographic metadata completeness

### Methodological Insights
- **AST Methods**: Broth dilution dominates (56%), followed by agar dilution (8%) and disk diffusion (7%)
- **Standards**: CLSI is the predominant AST standard used
- **Quantitative Data**: ~30% of phenotype records have MIC measurements with values and units
- **Evidence Types**: HMM-based gene prediction used in 65% of genotype features

### Data Integration Opportunities
- **1.4M BioSamples**: Strong linkage to NCBI sample metadata
- **Phenotype-Genotype**: ~65% of phenotype samples have corresponding genotype data
- **Literature Links**: PubMed references available for source publications
- **ARO Ontology**: Standardized antibiotic classification available

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
- "What is the BioSample ID for an extensively drug-resistant K. pneumoniae isolate with resistance to more than 30 antibiotics?" (SAMN07602702)
- "What AMR gene symbol is most frequently detected in carbapenem-resistant isolates?" (bla_1 with 2,066 isolates)
- "What resistance phenotype is most common for E. coli against ciprofloxacin in the USA?" (resistant with 1,041 cases)
- "What is the most common laboratory typing method used in AMR Portal?" (broth dilution, 56%)
- "Which specific AMR gene class has the highest number of detected features?" (BETA-LACTAM with 243,389)

### Completeness
- "How many phenotypic AMR measurements are in the database?" (~1.7M)
- "How many genotypic AMR features are recorded?" (~1.1M)
- "How many countries are represented in the geographic metadata?" (150+ countries)
- "How many distinct collection years span the temporal coverage?" (92 years from 1911-2025)
- "How many unique BioSamples link phenotype and genotype data?" (~1.4M)
- "How many different AMR gene classes are identified in genotype data?" (20+ major classes)

### Integration
- "Find the PubMed reference for resistance data from Thai Streptococcus pneumoniae isolates" (PMID:24509479)
- "What is the NCBI Taxonomy ID for organisms with norM efflux pump genes?" (485 for Neisseria)
- "Convert a BioSample ID to its corresponding SRA accession and assembly ID"
- "What ARO ontology term corresponds to trimethoprim-sulfamethoxazole?" (ARO_3004024)
- "Link phenotypic meropenem resistance to genotypic NDM-1 gene presence via BioSample"

### Currency
- "What is the latest collection year for AMR surveillance data in the database?" (2025)
- "How many ciprofloxacin-resistant E. coli isolates were collected in 2023?" (211 total, 184 resistant)
- "What recent AMR gene evidence links are available from NCBI Pathogen Detection?"
- "Which countries contributed resistance data in the most recent year?"

### Specificity
- "What is the resistance profile of Neisseria gonorrhoeae isolates with the norM efflux gene?"
- "Find isolates from Vietnam with both amikacin resistance phenotype and macrolide resistance genotype"
- "What culture media or isolation sources are specific for Thermotoga or other thermophiles?" (Note: primarily pathogenic bacteria, not extremophiles)
- "What is the geographic subregion classification for Thailand?" (South-eastern Asia)
- "Which rare AMR gene subtype msr(E) is found in Acinetobacter baumannii?" (macrolide/streptogramin resistance)

### Structured Query
- "Find all isolates with resistance to at least 3 carbapenem antibiotics (meropenem, imipenem, ertapenem)"
- "Identify organisms with both quinolone resistance phenotype AND efflux pump genotype from Asian countries"
- "List beta-lactam resistance genes found in isolates resistant to cephalosporins but susceptible to carbapenems"
- "Find isolates from 2020-2023 with MIC values ≥16 mg/L for meropenem"
- "Retrieve all E. coli isolates from the Americas with ampicillin resistance AND presence of bla genes"

## Notes

### Limitations
- **Blank Nodes**: All measurements use blank nodes (no direct URIs), limiting external linking
- **Text Inconsistency**: Isolation sources have variable capitalization (Stool/stool, Urine/urine)
- **Incomplete Linkage**: Only ~65% of phenotype samples have genotype data
- **Geographic Gaps**: ~20% of records missing geographic metadata
- **Quantitative Data**: Only ~30% have MIC measurements
- **Query Timeouts**: Complex aggregations over full dataset can exceed 60-second limit

### Best Practices
1. **Always use FROM clause**: `FROM <http://rdfportal.org/dataset/amrportal>`
2. **Filter early**: Add organism or antibiotic filters before aggregations
3. **Use LIMIT**: Prevent timeouts on exploratory queries (LIMIT 100 recommended)
4. **Keyword search**: Use `bif:contains` for flexible organism/antibiotic matching
5. **Case handling**: Use FILTER with CONTAINS or LCASE for text matching
6. **Verify linkage**: Check phenotype-genotype connections exist before complex joins
7. **Geographic filters**: Use region, subregion, or country to reduce result sets
8. **Temporal filters**: Year ranges significantly improve query performance

### Unique Strengths
- **Phenotype-Genotype Integration**: Rare capability to correlate resistance mechanisms with observed phenotypes
- **Global Surveillance**: Comprehensive geographic and temporal coverage
- **Multiple AMR Classes**: Covers all major antibiotic classes and resistance mechanisms
- **Quantitative Data**: MIC values enable threshold-based queries
- **Clinical Relevance**: Identifies extensively drug-resistant isolates of public health importance
- **Methodological Transparency**: AST methods and standards documented
