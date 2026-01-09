# Research Article Analysis Workflow using TogoMCP RDF Databases

## Introduction

This document outlines a comprehensive workflow for analyzing research articles using TogoMCP RDF databases.

**Analyze the uploaded research article using TogoMCP RDF databases.**

Follow this protocol:

## PHASE 1: EXTRACT KEY ELEMENTS

1. **Main Research Question**: What biological question is being addressed?

2. **Key Conclusions** (3-5 main findings)

3. **Experimental Logic**: For each conclusion:
   - Hypothesis → Experiment → Evidence → Conclusion

4. **Key Entities**: List all proteins (with IDs), genes, metabolites, pathways, cell types

## PHASE 2: DATABASE INVESTIGATION

### Step 1: Identify Relevant Databases
Run `list_databases()` to see all available databases and their descriptions.
Select databases relevant to your entities (proteins, pathways, compounds, etc.)

### Step 2: ⚠️ CRITICAL - Study MIE Files First
**BEFORE writing any SPARQL queries, you MUST read and study the MIE files:**

- `get_MIE_file(dbname)` for ALL selected databases
- Common databases: uniprot, reactome, rhea, chembl, pubchem, go, pdb, ncbigene, clinvar, mesh
- **Read the entire MIE file** to understand:
  - Schema structure and key properties
  - Required filters (e.g., `up:reviewed 1` for UniProt)
  - Performance optimizations (e.g., `bif:contains`, `FROM` clauses)
  - Common errors and anti-patterns
  - Example queries as templates

**Key MIE Insights to Apply:**

**UniProt:**
- ALWAYS filter `up:reviewed 1` (Swiss-Prot quality, 99.8% reduction)
- Use `bif:contains` but SPLIT property paths (no `/` with bif:contains)
- Organism: `up:organism <http://purl.uniprot.org/taxonomy/9606>` (never use mnemonic suffixes)
- COUNT queries require reviewed=1 filter to prevent timeout

**Reactome:**
- ALWAYS use `FROM <http://rdf.ebi.ac.uk/dataset/reactome>`
- Use `^^xsd:string` for bp:db comparisons (datatype matching)
- Use `bif:contains` for text searches, not FILTER(CONTAINS())
- Start property paths from specific entities, not unbounded variables

**Rhea:**
- Query reactions via `rdfs:subClassOf rhea:Reaction`
- Use `bif:contains` on rhea:equation for fast searches
- Reactions have 4 forms: master, L→R, R→L, bidirectional
- Always add LIMIT to exploratory queries

**GO:**
- ALWAYS use `FROM <http://rdfportal.org/ontology/go>`
- ALWAYS use `DISTINCT` (multiple graph storage causes duplicates)
- Filter: `STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_")`
- Use `STR(?namespace)` for namespace comparisons (avoid datatype mismatch)

### Step 3: Keyword Searches (Initial Discovery)
For each key entity:
- `search_uniprot_entity(query)` - proteins
- `search_reactome_entity(query)` - pathways  
- `search_rhea_entity(query)` - reactions
- `search_chembl_molecule(query)` - compounds
- `search_pdb_entity(db, query)` - structures
- Other keyword search APIs documented in the respective MIE file

Document the IDs obtained (UniProt IDs, Reactome IDs, Rhea IDs, etc.)

### Step 4: ⚠️ CRITICAL - Complex SPARQL Queries for Deep Validation

**DO NOT skip this step!** Complex queries reveal evidence that keyword searches miss.

#### For Each Major Claim in the Article:

**A. Enzymatic Mechanisms**
- Query Rhea for exact reaction equations (reveals stoichiometry, cofactors, products)
- Link reactions to EC numbers
- Verify EC numbers in UniProt for claimed enzymes
- Check GO molecular function terms for enzyme activities
- Example chain: Protein → EC number → Rhea reaction → Products (e.g., NH4+, metabolites)

**B. Metabolic Pathways**
- Query Reactome for complete pathway structure (not just names)
- Get all reactions in pathway with reactants/products
- Trace metabolite flow through reactions
- Verify substrate-product connections claimed in article
- Check for pathway compartmentalization (mitochondrial, cytosolic, etc.)

**C. Protein Functions and Interactions**
- Query UniProt for complete functional annotations (not just names)
- Get all GO terms (biological process, molecular function, cellular component)
- Query for protein-protein interactions if claimed
- Check cross-references to other databases (PDB, Reactome, KEGG)
- Verify tissue/cell-type specificity if claimed

**D. Cross-Database Validation Chains**
When article claims A causes B causes C:
- Build query chains that traverse multiple databases
- Example: UniProt protein → GO molecular function → Rhea reaction → Product metabolite → Reactome pathway
- Document complete evidence chain with database IDs

**E. Quantitative Validation**
- Query for binding constants if available (ChEMBL)
- Check for structure data (PDB) supporting claimed interactions
- Verify chemical properties (PubChem) supporting mechanisms
- Query disease associations (ClinVar, MedGen) if relevant

#### Template Complex SPARQL Queries:

**Template 1: Verify Enzyme Catalyzes Specific Reaction**
```sparql
# Step 1: Find reaction in Rhea
# Search for reactions with substrate + product keywords
# Get reaction equation, EC number, GO terms

# Step 2: Verify enzyme has EC number in UniProt
# Query protein for up:enzyme property
# Get GO molecular function terms

# Step 3: Link via EC number
# Confirm EC matches between Rhea and UniProt
```

**Template 2: Validate Metabolic Pathway Connection**
```sparql
# Step 1: Query Reactome pathway structure
# Get all reactions in pathway
# Extract reactants and products for each reaction

# Step 2: Verify substrate X produces product Y
# Check if Y appears as product in one reaction
# Check if Y appears as substrate in next reaction
# Confirm metabolic flow claimed in article
```

**Template 3: Cross-Database Evidence Chain**
```sparql
# Step 1: Start from protein in UniProt
# Get GO terms, EC numbers, cross-references

# Step 2: Follow EC to Rhea reactions
# Get reaction equations and products

# Step 3: Follow products to Reactome pathways
# Verify claimed pathway membership

# Step 4: Check GO biological process
# Confirm process matches claimed function
```

### Step 5: Document Query Results with Evidence Chains

For each major claim, document:
- **Database IDs cited**: UniProt P04424, GO:0019676, RHEA:15133, etc.
- **Evidence chain**: Protein → Function → Reaction → Product → Pathway
- **Exact quotes** from definitions/descriptions
- **Quantitative data** (KD values, stoichiometry, etc.)
- **What's missing**: Expected but absent annotations

## PHASE 3: EVIDENCE SYNTHESIS

### For Each Major Claim:

**✅ Supporting Evidence from Complex Queries**
- Exact reaction equations confirming mechanism (cite Rhea IDs)
- Complete pathway structures confirming metabolite flow (cite Reactome IDs)
- GO term definitions confirming biological processes (cite GO IDs)
- Cross-database chains supporting claimed connections
- Structural data supporting interactions (cite PDB IDs)
- Quantitative support (KD, IC50, stoichiometry)

**⚠️ Contradictory/Nuanced Evidence**
- Unexpected pathway components found
- Alternative mechanisms in databases
- Missing expected intermediate steps
- Conflicting substrate specificities
- Different cellular localizations

**🆕 Novel Discoveries (Not in Databases)**
- New protein functions (function exists, but context new)
- New ligand-receptor pairs (both known, but binding new)
- New pathway connections (pathways known, but link new)
- New regulatory mechanisms (proteins known, but regulation new)
- Cell-type-specific mechanisms (general mechanism known, but specificity new)

**❌ Critical Gaps Requiring Validation**
- Key enzymes missing expected EC numbers
- Reactions missing critical cofactors
- Pathways missing claimed components
- Proteins lacking claimed GO terms
- No structural data for claimed binding

## PHASE 4: ASSESSMENT

**Detailed Validation Scores:**

### For Each Major Conclusion:

| Aspect | Score (1-10) | RDF Evidence | Database IDs |
|--------|--------------|--------------|--------------|
| Enzymatic Mechanism | | Rhea reaction equation | RHEA:XXXXX |
| Pathway Connectivity | | Reactome structure | R-HSA-XXXXX |
| Molecular Function | | GO/UniProt terms | GO:XXXXXXX, P##### |
| Structural Support | | PDB structures | PDB: #### |
| Prior Knowledge | | Literature in databases | |
| Novelty Assessment | | Database gaps identified | |

**Overall Article Assessment:**

| Criterion | Score (1-10) | Evidence from Complex Queries |
|-----------|--------------|-------------------------------|
| Biochemical Plausibility | | (Exact reactions, stoichiometry) |
| Pathway Connectivity | | (Complete metabolic flows) |
| Mechanistic Detail | | (Cofactors, intermediates verified) |
| Database Support | | (Cross-database evidence chains) |
| Novelty Confirmed | | (Known components, new connections) |

**Evidence Quality Categories:**

- **★★★★★ Perfect Validation**: Exact mechanisms in databases (e.g., RHEA reaction matches claim)
- **★★★★☆ Strong Support**: Components all verified, connections inferred (e.g., substrate + enzyme + product all confirmed)
- **★★★☆☆ Moderate Support**: Major components verified, some gaps (e.g., enzyme confirmed but not all products)
- **★★☆☆☆ Weak Support**: Key components missing or contradictory
- **★☆☆☆☆ No Support**: Claims contradict database evidence

**Summary:**
- **Strengths**: Specific RDF evidence chains supporting claims
- **Novel Contributions**: What new biology is being added to existing knowledge
- **Validation Priorities**: What experimental verification is most critical
- **Database Update Recommendations**: What should be added to RDF databases

---

## QUALITY CHECKLIST

### Database Investigation:
- [ ] Ran `list_databases()` to identify relevant databases
- [ ] ⚠️ Read complete MIE files for ALL databases used
- [ ] ⚠️ Understood critical patterns (FROM clauses, reviewed=1, etc.)
- [ ] Keyword searches for all key entities
- [ ] Documented all obtained database IDs

### Complex SPARQL Queries:
- [ ] ⚠️ Queried Rhea for exact reaction mechanisms
- [ ] ⚠️ Verified enzyme EC numbers in UniProt
- [ ] ⚠️ Traced complete metabolic pathways in Reactome
- [ ] ⚠️ Retrieved GO term definitions (not just labels)
- [ ] ⚠️ Built cross-database evidence chains
- [ ] Queried for quantitative data (KD, structures, etc.)
- [ ] Documented exact equations, stoichiometry, cofactors

### Evidence Documentation:
- [ ] Cited specific database IDs for all claims
- [ ] Documented complete evidence chains (Protein→Reaction→Product→Pathway)
- [ ] Recorded positive AND negative results
- [ ] Identified novel vs. known components
- [ ] Noted critical gaps requiring experimental validation

### Assessment Quality:
- [ ] Provided validation scores with specific RDF evidence
- [ ] Distinguished between different evidence quality levels
- [ ] Assessed novelty via database gaps
- [ ] Made database update recommendations
- [ ] Identified validation priorities

---

## KEY REMINDERS

1. **MIE files are not optional** - They contain critical architecture knowledge
2. **Complex queries reveal more than keywords** - Exact mechanisms, stoichiometry, evidence chains
3. **Cross-database validation is powerful** - Same finding in multiple databases is strong evidence
4. **Document complete evidence chains** - Not just "protein X exists" but "X catalyzes Y producing Z via mechanism M"
5. **Distinguish component validation from novel connections** - Known components in new contexts is valuable science

---

**Template v2.0** | 2025-12-30 | Enhanced with mandatory complex SPARQL and MIE file analysis
