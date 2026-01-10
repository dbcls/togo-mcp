# BacDive Exploration Report

## Database Overview
- **Purpose**: Standardized bacterial and archaeal strain information metadatabase
- **Scope**: 97,000+ strain records with phenotypic and genotypic characterizations
- **Key Data Types**: 
  - Taxonomy (genus, species, family, order, class, phylum, domain)
  - Morphology (Gram stain, cell motility)
  - Physiology (oxygen tolerance, enzyme activities)
  - Culture conditions (media, temperature, pH)
  - Molecular data (16S rRNA sequences, genomes)
  - Geographic origin and isolation sources
  - Culture collection numbers and references

## Schema Analysis (from MIE file)

### Main Entity Types
1. **schema:Strain** - Central hub entity
   - Full taxonomic hierarchy (domain → phylum → class → order → family → genus → species)
   - BacDive ID and NCBI Taxonomy ID
   - Scientific name and designation
   - Type strain indicator (boolean)
   - Description text

2. **Phenotype Entities** (all link via schema:describesStrain)
   - **schema:Enzyme** - Enzyme activities with positive/negative/variable results, EC numbers
   - **schema:GramStain** - Gram staining results (positive/negative/variable)
   - **schema:CellMotility** - Motility indicator (boolean)
   - **schema:OxygenTolerance** - Aerobic/anaerobic classification

3. **Culture Condition Entities**
   - **schema:CultureMedium** - Medium names with optional MediaDive links
   - **schema:CultureTemperature** - Temperature ranges (start/end in °C)
   - **schema:CulturePH** - pH ranges (start/end)

4. **Molecular Data**
   - **schema:16SSequence** - 16S rRNA sequences with accession numbers, length, database source (ENA/GenBank)
   - **schema:GenomeSequence** - Genome sequences with accession and source

5. **Identifiers and References**
   - **schema:CultureCollectionNumber** - Strain repository numbers (DSMZ, JCM, KCTC, CCUG) with URLs
   - **schema:LocationOfOrigin** - Geographic origin with country, latitude, longitude
   - **schema:Reference** - Literature references with PubMed IDs and DOIs

### Important Relationships
- **Hub-and-spoke architecture**: Strain is central entity, all other data connects via `schema:describesStrain`
- **Multiple inheritance**: Enzyme is also Protein and GeneProduct
- **Optional data**: Use OPTIONAL blocks for phenotypes (~40% coverage)

### Query Patterns Observed
- Use `bif:contains` for keyword search with boolean operators (AND, OR, NOT)
- Must be triple pattern: `?var bif:contains "'keyword'" option (score ?sc)`
- Never use `?score` as variable name (reserved keyword)
- Always use OPTIONAL for phenotypes (incomplete coverage)
- Filter by genus/species using CONTAINS(LCASE(?var), 'text') for efficiency
- FROM clause: `FROM <http://rdfportal.org/dataset/bacdive>`

## Search Queries Performed

1. **Query**: Search for thermophilic strains using bif:contains
   **Results**: Empty results - likely because "thermophilic" appears in descriptions not labels. Need to search dct:description field instead.

2. **Query**: Filter Bacillus genus strains
   **Results**: Found 20 strains including Paenibacillus, Actinobacillus, Bacillus, Solibacillus, Lactobacillus, Marinilactibacillus species. Shows genus filter working correctly.

3. **Query**: Retrieve strains with 16S sequences
   **Results**: Found 20 strains with 16S sequences ranging from 207-1532 bp in length. Accessions from JN/JQ series (NCBI). Coverage includes Nocardia, Mycobacterium, Sphingomonas, Clostridium, etc.

4. **Query**: Positive enzyme activities
   **Results**: Found enzymes including catalase, beta-galactosidase, lysine decarboxylase, ornithine decarboxylase, gelatinase, amylase, DNase, caseinase, oxidase. All with "+" activity.

5. **Query**: E. coli growth conditions
   **Results**: Retrieved culture media (CIP Medium 3, CIP Medium 72), temperature ranges (5-41°C with 30°C optimal), but no pH data in these records. Multiple temperature points per strain.

6. **Query**: DSMZ culture collection numbers
   **Results**: Found 20 DSM strains (DSM 45197, DSM 45095, etc.) all with links to DSMZ catalogue. Strong DSMZ representation as expected.

7. **Query**: Bacillus phenotype profile (Gram stain + motility + oxygen tolerance)
   **Results**: All B. subtilis strains are Gram-positive, mostly motile (isMotile=1), mix of obligate aerobe and facultative anaerobe. B. cereus and B. licheniformis also present.

## SPARQL Queries Tested

```sparql
# Query 1: Filter by genus name
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?strain ?label ?genus ?species
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label ;
          schema:hasGenus ?genus ;
          schema:hasSpecies ?species .
  FILTER(CONTAINS(LCASE(?genus), "bacillus"))
}
LIMIT 20
```
**Results**: Successfully retrieved 20 Bacillus-related strains. Shows CONTAINS(LCASE()) effective for case-insensitive genus filtering.

```sparql
# Query 2: Strains with 16S sequences
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?strain ?strainLabel ?accession ?length
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?strainLabel .
  ?seq a schema:16SSequence ;
       schema:describesStrain ?strain ;
       schema:hasSequenceAccession ?accession ;
       schema:hasSequenceLength ?length .
}
LIMIT 20
```
**Results**: Retrieved 16S sequences with lengths 207-1532 bp, all from JN/JQ accession series. Demonstrates molecular data availability.

```sparql
# Query 3: Positive enzyme activities
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?strainLabel ?enzymeLabel ?activity
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?strainLabel .
  ?enzyme a schema:Enzyme ;
          schema:describesStrain ?strain ;
          rdfs:label ?enzymeLabel ;
          schema:hasActivity ?activity .
  FILTER(?activity = "+")
}
LIMIT 20
```
**Results**: Found diverse positive enzyme activities (catalase, beta-galactosidase, decarboxylases, etc.) across E. coli, Enterococcus, Proteus, Acinetobacter, Haemophilus, Salmonella, Kitasatospora, Bacillus, Aquaspirillum.

```sparql
# Query 4: Complete growth conditions for Escherichia
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?label ?medium ?tempStart ?tempEnd ?phStart ?phEnd
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label ;
          schema:hasGenus ?genus .
  FILTER(CONTAINS(LCASE(?genus), "escherichia"))
  
  OPTIONAL {
    ?m a schema:CultureMedium ;
       schema:describesStrain ?strain ;
       rdfs:label ?medium .
  }
  OPTIONAL {
    ?temp a schema:CultureTemperature ;
          schema:describesStrain ?strain ;
          schema:hasTemperatureRangeStart ?tempStart ;
          schema:hasTemperatureRangeEnd ?tempEnd .
  }
  OPTIONAL {
    ?ph a schema:CulturePH ;
        schema:describesStrain ?strain ;
        schema:hasPHRangeStart ?phStart ;
        schema:hasPHRangeEnd ?phEnd .
  }
}
LIMIT 20
```
**Results**: Retrieved E. coli growth conditions with CIP Media 3 and 72, temperature ranges 5-41°C. pH data absent for these samples. OPTIONAL clauses prevent excluding strains with missing data.

```sparql
# Query 5: DSMZ culture collection links
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?strain ?collectionLabel ?link
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain .
  ?ccn a schema:CultureCollectionNumber ;
       schema:describesStrain ?strain ;
       rdfs:label ?collectionLabel ;
       schema:hasLink ?link .
  FILTER(CONTAINS(?collectionLabel, "DSM"))
}
LIMIT 20
```
**Results**: Retrieved 20 DSM culture collection numbers with working URLs to DSMZ catalogue. All follow pattern DSM-XXXXX.

```sparql
# Query 6: Multi-phenotype profile
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?label ?gramStain ?isMotile ?oxygenTolerance
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label ;
          schema:hasGenus ?genus .
  FILTER(CONTAINS(LCASE(?genus), "bacillus"))
  
  OPTIONAL {
    ?gs a schema:GramStain ;
        schema:describesStrain ?strain ;
        schema:hasGramStain ?gramStain .
  }
  OPTIONAL {
    ?cm a schema:CellMotility ;
        schema:describesStrain ?strain ;
        schema:isMotile ?isMotile .
  }
  OPTIONAL {
    ?ot a schema:OxygenTolerance ;
        schema:describesStrain ?strain ;
        schema:hasOxygenTolerance ?oxygenTolerance .
  }
  FILTER(BOUND(?gramStain) && BOUND(?isMotile))
}
LIMIT 20
```
**Results**: Retrieved complete phenotype profiles for Bacillus strains. All Gram-positive, mostly motile, mix of obligate aerobes and facultative anaerobes. FILTER(BOUND()) ensures complete data.

## Interesting Findings

### Biological/Scientific Content
1. **Enzyme Diversity**: 573,112 enzyme records averaging 5.9 per strain, covering metabolic capabilities
2. **Bacillus subtilis Variation**: Multiple strains with different oxygen tolerances (obligate aerobe vs facultative anaerobe)
3. **16S Sequence Lengths**: Highly variable (207-1532 bp) suggesting partial vs complete sequences
4. **Temperature Ranges**: E. coli can grow 5-41°C with 30°C optimal
5. **Culture Media**: CIP Media series well-represented, suggesting French collection influence

### Taxonomic Coverage
- **97,334 total strains** across bacteria and archaea
- **100% NCBI Taxonomy linkage** enabling standardized classification
- **Type strains**: Indicated via isTypeStrain boolean flag
- **Diverse genera**: Bacillus, Escherichia, Nocardia, Mycobacterium, Sphingomonas, Clostridium, etc.

### Data Completeness Patterns
- **Gram stain**: ~40% of strains
- **16S sequences**: ~35% of strains (87,045 sequences)
- **Enzyme data**: ~55% of strains
- **Culture collections**: ~60% of strains (149,377 numbers)
- **Type strains**: Higher data completeness than non-type strains

### Culture Collection Integration
- **DSMZ dominance**: >90% culture collection coverage
- **JCM**: ~40% coverage (Japanese Collection)
- **KCTC**: ~30% coverage (Korean Collection)
- **All with working URLs** to institutional catalogues

### Molecular Data Availability
- **87,045 16S sequences** from ENA (~60%) and NCBI GenBank (~40%)
- **Genome sequences** available for subset
- **Sequence databases**: Indicated via `fromSequenceDB` property

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
- "What is the DSM culture collection number for Bacillus aryabhattai strain 1290?" (Need to verify from data)
- "What is the 16S rRNA sequence length for Olivibacter ginsenosidimutans strain 159786?" (1445 bp)
- "What is the NCBI Taxonomy ID for Acetobacter aceti?" (435)
- "What is the optimal growth temperature for Escherichia coli strains in BacDive?" (30°C)
- "What is the specific enzyme activity result for gelatinase in Bacillus aryabhattai?" (+)

### Completeness
- "How many bacterial strains are in BacDive?" (97,334)
- "How many enzyme activity records are available?" (573,112)
- "How many strains have 16S rRNA sequences?" (87,045)
- "How many culture collection numbers link to DSMZ?" (>90% of 149,377)
- "What is the average number of enzyme records per strain?" (5.9)
- "How many strains are designated as type strains?" (Need count)

### Integration
- "Convert BacDive strain ID to DSMZ culture collection number"
- "What is the NCBI Taxonomy ID for a strain with DSM number DSM 45197?"
- "Find the 16S rRNA sequence accession for strain with BacDive ID X"
- "Link strain to MediaDive culture medium recipe via hasMediaLink"
- "What PubMed references are associated with specific strains?"

### Currency
- "What is the latest version of BacDive data?" (2024)
- "What are the most recently added strains?" (Need temporal data)
- "Which strains have genome sequences deposited recently?"
- "What new culture media have been linked to strains?"

### Specificity
- "What is the oxygen tolerance classification for Aquaspirillum serpens?" (Need to find)
- "Find rare thermophilic archaea strains with growth temperatures above 70°C"
- "What is the Gram stain result for Marinilactibacillus psychrotolerans?" (Need to check)
- "Which strains from the JCM collection are motile anaerobes?"
- "Find strains from Japan with both 16S sequences and genome data"

### Structured Query
- "Find all Gram-positive, motile, obligate aerobe Bacillus strains"
- "List strains with positive catalase activity AND temperature range 5-41°C"
- "Find type strains from DSMZ collection with complete phenotype data (Gram stain, motility, oxygen tolerance)"
- "Retrieve strains with 16S sequences >1400 bp from genera containing 'coccus'"
- "Find strains that grow in CIP Medium 3 at temperatures >37°C with positive enzyme activities"

## Notes

### Limitations
- **Phenotype incompleteness**: Only ~40% have Gram stain, ~35% have 16S sequences
- **Variable data quality**: Type strains have better coverage than non-type strains
- **bif:contains restrictions**: Must use as triple pattern, not in FILTER; ?score is reserved keyword
- **Empty pH data**: Many culture conditions lack pH ranges
- **16S sequence variability**: Lengths range 207-1532 bp suggesting mix of partial/complete sequences

### Best Practices
1. **Always use OPTIONAL for phenotypes**: Prevents excluding strains with missing data
2. **Use CONTAINS(LCASE())** for genus/species text matching
3. **Never use ?score**: Use ?sc or other variable names
4. **bif:contains syntax**: `?var bif:contains "'keyword'" option (score ?sc)`
5. **Boolean operators**: "'keyword1' AND 'keyword2'", "'keyword1' OR 'keyword2'", "NOT 'keyword'"
6. **FROM clause required**: `FROM <http://rdfportal.org/dataset/bacdive>`
7. **LIMIT always**: Prevent processing entire 97K+ strains
8. **Check BOUND()**: Use FILTER(BOUND(?var)) to require specific data when needed

### Unique Strengths
- **Comprehensive phenotypic data**: Enzyme activities, Gram stain, motility, oxygen tolerance
- **Culture condition details**: Media, temperature, pH ranges for cultivation
- **Strong culture collection links**: Direct URLs to DSMZ, JCM, KCTC, CCUG catalogues
- **Type strain identification**: Boolean flag enables filtering for nomenclature standards
- **Molecular + phenotypic**: Combines 16S/genome sequences with physiological traits
- **Geographic metadata**: Isolation locations with coordinates
- **Hub-and-spoke design**: Clean schema with strain as central entity
- **Full taxonomic hierarchy**: Domain through species level for all strains
