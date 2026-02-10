# TogoMCP Usage Guide (Concise)

## Core Principle: Get MIE → Search → Inspect → Use Structured Properties

**Most errors come from using bif:contains before checking the MIE file for structured properties.**

For comprehensive queries ("how many", "find all"), you MUST:
1. **Get MIE file FIRST**: `get_MIE_file(dbname)` - examine schema for structured predicates
2. Use search tools (or exploratory SPARQL) to find 10-20 example entities  
3. Inspect examples to confirm which structured properties exist
4. Write comprehensive SPARQL using discovered structured properties

**Priority for comprehensive queries:**
```
Structured Properties > Annotation Patterns > bif:contains (only if no structured alternative)
     (BEST)                  (GOOD)              (LAST RESORT - rare)
```

**⚠️ bif:contains Gate Check:** Before using `bif:contains` in comprehensive queries, confirm you've:
- ✓ Examined entity Shape in MIE schema
- ✓ Checked for: classification predicates, external IRIs (taxonomy, MeSH, ontology terms), typed predicates, hierarchies
- ✓ Inspected example entities to verify what properties exist
- ✓ Can document: "No structured alternative exists because..."

Only use `bif:contains` when NO structured alternative exists (rare in modern RDF databases).

---

## Critical Concepts

### ⚠️ Search vs. Comprehensive Queries

**Search APIs (Exploratory)**
- Purpose: Find patterns, examples, cross-references
- Returns: 10-20 results typically
- Use for: Understanding data, identifying entities
- **NOT for**: Definitive answers to comprehensive questions

**SPARQL (Comprehensive)**
- Purpose: Validation, complete analysis, definitive answers
- Returns: All matching entities
- Use for: Aggregations, existence claims, phylogenetic distribution
- **Required for**: Yes/no questions, "are there any...", "which organisms..."

### Circular Reasoning Trap ⚠️

**WRONG** - Using search results in SPARQL VALUES:
```
1. Search API finds 8 example proteins
2. Hardcode those IDs: VALUES ?protein { uniprot:P1 uniprot:P2 ... }
3. Query only those 8 proteins
→ CIRCULAR: You only checked what you already found!
```

**CORRECT** - Check MIE schema, then comprehensive search:
```
1. Get MIE file → find structured properties in schema
2. Search API finds examples (identify patterns/synonyms)
3. Inspect examples to confirm properties
4. SPARQL searches ALL entities using structured properties
→ COMPREHENSIVE: Checked everything matching criteria
```

---

## Complete Workflow

```
1. ANALYZE QUERY
   ├─ Extract keywords, IDs, entities
   ├─ Identify domain (proteins/chemicals/diseases/etc.)
   └─ Classify: Comprehensive (yes/no, counts) or Example-based (specific, top-N)?

2. GET MIE FILE (⚠️ MANDATORY FIRST STEP FOR COMPREHENSIVE)
   ├─ Run: get_MIE_file(dbname)
   ├─ Examine schema_info and shape_expressions sections
   ├─ Look for structured predicates in your entity Shape:
   │  • Classification/Ontology: classification predicates, subClassOf, ontology links
   │  • External IRIs: taxonomy, MeSH, ChEBI, UniProt, GO term links
   │  • Typed Predicates: organism, type, status, phase (controlled values)
   │  • Hierarchies: parent-child relationships, pathways, subclasses
   └─ Check kw_search_tools section for available search functions

3. EXPLORATORY SEARCH
   ├─ If search tools listed → Use them (e.g., search_*_entity())
   ├─ If NO search tools → Use exploratory SPARQL with bif:contains (LIMIT 10-50)
   └─ COLLECT 10-20 example entity IDs/IRIs

4. INSPECT PROPERTIES (⚠️ MANDATORY - Confirm MIE findings)
   ├─ Query sample entities: SELECT * WHERE { VALUES ?entity {...} ?entity ?p ?o }
   ├─ Verify which structured predicates from MIE actually exist in the data
   └─ DOCUMENT: Which patterns match your query intent

5. COMPREHENSIVE SPARQL (if needed)
   ├─ 🚨 MANDATORY PRE-QUERY CHECKLIST 🚨
   │  □ Got MIE file and examined entity Shape?
   │  □ Checked for classification/ontology predicates in schema?
   │  □ Checked for external database IRIs in schema?
   │  □ Checked for typed predicates with controlled vocabularies?
   │  □ Inspected example entities to confirm available properties?
   │  □ If using bif:contains: Can document why no structured alternative exists?
   │
   ├─ Strategy based on Step 2 & 4:
   │  • Found structured predicates → Use those (BEST)
   │  • Found annotation patterns → Filter on annotation type + bif:contains (GOOD)
   │  • Only text labels → Use bif:contains with ALL synonyms (LAST RESORT)
   └─ ALWAYS include LIMIT

6. ID CONVERSION & RETRIEVAL
   └─ Use togoid_* and retrieval tools as needed
```

---

## 🚨 bif:contains GATE CHECK 🚨

**BEFORE using bif:contains in comprehensive queries, answer ALL:**

❓ Have I run `get_MIE_file(dbname)` and examined the entity Shape?  
❓ Have I checked MIE schema for: Classification/ontology predicates?  
❓ Have I checked MIE schema for: External database IRIs (taxonomy, MeSH, ChEBI, etc.)?  
❓ Have I checked MIE schema for: Typed predicates with controlled vocabularies?  
❓ Have I checked MIE schema for: Hierarchical relationships?  
❓ Have I used search tools (from kw_search_tools) OR exploratory SPARQL?  
❓ Have I inspected example entities with SELECT * WHERE { VALUES ... }?  
❓ Can I document: "No structured alternative exists because..."?

**If you answered NO to any → STOP and complete that step**

**bif:contains is ONLY for truly unstructured text:**
- Free-form comments (rdfs:comment)
- Descriptions without controlled vocabulary
- Abstract/summary fields without typed alternatives
- **This is RARE in modern RDF databases - most have structured alternatives**

---

## Decision Tree: Comprehensive Query Strategy

```
Need comprehensive results (count/find all)?
│
1. MIE ANALYSIS PHASE (DO THIS FIRST)
   ├─ Get MIE file: get_MIE_file(dbname)
   ├─ Examine entity Shape in schema_info for your entity type
   ├─ Scan for classification predicates, external IRIs, typed predicates
   └─ Check kw_search_tools section

2. EXPLORATION PHASE
   ├─ Use search tools from kw_search_tools (if listed)
   ├─ OR use exploratory SPARQL if no search tools (LIMIT 10-50)
   └─ Collect example entity IDs/IRIs

3. INSPECTION PHASE (⚠️ MANDATORY - Confirm MIE findings)
   ├─ Query: SELECT * WHERE { VALUES ?entity {...examples...} ?entity ?p ?o }
   ├─ Verify which structured predicates from MIE actually exist
   └─ Scan for these UNIVERSAL patterns:

   ┌────────────────────┬─────────────────────────────────────────┐
   │ Pattern Type       │ Examples Across Databases               │
   ├────────────────────┼─────────────────────────────────────────┤
   │ Classification/    │ ChEMBL: atcClassification               │
   │ Ontology Terms     │ UniProt: classifiedWith (keywords)      │
   │                    │ Any DB: GO terms, enzyme codes          │
   ├────────────────────┼─────────────────────────────────────────┤
   │ External Database  │ Taxonomy IRIs (organism)                │
   │ IRIs               │ MeSH IRIs (diseases)                    │
   │                    │ ChEBI, UniProt, GO IRIs                 │
   ├────────────────────┼─────────────────────────────────────────┤
   │ Typed Predicates   │ ChEMBL: assayType, mechanismActionType  │
   │ (controlled values)│ PDB: entityType                         │
   │                    │ UniProt: reviewed (boolean)             │
   ├────────────────────┼─────────────────────────────────────────┤
   │ Hierarchies        │ Reactome: pathwayComponent              │
   │                    │ GO: subClassOf                          │
   │                    │ ChEBI: has_role                         │
   └────────────────────┴─────────────────────────────────────────┘

4. COMPREHENSIVE QUERY STRATEGY (Use findings from Steps 1-3)
   ├─ Found Classification/Ontology terms?
   │  └─ ✓ Use: ?entity classification_predicate <term_iri>
   │     Example: ?molecule cco:atcClassification ?atc . FILTER(STRSTARTS(?atc, "J01"))
   │
   ├─ Found External Database IRIs?
   │  └─ ✓ Use: ?entity link_predicate <external_iri>
   │     Example: ?target cco:taxonomy <http://identifiers.org/taxonomy/9606>
   │
   ├─ Found Typed Predicates?
   │  └─ ✓ Use: ?entity typed_predicate ?value . FILTER(?value = "specific_value")
   │     Example: ?assay cco:assayType "Binding"
   │
   ├─ Found Hierarchies?
   │  └─ ✓ Use: ?entity parent_predicate+ ?ancestor
   │     Example: ?term rdfs:subClassOf+ <parent_term>
   │
   └─ Only text labels found (after checking MIE + inspecting examples)?
      └─ ✗ LAST RESORT: ?entity label_predicate ?label . 
                        ?label bif:contains "'term1' OR 'synonym1' OR 'variant1'"
         (⚠️ Must document: "No structured properties exist because...")
         (This is RARE - most databases have structured alternatives)
```

---

## Common Patterns

### Pattern 1: Comprehensive Query with Classification
```python
# Question: "How many antibiotics in ChEMBL?"

# Step 1: Get MIE file FIRST - check schema
get_MIE_file("chembl")
# Examine <MoleculeShape> in schema → Found: cco:atcClassification predicate
# Check kw_search_tools → Found: search_chembl_molecule

# Step 2: Exploratory search
results = search_chembl_molecule("antibiotic", limit=20)
# Get IDs: CHEMBL29, CHEMBL615, ...

# Step 3: Inspect examples to CONFIRM MIE findings
query = """
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?chemblId ?atc WHERE {
  VALUES ?chemblId { "CHEMBL29" "CHEMBL615" "CHEMBL606111" }
  ?molecule cco:chemblId ?chemblId .
  OPTIONAL { ?molecule cco:atcClassification ?atc }
} LIMIT 50
"""
# Confirmed: cco:atcClassification exists! Values like "J01*" for antibacterials

# Step 4: Comprehensive query using structured property from MIE schema
query = """
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT (COUNT(DISTINCT ?molecule) as ?count)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule cco:atcClassification ?atc .
  FILTER(STRSTARTS(?atc, "J01"))
}
"""
# Result: 216 antibiotics
```

### Pattern 2: Comprehensive Query with Keywords
```python
# Question: "How many proteins have function X?"

# Step 1: Get MIE file - check schema
get_MIE_file("uniprot")
# Examine <ProteinShape> → Found: up:classifiedWith predicate for keywords
# Check kw_search_tools → Found: search_uniprot_entity

# Step 2: Exploratory
results = search_uniprot_entity("function X", limit=20)
# Get IDs: P12345, P67890, ...

# Step 3: Inspect to confirm MIE findings
# Run inspection query → Confirmed: up:classifiedWith exists with keywords:KW-0123

# Step 4: Comprehensive
query = """
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX keywords: <http://purl.uniprot.org/keywords/>

SELECT (COUNT(DISTINCT ?protein) as ?count)
WHERE {
  ?protein up:reviewed 1 ;
           up:classifiedWith keywords:KW-0123 .
}
"""
```

### Pattern 3: Database Without Search Tools
```python
# Question: "How many GO terms relate to apoptosis?"

# Step 1: Get MIE file - check schema
get_MIE_file("go")
# Examine <ClassShape> → Found: rdfs:subClassOf hierarchy predicate
# Check kw_search_tools → [] (empty - no search tools available)

# Step 2: Exploratory SPARQL (no search tool exists)
query = """
SELECT ?term ?label WHERE {
  ?term rdfs:label ?label .
  ?label bif:contains "'apoptosis'"
} LIMIT 20
"""
# Get IRIs: GO:0006915, GO:0097194, ...

# Step 3: Inspect to confirm MIE findings
# Run: SELECT * WHERE { VALUES ?term { <GO:...> } ?term ?p ?o }
# Confirmed: rdfs:subClassOf hierarchy exists as indicated in MIE schema

# Step 4: Comprehensive (use hierarchy)
query = """
SELECT (COUNT(?term) as ?count) WHERE {
  ?term rdfs:subClassOf* <parent_apoptosis_term>
}
"""
```

---

## Quick Reference: Tools by Purpose

### Discovery
- `list_databases()` - List 22 RDF databases
- `get_sparql_endpoints()` - Get endpoint URLs and search tools
- `togoid_getAllDataset()` - ID conversion routes

### Search (Exploratory)
| Domain | Tool |
|--------|------|
| Proteins | `search_uniprot_entity(query, limit=20)` |
| Drugs/Molecules | `search_chembl_molecule(query, limit=20)` |
| Drug Targets | `search_chembl_target(query, limit=20)` |
| 3D Structures | `search_pdb_entity(db, query, limit=20)` |
| Pathways | `search_reactome_entity(query, rows=30)` |
| Reactions | `search_rhea_entity(query, limit=100)` |
| Medical Terms | `search_mesh_descriptor(query, limit=10)` |
| Ontologies | `OLS4:search(query)` |
| Chemicals | `get_pubchem_compound_id(name)` |
| NCBI | `ncbi_esearch(database, query)` |

### SPARQL (Comprehensive)
- `get_MIE_file(dbname)` - **MANDATORY** before SPARQL: schema + examples
- `run_sparql(dbname, query)` - Execute query
- `get_graph_list(dbname)` - Named graphs

### ID Conversion
- `togoid_convertId(ids, route)` - Convert IDs
- `togoid_getRelation(source, target)` - Check if route exists

---

## Database-Specific Rules

| Database | Critical Requirements |
|----------|---------------------|
| **UniProt** | ALWAYS: `?protein up:reviewed 1` |
| **ChEMBL** | ALWAYS: `FROM <http://rdf.ebi.ac.uk/dataset/chembl>` |
| **All** | ALWAYS: `LIMIT` clause (start 20-1000) |

---

## Common Anti-Patterns

❌ **Skipping MIE File**
```python
# WRONG: Skip MIE file, immediately use bif:contains
query = "SELECT ?mol WHERE { ?label bif:contains 'antibiotic' }"
# Result: Only 2 molecules (very few have "antibiotic" in label)

# CORRECT: Check MIE file FIRST
get_MIE_file("chembl")  
# Found in schema: cco:atcClassification (drug classification codes)
# Use structured property: FILTER(STRSTARTS(?atc, "J01"))
# Result: 216 antibiotics found
```

❌ **Skipping Inspection**
```python
# WRONG
search_chembl_molecule("antibiotic")  # → 645 results
# Immediately write: WHERE { ?label bif:contains "'antibiotic'" }

# CORRECT
get_MIE_file("chembl")  # Check schema first
search_chembl_molecule("antibiotic")  # Get example IDs
# Inspect IDs → confirm ATC codes exist
# Use discovered properties → Find 216 antibiotics
```

❌ **Circular Reasoning**
```python
# WRONG
search results → VALUES ?entity { <found_entities> }
# You only queried what you already found!

# CORRECT
MIE schema → search results → inspect → discover property → query ALL entities
```

---

## Critical Rules Summary

### ✅ ALWAYS
1. **Get MIE file FIRST**: `get_MIE_file(dbname)` - examine schema before any query
2. Check entity Shape in schema for structured predicates
3. Check kw_search_tools section for available search tools
4. Use search tools (or exploratory SPARQL if none exist) to find examples
5. **INSPECT examples** to confirm which structured predicates actually exist
6. Use structured predicates from MIE schema (not bif:contains) when they exist
7. Include `LIMIT` in all queries
8. UniProt: add `up:reviewed 1`

### ❌ NEVER
1. Skip getting MIE file before comprehensive queries
2. Skip examining entity Shape in MIE schema for structured predicates
3. Default to `bif:contains` without checking MIE schema + inspecting examples
4. Use VALUES with search results for comprehensive questions (circular reasoning)
5. Write comprehensive SPARQL without checking MIE file
6. Omit `LIMIT` clause
7. Forget `up:reviewed 1` in UniProt

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Don't know which database** | `list_databases()` |
| **Search tool exists?** | `get_MIE_file(dbname)` → check `kw_search_tools` section |
| **No structured properties found** | Verify you checked MIE schema + inspected examples, then document why |
| **SPARQL timeout** | Reduce LIMIT, add type filters, use `up:reviewed 1` |
| **Empty results** | Check prefixes, graph URIs, verify property exists in MIE schema |
| **Incomplete comprehensive results** | Did you skip MIE file? Check if using right predicates |

---

## Key ID Conversion Routes

**Common conversions:**
- `"uniprot,pdb"` - Protein to structure
- `"uniprot,ncbigene"` - Protein to gene  
- `"uniprot,chembl_target"` - Protein to drug target
- `"ncbigene,ensembl_gene"` - NCBI to Ensembl
- `"chebi,pubchem_compound"` - ChEBI to PubChem

Check availability: `togoid_getRelation(source, target)`
