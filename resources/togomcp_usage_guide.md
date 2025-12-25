# TogoMCP Usage Guide

A step-by-step workflow for answering user questions using TogoMCP tools.

---

## Quick Workflow

### Step 1: Extract Keywords
Identify key terms, IDs, and domain (proteins, chemicals, diseases, genes, pathways, etc.)

### Step 2: Select Databases
Run `list_databases()` and choose by domain:
- Proteins: `uniprot`, `pdb`, `ensembl`, `ncbigene`
- Chemicals: `pubchem`, `chembl`, `chebi`, `rhea`
- Diseases: `mondo`, `mesh`, `medgen`, `clinvar`
- Pathways: `reactome`, `go`

### Step 3: Search - ALWAYS Try Tools First

**Available Search Tools:**
- `search_uniprot_entity(query, limit)` - proteins (searches names, descriptions, AND disease associations)
- `search_chembl_molecule/target(query, limit)` - drugs/targets
- `search_pdb_entity(db, query, limit)` - structures
- `search_reactome_entity(query, rows)` - pathways
- `search_rhea_entity(query, limit)` - reactions
- `search_mesh_entity(query, limit)` - medical concepts

**Decision Tree:**
```
Try search tool → Got results? → Use them
                → Insufficient? → Try different keywords
                → Still no? → Use SPARQL (Step 4)
```

**Don't assume limitations - search tools are more powerful than their names suggest.**

### Step 4: SPARQL (When Needed)

**Before SPARQL, ALWAYS run:** `get_MIE_file(dbname)`

**Use SPARQL when you need:**
- Specific annotation types (Disease_Annotation vs Function_Annotation)
- Complex boolean logic (X AND Y AND NOT Z)
- Precise field targeting (search only within specific predicates)
- Aggregations (COUNT, GROUP BY)

**Critical Rules:**
- UniProt: Always filter `up:reviewed 1`
- ChEMBL: Use `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
- Split property paths when using `bif:contains`
- Always use `LIMIT` (20-100)
- **Avoid Cartesian products** - See detailed section below

---

## Avoiding Cartesian Product Errors

**What is a Cartesian Product?**
A Cartesian product occurs when SPARQL matches multiple independent patterns that aren't properly connected, resulting in every combination of results - often millions of unwanted rows.

**Common Causes:**
```sparql
# ❌ BAD: Two independent patterns
SELECT ?protein ?disease WHERE {
  ?protein a up:Protein .
  ?annotation up:disease ?disease .
}
# Returns every protein × every disease = millions of rows!
```

**How to Fix:**
```sparql
# ✅ GOOD: Patterns connected through shared variable
SELECT ?protein ?disease WHERE {
  ?protein a up:Protein ;
           rdfs:seeAlso ?annotation .
  ?annotation up:disease ?disease .
}
# Returns only proteins connected to their diseases
```

**Warning Signs:**
- Query returns thousands/millions of rows unexpectedly
- Results include random combinations of unrelated entities
- Query times out or runs very slowly
- Every entity appears with every other entity

**Prevention Checklist:**
1. ✅ Every triple pattern shares at least one variable with another pattern
2. ✅ Verify the connection path from subject to object
3. ✅ Use `LIMIT` during testing to catch problems early
4. ✅ Review MIE file to understand correct relationship paths
5. ✅ Test with small subset before running full query

**Common Patterns to Avoid:**
```sparql
# ❌ Independent annotations
?protein rdfs:seeAlso ?anno1 .
?anno2 a up:Disease_Annotation .
# Should be: ?protein rdfs:seeAlso ?anno2

# ❌ Disconnected filters
?protein up:mnemonic ?name .
?disease rdfs:label ?diseaseLabel .
# Missing: how protein and disease relate

# ❌ Multiple OPTIONAL blocks without connections
OPTIONAL { ?x a up:Protein }
OPTIONAL { ?y up:citation ?z }
# Should share variables if meant to be related
```

**Safe Patterns:**
```sparql
# ✅ Chain relationships
?protein rdfs:seeAlso ?annotation .
?annotation up:disease ?disease .
?disease rdfs:label ?label .

# ✅ Use property paths when appropriate
?protein rdfs:seeAlso/up:disease/rdfs:label ?label .

# ✅ Explicit FILTER to limit scope
?protein a up:Protein .
FILTER(?protein = <http://purl.uniprot.org/uniprot/P04637>)
```

**Before Running Any SPARQL:**
1. Trace the path from source to target using MIE examples
2. Ensure all triple patterns form a connected graph
3. Test with `LIMIT 10` first
4. If results look wrong, check for disconnected patterns

---

## Best Practices

✅ **Test, don't assume** - Try search tools before SPARQL
✅ **Read MIE files** - Before writing any SPARQL
✅ **Combine approaches** - Search for breadth, SPARQL for depth
✅ **Start simple** - Escalate complexity only when needed
✅ **Verify connections** - Ensure SPARQL patterns form a connected graph

❌ Don't skip search tools based on assumptions
❌ Don't write SPARQL without reading MIE file
❌ Don't forget `up:reviewed 1` in UniProt
❌ Don't use `bif:contains` with property paths
❌ Don't create disconnected triple patterns (Cartesian products)

---

## Complementary Approach: Search + SPARQL

**For comprehensive results, use both:**

```
1. search_uniprot_entity("cardiovascular disease") → Quick overview
2. SPARQL on Disease_Annotation → Targeted precision
3. Merge results, remove duplicates → Comprehensive coverage
```

**When to use both:**
- Initial exploration (search) + comprehensive analysis (SPARQL)
- Quality check (compare both methods)
- Different aspects (search names, SPARQL annotations)

---

## Quick Examples

**Disease-protein associations:**
```python
# Start with search
search_uniprot_entity("hypertension", limit=20)
# If incomplete, add SPARQL targeting Disease_Annotation
```

**Finding drug targets:**
```python
# Search protein
search_uniprot_entity("angiotensin converting enzyme")
# Convert to ChEMBL
togoid_convertId(ids="P12821", route="uniprot,chembl_target")
# Find inhibitors in ChEMBL
```

**Pathway analysis:**
```python
search_reactome_entity("apoptosis", rows=30)
```

---

## Common Query Patterns

| Question Type | Start With | Then |
|--------------|------------|------|
| "Proteins with disease X" | `search_uniprot_entity("disease")` | SPARQL if needed |
| "Drugs targeting protein Y" | `search_uniprot_entity("protein")` | Convert to ChEMBL |
| "Structure of protein Z" | `search_uniprot_entity("protein")` | Convert to PDB |
| "Pathways involving gene A" | `search_reactome_entity("gene")` | Cross-reference |

---

## Remember

**The goal is to find the best answer efficiently, not to use the most sophisticated tool.**

1. Try search tools first (they're more capable than you think)
2. Use SPARQL for precision when needed
3. Combine both for comprehensive results
4. Always read MIE files before SPARQL
5. Verify all SPARQL patterns are properly connected to avoid Cartesian products
