# MediaDive Exploration Report

## Database Overview
MediaDive is a comprehensive culture media database from DSMZ containing 3,289 standardized recipes for cultivating bacteria, archaea, fungi, yeast, microalgae, and phages. It provides detailed hierarchical recipe structures (medium → solution → solution_recipe → ingredient) with 1,489 ingredients, growth conditions for 45,685 strain records, and extensive chemical cross-references enabling metabolic and chemical database integration.

Key data types:
- **Culture Media**: Complete recipes with pH, complexity classification, ingredient compositions
- **Ingredients**: Chemical components with formulas, CAS numbers, ChEBI/PubChem/KEGG identifiers
- **Growth Conditions**: Temperature, pH, oxygen requirements linked to specific strains and media
- **Strain Records**: Microbial organisms with BacDive links (73% coverage), species names, DSM numbers

## Schema Analysis (from MIE file)

**Main Properties:**
- `schema:CultureMedium`: Media with labels, groups, pH ranges (hasFinalPH, hasMinPH, hasMaxPH), complexity flags
- `schema:Ingredient`: Components with formulas, CAS, ChEBI, PubChem, KEGG, GMO identifiers
- `schema:MediumComposition`: Links media to ingredients with gramsPerLiter concentrations
- `schema:GrowthCondition`: Cultivation parameters (temperature, pH, oxygen) for strain-medium pairs
- `schema:Strain`: Organisms with DSM numbers, BacDive IDs, species names, taxonomic groups

**Important Relationships:**
- `schema:partOfMedium`: Connects compositions and growth conditions to media
- `schema:containsIngredient`: Links compositions to specific ingredients
- `schema:relatedToStrain`: Associates growth conditions with strains
- `schema:hasBacDiveID`: Cross-references to BacDive phenotypic database (73% coverage, 33,226 strains)

**Query Patterns:**
- Keyword search via `bif:contains` for media labels, groups, species
- Numeric filtering on pH (hasMinPH/hasMaxPH) and temperature (growthTemperature)
- Hierarchical navigation: medium → composition → ingredient
- Cross-database joining via BacDiveID to BacDive strain phenotypes
- Chemical database integration via hasChEBI, hasPubChem, hasKEGG, hasCAS properties

## Search Queries Performed

1. **Query: LB medium variants** → Found 10 LB (Luria-Bertani) medium variants including standard LB, anaerobic alkaline LB, LB with antibiotics, LB agar with various supplements. Medium 381 is the main LB medium with 769 composition entries.

2. **Query: Glucose ingredient** → Found D-Glucose (ingredient/211) and Glucose (ingredient/5) with molecular formula C6H12O6, CAS 50-99-7, ChEBI IDs (17634, 17234), PubChem 5793. Demonstrates multi-database chemical cross-referencing.

3. **Query: Hyperthermophilic growth conditions (>60°C)** → Found extreme thermophiles including Pyrolobus fumarii (103°C), Pyrococcus kukulkanii (100°C), Hyperthermus butylicus (99°C), Pyrodictium abyssi (98°C), Methanopyrus kandleri (98°C). All are anaerobic with specialized media.

4. **Query: Marine media** → Found 5 marine-specific media with pH ranges 6.8-8.5, including Methanosarcina marine medium (non-complex), yeast extract-starch agar with 50% marine water (complex), marine medium with pyruvate, Bacto marine broth with Na-acetate, Acetobacterium marine medium.

5. **Query: BacDive cross-references** → Confirmed 33,226 unique strains with 33,177 distinct BacDiveIDs, representing 73% coverage of MediaDive strain records and ~34% of BacDive's 97,334 strains.

6. **Query: LB medium composition** → Retrieved detailed ingredient list for medium 381 (LB) showing NaCl (100 g/L in one variant, 30 g/L in others), Agar (20 g/L for solid media), and other components with precise concentrations.

## SPARQL Queries Tested

```sparql
# Query 1: Count media with specific keywords - adapted for "thermophile" media
SELECT ?medium ?label (COUNT(?composition) as ?ingredientCount)
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?medium a schema:CultureMedium ;
          rdfs:label ?label .
  ?label bif:contains "'thermophil'" .
  OPTIONAL { 
    ?composition schema:partOfMedium ?medium .
  }
}
GROUP BY ?medium ?label
LIMIT 10
# Results: Found 3 thermophile-specific media including Pyrolobus fumarii medium, Pyrococcus medium, Methanopyrus medium
```

```sparql
# Query 2: Ingredient chemical cross-references - adapted for "tryptone"
SELECT ?ingredient ?label ?formula ?cas ?chebi ?pubchem ?kegg
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?ingredient a schema:Ingredient ;
              rdfs:label ?label .
  ?label bif:contains "'tryptone'" .
  OPTIONAL { ?ingredient schema:hasFormula ?formula }
  OPTIONAL { ?ingredient schema:hasCAS ?cas }
  OPTIONAL { ?ingredient schema:hasChEBI ?chebi }
  OPTIONAL { ?ingredient schema:hasPubChem ?pubchem }
  OPTIONAL { ?ingredient schema:hasKEGG ?kegg }
}
# Results: Found tryptone ingredients with CAS numbers but limited ChEBI/PubChem coverage (demonstrates partial chemical mapping)
```

```sparql
# Query 3: Growth temperature extremes - adapted for psychrophiles (<15°C)
SELECT ?growth ?strain ?species ?medium ?mediumLabel ?temp ?ph ?oxygen
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?growth a schema:GrowthCondition ;
          schema:relatedToStrain ?strain ;
          schema:partOfMedium ?medium ;
          schema:growthTemperature ?temp .
  ?strain schema:hasSpecies ?species .
  ?medium rdfs:label ?mediumLabel .
  OPTIONAL { ?growth schema:growthPH ?ph }
  OPTIONAL { ?growth schema:hasOxygenRequirement ?oxygen }
  FILTER(?temp < 15)
}
ORDER BY ?temp
LIMIT 10
# Results: Found psychrophilic bacteria growing at 4-12°C including Polaromonas, Psychrobacter, Colwellia species with specialized cold-adapted media
```

```sparql
# Query 4: Media pH range filtering - adapted for alkaline media
SELECT ?medium ?label ?finalPH ?minPH ?maxPH ?isComplex
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?medium a schema:CultureMedium ;
          rdfs:label ?label ;
          schema:hasFinalPH ?finalPH ;
          schema:isComplex ?isComplex .
  OPTIONAL { ?medium schema:hasMinPH ?minPH }
  OPTIONAL { ?medium schema:hasMaxPH ?maxPH }
  FILTER(?minPH > 8.5)
}
# Results: Found alkaline media with pH >8.5 including alkaliphile media for Bacillus, Natronomonas species
```

```sparql
# Query 5: Detailed medium composition - adapted for marine medium 1303
SELECT ?composition ?medium ?mediumLabel ?ingredient ?ingredientLabel ?gPerL ?isOptional
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?composition a schema:MediumComposition ;
               schema:partOfMedium ?medium ;
               schema:containsIngredient ?ingredient ;
               schema:gramsPerLiter ?gPerL .
  ?medium rdfs:label ?mediumLabel .
  ?ingredient rdfs:label ?ingredientLabel .
  OPTIONAL { ?composition schema:isOptionalIngredient ?isOptional }
  FILTER(?medium = <https://purl.dsmz.de/mediadive/medium/1303>)
}
ORDER BY DESC(?gPerL)
# Results: Retrieved complete ingredient list for marine medium with pyruvate showing NaCl (27.5 g/L), MgSO4, CaCl2, pyruvate concentrations
```

## Cross-Reference Analysis

**Entity counts** (unique entities with mappings):

MediaDive Ingredients → Chemical Databases:
- 611 ingredients (41%) have GMO identifiers (metabolic context)
- 581 ingredients (39%) have CAS Registry numbers (chemical identification)
- 476 ingredients (32%) have ChEBI identifiers (biological chemistry)
- 268 ingredients (18%) have PubChem identifiers
- 194 ingredients (13%) have KEGG identifiers
- 104 ingredients (7%) have MetaCyc identifiers

MediaDive Strains → BacDive:
- 33,226 strains (73% of MediaDive) have BacDive IDs
- Represents ~34% of BacDive's 97,334 strains with phenotypic data

**Relationship counts** (total mappings):

Ingredient cross-references:
- 611 GMO mappings (1:1)
- 581 CAS mappings (1:1)
- 476 ChEBI mappings (1:1)
- 268 PubChem mappings (1:1)

Strain cross-references:
- 33,177 distinct BacDiveIDs (slight variance from 33,226 strains suggests some duplicate IDs)

**Distribution:**
- All chemical cross-references are 1:1 (one ingredient → one identifier per database)
- BacDive mapping is essentially 1:1 (33,226 strains → 33,177 unique IDs = 99.9%)
- GMO has highest coverage (41%) for metabolic pathway context
- Chemical coverage varies: GMO > CAS > ChEBI > PubChem > KEGG > MetaCyc

## Interesting Findings

**Discoveries requiring actual database queries:**

1. **Extreme thermophile cultivation data**: Found growth conditions for hyperthermophiles up to 103°C (Pyrolobus fumarii), all anaerobic. Requires querying GrowthCondition entities and filtering by temperature >90°C. MediaDive provides the most extreme cultivation temperatures in the database collection.

2. **LB medium diversity**: Medium 381 (standard LB) has 769 composition entries representing different preparation variants with NaCl ranging 30-100 g/L and optional agar supplementation. Demonstrates hierarchical recipe complexity requiring composition-level queries.

3. **Chemical cross-reference coverage gradient**: GMO leads (41%) followed by CAS (39%), ChEBI (32%), PubChem (18%), KEGG (13%), MetaCyc (7%). Requires aggregating OPTIONAL cross-reference patterns across all 1,489 ingredients to discover this distribution.

4. **BacDive integration depth**: 73% of MediaDive strains (33,226) link to BacDive, representing 34% coverage of BacDive's strain collection. Enables cross-database queries combining growth conditions (MediaDive) with phenotypic data (BacDive). Requires COUNT DISTINCT queries on hasBacDiveID property.

5. **pH range specialization**: Found marine media with broad pH tolerance (6.8-8.5), alkaliphile media (pH >9), and specialized media for specific metabolic groups. Requires filtering on hasMinPH/hasMaxPH numeric ranges.

6. **Psychrophile cultivation**: Growth conditions exist for bacteria at 4-12°C including Polaromonas, Psychrobacter, Colwellia species. Requires querying GrowthCondition with temperature <15°C filter.

7. **Medium composition granularity**: Average 21.9 compositions per medium with detailed ingredient concentrations (gramsPerLiter). Requires aggregating MediumComposition entities and calculating averages.

8. **Ingredient chemical diversity**: 1,489 unique ingredients with 611 having metabolic pathway context (GMO), enabling integration with KEGG, MetaCyc, Reactome databases. Requires analyzing hasGMO property distribution.

## Question Opportunities by Category

### Precision Questions ✅
- "What is the growth temperature for Pyrolobus fumarii in MediaDive?" (requires growth condition query)
- "What is the ChEBI ID for D-Glucose in MediaDive ingredients?" (requires ingredient cross-reference lookup)
- "What is the final pH of medium 381 (LB medium)?" (requires medium property query)
- "What is the CAS number for tryptone in MediaDive?" (requires ingredient chemical identifier lookup)

### Completeness Questions ✅
- "How many culture media in MediaDive are designed for thermophiles (>45°C)?" (requires COUNT with temperature filter)
- "How many ingredients in MediaDive have ChEBI cross-references?" (requires aggregating chemical mappings)
- "How many strains in MediaDive have BacDive links?" (requires COUNT on hasBacDiveID - answer: 33,226)
- "List all ingredients in LB medium (medium 381) with concentrations >10 g/L" (requires composition query with filtering)

### Integration Questions ✅
- "What is the PubChem CID for glucose in MediaDive?" (requires ingredient → PubChem mapping)
- "Find the BacDive ID for Pyrolobus fumarii strain in MediaDive" (requires strain → BacDive cross-reference)
- "Which MediaDive ingredients map to both ChEBI and KEGG?" (requires multi-database ingredient filtering)
- "Link MediaDive marine medium 1303 to its KEGG compound ingredients" (requires composition → ingredient → KEGG chain)

### Currency Questions ✅
- "What is the current number of hyperthermophile growth conditions (>90°C) in MediaDive?" (requires current count query)
- "How many marine media recipes were added to MediaDive?" (requires media classification query)
- "What are the most recently characterized psychrophile cultivation conditions?" (requires growth condition with temperature filter)

### Specificity Questions ✅
- "What culture medium is used for Methanopyrus kandleri (methanogenic archaea)?" (requires species-specific growth condition)
- "What are the ingredients in Pyrolobus fumarii medium (medium 792)?" (requires specialized extreme thermophile recipe)
- "What oxygen requirement does MediaDive specify for Hyperthermus butylicus?" (requires niche organism growth condition)
- "What is the recommended pH for growing alkaliphilic Bacillus species?" (requires alkaliphile-specific media properties)

### Structured Query Questions ✅
- "Find all anaerobic media with growth temperatures >80°C and pH <7" (requires multi-criteria filtering on growth conditions)
- "List media containing glucose as an ingredient with concentration >20 g/L" (requires composition → ingredient join with filtering)
- "Find strains with BacDive IDs that grow in marine media at temperatures 15-25°C" (requires strain → growth → medium integration)
- "Identify complex media (isComplex=true) with pH range 6.5-7.5 containing at least one KEGG-mapped ingredient" (requires media properties + composition + ingredient cross-references)

## Notes

**Hierarchical structure**: MediaDive uses nested recipe organization (medium → solution → solution_recipe → ingredient) enabling detailed preparation protocols. Most queries operate at the medium → composition → ingredient level for practical recipe retrieval.

**Chemical integration strength**: GMO (41%), CAS (39%), ChEBI (32%) coverage provides strong metabolic pathway and chemical property linking. Lower PubChem (18%), KEGG (13%) coverage means OPTIONAL patterns are essential.

**Cross-database optimization**: Shares "primary" endpoint with BacDive, Taxonomy, MeSH, GO, MONDO, NANDO. BacDive integration via hasBacDiveID (integer matching, no URI conversion) is highly efficient with proper filtering (genus/species pre-filters achieve 64-99% reduction in join size).

**Performance considerations**:
- Use `bif:contains` for keyword searches (faster than FILTER CONTAINS)
- Filter by specific medium before querying compositions (avg 21.9 per medium)
- Use OPTIONAL for partial chemical cross-references
- Apply LIMIT to composition queries (can return hundreds per medium)
- Cross-database queries: Pre-filter within GRAPH blocks (Strategy 2) before joins

**BacDive integration**: 73% strain coverage enables rich phenotype-cultivation integration. MediaDive provides quantitative growth parameters (temp, pH, oxygen) while BacDive adds taxonomic classification, morphology, enzymatic activities. Combined queries yield comprehensive strain characterization.

**Data quality**: pH stored as both string ranges (hasFinalPH: "7.0-7.2") and numeric min/max (hasMinPH: 7.0, hasMaxPH: 7.2) for flexible querying. Chemical cross-references vary by ingredient type (metabolites have higher ChEBI/KEGG coverage than complex media components).

**Unique value**: MediaDive is the only database in TogoMCP providing detailed culture media recipes with ingredient-level granularity and growth condition metadata. Essential for reproducible microbial cultivation research.

**Limitations**: 
- Ingredient chemical coverage incomplete (32% ChEBI, 18% PubChem)
- Some growth conditions lack pH or oxygen data (OPTIONAL patterns required)
- Recipe variants for same medium number create complexity (medium 381 has 769 compositions)
- BacDive link coverage at 73% means 27% of strains lack phenotypic integration
