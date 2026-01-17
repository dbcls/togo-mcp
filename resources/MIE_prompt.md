# Create a compact yet comprehensive MIE file for an RDF database.
**Target Database: __DBNAME__**

## Philosophy: Essential over Exhaustive
Create documentation that is **compact, clear, and complete** - sufficient for researchers to effectively query the database without unnecessary bloat.

## 1. Discovery Phase (CRITICAL: Follow Systematically)

**⚠️ WARNING: Avoid Sampling Bias and Premature Conclusions**
- The first 50 results from a SPARQL query may NOT represent the entire database
- Always verify comprehensively using multiple query patterns before drawing conclusions
- Check ontology graphs for class definitions BEFORE sampling data
- Never assume timeouts mean "data doesn't exist"

### 1.1 Systematic Discovery Workflow

**Step 1: Check for Existing Documentation** (2 minutes)
- Use `get_sparql_endpoints()` to identify available endpoints and keyword search APIs
  - Returns: SPARQL endpoint URL + recommended keyword search API for each database
  - Keyword search APIs include: dedicated tools (e.g., `search_uniprot_entity`), `OLS4:searchClasses`, `ncbi_esearch`, or "sparql" (SPARQL-only)
- Use `get_graph_list(dbname)` to find ALL named graphs (data + ontology graphs)
- Attempt `get_shex(dbname)` to retrieve existing shape expressions
- Attempt `get_MIE_file(dbname)` to retrieve existing MIE files
  - **If an existing MIE file is found**: Perform compliance check (see section 1.2 below)
  - **If compliant**: Update/improve the file as needed
  - **If non-compliant**: Create a new MIE file from scratch
- Attempt `get_sparql_example(dbname)` to retrieve an example SPARQL query

**Step 1.5: Identify Shared Endpoint Databases** (2 minutes)
- Use `get_sparql_endpoints()` to identify which databases share the same endpoint
- For databases on shared endpoints, explore cross-database integration opportunities
- Check for common cross-reference patterns between co-located databases

Example:
```python
endpoints = get_sparql_endpoints()
# Find databases on same endpoint as current database
my_endpoint = endpoints['databases'][dbname]['endpoint_name']
shared_databases = endpoints['endpoints'][my_endpoint]['databases']
```

**Why this matters**: Databases on the same endpoint can be queried together in a single SPARQL query using multiple GRAPH clauses, enabling powerful cross-database integration.

**Step 2: Discover Schema/Ontology Definitions** (5 minutes)
```sparql
# Query 1: Get all RDF classes from ontology graphs
SELECT DISTINCT ?class
FROM <ontology_graph_uri>
WHERE {
  ?class a owl:Class .
}
LIMIT 100

# Query 2: Get all properties from ontology graphs
SELECT DISTINCT ?property ?type
FROM <ontology_graph_uri>
WHERE {
  ?property a ?type .
  FILTER(?type IN (owl:ObjectProperty, owl:DatatypeProperty, rdf:Property))
}
LIMIT 100

# Query 3: Sample property domains and ranges
SELECT ?property ?domain ?range
FROM <ontology_graph_uri>
WHERE {
  ?property rdfs:domain ?domain ;
            rdfs:range ?range .
}
LIMIT 100
```

**Why this matters**: Ontology graphs reveal what SHOULD exist, preventing you from missing entire entity types.

**Step 3: Explore URI Patterns** (5 minutes)

Test multiple URI namespace patterns to discover different entity types:

```sparql
# Pattern 1: identifiers.org/[namespace]
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
  FILTER(STRSTARTS(STR(?s), "http://identifiers.org/"))
}
LIMIT 50

# Pattern 2: Database-specific namespace
SELECT ?s ?p ?o  
WHERE {
  ?s ?p ?o .
  FILTER(STRSTARTS(STR(?s), "http://[database-specific-uri]/"))
}
LIMIT 50

# Pattern 3: Sample different prefixes found in ontology
SELECT ?s ?type
WHERE {
  ?s a ?type .
}
LIMIT 100
```

**Why this matters**: Different URI patterns often indicate different data layers (e.g., identifiers vs full records vs features).

**Step 4: Systematic Class Instance Sampling** (10 minutes)

For EACH class discovered in Step 2, sample actual instances:

```sparql
# For each class found:
SELECT ?instance ?p ?o
WHERE {
  ?instance a <ClassURI> .
  ?instance ?p ?o .
}
LIMIT 50
```

**Why this matters**: Prevents assuming the database only contains what you see first. Some classes may have millions of instances, others only a few.

**Step 5: Verify and Cross-Check** (5 minutes)

If queries timeout or return no results:
- ✅ Try with smaller LIMIT values
- ✅ Try without FROM clauses
- ✅ Try with different FILTER patterns
- ✅ Sample from different graph URIs
- ✅ Use `^^xsd:string` for string type restriction or `STR()` to make a plain string.
- ❌ DON'T assume "no results = doesn't exist"

### 1.2 MIE File Compliance Check

When an existing MIE file is retrieved, verify it complies with these instructions:

**Structure & Format:**
- [ ] Properly formatted YAML
- [ ] Contains all required sections: schema_info, shape_expressions, sample_rdf_entries, sparql_query_examples, cross_database_queries (if applicable), cross_references, architectural_notes, data_statistics, anti_patterns, common_errors
- [ ] Schema_info includes version/license/access metadata

**Sample RDF Entries:**
- [ ] Exactly 5 examples covering diverse categories
- [ ] Each has concise 1-2 sentence description

**SPARQL Query Examples:**
- [ ] Exactly 7 queries (2 basic, 3 intermediate, 2 advanced)
- [ ] Includes: keyword filtering + biological annotations
- [ ] No cross-reference queries (those in cross_references section)
- [ ] All tested and working

**Cross-Database Queries (if applicable):**
- [ ] 2-3 examples if database shares endpoint with others
- [ ] Uses proper GRAPH clauses for each database
- [ ] Includes practical use cases
- [ ] Performance notes documented

**Shape Expressions:**
- [ ] Minimal comments (only non-obvious properties)
- [ ] Covers ALL major entity types

**Other Sections:**
- [ ] Cross-references organized by RDF pattern with all databases
- [ ] Architectural notes in YAML bullet format (not prose)
- [ ] Data statistics with coverage, cardinality, performance
- [ ] 2-3 anti-patterns with wrong/correct versions
- [ ] 2-3 common errors with solutions

**Decision:**
- If ≥90% pass: Update existing file
- If <90% pass: Create new from scratch

## 2. Schema Analysis (DO NOT SKIP)

**Critical First Step: Get Complete Class Inventory**
```sparql
# From ontology graph
SELECT ?class (COUNT(?instance) as ?count)
WHERE {
  ?instance a ?class .
}
GROUP BY ?class
ORDER BY DESC(?count)
```

**If the above times out, try sampling:**
```sparql
SELECT DISTINCT ?class
WHERE {
  ?s a ?class .
}
LIMIT 100
```

Then for each class:
- Query for sample instances
- Examine property patterns
- Identify required vs optional properties
- Check for hierarchical relationships

## 3. Deep Dive Investigation

For EACH major entity type discovered:

### 3.1 Property Analysis
```sparql
# Get all properties used by this entity type
SELECT DISTINCT ?property (COUNT(?value) as ?usage)
WHERE {
  ?entity a <EntityType> .
  ?entity ?property ?value .
}
GROUP BY ?property
ORDER BY DESC(?usage)
LIMIT 50
```

### 3.2 Relationship Mapping
```sparql
# Find relationships between entity types
SELECT ?type1 ?property ?type2 (COUNT(*) as ?count)
WHERE {
  ?entity1 a ?type1 .
  ?entity1 ?property ?entity2 .
  ?entity2 a ?type2 .
}
GROUP BY ?type1 ?property ?type2
ORDER BY DESC(?count)
LIMIT 50
```

### 3.3 Cross-Reference Discovery
```sparql
# Pattern 1: rdfs:seeAlso links
SELECT ?entity ?externalDB
WHERE {
  ?entity rdfs:seeAlso ?externalDB .
}
LIMIT 100

# Pattern 2: owl:sameAs links (or database-specific properties)
SELECT ?entity ?externalDB
WHERE {
  ?entity owl:sameAs ?externalDB .
}
LIMIT 100
```

### 3.4 Data Quality Assessment
```sparql
# Check property completeness (for coverage statistics)
SELECT 
  (COUNT(DISTINCT ?entity) as ?total)
  (COUNT(DISTINCT ?withProperty) as ?withProperty)
WHERE {
  ?entity a <EntityType> .
  OPTIONAL { 
    ?entity <PropertyToCheck> ?value .
    BIND(?entity as ?withProperty)
  }
}
```

**While testing queries, note patterns that fail (timeouts, errors, empty results) to document as anti-patterns.**

### 3.5 Cross-Database Link Discovery (For Shared Endpoints Only)

**Only perform this if multiple databases share the same endpoint.**

**Step 1: Retrieve MIE files for co-located databases**
```python
# For each database on the same endpoint
for co_db in shared_databases:
    if co_db != dbname:
        try:
            mie_content = get_MIE_file(co_db)
            # Extract: graph URIs, entity types, linking properties, prefixes
            # Store for reference when creating cross-database queries
        except:
            # MIE file doesn't exist yet - proceed with discovery
            pass
```

**Why this matters**: Existing MIE files provide:
- Correct graph URIs for GRAPH clauses
- Entity type definitions and class URIs
- Property patterns and namespaces
- Known cross-references and linking properties
- Anti-patterns to avoid

**Step 2: Identify linking properties**
```sparql
# Find properties that reference entities in other databases
SELECT DISTINCT ?property ?targetDB
WHERE {
  GRAPH <current_database_graph> {
    ?entity ?property ?target .
    # Filter for URIs from other databases on same endpoint
    FILTER(STRSTARTS(STR(?target), "http://purl.obolibrary.org/obo/"))  # Example: ChEBI from ChEMBL
  }
  BIND(REPLACE(STR(?target), "^(https?://[^/]+/).*", "$1") AS ?targetDB)
}
LIMIT 100
```

**Step 3: Verify cross-database queries work**
```sparql
# Test query combining two databases
# Use graph URIs, prefixes, and entity types from retrieved MIE files
SELECT ?entity1 ?entity2 ?label1 ?label2
WHERE {
  GRAPH <database1_graph> {  # From database1 MIE file
    ?entity1 a <Type1> ;      # From database1 shape expressions
             <link_property> ?entity2 ;
             rdfs:label ?label1 .
  }
  GRAPH <database2_graph> {  # From database2 MIE file
    ?entity2 a <Type2> ;      # From database2 shape expressions
             rdfs:label ?label2 .
  }
}
LIMIT 10
```

**Step 4: Reference co-located database schemas**
When creating cross-database query examples:
- Use correct entity type URIs from retrieved MIE files
- Apply property patterns documented in co-database MIE files
- Follow prefix conventions from co-database MIE files
- Avoid anti-patterns documented in co-database MIE files
- Use successful query patterns from co-database sparql_query_examples

**Step 5: Document common link patterns**
- Note which properties create links (e.g., `skos:exactMatch`, `rdfs:seeAlso`)
- Identify most useful cross-database query patterns
- Test performance of cross-database queries (may be slower)
- Document which co-database MIE files were referenced

## 4. MIE File Construction

### Required Sections (in order):

1. **schema_info** - Database metadata + version/license/access info
2. **shape_expressions** - ShEx schemas for all entity types (minimal comments)
3. **sample_rdf_entries** - 5 diverse examples (core entity, related entity, sequence/molecular, cross-ref, geographic/temporal)
4. **sparql_query_examples** - 7 tested queries (2 basic, 3 intermediate, 2 advanced)
5. **cross_database_queries** - 2-3 examples leveraging shared endpoint (ONLY if applicable)
6. **cross_references** - Pattern-based organization with all external databases
7. **architectural_notes** - schema_design, performance, data_integration, data_quality (YAML bullets, not prose)
8. **data_statistics** - Counts, coverage, cardinality, performance_characteristics, data_quality_notes
9. **anti_patterns** - 2-3 common mistakes with wrong/correct versions
10. **common_errors** - 2-3 error scenarios with solutions

### Key Constraints:
- RDF examples: Exactly 5, each 1-2 sentence description
- SPARQL queries: Exactly 7, must include keyword filtering + biological annotations
- Cross-database queries: 2-3 examples (ONLY if database shares endpoint with others)
- Anti-patterns: 2-3 examples showing wrong query → correct query
- Common errors: 2-3 scenarios with causes and solutions
- Keep everything concise - if it doesn't help query writing, omit it

## 5. Quality Assurance Checklist

Before finalizing, verify:

**Discovery:**
- [ ] Queried ontology graphs for all entity types
- [ ] Explored multiple URI patterns
- [ ] Documented ALL major entity types
- [ ] Identified co-located databases on shared endpoint (if applicable)

**Structure:**
- [ ] Valid YAML with all required sections (9 or 10 depending on shared endpoint)
- [ ] Schema_info includes version/license/access
- [ ] ShEx minimal comments, covers all types
- [ ] Exactly 5 diverse RDF examples
- [ ] Exactly 7 SPARQL queries (2/3/2 distribution)
- [ ] Required queries: keyword filtering + biological annotations
- [ ] Cross-database queries if database shares endpoint (2-3 examples)
- [ ] Cross-references by pattern (not by individual DB)
- [ ] Architectural notes in YAML bullets

**Quality:**
- [ ] All SPARQL queries tested and work
- [ ] Cross-database queries tested (if included)
- [ ] 2-3 anti-patterns with wrong/correct versions
- [ ] 2-3 common errors with solutions
- [ ] Statistics: counts, coverage, cardinality, performance
- [ ] Everything concise - no unnecessary content

**Cross-Database (if applicable):**
- [ ] Identified all databases on same endpoint
- [ ] Retrieved MIE files for all co-located databases using get_MIE_file()
- [ ] Extracted graph URIs, entity types, and properties from co-database MIE files
- [ ] Found at least 1 linking property to co-located databases
- [ ] 2-3 cross-database query examples tested and working
- [ ] Cross-database queries use proper GRAPH clauses from co-database MIE files
- [ ] Cross-database queries use correct entity types from co-database shape expressions
- [ ] Avoided anti-patterns documented in co-database MIE files
- [ ] Performance notes for cross-database queries documented
- [ ] Query notes document which MIE files were referenced

## Common Pitfalls to Avoid

**❌ Sampling Bias**: First 50 results may not represent entire database → Check ontology graphs, explore multiple URI patterns

**❌ Premature Conclusions**: Query timeout ≠ "data doesn't exist" → Try smaller LIMITs, different patterns, alternative graphs

**❌ Incomplete Coverage**: Documenting only obvious entity types → Query ontology graphs first, create shapes for ALL types

**❌ Missing Error Guidance**: Not testing what fails → Note failing patterns during testing to document as anti-patterns

**❌ Ignoring Cross-Database Opportunities**: Not exploring shared endpoint databases → Check for co-located databases and linking properties

## Available Tools
- `get_sparql_endpoints()` - Get available SPARQL endpoints and keyword search APIs for all databases
- `get_graph_list(dbname)` - List named graphs in database
- `get_sparql_example(dbname)` - Get an example SPARQL query
- `run_sparql(dbname, sparql_query)` - Execute SPARQL queries
- `run_sparql(endpoint_name=endpoint, sparql_query)` - Execute cross-database queries on shared endpoint
- `get_shex(dbname)` - Retrieve ShEx schema if available
- `get_MIE_file(dbname)` - Retrieve existing MIE file if available
- `save_MIE_file(dbname, mie_content)` - Save the final MIE file

### Keyword Search APIs by Database Type:
**Dedicated Search Tools:**
- UniProt: `search_uniprot_entity(query, limit=20)`
- PDB: `search_pdb_entity(db, query, limit=20)` where db="pdb"|"cc"|"prd"
- ChEMBL: `search_chembl_molecule(query, limit=20)` or `search_chembl_target(query, limit=20)`
- Reactome: `search_reactome_entity(query, species=None, types=None, rows=30)`
- Rhea: `search_rhea_entity(query, limit=100)`
- MeSH: `search_mesh_entity(query, limit=10)`

**OLS4 (Ontology Lookup Service):**
- ChEBI, GO, Mondo, NANDO: `OLS4:searchClasses(query, ontologyId=None, pageSize, pageNum)`

**NCBI E-utilities:**
- PubChem, Taxonomy, ClinVar, PubMed, NCBIGene, MedGen: `ncbi_esearch(database, query, max_results=20, start_index=0)`

**SPARQL-Only (use bif:contains for keyword search):**
- BacDive, MediaDive, DDBJ, GlyCosmos, Ensembl, PubTator: Use `run_sparql()` with `bif:contains` pattern

## Using `bif:contains` for the Virtuoso backend.
If the backend database is Virtuoso, **DO use `bif:contains` for string filtering whenever possible.**
```sparql
SELECT ?label
WHERE {
  ?s rdfs:label ?label .
  label bif:contains "('amyloid' AND NOT 'precursor') OR 'alzheimer'" option (score ?sc)
}
ORDER BY DESC (?sc)
LIMIT 50
```
You can sort the results by `?sc` (keyword relevance score).　
**DON'T use `?score` for the variable name** That would result in an error.

## YAML Formatting Rules

**CRITICAL: Use "|" (pipe) syntax for ALL multiline strings**

For readability and consistency, ALL multiline string values in the MIE file MUST use the pipe (|) syntax:

```yaml
# ✅ CORRECT - Use pipe for multiline strings
description: |
  First line of description.
  Second line of description.
  
sparql: |
  SELECT ?s ?p ?o
  WHERE {
    ?s ?p ?o .
  }
  LIMIT 10

# ❌ WRONG - Don't use quoted strings for multiline content
description: "First line.\nSecond line."
sparql: "SELECT ?s ?p ?o WHERE { ?s ?p ?o . } LIMIT 10"
```

**When to use "|" syntax:**
- description fields
- sparql queries
- rdf examples
- shape_expressions
- explanation fields
- Any string value that spans multiple lines

**Benefits:**
- Better readability
- Preserves formatting and indentation
- Easier to edit SPARQL queries
- Consistent style throughout the file

## Cross-Database Query Guidelines

**When to Include Cross-Database Queries:**
- Database shares SPARQL endpoint with 2+ other databases
- Clear linking properties exist (skos:exactMatch, rdfs:seeAlso, etc.)
- Practical use cases benefit from integration (don't force it)

**When NOT to Include:**
- Database is on standalone endpoint (PubChem, PDB, DDBJ, GlyCosmos)
- No clear linking mechanisms exist
- Cross-database queries consistently timeout

**CRITICAL: Reference Co-Located Database MIE Files**

Before creating cross-database query examples:
1. **Retrieve MIE files** for all co-located databases using `get_MIE_file(co_db_name)`
2. **Extract key information** from retrieved MIE files:
   - Graph URIs from `schema_info.graphs`
   - PREFIX definitions from `shape_expressions`
   - Entity type URIs from `shape_expressions`
   - Property patterns from `sample_rdf_entries`
   - Linking properties from `cross_references`
   - Anti-patterns to avoid from `anti_patterns`
3. **Use this information** to create accurate, well-formed cross-database queries
4. **Document which MIE files were consulted** in query notes

**Why this matters:**
- Ensures correct graph URIs (avoid query failures)
- Uses proper entity types and properties (avoid empty results)
- Follows established naming conventions (consistency)
- Avoids known anti-patterns (better performance)
- Creates queries that align with existing documentation

**Best Practices:**
1. **Use explicit GRAPH clauses** for each database
2. **Start with smaller LIMITs** (cross-database queries are slower)
3. **Filter early** - apply constraints within each GRAPH clause
4. **Document performance** - note if queries are slow
5. **Show practical value** - examples should solve real research questions
6. **Reference MIE files** - use correct URIs, types, and patterns from co-database documentation

**Example Pattern:**
```sparql
# Good: Filter within GRAPH clauses, explicit naming
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?molecule ?moleculeLabel ?chebiLabel ?formula
WHERE {
  GRAPH <http://rdf.ebi.ac.uk/dataset/chembl> {
    ?molecule a cco:SmallMolecule ;
              rdfs:label ?moleculeLabel ;
              skos:exactMatch ?chebiId .
    FILTER(?moleculeLabel = "ASPIRIN")
  }
  GRAPH <http://rdf.ebi.ac.uk/dataset/chebi> {
    ?chebiId a owl:Class ;
             rdfs:label ?chebiLabel ;
             chebi:formula ?formula .
  }
}
LIMIT 10
```

**Common Link Patterns by Endpoint:**
- **EBI** (chembl, chebi, reactome, ensembl, amrportal):
  - ChEMBL ↔ ChEBI: `skos:exactMatch`
  - ChEMBL targets ↔ Ensembl: via UniProt IDs
  - Reactome ↔ Ensembl: gene identifiers
  - Ensembl ↔ ChEMBL: protein targets
  
- **SIB** (uniprot, rhea):
  - UniProt ↔ Rhea: enzyme-catalyzed reactions
  
- **Primary** (mesh, go, taxonomy, mondo, nando, bacdive, mediadive):
  - MONDO ↔ MeSH: disease concept IDs
  - BacDive ↔ MediaDive: bacterial strain to culture media
  - GO ↔ Taxonomy: gene ontology across species
  
- **NCBI** (clinvar, pubmed, pubtator, ncbigene, medgen):
  - ClinVar ↔ NCBI Gene: variant-to-gene mappings
  - PubMed ↔ PubTator: article-to-entity annotations
  - MedGen ↔ NCBI Gene: clinical genetics

## MIE File Structure Template
```yaml
schema_info:
  title: [DATABASE_NAME]
  description: |
    [3-5 sentences: what it contains, main entity types (ALL), use cases, key features]
  endpoint: https://rdfportal.org/example/sparql
  base_uri: http://example.org/
  graphs:
    - http://example.org/dataset
    - http://example.org/ontology
  kw_search_tools:
    # Obtained from get_sparql_endpoints()
    # Categories:
    # - Dedicated: search_uniprot_entity, search_pdb_entity, search_chembl_molecule/target, 
    #              search_reactome_entity, search_rhea_entity, search_mesh_entity
    # - OLS4: OLS4:searchClasses (for chebi, go, mondo, nando)
    # - NCBI: ncbi_esearch (for pubchem, taxonomy, clinvar, pubmed, ncbigene, medgen)
    # - SPARQL-only: Use run_sparql with bif:contains for keyword search
    - [keyword_search_api_name]  # e.g., search_uniprot_entity, OLS4:searchClasses, ncbi_esearch, or "sparql"

  # Metadata (integrated into schema_info)
  version:
    mie_version: "1.0"
    mie_created: "YYYY-MM-DD"
    data_version: "Release YYYY.MM"
    update_frequency: "Monthly"
  license:
    data_license: "License name"
    license_url: "https://..."
  access:
    rate_limiting: "100 queries/min"
    max_query_timeout: "60 seconds"
    backend: "Virtuoso" or "Other"  # Important for bif:contains usage

shape_expressions: |
  # Minimal comments - only for non-obvious properties
  # Cover ALL major entity types
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  
  <EntityShape> {
    a [ schema:Type ] ;
    schema:property xsd:string ;
    schema:optional xsd:string ?     # Comment only if needed
  }

sample_rdf_entries:
  # Exactly 5: core entity, related entity, molecular, cross-ref, temporal/geo
  - title: [Descriptive title]
    description: [1-2 sentences]
    rdf: |
      # Real RDF from database

sparql_query_examples:
  # Exactly 7: 2 basic, 3 intermediate, 2 advanced
  # Must include: keyword filtering + biological annotations
  - title: [What it does]
    description: [Context]
    question: [Natural language]
    complexity: basic
    sparql: |
      # Tested working query

cross_database_queries:
  # Only include if database shares endpoint with others
  # 2-3 examples showing practical integration
  # CRITICAL: Reference co-database MIE files for accurate URIs and patterns
  shared_endpoint: ebi  # or sib, primary, ncbi, etc.
  co_located_databases:
    - database1
    - database2
  examples:
    - title: [What integration achieves]
      description: |
        [Why this cross-database query is useful - 2-3 sentences]
      databases_used:
        - database1
        - database2
      complexity: intermediate  # or advanced
      sparql: |
        # Prefixes from database1 and database2 MIE files
        PREFIX db1: <http://example1.org/>
        PREFIX db2: <http://example2.org/>
        
        SELECT ?entity1 ?entity2 ?property
        WHERE {
          # Graph URI from database1 MIE file (schema_info.graphs)
          GRAPH <http://example1.org/dataset> {
            # Entity type from database1 MIE file (shape_expressions)
            ?entity1 a db1:Type ;
                     db1:links ?entity2 .
          }
          # Graph URI from database2 MIE file (schema_info.graphs)
          GRAPH <http://example2.org/dataset> {
            # Entity type from database2 MIE file (shape_expressions)
            ?entity2 a db2:Type ;
                     db2:property ?property .
          }
        }
        LIMIT 50
      notes: |
        - Query uses graph URIs from database1 and database2 MIE files
        - Entity types and properties verified against co-database shape expressions
        - Performance: [timing or considerations]
        - Use case: [practical application]

cross_references:
  - pattern: rdfs:seeAlso
    description: |
      [How external links work]
    databases:
      category:
        - Database: coverage
    sparql: |
      # Representative query

architectural_notes:
  schema_design:
    - [Bullet: entity relationships]
  performance:
    - [Bullet: optimization tips]
  data_integration:
    - [Bullet: cross-references]
    - [Bullet: cross-database opportunities if applicable]
  data_quality:
    - [Bullet: data quirks]

data_statistics:
  total_entity_type: count
  coverage:
    property_coverage: "~XX%"
  cardinality:
    avg_per_entity: X.X
  performance_characteristics:
    - "Tested observation"
    - "Cross-database query performance (if applicable)"
  data_quality_notes:
    - "Data issue"

anti_patterns:
  # 2-3 examples
  - title: "Common mistake"
    problem: "Why wrong"
    wrong_sparql: |
      # Bad query
    correct_sparql: |
      # Fixed query
    explanation: "What changed"

common_errors:
  # 2-3 scenarios
  - error: "Error type"
    causes:
      - "Cause 1"
    solutions:
      - "Solution 1"
    example_fix: |
      # Before/after (optional, if helpful)
```

## Success Criteria
- Ontology graphs checked for complete class inventory
- Multiple URI patterns explored
- All SPARQL queries tested and working
- Cross-database queries included if database shares endpoint (2-3 examples)
- Shape expressions cover ALL major entity types with minimal comments
- Sample RDF: exactly 5, covering different types
- SPARQL queries: exactly 7 (2 basic, 3 intermediate, 2 advanced) including required ones
- Cross-references by RDF pattern, all databases listed
- Architectural notes in YAML bullets (include cross-database if applicable)
- Statistics: counts, coverage, cardinality, performance (include cross-database notes if applicable)
- 2-3 anti-patterns with wrong/correct versions
- 2-3 common errors with solutions
- Metadata in schema_info (version, license, access)
- File is valid YAML, compact yet complete

## Remember
**The goal: Compact, Complete, Clear, Correct, Actionable**
- Document ALL entity types, not just some
- Include cross-database queries if database shares endpoint with others
- 2-3 anti-patterns prevent common mistakes  
- If it doesn't help query writing, omit it
- NEVER assume first results represent entire database
- Cross-database queries should show practical integration value