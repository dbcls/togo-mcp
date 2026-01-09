# TogoMCP Usage Guide

A comprehensive, step-by-step workflow for answering user questions using TogoMCP tools. **Follow each step carefully—do not skip any step.**

---

## Table of Contents

1. [Quick Reference: Tool Categories](#quick-reference-tool-categories)
2. [Complete Workflow](#complete-workflow)
3. [Step 1: Analyze the Query](#step-1-analyze-the-query)
4. [Step 2: Select the Right Database(s)](#step-2-select-the-right-databases)
5. [Step 3: Execute Search Tools](#step-3-execute-search-tools)
6. [Step 4: Use SPARQL for Advanced Queries](#step-4-use-sparql-for-advanced-queries)
7. [Step 5: Convert and Link IDs](#step-5-convert-and-link-ids)
8. [Step 6: Retrieve Additional Information](#step-6-retrieve-additional-information)
9. [Step 7: Synthesize and Present Results](#step-7-synthesize-and-present-results)
10. [Common Query Patterns](#common-query-patterns)
11. [Critical Rules and Best Practices](#critical-rules-and-best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Quick Reference: Tool Categories

### 📋 Discovery Tools
| Tool | Purpose |
|------|---------|
| `list_databases()` | List all 22 available RDF databases with descriptions |
| `get_sparql_endpoints()` | Get SPARQL endpoint URLs and recommended search tools |
| `togoid_getAllDataset()` | List all datasets available for ID conversion |
| `togoid_getDescription()` | Get detailed descriptions of all databases |
| `ncbi_list_databases()` | List NCBI databases (Gene, Taxonomy, ClinVar, etc.) |

### 🔍 Search Tools (by Domain)

| Domain | Tool | Usage |
|--------|------|-------|
| **Proteins** | `search_uniprot_entity(query, limit)` | Search proteins, functions, diseases |
| **Chemicals/Drugs** | `search_chembl_molecule(query, limit)` | Search drug-like molecules |
| | `search_chembl_target(query, limit)` | Search drug targets |
| | `get_pubchem_compound_id(compound_name)` | Get PubChem Compound ID |
| | `get_compound_attributes_from_pubchem(id)` | Get compound properties |
| **Structures** | `search_pdb_entity(db, query, limit)` | Search PDB (db: "pdb", "cc", "prd") |
| **Pathways** | `search_reactome_entity(query, rows)` | Search pathways and reactions |
| **Reactions** | `search_rhea_entity(query, limit)` | Search biochemical reactions |
| **Medical Terms** | `search_mesh_entity(query, limit)` | Search MeSH vocabulary |
| **Ontologies** | `OLS4:search(query)` | Search all ontologies (GO, MONDO, etc.) |
| | `OLS4:searchClasses(query, ontologyId)` | Search specific ontology |
| **NCBI** | `ncbi_esearch(database, query)` | Search Gene, Taxonomy, ClinVar, MedGen, PubMed, PubChem |
| | `ncbi_esummary(database, ids)` | Get summaries for IDs |
| | `ncbi_efetch(database, ids, rettype)` | Fetch full records |

### 🔗 ID Conversion Tools (TogoID)
| Tool | Purpose |
|------|---------|
| `togoid_convertId(ids, route)` | Convert IDs between databases (e.g., "uniprot,pdb") |
| `togoid_countId(ids, source, target)` | Count convertible IDs |
| `togoid_getDataset(dataset)` | Get dataset configuration (regex, examples) |
| `togoid_getRelation(source, target)` | Get relationship between databases |
| `togoid_getAllRelation()` | Get all possible conversion routes |

### 🗄️ SPARQL Tools
| Tool | Purpose |
|------|---------|
| `get_MIE_file(dbname)` | **MANDATORY before SPARQL** - Get schema, examples |
| `get_sparql_example(dbname)` | Get example SPARQL queries |
| `get_graph_list(dbname)` | List named graphs in database |
| `run_sparql(dbname, sparql_query)` | Execute SPARQL query |

### 📚 Ontology Tools (OLS4)
| Tool | Purpose |
|------|---------|
| `OLS4:search(query)` | General ontology search |
| `OLS4:searchClasses(query, ontologyId)` | Search within specific ontology |
| `OLS4:fetch(id)` | Get entity details |
| `OLS4:getAncestors(classIri, ontologyId)` | Get parent terms |
| `OLS4:getDescendants(classIri, ontologyId)` | Get child terms |
| `OLS4:listOntologies()` | List all available ontologies |

### 📖 Dictionary Tools (PubDictionaries)
| Tool | Purpose |
|------|---------|
| `PubDictionaries:list_dictionaries()` | List available dictionaries |
| `PubDictionaries:get_dictionary_description(name)` | Get dictionary info |
| `PubDictionaries:find_ids(dictionary, labels)` | Find IDs for terms |
| `PubDictionaries:find_terms(dictionary, ids)` | Find terms for IDs |
| `PubDictionaries:search(dictionary, labels)` | Search dictionary |

---

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│  START: User Query                                                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: Analyze the Query                                         │
│  • Extract keywords, IDs, entities                                  │
│  • Identify domain (proteins, chemicals, diseases, etc.)           │
│  • Determine query type (search, convert, annotate)                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: Select Database(s)                                        │
│  • Run list_databases() if unsure                                  │
│  • Check get_sparql_endpoints() for search tools                   │
│  • Match domain to database(s)                                     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: Execute Search Tools                                      │
│  ⚠️  ALWAYS TRY SEARCH TOOLS FIRST                                 │
│  • Use domain-specific search (see table above)                    │
│  • Try multiple keywords if initial search fails                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            ┌───────────┐                   ┌───────────────┐
            │ Got IDs?  │───── YES ─────────│  STEP 5: ID   │
            │           │                   │  Conversion   │
            └───────────┘                   └───────────────┘
                    │                               │
                   NO                               │
                    │                               │
                    ▼                               │
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: SPARQL (When Search Insufficient)                         │
│  ⚠️  MANDATORY: Run get_MIE_file(dbname) FIRST                     │
│  • Use for complex queries, specific annotations                   │
│  • Always include LIMIT clause                                     │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6: Retrieve Additional Information                           │
│  • ncbi_esummary() for detailed metadata                           │
│  • ncbi_efetch() for full records                                  │
│  • OLS4:fetch() for ontology details                               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 7: Synthesize Results                                        │
│  • Combine data from multiple sources                              │
│  • Cite databases used                                             │
│  • Note any limitations or missing data                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Analyze the Query

### ✅ CHECKLIST - Do Not Skip

- [ ] **Extract keywords**: Identify proteins, genes, diseases, chemicals, species
- [ ] **Identify IDs**: Look for existing IDs (UniProt: P12345, PDB: 1ABC, etc.)
- [ ] **Determine domain**: Which biological area? (See table below)
- [ ] **Clarify intent**: What does the user want to know?

### Domain Classification

| Domain | Keywords to Look For | Primary Databases |
|--------|---------------------|-------------------|
| **Proteins** | protein, enzyme, receptor, kinase, sequence | UniProt, PDB, Ensembl |
| **Genes** | gene, transcript, expression, chromosome | NCBI Gene, Ensembl, GO |
| **Chemicals/Drugs** | drug, compound, molecule, inhibitor, SMILES | ChEMBL, PubChem, ChEBI |
| **Diseases** | disease, disorder, syndrome, cancer, condition | MONDO, MeSH, MedGen, ClinVar |
| **Pathways** | pathway, signaling, metabolism, process | Reactome, GO, KEGG |
| **Reactions** | reaction, catalysis, enzyme activity | Rhea, Reactome |
| **Taxonomy** | species, organism, bacteria, human, mouse | NCBI Taxonomy, BacDive |
| **Structures** | structure, 3D, crystal, cryo-EM, NMR | PDB |
| **Variants** | mutation, variant, SNP, polymorphism | ClinVar, dbSNP |
| **Glycans** | glycan, sugar, carbohydrate, glycoprotein | GlyCosmos, GlyTouCan |
| **Literature** | paper, publication, abstract, citation | PubMed, PubTator |

---

## Step 2: Select the Right Database(s)

### ✅ CHECKLIST - Do Not Skip

- [ ] **If unsure**: Run `list_databases()` to see all 22 databases
- [ ] **Check recommended search tools**: Run `get_sparql_endpoints()` 
- [ ] **For ID conversion**: Run `togoid_getAllDataset()` to see available routes

### Database Quick Reference

| Category | Database | Description | Search Tool |
|----------|----------|-------------|-------------|
| **Proteins** | `uniprot` | 444M proteins, functions, diseases | `search_uniprot_entity` |
| | `pdb` | 204K+ 3D structures | `search_pdb_entity` |
| | `ensembl` | Genome annotations, 100+ species | SPARQL only |
| **Chemicals** | `pubchem` | 119M compounds, 1.7M bioassays | `ncbi_esearch` |
| | `chembl` | 2.4M+ bioactive molecules | `search_chembl_molecule/target` |
| | `chebi` | 217K+ chemical entities | `OLS4:searchClasses` |
| **Diseases** | `mondo` | 30K+ disease classes | `OLS4:searchClasses` |
| | `mesh` | 30K descriptors, 250K chemicals | `search_mesh_entity` |
| | `medgen` | 233K+ clinical concepts | `ncbi_esearch` |
| | `clinvar` | 3.5M+ variant records | `ncbi_esearch` |
| | `nando` | Japanese intractable diseases | `OLS4:searchClasses` |
| **Pathways** | `reactome` | 22K+ pathways, 30+ species | `search_reactome_entity` |
| | `go` | 48K+ GO terms | `OLS4:searchClasses` |
| **Reactions** | `rhea` | 17K+ biochemical reactions | `search_rhea_entity` |
| **Genes** | `ncbigene` | 57M+ gene entries | `ncbi_esearch` |
| **Taxonomy** | `taxonomy` | 3M+ organisms | `ncbi_esearch` |
| **Literature** | `pubmed` | Biomedical literature | `ncbi_esearch` |
| | `pubtator` | Entity annotations from PubMed | SPARQL only |
| **Microbiology** | `bacdive` | 97K+ bacterial strains | SPARQL only |
| | `mediadive` | 3.3K culture media recipes | SPARQL only |
| | `amrportal` | AMR surveillance data | SPARQL only |
| **Sequences** | `ddbj` | Nucleotide sequences | SPARQL only |
| **Glycans** | `glycosmos` | Glycan structures | SPARQL only |

---

## Step 3: Execute Search Tools

### ✅ CHECKLIST - Do Not Skip

- [ ] **ALWAYS try search tools FIRST** - They are often more capable than expected
- [ ] **Use the correct tool** for your domain (see table below)
- [ ] **Try multiple keywords** if initial search returns insufficient results
- [ ] **Adjust limit parameter** (default usually 20, increase if needed)

### Search Tool Decision Matrix

```
What are you searching for?
│
├─► Proteins/Enzymes ──────────► search_uniprot_entity(query, limit=20)
│   (includes disease associations!)
│
├─► Drugs/Compounds ───────────► search_chembl_molecule(query, limit=20)
│
├─► Drug Targets ──────────────► search_chembl_target(query, limit=20)
│
├─► 3D Structures ─────────────► search_pdb_entity(db="pdb", query, limit=20)
│   Small molecules in PDB ────► search_pdb_entity(db="cc", query, limit=20)
│   Peptides in PDB ───────────► search_pdb_entity(db="prd", query, limit=20)
│
├─► Pathways/Processes ────────► search_reactome_entity(query, rows=30)
│
├─► Biochemical Reactions ─────► search_rhea_entity(query, limit=100)
│
├─► Medical Terms/MeSH ────────► search_mesh_entity(query, limit=10)
│
├─► Ontology Terms ────────────► OLS4:search(query)
│   (GO, MONDO, ChEBI, etc.)    or OLS4:searchClasses(query, ontologyId)
│
├─► NCBI Data ─────────────────► ncbi_esearch(database, query)
│   Genes ─────────────────────► ncbi_esearch("gene", query)
│   Taxonomy ──────────────────► ncbi_esearch("taxonomy", query)
│   ClinVar ───────────────────► ncbi_esearch("clinvar", query)
│   MedGen ────────────────────► ncbi_esearch("medgen", query)
│   PubMed ────────────────────► ncbi_esearch("pubmed", query)
│   PubChem Compound ──────────► ncbi_esearch("pccompound", query)
│
└─► Chemical by Name ──────────► get_pubchem_compound_id(compound_name)
                                 → get_compound_attributes_from_pubchem(id)
```

### Search Tips

1. **Start broad, then narrow**: Begin with simple terms, add specificity if needed
2. **Use synonyms**: If "hypertension" doesn't work, try "high blood pressure"
3. **Include species**: Add "human" or organism name for more relevant results
4. **Check multiple databases**: Cross-reference results for completeness

---

## Step 4: Use SPARQL for Advanced Queries

### ⚠️ MANDATORY PREREQUISITE

**BEFORE writing ANY SPARQL query, you MUST:**

```python
# Step 4.1: ALWAYS run this first
get_MIE_file(dbname)  # Returns schema, RDF patterns, and examples
```

### ✅ CHECKLIST - Do Not Skip

- [ ] **Run `get_MIE_file(dbname)`** - Contains ShEx schema, RDF examples, SPARQL examples
- [ ] **Optionally run `get_sparql_example(dbname)`** - Get additional examples
- [ ] **Check `get_graph_list(dbname)`** if you need specific named graphs
- [ ] **Include LIMIT clause** - Always limit results (20-100)
- [ ] **Apply database-specific rules** (see below)

### When to Use SPARQL

| Use Search Tools When... | Use SPARQL When... |
|--------------------------|-------------------|
| Looking for entities by name | Need specific annotation types |
| Simple keyword search | Complex boolean logic (AND, NOT) |
| Broad exploration | Precise field targeting |
| Quick results needed | Aggregations (COUNT, GROUP BY) |
| | Cross-linking within database |

### Critical Database-Specific Rules

| Database | Critical Rule |
|----------|--------------|
| **UniProt** | ALWAYS filter `?protein up:reviewed 1` for Swiss-Prot quality |
| **ChEMBL** | Use `FROM <http://rdf.ebi.ac.uk/dataset/chembl>` |
| **Full-text search** | Split property paths when using `bif:contains` |
| **All databases** | ALWAYS use `LIMIT` (start with 20-100) |

### SPARQL Workflow

```python
# 1. Get the schema and examples (MANDATORY)
mie_info = get_MIE_file("uniprot")

# 2. Optionally get more examples
examples = get_sparql_example("uniprot")

# 3. Check named graphs if needed
graphs = get_graph_list("uniprot")

# 4. Write and execute query
query = """
PREFIX up: <http://purl.uniprot.org/core/>
SELECT ?protein ?name
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:recommendedName/up:fullName ?name .
  FILTER(CONTAINS(LCASE(?name), "kinase"))
}
LIMIT 50
"""

results = run_sparql("uniprot", query)
```

---

## Step 5: Convert and Link IDs

### ✅ CHECKLIST - Do Not Skip

- [ ] **Check if conversion route exists**: Use `togoid_getRelation(source, target)`
- [ ] **Use correct database keys**: e.g., "uniprot", "pdb", "ncbigene"
- [ ] **Handle missing conversions**: Not all IDs have mappings

### ID Conversion Workflow

```python
# 1. Check available datasets
all_datasets = togoid_getAllDataset()

# 2. Check if route exists between two databases
relation = togoid_getRelation("uniprot", "pdb")

# 3. Convert IDs
result = togoid_convertId(
    ids="P04637,P17612",           # Comma-separated IDs
    route="uniprot,pdb"            # Source,target
)

# 4. For multi-hop conversions
result = togoid_convertId(
    ids="P04637",
    route="uniprot,ncbigene,ensembl_gene"  # Chain of databases
)
```

### Common Conversion Routes

| From | To | Route |
|------|-----|-------|
| UniProt → PDB | `togoid_convertId(ids, "uniprot,pdb")` |
| UniProt → NCBI Gene | `togoid_convertId(ids, "uniprot,ncbigene")` |
| UniProt → ChEMBL Target | `togoid_convertId(ids, "uniprot,chembl_target")` |
| NCBI Gene → Ensembl | `togoid_convertId(ids, "ncbigene,ensembl_gene")` |
| PDB → UniProt | `togoid_convertId(ids, "pdb,uniprot")` |
| ChEBI → PubChem | `togoid_convertId(ids, "chebi,pubchem_compound")` |

---

## Step 6: Retrieve Additional Information

### ✅ CHECKLIST - Do Not Skip

- [ ] **After getting IDs**: Fetch detailed information
- [ ] **Use appropriate fetch tool** for the data type
- [ ] **Handle missing data gracefully**

### Retrieval Tools

| Data Type | Tool | Usage |
|-----------|------|-------|
| **NCBI Records** | `ncbi_esummary(database, ids)` | Get summaries for gene, pubmed, etc. |
| | `ncbi_efetch(database, ids, rettype)` | Get full records (fasta, gb, xml) |
| **Ontology Terms** | `OLS4:fetch(id)` | Get term details |
| | `OLS4:getAncestors(classIri, ontologyId)` | Get parent terms |
| | `OLS4:getDescendants(classIri, ontologyId)` | Get child terms |
| **PubChem** | `get_compound_attributes_from_pubchem(id)` | Get compound properties |
| **Dictionaries** | `PubDictionaries:find_terms(dict, ids)` | Get labels for IDs |

### Example: Complete Information Retrieval

```python
# 1. Search for a protein
results = search_uniprot_entity("BRCA1 human", limit=5)
# → Get UniProt ID: P38398

# 2. Convert to other databases
pdb_ids = togoid_convertId("P38398", "uniprot,pdb")
gene_ids = togoid_convertId("P38398", "uniprot,ncbigene")

# 3. Get detailed gene information
gene_summary = ncbi_esummary("gene", gene_ids)

# 4. Get ontology annotations
go_terms = OLS4:search("BRCA1")
```

---

## Step 7: Synthesize and Present Results

### ✅ CHECKLIST - Do Not Skip

- [ ] **Combine information** from all sources queried
- [ ] **Cite databases used** (UniProt, PDB, ChEMBL, etc.)
- [ ] **Note limitations**: Missing data, incomplete conversions
- [ ] **Provide IDs and links** for user follow-up

### Response Template

```markdown
## Summary
[Brief answer to the user's question]

## Details
[Organized findings from databases]

## Data Sources
- UniProt: [IDs used]
- PDB: [IDs used]
- [Other databases]

## Notes
- [Any limitations or caveats]
- [Suggestions for further exploration]
```

---

## Common Query Patterns

### Pattern 1: Find Proteins Associated with a Disease

```python
# Step 1: Search UniProt (includes disease associations!)
proteins = search_uniprot_entity("Alzheimer disease", limit=50)

# Step 2: If more precision needed, use SPARQL
get_MIE_file("uniprot")  # MANDATORY
query = """
PREFIX up: <http://purl.uniprot.org/core/>
SELECT ?protein ?name ?disease
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:recommendedName/up:fullName ?name ;
           up:annotation ?annot .
  ?annot a up:Disease_Annotation ;
         rdfs:comment ?disease .
  FILTER(CONTAINS(LCASE(?disease), "alzheimer"))
}
LIMIT 50
"""
results = run_sparql("uniprot", query)
```

### Pattern 2: Find Drug Targets and Inhibitors

```python
# Step 1: Search for the protein target
protein = search_uniprot_entity("angiotensin converting enzyme human", limit=5)
# → UniProt ID: P12821

# Step 2: Convert to ChEMBL target
chembl_target = togoid_convertId("P12821", "uniprot,chembl_target")

# Step 3: Search for inhibitors in ChEMBL
inhibitors = search_chembl_molecule("ACE inhibitor", limit=20)

# Step 4: Get compound details from PubChem
compound_id = get_pubchem_compound_id("lisinopril")
properties = get_compound_attributes_from_pubchem(compound_id)
```

### Pattern 3: Find Protein Structure

```python
# Step 1: Search for protein
protein = search_uniprot_entity("p53 human", limit=5)
# → UniProt ID: P04637

# Step 2: Convert to PDB
pdb_ids = togoid_convertId("P04637", "uniprot,pdb")

# Step 3: Or search PDB directly
structures = search_pdb_entity(db="pdb", query="p53 tumor suppressor", limit=20)
```

### Pattern 4: Explore Pathways

```python
# Step 1: Search Reactome
pathways = search_reactome_entity("apoptosis", rows=30)

# Step 2: For related reactions
reactions = search_rhea_entity("caspase", limit=50)

# Step 3: Get GO terms for biological process
go_terms = OLS4:searchClasses("programmed cell death", ontologyId="go")
```

### Pattern 5: Cross-Database Integration

```python
# Goal: From gene name to structures, drugs, and pathways

# 1. Find gene
gene = ncbi_esearch("gene", "EGFR human")
# → Gene ID: 1956

# 2. Get UniProt ID
uniprot_ids = togoid_convertId("1956", "ncbigene,uniprot")
# → P00533

# 3. Get structures
pdb_ids = togoid_convertId("P00533", "uniprot,pdb")

# 4. Get drug targets
chembl_targets = togoid_convertId("P00533", "uniprot,chembl_target")

# 5. Search pathways
pathways = search_reactome_entity("EGFR signaling", rows=20)
```

---

## Critical Rules and Best Practices

### ✅ ALWAYS DO

1. **Try search tools first** - They're more capable than you might think
2. **Run `get_MIE_file()` before SPARQL** - This is mandatory, not optional
3. **Use `LIMIT` in all SPARQL queries** - Start with 20-100
4. **Filter UniProt by `up:reviewed 1`** - For Swiss-Prot quality data
5. **Check conversion routes exist** before calling `togoid_convertId()`
6. **Cite your data sources** in the final response
7. **Handle empty results gracefully** - Try alternative keywords

### ❌ NEVER DO

1. **Don't skip to SPARQL** without trying search tools first
2. **Don't write SPARQL** without reading MIE file first
3. **Don't assume search tools are limited** - Test them first
4. **Don't forget `up:reviewed 1`** in UniProt queries (gets TrEMBL noise)
5. **Don't omit LIMIT** - Can cause timeouts with large datasets
6. **Don't use `bif:contains` with property paths** - Split them
7. **Don't assume all IDs convert** - Check conversion availability

---

## Troubleshooting

### Problem: Search Returns No Results

```
✓ Check spelling and try synonyms
✓ Try broader terms
✓ Remove species filter temporarily
✓ Try a different database
✓ Use SPARQL with get_MIE_file() for complex queries
```

### Problem: SPARQL Query Fails

```
✓ Did you run get_MIE_file() first? (MANDATORY)
✓ Check prefix declarations
✓ Add LIMIT clause
✓ For UniProt: add up:reviewed 1
✓ For ChEMBL: add FROM <http://rdf.ebi.ac.uk/dataset/chembl>
✓ Check property paths - split if using bif:contains
```

### Problem: ID Conversion Returns Empty

```
✓ Check if route exists: togoid_getRelation(source, target)
✓ Verify ID format matches expected pattern
✓ Try alternative routes (multi-hop conversion)
✓ Not all IDs have mappings - this is expected
```

### Problem: Timeout or Slow Query

```
✓ Reduce LIMIT
✓ Add more specific filters
✓ For UniProt: MUST use up:reviewed 1
✓ Consider using search tools instead
```

---

## Appendix: All Available Databases

Run `list_databases()` to see the complete list of 22 databases:

| Database | Domain | Description |
|----------|--------|-------------|
| amrportal | Microbiology | Antimicrobial resistance data |
| bacdive | Microbiology | Bacterial strain information |
| chebi | Chemistry | Chemical entities of biological interest |
| chembl | Chemistry/Drugs | Bioactive molecules, drug data |
| clinvar | Genetics | Genomic variation and health |
| ddbj | Sequences | Nucleotide sequence data |
| ensembl | Genomics | Genome annotations |
| glycosmos | Glycobiology | Glycan structures |
| go | Ontology | Gene Ontology terms |
| medgen | Medicine | Medical genetics concepts |
| mediadive | Microbiology | Culture media recipes |
| mesh | Medicine | Medical subject headings |
| mondo | Diseases | Disease ontology |
| nando | Diseases | Japanese intractable diseases |
| ncbigene | Genes | NCBI Gene database |
| pdb | Structures | Protein 3D structures |
| pubchem | Chemistry | Chemical compounds |
| pubmed | Literature | Biomedical publications |
| pubtator | Literature | Entity annotations from PubMed |
| reactome | Pathways | Biological pathways |
| rhea | Reactions | Biochemical reactions |
| taxonomy | Taxonomy | Organism classification |
| uniprot | Proteins | Protein sequences and functions |

---

**Remember: The goal is to find the best answer efficiently. Start simple, escalate complexity only when needed.**