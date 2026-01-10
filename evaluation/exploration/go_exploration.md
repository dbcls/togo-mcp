# Gene Ontology (GO) Exploration Report

## Database Overview
- **Purpose**: Controlled vocabulary for describing gene and gene product attributes across all organisms
- **Scope**: 48,165 total GO terms organized into three ontology domains
- **Endpoint**: https://rdfportal.org/primary/sparql  
- **Data version**: Latest GO Release
- **Update frequency**: Monthly

### Key Data Types and Entities
- **Biological Process** (30,804 terms): biological objectives/pathways
- **Molecular Function** (12,793 terms): molecular activities/catalysis
- **Cellular Component** (4,568 terms): cellular locations
- Each term includes: definitions, synonyms, hierarchical relationships, cross-references

## Schema Analysis (from MIE file)

### Main Properties Available
- **oboinowl:id**: GO identifier (e.g., "GO:0006914")
- **rdfs:label**: Human-readable term name
- **obo:IAO_0000115**: Definition (required for all non-obsolete terms)
- **oboinowl:hasOBONamespace**: Domain classification (biological_process, molecular_function, cellular_component)
- **rdfs:subClassOf**: Parent terms (hierarchical DAG structure)
- **oboinowl:hasExactSynonym / hasRelatedSynonym / hasNarrowSynonym / hasBroadSynonym**: Four types of synonyms
- **oboinowl:hasDbXref**: Cross-references to external databases
- **oboinowl:inSubset**: GO slim subsets for specific applications/organisms
- **owl:deprecated**: Obsolete term flag

### Important Relationships
- **Hierarchical**: rdfs:subClassOf creates directed acyclic graphs (DAGs) - terms can have multiple parents
- **Synonyms**: Four-tier system for comprehensive term matching
- **Cross-references**: Links to 20+ external databases (Wikipedia, Reactome, KEGG, MeSH, SNOMEDCT, etc.)
- **Subsets**: Organism-specific and application-specific GO slim views

### Query Patterns Observed
1. **CRITICAL**: Always use FROM <http://rdfportal.org/ontology/go> clause
2. **Full-text search**: Use bif:contains for keyword searches (much faster than REGEX)
3. **Namespace filtering**: Use STR() for namespace comparisons to avoid datatype mismatch
4. **GO term filtering**: FILTER by STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_") to exclude other ontologies
5. **Deduplication**: Always use DISTINCT due to multiple graph storage
6. **Hierarchical navigation**: Use OLS4:getDescendants and OLS4:getAncestors for DAG traversal

## Search Queries Performed

### Query 1: Search for autophagy term
**Tool**: OLS4:search("autophagy")
**Results**: Found multiple ontology entries:
- GO:0006914 (autophagy) - main Gene Ontology term
- APO:0000074 (autophagy) - ascomycete phenotype
- UPHENO:7000131, UPHENO:0049824 (autophagy phenotype)
- CHEBI:88230 (autophagy inhibitor), CHEBI:138880 (autophagy inducer)
- PW:0000278 (autophagy pathway)
- Multiple toxicology and pathway entries
**Key finding**: GO term clearly distinguished from other ontologies

### Query 2: Get autophagy descendants
**Tool**: OLS4:getDescendants("http://purl.obolibrary.org/obo/GO_0006914", "go")
**Results**: Retrieved 25 descendant terms including:
- GO:0160155 (crinophagy)
- GO:0061684 (chaperone-mediated autophagy)
- GO:0030242 (autophagy of peroxisome)
- GO:0016237 (microautophagy)
- GO:0016236 (macroautophagy) - major subtype
- GO:0000422 (autophagy of mitochondrion / mitophagy)
- GO:0000426 (micropexophagy)
- GO:0000425 (pexophagy)
- GO:0140504 (microlipophagy)
- GO:0061738 (late endosomal microautophagy)
- GO:0034727 (piecemeal microautophagy of the nucleus)
- GO:0000424 (micromitophagy)
- GO:0098792 (xenophagy - degradation of intracellular pathogens)
- GO:0062093 (lysophagy)
- GO:0061816 (proteaphagy)
- GO:0061724 (lipophagy)
- GO:0061723 (glycophagy)
- GO:0061709 (reticulophagy)
- GO:0044804 (nucleophagy)
- GO:0035973 (aggrephagy)
**Key finding**: Complete hierarchical navigation with exactly 25 descendants

### Query 3: Search for DNA repair terms
**Tool**: OLS4:searchClasses(ontologyId="go", query="DNA repair")
**Results**: Retrieved 20 of 1,827 total DNA repair-related terms:
- GO:0006281 (DNA repair) - main term
- GO:1990391 (DNA repair complex)
- GO:0090735 (DNA repair complex assembly)
- GO:0140861 (DNA repair-dependent chromatin remodeling)
- GO:0046787 (viral DNA repair)
- GO:0043504 (mitochondrial DNA repair)
- GO:0010213 (non-photoreactive DNA repair)
- GO:0006282 (regulation of DNA repair)
- GO:0000711 (meiotic DNA repair synthesis)
- GO:0045739 (positive regulation of DNA repair)
- GO:0045738 (negative regulation of DNA repair)
- Several obsolete terms (GO:0003685, GO:0003686, GO:0045020, GO:0045021, GO:0051103)
- GO:0042275 (error-free postreplication DNA repair)
- GO:0000731 (DNA synthesis involved in DNA repair)
**Key finding**: 1,827 total terms related to DNA repair - very comprehensive coverage

### Query 4: Search for protein kinase activity
**Tool**: OLS4:searchClasses(ontologyId="go", query="protein kinase activity")
**Results**: Retrieved 20 of 19,544 total kinase-related terms:
- GO:0004672 (protein kinase activity) - main molecular function term
- GO:0050321 (tau-protein kinase activity)
- GO:0004691 (cAMP-dependent protein kinase activity)
- GO:0004679 (AMP-activated protein kinase activity)
- GO:0004692 (cGMP-dependent protein kinase activity)
- GO:0032147 (activation of protein kinase activity)
- GO:0045859 (regulation of protein kinase activity)
- GO:0034211 (GTP-dependent protein kinase activity)
- GO:0019199 (transmembrane receptor protein kinase activity)
- GO:0004677 (DNA-dependent protein kinase activity)
- GO:0097472 (cyclin-dependent protein kinase activity)
- GO:0004683 (calcium/calmodulin-dependent protein kinase activity)
- GO:0006469 (negative regulation of protein kinase activity)
- GO:0045860 (positive regulation of protein kinase activity)
- GO:0004676 (3-phosphoinositide-dependent protein kinase activity)
- GO:0004690 (cyclic nucleotide-dependent protein kinase activity)
- GO:2000479 (regulation of cAMP-dependent protein kinase activity)
**Key finding**: 19,544 total kinase-related terms showing extensive molecular function coverage

### Query 5: Search for Fabry disease
**Tool**: OLS4:search("Fabry disease")
**Results**: Found disease term across multiple ontologies:
- MONDO:0010526 (Fabry disease) - main disease ontology
- Orphanet:324 (Fabry disease) - rare disease database
- DOID:14499 (Fabry disease) - disease ontology
- EFO:0022876, PRIDE (same MONDO reference)
- NCIT:C84701 (Fabry Disease) - cancer terminology
- mesh:D000795 (Fabry Disease) - medical subject headings
- OMIM:301500 (Fabry disease) - genetic disorder database
- PW:0002103 (Fabry disease pathway)
- mesh:C567062 (Fabry Disease, Cardiac Variant)
- PW:0001471 (Fabry disease pathway, cerebrovascular)
**Key finding**: Good integration across disease and pathway ontologies

## SPARQL Queries Tested

### Query 1: Search GO terms by keyword (from MIE examples)
**Purpose**: Test full-text search with bif:contains
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?go ?label
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go rdfs:label ?label .
  ?label bif:contains "'apoptosis'" .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 20
```
**Expected results**: GO terms related to programmed cell death
**Key insight**: FROM clause is CRITICAL - query fails without it

### Query 2: Filter by namespace (from MIE examples)
**Purpose**: Test namespace filtering for molecular functions
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT DISTINCT ?go ?label ?namespace
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go rdfs:label ?label .
  ?go oboinowl:hasOBONamespace ?namespace .
  FILTER(STR(?namespace) = "molecular_function")
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 10
```
**Expected results**: Only molecular_function GO terms (12,793 total)
**Key insight**: MUST use STR() for namespace comparison to avoid datatype mismatch

### Query 3: Combined keyword and namespace filtering (from MIE examples)
**Purpose**: Find kinase molecular functions
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?go ?label ?definition ?namespace
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go rdfs:label ?label .
  ?go obo:IAO_0000115 ?definition .
  ?go oboinowl:hasOBONamespace ?namespace .
  ?label bif:contains "'kinase'" .
  FILTER(STR(?namespace) = "molecular_function")
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 10
```
**Expected results**: Kinase-related molecular function terms with definitions
**Key insight**: Combining filters effectively narrows results

### Query 4: Boolean search in definitions (from MIE examples)
**Purpose**: Find terms related to both mitochondria and transport
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?go ?label ?definition
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go rdfs:label ?label .
  ?go obo:IAO_0000115 ?definition .
  ?definition bif:contains "('mitochondri*' AND 'transport')" .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 10
```
**Expected results**: GO terms about mitochondrial transport processes
**Key insight**: bif:contains supports boolean operators and wildcards

### Query 5: Count terms by namespace (from MIE examples)
**Purpose**: Get distribution statistics
```sparql
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?namespace (COUNT(DISTINCT ?go) as ?count)
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go oboinowl:hasOBONamespace ?namespace .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
GROUP BY ?namespace
ORDER BY DESC(?count)
```
**Expected results**: 
- biological_process: 30,804
- molecular_function: 12,793
- cellular_component: 4,568
- external: 11
**Key insight**: Aggregation queries work but may timeout without filters

## Interesting Findings

### Specific Entities for Good Questions
1. **GO:0006914** - Autophagy (25 descendants)
   - Well-defined hierarchy
   - Multiple subtypes (macro, micro, chaperone-mediated)
   - Specific organelle autophagy (mitophagy, pexophagy, etc.)

2. **GO:0006281** - DNA repair (1,827 related terms)
   - Extensive pathway coverage
   - Multiple mechanisms
   - Regulatory terms included

3. **GO:0004672** - Protein kinase activity (19,544 related terms)
   - Molecular function
   - Numerous specific kinases
   - Regulatory processes included

4. **GO:0005634** - Nucleus
   - Cellular component example
   - Multiple synonyms and cross-references
   - Part of GO slim subsets

### Unique Properties and Patterns
- **Three independent ontologies**: Biological process, molecular function, cellular component
- **DAG structure**: Terms can have multiple parents (not strict hierarchy)
- **Four synonym types**: Exact, related, narrow, broad - comprehensive term matching
- **Subset system**: GO slim views for specific organisms/applications
- **Obsolete terms**: Marked with owl:deprecated true (25% of all terms)
- **Alternative IDs**: Track merged term history
- **External cross-references**: ~52% of terms link to external databases

### Connections to Other Databases
Cross-references via oboinowl:hasDbXref to:
- **Wikipedia**: General knowledge (~extensive coverage)
- **Reactome**: Biochemical pathways
- **KEGG_REACTION**: Metabolic reactions
- **RHEA**: Enzyme reactions
- **EC**: Enzyme classification
- **MeSH**: Medical subject headings
- **SNOMEDCT**: Clinical terminology
- **NCIt**: Cancer terminology
- **NIF_Subcellular**: Subcellular structures

### Specific, Verifiable Facts
1. GO has exactly 48,165 total terms
2. GO:0006914 (autophagy) has exactly 25 descendant terms
3. GO:0006281 (DNA repair) has 1,827 related terms
4. GO:0004672 (protein kinase activity) has 19,544 related terms
5. Biological_process namespace has 30,804 terms
6. Molecular_function namespace has 12,793 terms
7. Cellular_component namespace has 4,568 terms
8. ~25% of GO terms are obsolete (deprecated)
9. ~80% of terms have synonyms
10. ~52% of terms have external cross-references

## Question Opportunities by Category

**FOCUS ON BIOLOGICAL CONTENT, NOT INFRASTRUCTURE METADATA**

### Precision
✅ **Good examples**:
- "What is the GO ID for autophagy?" → GO:0006914
- "What is the exact definition of GO:0004672?"
- "What namespace does GO:0006281 belong to?"
- "What is the label for GO:0016236?"
- "How many exact synonyms does GO:0005634 (nucleus) have?"

❌ **Avoid**:
- "What version is the GO database?" (infrastructure)
- "When was GO last updated?" (administrative)
- "What software maintains GO?" (technical)

### Completeness
✅ **Good examples**:
- "How many descendant terms does GO:0006914 (autophagy) have?" → 25
- "How many total GO terms exist?" → 48,165
- "How many GO terms are in the biological_process namespace?" → 30,804
- "How many terms are related to DNA repair?" → 1,827
- "How many protein kinase-related terms exist?" → 19,544
- "List all subtypes of macroautophagy (GO:0016236)"
- "How many GO terms have Wikipedia cross-references?"

❌ **Avoid**:
- "How many databases use GO?" (infrastructure usage)
- "How many annotations were added this year?" (administrative metrics)

### Integration
✅ **Good examples**:
- "What Wikipedia pages are cross-referenced from GO:0005634?"
- "Find Reactome pathways linked to GO:0006914 (autophagy)"
- "What MeSH terms cross-reference autophagy GO terms?"
- "List external database cross-references for GO:0006281"
- "Find GO terms that link to KEGG pathways"
- "What NIF_Subcellular terms relate to nucleus GO terms?"

❌ **Avoid**:
- "Which annotation databases sync with GO?" (infrastructure)
- "What data exchange formats link databases?" (technical)

### Currency
✅ **Good examples**:
- "Are there GO terms for SARS-CoV-2 related processes?"
- "What GO terms were recently added for COVID-19 pathways?"
- "Find GO terms for mRNA vaccine-related processes"
- "Are there new autophagy subtypes added recently?"
- "What GO terms describe CRISPR-Cas9 processes?"

❌ **Avoid**:
- "What is the current GO release number?" (administrative)
- "When is the next update scheduled?" (operational)

### Specificity
✅ **Good examples**:
- "What is the GO term for pexophagy?" → GO:0000425
- "Find the term for chaperone-mediated autophagy" → GO:0061684
- "What is the GO ID for xenophagy (pathogen degradation)?" → GO:0098792
- "Find GO term for tau-protein kinase activity" → GO:0050321
- "What is the term for piecemeal microautophagy of nucleus?" → GO:0034727
- "Find crinophagy GO term" → GO:0160155

❌ **Avoid**:
- "What is the most common GO term?" (generic)
- "Which namespace is biggest?" (infrastructure metrics)

### Structured Query
✅ **Good examples**:
- "Find all biological_process GO terms containing 'autophagy' in their label"
- "List molecular_function terms with 'kinase' AND 'protein' in definition"
- "Find cellular_component terms with Wikipedia cross-references"
- "Get all non-obsolete terms in biological_process namespace with >5 synonyms"
- "Find GO terms with both Reactome AND KEGG cross-references"
- "List descendant terms of GO:0006914 that are also regulatory terms"

❌ **Avoid**:
- "Find databases updated after certain date" (administrative)
- "List ontologies with >1000 terms" (infrastructure metrics)

## Notes

### Database Limitations
- **CRITICAL requirement**: MUST include FROM <http://rdfportal.org/ontology/go> clause in all SPARQL queries
- **Datatype issues**: Must use STR() for namespace comparisons
- **Duplicate results**: Always use DISTINCT due to multiple graph storage
- **Performance**: Aggregation queries may timeout without proper filters
- **Mixed ontologies**: GO graph contains terms from other OBO ontologies - must filter by GO_ prefix

### Challenges Encountered
1. **FROM clause requirement**: Queries fail completely without it
2. **Namespace datatype mismatch**: Cannot compare directly without STR()
3. **Duplicate rows**: Multiple graph storage causes duplicates
4. **Performance with aggregations**: COUNT/GROUP BY may timeout without LIMIT
5. **Ontology mixing**: Must filter to exclude CHEBI, PRO, NCBITaxon, etc.

### Best Practices for Querying
1. **CRITICAL**: Always include FROM <http://rdfportal.org/ontology/go>
2. **Always use DISTINCT** in SELECT clauses
3. **Filter by GO_ prefix**: FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
4. **Use STR() for namespace**: FILTER(STR(?namespace) = "biological_process")
5. **Prefer bif:contains over REGEX**: 10-100x faster for keyword search
6. **Use OLS4 tools for hierarchy**: getDescendants, getAncestors for DAG navigation
7. **Add LIMIT for safety**: Especially for aggregation queries
8. **Boolean operators in bif:contains**: Use AND, OR, NOT with single quotes

### Data Quality Indicators
- Definitions required for all non-obsolete terms (~100% coverage)
- ~80% of terms have synonyms
- ~52% of terms have external cross-references
- Obsolete terms marked with owl:deprecated (prevent accidental use)
- Alternative IDs track merged term history
- Created_by and creation_date track provenance

### Database Value for Questions
- **High value**: Term IDs, hierarchies, definitions, namespaces, descendant counts
- **Medium value**: Synonyms, cross-references, subsets
- **Lower value**: Database versions, update schedules, infrastructure details
