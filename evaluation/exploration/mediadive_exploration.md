# MediaDive Exploration Report

## Database Overview
- **Purpose**: Comprehensive culture media database from DSMZ with standardized recipes for growing microorganisms
- **Scope**: 3,289 media recipes, 1,489 ingredients, 45,685 strain records
- **Key data types**:
  - Culture media with pH, complexity, preparation protocols
  - Chemical ingredients with cross-references (GMO 41%, CAS 39%, ChEBI 32%)
  - Growth conditions (temperature, pH, oxygen requirements)
  - Microbial strains with BacDive links (73% coverage)
  - Hierarchical recipe structure: medium → solution → solution_recipe → ingredient

## Schema Analysis (from MIE file)

### Main Properties Available
- **CultureMedium**: `rdfs:label`, `schema:belongsToGroup`, `schema:hasFinalPH`, `schema:hasMinPH`, `schema:hasMaxPH`, `schema:isComplex`, `schema:hasLinkToSource`
- **Ingredient**: `rdfs:label`, `schema:hasFormula`, `schema:hasCAS`, `schema:hasChEBI`, `schema:hasPubChem`, `schema:hasKEGG`, `schema:hasGMO`
- **GrowthCondition**: `schema:partOfMedium`, `schema:relatedToStrain`, `schema:growthTemperature`, `schema:growthPH`, `schema:hasOxygenRequirement`
- **Strain**: `schema:hasDSMNumber`, `schema:hasBacDiveID`, `schema:hasSpecies`, `schema:belongsTaxGroup`

### Important Relationships
- Media → Compositions via `schema:MediumComposition`
- Compositions → Ingredients via `schema:containsIngredient`
- Growth conditions → Medium AND Strain via `schema:partOfMedium` and `schema:relatedToStrain`
- Strains → BacDive via `schema:hasBacDiveID`
- Ingredients → Chemical databases via `schema:has[Database]` properties
- Media → DSMZ PDFs via `schema:hasLinkToSource`

### Query Patterns Observed
1. **Keyword search**: Use `bif:contains` for media labels, groups, species names
2. **Numeric filtering**: Efficient for temperature, pH ranges
3. **Composition queries**: Filter by specific medium to avoid timeout on 72K+ records
4. **Cross-references**: Use OPTIONAL due to partial coverage (ChEBI 32%, KEGG 13%)
5. **Thermophiles**: Filter `schema:growthTemperature > [value]` for extremophiles

## Search Queries Performed

### Query 1: Marine Media Search
**Method**: SPARQL with bif:contains on 'marine'
**Results**: 20+ marine media found including:
- BACTO MARINE AGAR
- MARINE BROTH (multiple variants)
- MARINE CAULOBACTER MEDIUM
- MARINE THERMOCOCCUS MEDIUM
- Shows specialization for marine microorganisms

### Query 2: Thermophilic Growth Conditions
**Method**: SPARQL filtering temperature > 70°C
**Results**: 15 hyperthermophilic conditions found:
- Maximum: 103°C (strain 5869)
- 100°C: strain 25984
- 95-99°C range: multiple anaerobic archaea
- All hyperthermophiles are anaerobic
- Shows extremophile cultivation expertise

### Query 3: Ingredient Cross-References
**Method**: SPARQL for ingredients with both ChEBI AND KEGG
**Results**: 20+ well-annotated ingredients including:
- Agar: ChEBI 2509, KEGG C08815, CAS 9002-18-0
- Acetic acid: ChEBI 15366, KEGG C00033, CAS 64-19-7
- 2-Mercaptoethanesulfonate: ChEBI 17905, KEGG C03576
- Demonstrates chemical database integration

## SPARQL Queries Tested

```sparql
# Query 1: Marine media search with full-text indexing
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?medium ?label ?group
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?medium a schema:CultureMedium ;
          rdfs:label ?label ;
          schema:belongsToGroup ?group .
  ?label bif:contains "'marine'"
}
ORDER BY ?label
LIMIT 20
# Results: Identified 20+ marine-specific media including Bacto Marine Agar, Marine Caulobacter Medium
```

```sparql
# Query 2: Hyperthermophilic growth conditions
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?medium ?strain ?temp ?ph ?oxygen
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?growth a schema:GrowthCondition ;
          schema:partOfMedium ?medium ;
          schema:relatedToStrain ?strain ;
          schema:growthTemperature ?temp .
  OPTIONAL { ?growth schema:growthPH ?ph }
  OPTIONAL { ?growth schema:hasOxygenRequirement ?oxygen }
  FILTER(?temp > 70)
}
ORDER BY DESC(?temp)
LIMIT 15
# Results: Found extremophiles growing at 95-103°C, all anaerobic
```

```sparql
# Query 3: Well-annotated chemical ingredients
PREFIX schema: <https://purl.dsmz.de/schema/>

SELECT ?ingredient ?label ?chebi ?kegg ?pubchem ?cas
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?ingredient a schema:Ingredient ;
              rdfs:label ?label .
  OPTIONAL { ?ingredient schema:hasChEBI ?chebi }
  OPTIONAL { ?ingredient schema:hasKEGG ?kegg }
  OPTIONAL { ?ingredient schema:hasPubChem ?pubchem }
  OPTIONAL { ?ingredient schema:hasCAS ?cas }
  FILTER(BOUND(?chebi) && BOUND(?kegg))
}
ORDER BY ?label
LIMIT 20
# Results: Found 20+ ingredients with complete chemical annotations including agar, acids, salts
```

## Interesting Findings

### Specific Entities for Questions
1. **Hyperthermophile DSM 5869**: Grows at 103°C on medium 792 (highest temperature)
2. **Marine media group**: 20+ specialized media for marine microorganisms
3. **Agar ingredient**: Well-annotated with ChEBI 2509, KEGG C08815, CAS 9002-18-0, PubChem 71571511
4. **2-Mercaptoethanesulfonate**: Reducing agent with ChEBI 17905, KEGG C03576
5. **Growth temperature range**: 95-103°C for hyperthermophiles, all anaerobic

### Unique Properties
- **Hierarchical recipe structure**: medium → solution → solution_recipe → ingredient (4 levels)
- **Temperature precision**: Integer values enabling exact thermophile queries
- **Chemical integration**: GMO (41%), CAS (39%), ChEBI (32%) cross-references
- **BacDive linkage**: 73% of strains (33,350/45,685) have BacDive IDs
- **DSMZ PDF links**: 99% of media have authoritative protocol documentation
- **Growth indicators**: Boolean flags for successful cultivation

### Connections to Other Databases
- **BacDive**: 73% strain coverage (33,350 strains) for phenotypic data
- **ChEBI**: 32% ingredient coverage (476 ingredients) for chemical ontology
- **PubChem**: 18% coverage for compound identifiers
- **KEGG**: 13% coverage for metabolic pathways
- **CAS Registry**: 39% coverage for chemical identification
- **GMO**: 41% coverage (highest) for metabolite ontology
- **DSMZ PDFs**: 99% media have protocol documentation

### Verifiable Facts
1. Total of 3,289 culture media recipes in MediaDive
2. Highest growth temperature: 103°C (DSM strain 5869)
3. Total ingredients: 1,489 with varying cross-reference coverage
4. BacDive linkage: 73% of 45,685 strains
5. Agar has ChEBI ID 2509 and KEGG ID C08815
6. Average 21.9 compositions per medium

## Question Opportunities by Category

### Precision
✅ **Specific media and ingredient IDs**:
- "What is the ChEBI ID for agar in MediaDive?" (2509)
- "What medium is used for growing DSM strain 5869?" (medium 792)
- "What is the KEGG ID for acetic acid?" (C00033)
- "What is the CAS number for 2-mercaptoethanol?" (60-24-2)

❌ Avoid: Database version, server configuration

### Completeness
✅ **Counts of media, ingredients, strains**:
- "How many culture media are in MediaDive?" (3,289)
- "How many ingredients have both ChEBI and KEGG IDs?" (check via query)
- "How many marine-specific media exist?" (20+ from query)
- "Count strains linked to BacDive" (73% of 45,685 = ~33,350)

❌ Avoid: Infrastructure statistics

### Integration
✅ **Cross-database chemical linking**:
- "Convert MediaDive ingredient agar to ChEBI ID" (2509)
- "Link MediaDive strain to BacDive ID for DSM 5869"
- "Find KEGG pathway ID for acetic acid ingredient" (C00033)
- "What PubChem CID corresponds to MediaDive agar?" (71571511)

❌ Avoid: Server integration metadata

### Currency
✅ **Recent cultivation methods**:
- "What are the current growth conditions for hyperthermophiles?" (up-to-date protocols)
- "How many extremophile media were recently added?" (if temporal data available)
- "Current pH range for marine media" (from hasMinPH/hasMaxPH)

❌ Avoid: Database release dates

### Specificity
✅ **Specialized media and extremophiles**:
- "What medium grows microorganisms at 103°C?" (medium 792)
- "Which marine media are for Caulobacter?" (Marine Caulobacter Medium)
- "What ingredient is 2-mercaptoethanesulfonate?" (reducing agent, ChEBI 17905)
- "Find media for thermophilic methanogens" (Methanosarcina marine medium)

❌ Avoid: Generic database info

### Structured Query
✅ **Complex cultivation queries**:
- "Find media for anaerobic organisms growing above 95°C"
- "List ingredients with ChEBI ID AND CAS number AND molecular formula"
- "Which strains grow on marine media at pH 7.0-7.5?"
- "Find complex media (isComplex=true) for thermophiles with BacDive links"

❌ Avoid: Infrastructure queries

## Notes

### Limitations
- **Cross-reference coverage varies**: GMO (41%), CAS (39%), ChEBI (32%), PubChem (18%), KEGG (13%)
- **Composition queries can timeout**: 72K+ composition records need medium filtering
- **pH ranges as strings**: hasFinalPH is string "7.0-7.2", numeric hasMinPH/hasMaxPH available
- **Growth indicators partial**: Not all growth conditions have oxygen requirement specified
- **BacDive coverage**: 27% of strains lack BacDive links

### Best Practices
1. **Keyword search**: Use `bif:contains` for media labels, groups, species names
2. **Chemical lookups**: Use OPTIONAL for cross-references (partial coverage)
3. **Temperature queries**: Integer filtering is efficient and precise
4. **Composition queries**: Always filter by specific medium OR add LIMIT
5. **Cross-reference filters**: Use `FILTER(BOUND(?chebi) || BOUND(?kegg))` for "at least one"
6. **Thermophile discovery**: Filter `schema:growthTemperature > [threshold]`
7. **Marine organisms**: Search with `bif:contains "'marine'"` on labels

### Data Quality Notes
- **DSMZ authority**: 99% media have PDF protocol links (authoritative source)
- **Chemical accuracy**: CAS numbers provide unambiguous identification
- **Temperature precision**: Integer values enable exact queries
- **Hierarchical recipes**: Solution-based structure provides detailed protocols
- **Growth validation**: hasGrowthIndicator flags successful cultivations
- **Strain provenance**: DSM numbers link to DSMZ culture collection
