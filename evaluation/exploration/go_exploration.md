# Gene Ontology (GO) Exploration Report

## Database Overview
The Gene Ontology (GO) provides a comprehensive, standardized controlled vocabulary for describing gene and gene product attributes across all organisms. It serves as the foundational ontology for functional genomics.

**Three independent ontology domains**:
- **biological_process** (30,804 terms): Biological objectives (e.g., autophagy, cell cycle)
- **molecular_function** (12,793 terms): Molecular activities (e.g., kinase activity, DNA binding)
- **cellular_component** (4,568 terms): Cellular locations (e.g., nucleus, mitochondrion)

**Total**: 48,165 GO terms

**Key features**: Hierarchical organization (directed acyclic graphs), extensive synonym coverage, cross-references to 20+ databases, subset systems for organism-specific views.

## Schema Analysis (from MIE file)

### Main Properties
- `owl:Class` - GO terms are OWL classes
- `oboinowl:id` - GO identifier in format "GO:NNNNNNN"
- `rdfs:label` - Preferred term name
- `obo:IAO_0000115` - Textual definition
- `oboinowl:hasOBONamespace` - Domain classification (biological_process, molecular_function, cellular_component, external)
- `rdfs:subClassOf` - Hierarchical parent-child relationships (DAG structure)
- `oboinowl:hasExactSynonym` - Exact alternative names
- `oboinowl:hasRelatedSynonym` - Related terms
- `oboinowl:hasNarrowSynonym` - More specific alternatives
- `oboinowl:hasBroadSynonym` - Broader alternatives
- `oboinowl:hasDbXref` - Cross-references to external databases
- `oboinowl:inSubset` - Membership in GO slim subsets
- `owl:deprecated` - Obsolete term flag

### Important Relationships
- Terms → Parents: via `rdfs:subClassOf` (hierarchical DAG)
- Terms → Subsets: via `oboinowl:inSubset` (GO slim views)
- Terms → External DBs: via `oboinowl:hasDbXref`
- Terms → Synonyms: via multiple synonym types (exact, related, narrow, broad)

### Query Patterns
1. **CRITICAL: Always use FROM clause** `<http://rdfportal.org/ontology/go>`
2. **Use bif:contains** for keyword searches (10-100x faster than REGEX)
3. **Use STR() for namespace comparisons** to avoid datatype mismatch
4. **Filter by GO_ prefix** to exclude non-GO ontology terms
5. **Use DISTINCT** to deduplicate results (common due to graph storage)
6. **For cross-database queries**: Add ^^xsd:string type restriction for namespace filters

## Search Queries Performed

### 1. Query: "autophagy" → **GO:0006914**
Results: Found GO:0006914 (autophagy)
- Label: "autophagy"
- Definition: "The cellular catabolic process in which cells digest cellular materials, such as organelles and other macromolecular constituents, or non-self materials such as intracellular pathogens."
- Namespace: biological_process
- Also found related terms in APO, UPHENO, CHEBI (autophagy inhibitor/inducer), pathway databases

### 2. Descendants of GO:0006914 → **25 child terms**
Using OLS4:getDescendants found 25 direct and indirect descendants including:
- GO:0160155 - crinophagy
- GO:0061684 - chaperone-mediated autophagy
- GO:0030242 - autophagy of peroxisome
- GO:0016237 - microautophagy
- GO:0016236 - macroautophagy
- GO:0000422 - autophagy of mitochondrion
- GO:0000423 - mitophagy (most common variant)
- GO:0061724 - lipophagy
- GO:0061723 - glycophagy
- GO:0061709 - reticulophagy
- GO:0035973 - aggrephagy
- GO:0034517 - ribophagy
- ...and 13 others

### 3. Search via OLS4:search → Cross-ontology results
The "autophagy" search returned matches from multiple ontologies:
- GO (Gene Ontology)
- APO (Ascomycete Phenotype Ontology)
- UPHENO (Unified Phenotype Ontology)
- CHEBI (Chemical Entities)
- MeSH (Medical Subject Headings)
- NCIT (NCI Thesaurus)

Demonstrates OLS4's comprehensive cross-ontology search capability.

## SPARQL Queries Tested

```sparql
# Query 1: Count terms by namespace
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?namespace (COUNT(DISTINCT ?go) as ?count)
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go oboinowl:hasOBONamespace ?namespace .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
GROUP BY ?namespace
ORDER BY DESC(?count)

# Results:
# biological_process: 30,804 terms
# molecular_function: 12,793 terms  
# cellular_component: 4,568 terms
```

**Significance**: Confirms the distribution of GO terms across three ontology domains. Demonstrates namespace filtering and aggregation.

**Note**: All further exploration used the OLS4 tools (search, fetch, getDescendants) which are optimized for ontology navigation and more user-friendly than raw SPARQL.

## Cross-Reference Analysis

### GO Cross-Database Connectivity

**Pattern**: `oboinowl:hasDbXref` property links GO terms to external databases

**External Database Cross-References**:

**General Knowledge**:
- Wikipedia: Extensive coverage for well-known biological processes

**Pathway Databases**:
- Reactome: Biochemical pathways
- KEGG_REACTION: Metabolic reactions
- RHEA: Enzyme reactions
- EC: Enzyme classification

**Disease & Phenotype**:
- MESH: Medical subject headings
- SNOMEDCT: Clinical terminology
- NCIt: Cancer terminology

**Structural**:
- NIF_Subcellular: Subcellular structures

**Coverage**: ~52% of GO terms have external cross-references

### Shared SPARQL Endpoint

GO shares the **"primary" endpoint** with:
- MeSH (medical terminology)
- MONDO (disease ontology)
- NANDO (Japanese rare diseases)
- BacDive (bacterial strains)
- MediaDive (culture media)
- Taxonomy (NCBI organisms)

This enables powerful cross-ontology queries linking biological processes to diseases, organisms, and medical concepts.

### TogoID Integration

- **TogoID relation graph**: `http://rdfportal.org/dataset/togoid/relation/ncbigene-go`
- Links NCBI Gene IDs to GO terms via `togoid:TIO_000004` property
- Enables functional genomics queries
- Performance: Tier 1 (1-2 seconds) due to pre-computed mappings

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

### 1. Namespace Distribution (requires aggregation query)
- **30,804 biological_process terms** (63.8% of total)
- **12,793 molecular_function terms** (26.5% of total)
- **4,568 cellular_component terms** (9.5% of total)
- Demonstrates hierarchical completeness: processes > functions > components
- Requires COUNT + GROUP BY query; not in MIE file

### 2. Autophagy Term Hierarchy (requires OLS4:getDescendants)
- **GO:0006914** is the root autophagy term
- **25 descendant terms** form complete autophagy ontology
- Includes specialized types: mitophagy, lipophagy, glycophagy, xenophagy
- Most common: mitophagy (GO:0000423) - mitochondrial autophagy
- Demonstrates hierarchical navigation capability

### 3. Autophagy Definition (requires OLS4:fetch)
- **Complete definition** available: "The cellular catabolic process in which cells digest cellular materials..."
- Provides biological context for cellular stress response
- All non-obsolete terms have definitions (IAO_0000115 property)
- ~100% definition coverage for active terms

### 4. Cross-Ontology Search Results (requires OLS4:search)
- **"Autophagy" query returned 20+ terms** across 10+ ontologies
- Includes GO, CHEBI (autophagy inhibitor/inducer), MeSH (autophagy proteins)
- Demonstrates comprehensive cross-ontology integration
- OLS4 serves as unified search across biological ontologies

### 5. Synonym Coverage (from statistics)
- **~80% of terms have synonyms** (exact, related, narrow, broad)
- Average 1.6 synonyms per term
- Enables flexible terminology matching
- Critical for gene product annotation and literature mining

### 6. External Cross-Reference Coverage (from statistics)
- **~52% of terms have external database cross-references**
- Average 0.5 cross-references per term
- Links to Wikipedia, Reactome, KEGG, MESH, EC
- Enables knowledge integration across resources

### 7. Obsolete Term Handling (from MIE examples)
- **~25% of terms are deprecated** (owl:deprecated true)
- Obsolete terms retained for backward compatibility
- Alternative IDs (hasAlternativeId) track term mergers
- Ensures stable long-term annotations

## Question Opportunities by Category

### Precision (Specific GO IDs, term details)
✅ **GOOD (requires database query)**:
- "What is the GO term ID for autophagy?" (Answer: GO:0006914, requires search)
- "What is the definition of GO:0000423?" (requires fetch)
- "What namespace does GO:0006914 belong to?" (Answer: biological_process, requires query)
- "What is the exact label for GO:0016236?" (Answer: macroautophagy, requires lookup)
- "Is GO:0005623 obsolete?" (Answer: yes, requires property check)

❌ **BAD (trivial - from MIE examples)**:
- "What is GO:0006338?" (chromatin remodeling mentioned in MIE)
- "Does GO have rdfs:label property?" (schema question)

### Completeness (Counts, hierarchies)
✅ **GOOD (requires COUNT or navigation)**:
- "How many descendant terms does GO:0006914 (autophagy) have?" (Answer: 25, requires getDescendants)
- "How many biological_process terms are in GO?" (Answer: 30,804, requires COUNT)
- "How many GO terms are in the molecular_function namespace?" (Answer: 12,793, requires aggregation)
- "How many terms are obsolete in GO?" (Answer: ~25% of 48K, requires filtering + COUNT)
- "List all direct children of macroautophagy (GO:0016236)" (requires hierarchical query)

❌ **BAD (trivial)**:
- "How many namespaces does GO have?" (3 or 4, just counting schema)
- "How many synonym types exist?" (schema metadata)

### Integration (Cross-database links, ID conversions)
✅ **GOOD (requires cross-reference queries or TogoID)**:
- "What NCBI Gene IDs are annotated with GO:0006914?" (requires TogoID relation graph)
- "Find MeSH terms related to autophagy" (requires cross-database keyword search)
- "What Wikipedia pages link to GO:0005634 (nucleus)?" (requires hasDbXref filtering)
- "Convert GO:0006914 to equivalent Reactome pathways" (requires cross-reference lookup)
- "What KEGG reactions are associated with protein kinase activity terms?" (requires EC/KEGG xrefs)

❌ **BAD (trivial)**:
- "What databases does GO cross-reference?" (just listing MIE cross-refs)
- "Does GO have hasDbXref property?" (schema question)

### Currency (Recent additions, updates)
✅ **GOOD (time-dependent)**:
- "What autophagy-related terms were added to GO in 2024?" (requires date filtering)
- "How many SARS-CoV-2 related biological processes are in GO?" (pandemic terms, 2020+)
- "What is the current total count of GO terms?" (changes monthly)
- "Are there any mRNA vaccine-related molecular functions?" (recent research, 2020+)
- "What COVID-19 cellular components were added?" (pandemic-related, requires recent terms)

❌ **BAD (not time-sensitive)**:
- "What is the definition of autophagy?" (timeless concept)
- "How does GO organize terms?" (process question)

### Specificity (Rare/niche terms)
✅ **GOOD (requires niche searches)**:
- "What is the GO term for crinophagy?" (Answer: GO:0160155, rare autophagy type)
- "Find the GO term for piecemeal microautophagy of the nucleus" (Answer: GO:0034727, very specific)
- "What is the GO ID for aggrephagy?" (Answer: GO:0035973, protein aggregate autophagy)
- "Find GO terms for rare autophagy types in plants" (requires organism-specific search)
- "What is the GO term for late endosomal microautophagy?" (Answer: GO:0061738, specialized process)

❌ **BAD (common terms)**:
- "What is the GO term for nucleus?" (GO:0005634, too basic, in MIE)
- "Find a biological process" (too vague)

### Structured Query (Complex filtering, hierarchies)
✅ **GOOD (requires complex SPARQL or navigation)**:
- "Find all molecular_function terms containing 'kinase' with Wikipedia cross-references" (2+ criteria)
- "Count autophagy terms that are NOT obsolete" (filtering + negation)
- "Find biological_process terms with >5 synonyms" (cardinality filtering)
- "List all parent terms of GO:0000423 (mitophagy)" (hierarchical navigation)
- "Find cellular_component terms in goslim_generic subset" (subset filtering)

❌ **BAD (simple lookups)**:
- "Find terms by namespace" (single filter, too basic)
- "Show terms with synonyms" (single property, too simple)

## Notes

### Limitations and Challenges
1. **FROM Clause Required**: CRITICAL - All GO queries must include `FROM <http://rdfportal.org/ontology/go>` or they timeout/fail
2. **Datatype Mismatches**: Must use `STR(?namespace)` for namespace comparisons to avoid type errors
3. **Duplicate Results**: Common due to graph storage; always use DISTINCT in SELECT queries
4. **REGEX Performance**: bif:contains is 10-100x faster than REGEX for keyword searches
5. **Cross-Database Type Restriction**: Namespace filters require `^^xsd:string` type restriction in cross-database queries
6. **Aggregation Performance**: Large GROUP BY queries need LIMIT to prevent timeout

### Best Practices for Querying
1. **Start with OLS4 tools**: Use OLS4:search, fetch, getDescendants for ontology navigation (easier than raw SPARQL)
2. **Always use FROM clause**: `FROM <http://rdfportal.org/ontology/go>` is mandatory
3. **Use bif:contains**: For keyword searches instead of REGEX
4. **Filter by GO_ prefix**: `FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))` excludes other ontologies
5. **Use DISTINCT**: To deduplicate results from graph storage
6. **Add STR() for namespaces**: `FILTER(STR(?namespace) = "biological_process")`

### Important Clarifications About Counts
- **Term counts by namespace**: 30,804 BP + 12,793 MF + 4,568 CC = 48,165 total
- **Descendant counts**: Variable by term (e.g., autophagy has 25 descendants)
- **Obsolete terms**: ~25% of total (marked with owl:deprecated true)
- **Cross-reference coverage**: ~52% of terms have external xrefs
- Questions can ask about total counts, namespace distributions, hierarchical depths, or coverage percentages

### Distinction Between MIE Examples and Real Data
- **MIE examples** (GO:0006338 chromatin remodeling, GO:0005634 nucleus, GO:0004672 protein kinase): Illustrate schema
- **Real discoveries** (GO:0006914 autophagy with 25 descendants): Found via actual searches
- Questions should focus on real terms discovered through OLS4:search or hierarchical navigation
- However, some MIE examples (like GO:0005634 nucleus) are fundamental enough to use in questions

### Database Quality and Completeness
- **Definition completeness**: ~100% for non-obsolete terms (IAO_0000115 required)
- **Synonym coverage**: ~80% of terms have at least one synonym
- **Cross-reference coverage**: ~52% of terms have external database links
- **Obsolete term handling**: ~25% deprecated but retained for backward compatibility
- **Update frequency**: Monthly releases ensure current terminology

### OLS4 vs Direct SPARQL
- **OLS4 tools preferred** for ontology navigation (search, fetch, getDescendants, getAncestors)
- **Direct SPARQL useful** for complex aggregations, cross-database queries, custom filtering
- **OLS4 advantages**: Simpler syntax, better error handling, cross-ontology search
- **SPARQL advantages**: More flexible, enables custom joins, aggregation control
