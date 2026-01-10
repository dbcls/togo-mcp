# NANDO (Nanbyo Data) Exploration Report

## Database Overview
- **Purpose**: Comprehensive ontology for Japanese intractable (rare) diseases
- **Scope**: 2,777 disease classes focusing on designated intractable diseases eligible for Japanese government support
- **Key entities**: Disease classes with multilingual labels (English, Japanese kanji, hiragana), notification numbers, cross-references
- **Integration**: Maps to MONDO ontology, KEGG Disease, Japanese government documents, patient resources

## Schema Analysis (from MIE file)

### Main Properties
- `rdfs:label`: Disease name in multiple languages (@en, @ja, @ja-hira)
- `dct:identifier`: NANDO identifier (e.g., "NANDO:1200010")
- `skos:prefLabel`: Preferred label (Japanese kanji)
- `nando:hasNotificationNumber`: Official government notification number (e.g., "6")
- `dct:description`: Disease description (in Japanese)
- `rdfs:subClassOf`: Parent disease class (hierarchical classification)
- `skos:altLabel`: Alternative labels/synonyms
- `skos:closeMatch`: MONDO ontology mappings
- `rdfs:seeAlso`: External resources (KEGG, government documents)
- `dct:source`: Source documentation (government PDFs)
- `owl:deprecated`: Deprecation status

### Important Relationships
- **Hierarchical**: `rdfs:subClassOf` for disease taxonomy
- **MONDO mapping**: `skos:closeMatch` links to international disease ontology
- **External resources**: `rdfs:seeAlso` links to KEGG, government documents, patient portals
- **Source documentation**: `dct:source` links to official PDF documents

### Query Patterns Observed
- Use `bif:contains` for efficient full-text search with relevance scoring
- Always include `FROM <http://nanbyodata.jp/ontology/nando>` clause
- Use `FILTER(LANG(?label) = "en")` for English labels
- Use `FILTER(LANG(?label) = "ja" && !REGEX(STR(?label), "^[ぁ-ん]+$"))` for kanji
- Use `FILTER(REGEX(STR(?label), "^[ぁ-ん]+$"))` for hiragana
- Use `STRSTARTS(STR(?mondo_id), "http://purl.obolibrary.org/obo/MONDO_")` for MONDO filtering
- Disease categories use NANDO:11xxxxx IDs, specific diseases use NANDO:12xxxxx or NANDO:22xxxxx

## Search Queries Performed

1. **Query**: "Parkinson*" (SPARQL bif:contains)
   - **Results**: Found 3 Parkinson-related diseases
     - NANDO:1200010: Parkinson's disease (top ranked)
     - NANDO:1200524: Rapid-onset dystonia-parkinsonism
     - NANDO:1200036: Multiple system atrophy, Parkinsonian type
   - Demonstrates relevance ranking with bif:contains

2. **Query**: Designated diseases with notification numbers (first 10)
   - **Results**: Retrieved diseases eligible for government support
     - NANDO:1200001: Spinal and bulbar muscular atrophy (通知番号: 1)
     - NANDO:2200079: Malignant thymoma (通知番号: 1)
     - NANDO:2200460: Diabetes mellitus type 1 (通知番号: 1)
     - All show multilingual labels (English + Japanese kanji)

3. **Query**: Diseases with MONDO cross-references (first 10)
   - **Results**: Found category-level mappings
     - Neuromuscular disease → MONDO:0019056
     - Metabolic disease → MONDO:0004955 AND MONDO:0005066 (multiple mappings!)
     - Immune system disease → MONDO:0005046
     - Demonstrates one-to-many MONDO mappings

4. **Query**: Disease counts by category (aggregation)
   - **Results**: Top 10 categories by disease count
     - Neuromuscular disease: 84 diseases (largest)
     - Metabolic disease: 45 diseases
     - Chromosome abnormality: 42 diseases
     - Immune system disease: 27 diseases
     - Demonstrates distribution across categories

## SPARQL Queries Tested

```sparql
# Query 1: Keyword search with bif:contains
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?disease ?label ?identifier
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?disease a owl:Class ;
           rdfs:label ?label ;
           dct:identifier ?identifier .
  ?label bif:contains "'Parkinson*'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10

# Results: 3 Parkinson-related diseases with relevance ranking
# Parkinson's disease ranked highest
```

```sparql
# Query 2: Designated diseases with notification numbers
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX nando: <http://nanbyodata.jp/ontology/NANDO_>

SELECT ?disease ?identifier ?prefLabel ?en_label ?notif_num
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?disease a owl:Class ;
           dct:identifier ?identifier ;
           skos:prefLabel ?prefLabel ;
           nando:hasNotificationNumber ?notif_num .
  OPTIONAL {
    ?disease rdfs:label ?en_label .
    FILTER(LANG(?en_label) = "en")
  }
}
ORDER BY xsd:integer(?notif_num)
LIMIT 10

# Results: First 10 designated diseases sorted by notification number
# All have Japanese kanji labels and English translations
# Shows diseases eligible for government support
```

```sparql
# Query 3: Diseases with MONDO cross-references
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?disease ?label ?mondo_id
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?disease a owl:Class ;
           rdfs:label ?label ;
           skos:closeMatch ?mondo_id .
  FILTER(STRSTARTS(STR(?mondo_id), "http://purl.obolibrary.org/obo/MONDO_"))
  FILTER(LANG(?label) = "en")
}
LIMIT 10

# Results: 10 diseases with MONDO mappings
# Metabolic disease has 2 MONDO IDs (one-to-many mapping)
# Demonstrates international disease harmonization
```

```sparql
# Query 4: Disease counts by category
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX nando: <http://nanbyodata.jp/ontology/NANDO_>

SELECT ?category ?category_label (COUNT(DISTINCT ?disease) as ?disease_count)
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?category a owl:Class ;
            rdfs:subClassOf nando:1000001 ;
            rdfs:label ?category_label .
  ?disease rdfs:subClassOf ?category ;
           a owl:Class .
  FILTER(LANG(?category_label) = "en")
}
GROUP BY ?category ?category_label
ORDER BY DESC(?disease_count)
LIMIT 10

# Results: Top 10 categories by disease count
# Neuromuscular disease: 84 (largest)
# Metabolic disease: 45
# Chromosome abnormality: 42
```

## Interesting Findings

### Specific Entities for Questions
- **Parkinson's disease (NANDO:1200010)**: Notification number 6, MONDO:0005180
- **Spinal and bulbar muscular atrophy (NANDO:1200001)**: Notification number 1, Kennedy disease
- **Metabolic disease (NANDO:1100002)**: Has TWO MONDO mappings (one-to-many)
- **Neuromuscular disease (NANDO:1100001)**: Largest category with 84 diseases

### Unique Properties
- **2,777 total disease classes**: Focused on rare/intractable diseases
- **Trilingual labels**: English, Japanese kanji, Japanese hiragana
- **88% have notification numbers**: 2,454 designated diseases eligible for government support
- **84% have MONDO mappings**: 2,341 diseases mapped to international ontology
- **One-to-many MONDO mappings**: Some diseases map to multiple MONDO terms

### Connections to Other Databases
- **MONDO**: 2,341 mappings (84%) for international harmonization
- **KEGG Disease**: ~500 links for molecular and pathway context
- **Japanese Government**: Official documents (.docx) with diagnostic criteria
- **Patient Resources**: Nanbyou.or.jp portal with patient information PDFs
- **Source Documentation**: 2,397 diseases with PDF source references

### Verifiable Facts
- 2,777 total disease classes
- 2,454 designated diseases with notification numbers (88%)
- 2,341 diseases with MONDO mappings (84%)
- ~500 diseases with KEGG links
- 84 neuromuscular diseases (largest category)
- 45 metabolic diseases
- 42 chromosome abnormality diseases
- Average 3.0 labels per disease (English + kanji + hiragana)
- Average 2.2 external references per disease

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Biological IDs and disease classifications**
- "What is the NANDO ID for Parkinson's disease?"
- "What is the notification number for spinal and bulbar muscular atrophy?"
- "What is the MONDO ID for Parkinson's disease in NANDO?"
- "What is the English name for NANDO:1200001?"
- "What is the Japanese kanji label for Parkinson's disease in NANDO?"

❌ Avoid: "What database version is this?" "When was NANDO released?"

### Completeness
✅ **Counts and comprehensive lists of diseases**
- "How many total disease classes are in NANDO?"
- "How many designated intractable diseases have notification numbers?"
- "How many neuromuscular diseases are in NANDO?"
- "List all disease categories in NANDO"
- "How many diseases have MONDO cross-references?"

❌ Avoid: "How many database tables exist?" "What is the total storage size?"

### Integration
✅ **Cross-database disease entity linking**
- "Convert NANDO:1200010 to its MONDO identifier"
- "What is the KEGG Disease ID for Parkinson's disease in NANDO?"
- "Find all NANDO diseases that map to MONDO:0019056"
- "Which NANDO diseases have multiple MONDO mappings?"
- "Link NANDO metabolic diseases to MONDO ontology"

❌ Avoid: "What databases connect to this endpoint?" "List all integration APIs"

### Currency
✅ **Recent disease classifications and updates**
- "What diseases were recently added to NANDO?"
- "Has the notification number for Parkinson's disease changed?"
- "Are there any newly designated intractable diseases?"
- "What is the current count of obsolete disease terms?"

❌ Avoid: "What is the current database version?" "When was the server updated?"

### Specificity
✅ **Rare Japanese intractable diseases**
- "What is the NANDO ID for Kennedy disease?"
- "Find the Japanese name for rapid-onset dystonia-parkinsonism"
- "What is the notification number for diabetes mellitus type 1 in NANDO?"
- "What rare neuromuscular diseases are designated in Japan?"
- "Find diseases with notification number 1"

❌ Avoid: "What is the most popular search query?" "Which data format is used?"

### Structured Query
✅ **Complex disease queries with multiple criteria**
- "Find all neuromuscular diseases with MONDO mappings AND notification numbers"
- "List designated diseases that have both KEGG links AND government documentation"
- "Find diseases with notification number < 10 that are metabolic disorders"
- "Which disease categories have more than 20 diseases?"
- "Find diseases with multiple MONDO mappings"

❌ Avoid: "Find databases updated in 2024" "List all server configurations"

## Notes

### Limitations and Challenges
- **Language complexity**: Need careful filtering for English, kanji, and hiragana
- **OLS4 search doesn't work**: Must use SPARQL with bif:contains instead
- **Smaller dataset**: 2,777 diseases (focused on rare/intractable)
- **Japanese focus**: Designed for Japanese healthcare system
- **Some MONDO many-to-many**: Disease categories may map to multiple MONDO terms

### Best Practices for Querying
1. **Always use FROM clause**: `FROM <http://nanbyodata.jp/ontology/nando>`
2. **Use bif:contains for search**: Much faster than REGEX
3. **Filter language carefully**:
   - English: `FILTER(LANG(?label) = "en")`
   - Kanji: `FILTER(LANG(?label) = "ja" && !REGEX(STR(?label), "^[ぁ-ん]+$"))`
   - Hiragana: `FILTER(REGEX(STR(?label), "^[ぁ-ん]+$"))`
4. **Use STRSTARTS for MONDO filtering**: Efficient prefix matching
5. **Notification number sorting**: `ORDER BY xsd:integer(?notif_num)` for proper numeric sort
6. **Use OPTIONAL for multilingual**: Not all diseases have all language labels
7. **Direct parent-child queries**: Faster than deep hierarchy traversal

### Data Quality Notes
- All 2,777 diseases have identifiers and labels (100%)
- 88% have notification numbers (designated diseases)
- 84% have MONDO mappings (international harmonization)
- 44% have descriptions (in Japanese)
- ~500 have KEGG links (molecular context)
- 9 deprecated classes marked with owl:deprecated
- Trilingual labels: English, Japanese kanji, Japanese hiragana
- Some categories have one-to-many MONDO mappings (valid for disease variants)
- External URLs mostly stable (KEGG most reliable)
- Government documents may be updated periodically
