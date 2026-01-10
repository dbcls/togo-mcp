# ChEBI (Chemical Entities of Biological Interest) Exploration Report

## Database Overview
- **Purpose**: Ontology database for chemical entities of biological interest
- **Scope**: 217,000+ chemical entities including small molecules, atoms, ions, functional groups, macromolecules
- **Key entities**: Chemical compounds with hierarchical classification, molecular data, biological roles, chemical relationships
- **Integration**: Cross-references to 20+ databases (KEGG, DrugBank, PubChem, HMDB, CAS, etc.)

## Schema Analysis (from MIE file)

### Main Properties
- `rdfs:label`: Chemical name (e.g., "ATP", "water", "aspirin")
- `rdfs:subClassOf`: Parent chemical class (hierarchical classification)
- `obo:IAO_0000115`: Definition/description
- `oboInOwl:id`: ChEBI identifier (e.g., "CHEBI:15422")
- `oboInOwl:hasDbXref`: Cross-references to external databases
- `oboInOwl:hasRelatedSynonym`: Alternative names
- `oboInOwl:hasExactSynonym`: Exact synonyms
- `chebi:formula`: Molecular formula (e.g., "C9H8O4")
- `chebi:mass`: Molecular mass (e.g., "180.15740")
- `chebi:charge`: Ionic charge
- `chebi:smiles`: SMILES notation
- `chebi:inchi`: InChI string
- `chebi:inchikey`: InChI Key
- `owl:deprecated`: Deprecation status

### Important Relationships
- **Hierarchical**: `rdfs:subClassOf` for chemical classification
- **Biological roles**: Via `RO_0000087` property through OWL restrictions
- **Chemical relationships**: Conjugate acids/bases, tautomers, enantiomers (via OWL restrictions)
- **Cross-references**: Links to 20+ external databases via `oboInOwl:hasDbXref`

### Query Patterns Observed
- **CRITICAL**: ChEBI uses TWO namespaces:
  - Data properties (formula, mass, smiles): `http://purl.obolibrary.org/obo/chebi/`
  - Relationship properties (is_conjugate_acid_of, etc.): `http://purl.obolibrary.org/obo/chebi#`
- Use `bif:contains` for efficient keyword search with relevance scoring
- Always include `FROM <http://rdf.ebi.ac.uk/dataset/chebi>` clause
- Filter by `CHEBI_` URI prefix to exclude non-entity classes
- Use OWL restrictions to access biological roles and chemical relationships
- Use OPTIONAL for molecular properties (not all entities have all properties)

## Search Queries Performed

1. **Query**: "ATP" (OLS4 searchClasses)
   - **Results**: Found 10 entities including:
     - CHEBI:15422: ATP (main entity)
     - CHEBI:30616: ATP(4-) (deprotonated form at pH 7.3)
     - CHEBI:20855: ATP-sugar
     - CHEBI:20854: ATP synthase inhibitor
     - CHEBI:57299: ATP(3-)
     - Multiple hierarchical ancestors shown (76 total ancestors for ATP)
   - Definition: "An adenosine 5'-phosphate in which the 5'-phosphate is a triphosphate group"

2. **Query**: Aspirin molecular properties (CHEBI:15365)
   - **Results**: Complete molecular data retrieved
     - Label: "acetylsalicylic acid"
     - Formula: C9H8O4
     - Mass: 180.15740
     - SMILES: CC(=O)Oc1ccccc1C(O)=O
     - InChIKey: BSYNRYMUTXBXSQ-UHFFFAOYSA-N

3. **Query**: ATP(4-) parent classes
   - **Results**: Single direct parent
     - CHEBI:61557: nucleoside 5'-triphoshate(4-)
   - Demonstrates precise hierarchical classification

4. **Query**: "antibiotic" (OLS4 searchClasses)
   - **Results**: Found 494 total entities, including:
     - CHEBI:80084: Antibiotic TA (macrolide)
     - CHEBI:39208: antibiotic insecticide
     - CHEBI:39215: antibiotic pesticide
     - CHEBI:39216: antibiotic acaricide
     - CHEBI:39217: antibiotic nematicide
   - Demonstrates biological role classification

5. **Query**: General ATP search (OLS4:search across all ontologies)
   - **Results**: Mixed results from multiple ontologies
   - Confirmed need to specify ontologyId for precise ChEBI queries

## SPARQL Queries Tested

```sparql
# Query 1: Get molecular properties for aspirin
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>

SELECT ?label ?formula ?mass ?smiles ?inchikey
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  obo:CHEBI_15365 rdfs:label ?label .
  OPTIONAL { obo:CHEBI_15365 chebi:formula ?formula }
  OPTIONAL { obo:CHEBI_15365 chebi:mass ?mass }
  OPTIONAL { obo:CHEBI_15365 chebi:smiles ?smiles }
  OPTIONAL { obo:CHEBI_15365 chebi:inchikey ?inchikey }
}

# Results: Complete molecular characterization
# - acetylsalicylic acid, C9H8O4, 180.15740, SMILES, InChIKey
# Demonstrates comprehensive molecular data availability
```

```sparql
# Query 2: Get hierarchical parents for ATP(4-)
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT ?parent ?parentLabel
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  obo:CHEBI_30616 rdfs:subClassOf ?parent .
  FILTER(STRSTARTS(STR(?parent), "http://purl.obolibrary.org/obo/CHEBI_"))
  ?parent rdfs:label ?parentLabel .
}

# Results: nucleoside 5'-triphoshate(4-)
# Shows single immediate parent in hierarchy
# Demonstrates how to navigate chemical classification tree
```

```sparql
# Query 3: Keyword search with bif:contains (from MIE example)
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?entity ?label ?sc
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  ?entity a owl:Class ;
          rdfs:label ?label .
  ?label bif:contains "'glucose'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 20

# Would return glucose and related compounds ranked by relevance
# Demonstrates efficient full-text search capability
```

## Interesting Findings

### Specific Entities for Questions
- **ATP (CHEBI:15422)**: Energy currency, 76 hierarchical ancestors
- **ATP(4-) (CHEBI:30616)**: Physiological form at pH 7.3
- **Aspirin (CHEBI:15365)**: Complete molecular data, drug compound
- **Water (CHEBI:15377)**: Simplest example, all properties present
- **L-proline (CHEBI:17203)**: Amino acid with structural data
- **Ciprofloxacin (CHEBI:100241)**: Shows conjugate base/tautomer relationships

### Unique Properties
- **Dual namespace system**: chebi/ for data, chebi# for relationships
- **OWL restriction encoding**: Biological roles and chemical relationships
- **217,368 total entities**: 86% have formulas, 81% have InChI
- **Complete structural data**: SMILES, InChI, InChIKey for most compounds
- **Hierarchical depth**: Some compounds have 76+ ancestors (like ATP)

### Connections to Other Databases
- **KEGG**: Metabolic pathway integration
- **DrugBank**: Drug information
- **PubChem**: Chemical substance database
- **HMDB**: Human metabolome
- **CAS**: Chemical abstracts
- **20+ databases total**: Comprehensive cross-referencing

### Verifiable Facts
- 217,368 total chemical entities
- 187,110 have molecular formulas (86%)
- 81% have InChI identifiers
- 85% have SMILES notations
- Average 1.9 cross-references per entity
- Average 1.2 synonyms per entity
- 494 antibiotic-related entities
- 176 ATP-related entities

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Biological IDs and molecular properties**
- "What is the ChEBI ID for ATP?"
- "What is the molecular weight of aspirin?"
- "What is the InChIKey for acetylsalicylic acid?"
- "What is the SMILES notation for L-proline?"
- "What is the exact molecular formula for ATP(4-)?"

❌ Avoid: "What version is ChEBI?" "When was the database updated?"

### Completeness
✅ **Counts and comprehensive lists of chemical entities**
- "How many chemical entities are in ChEBI?"
- "How many antibiotic-related compounds are in ChEBI?"
- "List all parent classes of ATP"
- "How many compounds have InChI identifiers?"
- "How many hierarchical ancestors does ATP have?"

❌ Avoid: "How many database tables exist?" "What is the server capacity?"

### Integration
✅ **Cross-database chemical entity linking**
- "What is the KEGG identifier for ATP?"
- "Convert ChEBI:15365 to its corresponding PubChem CID"
- "What DrugBank ID corresponds to aspirin in ChEBI?"
- "Find all HMDB cross-references for glucose"
- "What CAS number is associated with water in ChEBI?"

❌ Avoid: "What databases link to this endpoint?" "List all API URLs"

### Currency
✅ **Recent chemical classifications and updates**
- "What new drug compounds were added to ChEBI in 2024?"
- "Has the classification of ciprofloxacin been updated?"
- "What is the current count of deprecated entities?"
- "Are there any recent antibiotic entries?"

❌ Avoid: "What is the current database version?" "When was the server migrated?"

### Specificity
✅ **Rare or specialized chemical entities**
- "What is the ChEBI ID for Atpenin B (rare antibiotic)?"
- "Find the molecular structure of ATP synthase inhibitor"
- "What is the chemical classification of ATP-sugar?"
- "What are the conjugate acid/base relationships for ciprofloxacin?"
- "What enantiomers exist for specific chiral drugs?"

❌ Avoid: "What is the most queried compound?" "Which data format is most common?"

### Structured Query
✅ **Complex chemical queries with multiple criteria**
- "Find all compounds with molecular weight < 200 AND containing nitrogen"
- "List antibiotics that are also pesticides (dual biological roles)"
- "Find all nucleotides with triphosphate groups"
- "Which compounds have both KEGG AND DrugBank cross-references?"
- "Find all aromatic ketones with antibiotic properties"

❌ Avoid: "Find databases updated after 2024" "List all ontology formats available"

## Notes

### Limitations and Challenges
- **Dual namespace complexity**: Must use correct namespace (chebi/ vs chebi#)
- **OWL restriction pattern**: Biological roles require complex SPARQL
- **Incomplete properties**: Not all entities have molecular data (abstract classes)
- **Deprecated entities**: Need to filter with owl:deprecated
- **Large dataset**: 217K+ entities require careful query design

### Best Practices for Querying
1. **Always use FROM clause**: `FROM <http://rdf.ebi.ac.uk/dataset/chebi>`
2. **Use correct namespace**:
   - Data properties: PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
   - Relationship properties: PREFIX chebi: <http://purl.obolibrary.org/obo/chebi#>
3. **Use bif:contains for search**: Much faster than FILTER(CONTAINS())
4. **Filter by CHEBI_ URI**: Exclude non-entity classes early
5. **Use OPTIONAL for properties**: Not all entities have all molecular data
6. **Access roles via restrictions**: Don't look for direct properties
7. **Use OLS4:searchClasses**: More efficient than raw SPARQL for simple searches

### Data Quality Notes
- Molecular properties: ~86% completeness for formulas
- Structural identifiers: 81% InChI, 85% SMILES
- Cross-references: Average 1.9 per entity (some have 5+)
- Synonyms: Average 1.2 per entity
- Hierarchical structure: Well-defined with rdfs:subClassOf
- Deprecated entities: Marked with owl:deprecated flag
- Abstract classes: May lack molecular properties (designed for classification only)
