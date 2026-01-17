# MIE Prompt Changelog - Cross-Database MIE File Referencing

## Summary
Updated the MIE file creation prompt to include comprehensive instructions for referencing co-located databases' MIE files when creating cross-database query examples.

## Key Changes

### 1. Enhanced Discovery Phase (Section 3.5)

**Added Step 1: Retrieve MIE files for co-located databases**
```python
for co_db in shared_databases:
    if co_db != dbname:
        try:
            mie_content = get_MIE_file(co_db)
            # Extract: graph URIs, entity types, linking properties, prefixes
```

**Benefits of retrieving MIE files:**
- Correct graph URIs for GRAPH clauses
- Entity type definitions and class URIs
- Property patterns and namespaces
- Known cross-references and linking properties
- Anti-patterns to avoid

**Added Step 4: Reference co-located database schemas**
When creating cross-database queries:
- Use correct entity type URIs from retrieved MIE files
- Apply property patterns documented in co-database MIE files
- Follow prefix conventions from co-database MIE files
- Avoid anti-patterns documented in co-database MIE files
- Use successful query patterns from co-database sparql_query_examples

### 2. Enhanced Cross-Database Query Guidelines

**Added "CRITICAL: Reference Co-Located Database MIE Files" section**

Before creating cross-database query examples:
1. Retrieve MIE files using `get_MIE_file(co_db_name)`
2. Extract key information:
   - Graph URIs from `schema_info.graphs`
   - PREFIX definitions from `shape_expressions`
   - Entity type URIs from `shape_expressions`
   - Property patterns from `sample_rdf_entries`
   - Linking properties from `cross_references`
   - Anti-patterns to avoid from `anti_patterns`
3. Use this information to create accurate queries
4. Document which MIE files were consulted

**Why this matters:**
- Ensures correct graph URIs (avoid query failures)
- Uses proper entity types and properties (avoid empty results)
- Follows established naming conventions (consistency)
- Avoids known anti-patterns (better performance)
- Creates queries that align with existing documentation

**Added Best Practice #6:**
- **Reference MIE files** - use correct URIs, types, and patterns from co-database documentation

### 3. Updated Template Structure

**Enhanced cross_database_queries section with inline comments:**
```yaml
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
```

### 4. Enhanced Quality Assurance Checklist

**Updated Cross-Database section with 10 specific checks:**
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

## Benefits of These Changes

### 1. **Accuracy**
- Queries use verified graph URIs, entity types, and properties
- Reduces errors from incorrect URIs or non-existent properties
- Ensures queries actually work on first attempt

### 2. **Consistency**
- Cross-database queries follow established patterns
- Naming conventions align across related databases
- Documentation style remains consistent

### 3. **Quality**
- Avoids repeating mistakes documented in anti-patterns
- Leverages proven query patterns from co-databases
- Creates queries that align with existing documentation

### 4. **Efficiency**
- Faster query development using existing schemas
- Less trial-and-error when finding correct URIs
- Reduces need for extensive testing

### 5. **Maintainability**
- Clear documentation of which MIE files influenced queries
- Easy to update when co-database schemas change
- Transparent dependencies between database documentations

## Example Workflow

When creating ChEMBL MIE file with cross-database queries:

1. **Discover co-located databases:**
   ```python
   endpoints = get_sparql_endpoints()
   # ChEMBL is on 'ebi' endpoint with: chebi, reactome, ensembl, amrportal
   ```

2. **Retrieve MIE files:**
   ```python
   chebi_mie = get_MIE_file('chebi')
   reactome_mie = get_MIE_file('reactome')
   ensembl_mie = get_MIE_file('ensembl')
   ```

3. **Extract key information:**
   - ChEBI graph: `http://rdf.ebi.ac.uk/dataset/chebi`
   - ChEBI entity type: `owl:Class` with ChEBI_ prefix
   - ChEBI linking: `skos:exactMatch`
   - ChEBI formula property: `chebi:formula` (note namespace!)

4. **Create accurate cross-database query:**
   ```sparql
   PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
   PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
   PREFIX owl: <http://www.w3.org/2002/07/owl#>
   
   SELECT ?molecule ?chebiLabel ?formula
   WHERE {
     GRAPH <http://rdf.ebi.ac.uk/dataset/chembl> {
       ?molecule a cco:SmallMolecule ;
                 skos:exactMatch ?chebiId .
     }
     GRAPH <http://rdf.ebi.ac.uk/dataset/chebi> {
       ?chebiId a owl:Class ;
                rdfs:label ?chebiLabel ;
                chebi:formula ?formula .
     }
   }
   LIMIT 50
   ```

5. **Document in notes:**
   ```yaml
   notes: |
     - Graph URIs from ChEMBL and ChEBI MIE files
     - Entity types verified against shape expressions
     - Uses skos:exactMatch linking pattern from ChEMBL cross_references
     - Note: ChEBI uses chebi/ namespace for properties (not chebi#)
   ```

## Implementation Notes

- Changes are backward compatible - existing MIE files without cross-database queries remain valid
- Only applies to databases sharing SPARQL endpoints
- Gracefully handles cases where co-database MIE files don't exist yet
- Emphasizes verification and documentation over assumptions

## Files Modified

- `/Users/arkinjo/work/GitHub/togo-mcp/resources/MIE_prompt.md`

## Version

- MIE Prompt Version: 1.1 (with cross-database MIE file referencing)
- Date: 2025-01-16
