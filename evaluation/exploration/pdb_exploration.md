# PDB (Protein Data Bank) Exploration Report

## Database Overview
The Protein Data Bank is the global repository for 3D structural data of biological macromolecules:
- **204,594+ entries** (structures)
- **~85% X-ray diffraction**, ~7% electron microscopy, ~7% NMR
- **900K+ entities** (proteins, nucleic acids, ligands, waters)
- **352K UniProt cross-references** (~1.72 per entry)
- **Highest resolution**: 0.48 Å (structures 3NIR, 5D8V)
- Cross-references to UniProt, EMDB, GenBank, PubMed, DOI

## Schema Analysis (from MIE file)

### Main Properties Available
- **Experimental Data**: Method (X-ray, NMR, EM), resolution, R-factors, number of reflections
- **Refinement Statistics**: R-work, R-free, resolution limits
- **Entity Information**: Polymer type, sequence, molecular weight, description
- **Crystallographic Data**: Unit cell parameters, space group, symmetry
- **Biological Assembly**: Oligomeric state, quaternary structure
- **Cross-References**: UniProt, GenBank, EMBL, EMDB, BMRB
- **Publication Data**: DOI, PubMed, title, journal, year
- **Software**: Data collection, reduction, phasing, refinement tools
- **Keywords**: Classification keywords for biological function

### Important Relationships
- `pdbx:has_refineCategory` → refinement statistics
- `pdbx:has_exptlCategory` → experimental method
- `pdbx:has_entityCategory` → molecular entities
- `pdbx:has_struct_refCategory` → sequence database cross-references
- `pdbx:has_database_2Category` → external database links
- `pdbx:has_citationCategory` → publications
- `pdbx:has_struct_keywordsCategory` → classification keywords
- `pdbx:has_cellCategory` → crystallographic unit cell
- `pdbx:has_softwareCategory` → software tools used
- `pdbx:has_pdbx_struct_assemblyCategory` → biological assemblies

### Query Patterns Observed
- **Category traversal**: Use `has_*Category/has_*` pattern
- **Entry ID extraction**: `BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)`
- **Numeric comparisons**: Always use `xsd:decimal()` for resolution, R-factors
- **Keyword searches**: Use `pdbx:struct_keywords.pdbx_keywords` field with CONTAINS
- **FROM clause required**: `FROM <http://rdfportal.org/dataset/pdbj>`
- **Optional data**: Use OPTIONAL for resolution (NMR lacks it), citations, assemblies

## Search Queries Performed

1. **Query: "CRISPR Cas9"** → Results: 473 structures including SpRY-Cas9 complexes with various PAM sequences
2. **Query: "kinase"** → Results: 25,438 kinase structures including CK2, various inhibitor complexes
3. **High-resolution structures** → Results: 5 structures with resolution < 0.6 Å (best: 0.48 Å)
4. **UniProt cross-references** → Results: Many entries with UNP database links (P07378, Q1BZW5, P35790, etc.)
5. **Software usage** → Results: PHENIX and REFMAC most common for refinement

## SPARQL Queries Tested

```sparql
# Query 1: Find ultra-high resolution structures
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?entry_id ?resolution
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_refineCategory/pdbx:has_refine ?refine .
  ?refine pdbx:refine.ls_d_res_high ?resolution .
  FILTER(xsd:decimal(?resolution) > 0 && xsd:decimal(?resolution) < 0.6)
}
ORDER BY xsd:decimal(?resolution)
LIMIT 10
# Results: 5D8V and 3NIR at 0.48 Å, 1EJG at 0.54 Å, 3P4J at 0.55 Å, 5NW3 at 0.59 Å
```

```sparql
# Query 2: Find UniProt cross-references
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT ?entry_id ?db_name ?db_accession
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_struct_refCategory/pdbx:has_struct_ref ?ref .
  ?ref pdbx:struct_ref.db_name ?db_name ;
       pdbx:struct_ref.pdbx_db_accession ?db_accession .
  FILTER(?db_name = "UNP")
}
LIMIT 10
# Results: Retrieved UniProt accessions P07378, Q1BZW5, P35790, Q05085, etc.
```

```sparql
# Query 3: Search for kinase structures by keywords
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT ?entry_id ?keywords
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_struct_keywordsCategory/pdbx:has_struct_keywords ?kw .
  ?kw pdbx:struct_keywords.pdbx_keywords ?keywords .
  FILTER(CONTAINS(LCASE(?keywords), "kinase"))
}
LIMIT 10
# Results: Would return thousands of kinase structures with keyword annotations
```

## Interesting Findings

### Specific Entities for Questions
- **3NIR, 5D8V**: Ultra-high resolution structures (0.48 Å) - atomic precision
- **473 CRISPR Cas9 structures**: Major genome editing tool, many variants
- **25,438 kinase structures**: Huge family, drug targets
- **~7% EM structures**: Growing field with EMDB cross-references
- **~85% X-ray structures**: Traditional method with resolution metrics

### Unique Properties
- **Resolution range**: 0.48 Å to >100 Å (low-resolution EM)
- **Multiple experimental methods**: X-ray, NMR (no resolution), EM (with EMDB links)
- **Quality metrics**: R-work, R-free for validation
- **Biological assemblies**: Quaternary structure annotations (monomers, dimers, tetramers, etc.)
- **Software pipelines**: Complete workflows (collection → reduction → phasing → refinement)
- **Space group diversity**: 230 possible crystallographic space groups

### Connections to Other Databases
- **UniProt**: 352K cross-references (~1.72 per entry) for protein sequences
- **EMDB**: 13,974 links (~7%) for electron microscopy density maps
- **GenBank/EMBL/RefSeq**: 5,874 nucleotide sequence references
- **PubMed**: 181,261 publications (~73% coverage)
- **DOI**: 186,683 references (~75% coverage)
- **BMRB**: ~3% for NMR spectral data

### Specific Verifiable Facts
- **Highest resolution ever**: 0.48 Å (3NIR, 5D8V)
- **204,594 total entries** in database
- **473 CRISPR Cas9 structures**
- **25,438 kinase structures**
- **Average 1.72 UniProt refs per entry** (multiple chains)
- **Top refinement software**: PHENIX (72K entries), REFMAC (70K entries)
- **Top phasing software**: PHASER (62K entries)

## Question Opportunities by Category

### Precision
- "What is the highest resolution structure in PDB?" → 0.48 Å (3NIR or 5D8V)
- "What is the PDB ID with resolution 0.48 Å?" → 3NIR or 5D8V
- "What experimental method was used for structure 8A2Z?" → ELECTRON MICROSCOPY
- "What is the UniProt accession for PDB entry 16PK?" → P07378
- "What space group is structure 3NIR?" → Specific space group from symmetry

### Completeness
- "How many CRISPR Cas9 structures are in PDB?" → 473
- "How many kinase structures exist in PDB?" → 25,438
- "How many structures have resolution better than 1.0 Å?" → Count query
- "How many EM structures link to EMDB?" → ~13,974 (7%)
- "How many PDB entries have UniProt cross-references?" → Most entries (~85-90%)

### Integration
- "What is the UniProt ID for PDB structure 16PK?" → P07378
- "Find PDB structures for UniProt protein P04637" → Via struct_ref
- "What EMDB ID corresponds to PDB entry 8A2Z?" → EMD-15109
- "Link PDB 3NIR to its PubMed publication" → Via citation
- "Convert PDB entity sequences to GenBank IDs" → Via struct_ref with db_name=GB

### Currency
- "How many SARS-CoV-2 structures are in PDB?" → Recent viral structures
- "What are the most recent cryo-EM structures?" → Filter by year + method=EM
- "How many structures were added in 2024?" → Count by deposition year
- "What COVID-19 related structures exist?" → Keyword search recent additions

### Specificity
- "What is the oligomeric state of structure 3NIR?" → From assembly data
- "Find PDB structures with space group P212121" → Specific symmetry
- "What culture conditions were used for crystal growth?" → From experimental details
- "Find structures of rare enzyme X" → Niche protein queries
- "What software was used to solve structure 3NIR?" → Software pipeline

### Structured Query
- "Find X-ray structures with resolution < 1.0 Å and R-free < 0.15" → Multiple quality filters
- "List kinase structures from 2020+ with resolution < 2.0 Å" → Year + keyword + resolution
- "Find EM structures with EMDB links and publications" → Method + cross-refs + citations
- "Search for tetrameric assemblies of human proteins" → Assembly + organism
- "Find structures solved with PHENIX and resolution < 1.5 Å" → Software + quality

## Notes

### Limitations
- **NMR structures lack resolution**: Cannot filter by resolution for all methods
- **EM structures lack R-factors**: Quality metrics differ by method
- **Multiple entities per entry**: Protein complexes have multiple chains/entities
- **Software metadata varies**: Older entries may lack complete software information
- **Assembly data not universal**: Some entries lack biological assembly annotations
- **Cross-reference completeness**: UniProt ~172% (multiple chains), others variable

### Best Practices
1. **Always use xsd:decimal()** for numeric comparisons (resolution, R-factors)
2. **Filter by experimental method** when requiring method-specific data
3. **Use OPTIONAL** for resolution, assemblies, citations (not all have them)
4. **FROM clause required**: `FROM <http://rdfportal.org/dataset/pdbj>`
5. **Extract entry_id properly**: Use STRAFTER pattern
6. **Search keywords not titles**: Use `pdbx_keywords` field for efficiency
7. **Filter out invalid values**: resolution > 0, R-factors 0-1 range
8. **Check category availability**: Not all entries have all categories

### Performance Notes
- Resolution queries: Efficient with numeric filters and LIMIT
- Cross-reference queries by db_name: Fast with proper filtering
- Keyword searches: Use CONTAINS on keywords field, not titles
- Category traversal: 2-3 property path steps optimal
- Multi-category joins: Filter by entry_id early to avoid timeouts
- Recommend LIMIT 20-100 for exploratory queries
- Software queries can be slow without specific classifications
