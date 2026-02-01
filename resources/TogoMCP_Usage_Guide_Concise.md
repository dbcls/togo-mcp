# TogoMCP Usage Guide - CONCISE VERSION

## STEP 0: Complexity Assessment (MANDATORY FIRST)

**SIMPLE** → Search tools may suffice:
- "Find protein X", "Get ID for Y", Single lookups

**COMPLEX** → SPARQL MANDATORY:
- Keywords: "how", "mechanism", "pathway", "cascade", "lead to", "interactions"
- Multi-level models, reactions, drug mechanisms
- **Your original question about Alzheimer's? COMPLEX → SPARQL REQUIRED**

---

## The Workflow

```
0. Classify: SIMPLE or COMPLEX?
   └→ If COMPLEX: Mark "SPARQL MANDATORY"

1. Run search tools (reconnaissance only)

2. Decision Checkpoint:
   ❓ Have substrate→enzyme→product chains?
   ❓ Have specific reactions/interactions?
   ❓ Can explain MECHANISM (not just list entities)?
   
   If ANY NO or question was COMPLEX → Run SPARQL

3. Execute SPARQL (if required):
   - ALWAYS run get_MIE_file(dbname) first
   - Run 3-5 queries: reactions, interactions, xrefs, regulation
   
4. Final check before answering:
   ✓ Can explain HOW things work?
   ✓ Have mechanistic details?
   If NO → More SPARQL queries needed

5. Synthesize answer
```

---

## SPARQL Decision Matrix

| Situation | SPARQL? |
|-----------|---------|
| User asks "how/mechanism/pathway" | ✅ YES |
| Search gave only names/IDs | ✅ YES |
| Building multi-level models | ✅ YES |
| Need reaction details | ✅ YES |
| Simple entity lookup | ⚠️ Maybe |

---

## Mandatory SPARQL Queries for Complex Questions

### 1. Pathway/Reaction Details
```sparql
SELECT ?reaction ?substrate ?product ?enzyme
WHERE {
  # Pathway with reactions
  # Left/right (substrate/product)
  # Catalysis (enzyme)
}
```

### 2. Cross-References
```sparql
SELECT ?entity ?uniprotID ?chebiID
WHERE {
  # Entity with xrefs
  # Use ^^xsd:string for db names
}
```

### 3. Interactions/Complexes
```sparql
SELECT ?protein1 ?protein2 ?complex
WHERE {
  # Complex components
  # Binding interactions
}
```

---

## Common Mistakes

❌ "Search results look good" → Still run SPARQL for complex questions
❌ Explaining from general knowledge → Use database mechanistic data
❌ One SPARQL query → Need 3-5 complementary queries
❌ Skipping get_MIE_file() → Always read schema first

---

## Key Rules

1. **COMPLEX questions ALWAYS need SPARQL** - no exceptions
2. **Search tools = reconnaissance, SPARQL = mechanisms**
3. **Before responding: "Can I explain HOW?" If no → more queries**
4. **Quality gate: Have substrate→enzyme→product chains?**

---

## Example Application

**Q: "How does amyloid-β lead to neurodegeneration?"**

✓ Step 0: COMPLEX (has "how", multi-level)
✓ Step 1: Search tools (get protein/pathway IDs)
✓ Step 2: Checkpoint: No mechanism details → SPARQL required
✓ Step 3: Run get_MIE_file("reactome")
✓ Step 3: Query amyloid processing reactions
✓ Step 3: Query inflammatory cascade
✓ Step 3: Query cross-references
✓ Step 4: Can explain mechanism? Yes → Proceed
✓ Step 5: Synthesize with mechanistic details

---

## Self-Check (Before Every Response)

1. Did I classify complexity? 
2. If COMPLEX, did I run SPARQL?
3. Can I explain HOW (not just WHAT)?
4. Do I have reaction chains?

**Any NO = Not done yet**
