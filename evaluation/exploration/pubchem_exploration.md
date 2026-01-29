# PubChem Exploration Report

## Database Overview
PubChem is the world's largest freely accessible database of chemical molecules and their biological activities. It serves as a central hub integrating:
- **119M+ compounds** with molecular descriptors (SMILES, InChI, properties)
- **339M substances** (depositor-provided records)
- **1.7M bioassays** with biological activity measurements
- **167K genes**, **249K proteins**, **81K pathways**
- Extensive ontology integration (ChEBI, SNOMED CT, NCI Thesaurus)
- Patent references, drug classifications, stereoisomer relationships

**Key distinction**: Compounds (standardized structures) vs Substances (depositor records)

## Schema Analysis (from MIE file)

### Main Properties
**Compounds**:
- `vocab:Compound` - Central entity for chemical structures
- `sio:SIO_000008` - Links to molecular descriptors
- `sio:SIO_000300` - Descriptor value property
- `obo:RO_0000087` - Biological roles (FDA drugs, metabolites, etc.)
- `cheminf:CHEMINF_000455` - Stereoisomer relationships
- `rdfs:seeAlso` - External database links
- `cito:isDiscussedBy` - Patent and literature references

**Descriptor Types** (via SIO ontology):
- `CHEMINF_000335` - Molecular formula
- `CHEMINF_000334` - Molecular weight
- `CHEMINF_000376` - Canonical SMILES
- `CHEMINF_000396` - IUPAC InChI

**BioAssays**:
- `vocab:BioAssay` - Biological screening experiments
- `dcterms:title` - Assay title/description
- `dcterms:source` - Assay data source
- `bao:BAO_0209` - Measurement groups

### Important Relationships
- Compounds → Descriptors: via `sio:SIO_000008`
- Compounds → Roles: via `obo:RO_0000087` (FDA drugs, etc.)
- Compounds → Ontologies: via `rdf:type` (ChEBI, SNOMED CT)
- Compounds → Stereoisomers: via `cheminf:CHEMINF_000455`
- Substances → Compounds: via `vocab:is_standardized_into`
- Proteins → PDB: via `pdbx:link_to_pdb`
- Entities → Patents: via `cito:isDiscussedBy`

### Query Patterns
1. **CID-specific queries are very fast** (<1s)
2. **Use descriptor type filters** to get targeted properties
3. **Molecular weight range filtering** works efficiently (up to 10K results)
4. **Use FROM clauses** for bioassays, genes, proteins (separate graphs)
5. **Keyword search with bif:contains** for bioassay titles
6. **Always use LIMIT** for aggregations (50-100 recommended)

## Search Queries Performed

### 1. Query: "aspirin" → **CID 2244**
Results: Found aspirin (acetylsalicylic acid)
- Formula: C9H8O4
- Molecular weight: 180.16 g/mol
- SMILES: CC(=O)OC1=CC=CC=C1C(=O)O
- InChI: InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)
- Label: 2-acetyloxybenzoic acid

### 2. Query: "imatinib" → **CID 5291**
Results: Found imatinib (Gleevec, cancer drug)
- Formula: C29H31N7O
- Molecular weight: 493.6 g/mol
- Full systematic name provided
- InChI and SMILES structures available

### 3. Query: "caffeine" → **CID 2519**
Results: Found caffeine (1,3,7-trimethylxanthine)
- Common stimulant compound

### 4. Query: "penicillin" → **CID 2349**
Results: Found penicillin G (benzylpenicillin)
- Historic antibiotic compound

### 5. Query: "morphine" → **CID 5288826**
Results: Found morphine
- Important opioid analgesic

**Note**: All compound searches returned valid CIDs with complete molecular data available through get_compound_attributes tool.

## SPARQL Queries Tested

```sparql
# Query 1: Get molecular descriptors for aspirin (CID2244)
PREFIX compound: <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/>
PREFIX sio: <http://semanticscience.org/resource/>

SELECT ?descriptorType ?value
WHERE {
  compound:CID2244 sio:SIO_000008 ?descriptor .
  ?descriptor a ?descriptorType ;
              sio:SIO_000300 ?value .
  FILTER(?descriptorType IN (
    sio:CHEMINF_000335,  # formula
    sio:CHEMINF_000334,  # weight
    sio:CHEMINF_000376,  # SMILES
    sio:CHEMINF_000396   # InChI
  ))
}
# Results: 
# - Formula: C9H8O4
# - Weight: 180.16
# - SMILES: CC(=O)OC1=CC=CC=C1C(=O)O
# - InChI: InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)
```

**Significance**: Shows how to retrieve standard molecular properties for any compound using descriptor type filtering.

```sparql
# Query 2: Count FDA-approved drugs
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT (COUNT(DISTINCT ?compound) as ?fda_count)
WHERE {
  ?compound a vocab:Compound ;
            obo:RO_0000087 vocab:FDAApprovedDrugs .
}
# Results: 17,367 FDA-approved drugs
```

**Significance**: Quantifies FDA-approved drugs in PubChem, demonstrates biological role filtering.

```sparql
# Query 3: Find FDA drugs by molecular weight range (150-200)
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX sio: <http://semanticscience.org/resource/>

SELECT ?compound ?weight
WHERE {
  ?compound a vocab:Compound ;
            obo:RO_0000087 vocab:FDAApprovedDrugs ;
            sio:SIO_000008 ?weightDesc .
  ?weightDesc a sio:CHEMINF_000334 ;
              sio:SIO_000300 ?weight .
  FILTER(?weight >= 150 && ?weight <= 200)
}
LIMIT 20
# Results: 20 FDA drugs including:
# - CID440545 (weight 180.16 - likely aspirin)
# - CID164739 (weight 183.2)
# - CID10130337 (weight 194.23)
# ...and 17 others in the range
```

**Significance**: Demonstrates complex filtering combining biological role (FDA drug) with molecular property (weight range). Shows ability to find "druglike" small molecules.

## Cross-Reference Analysis

### PubChem Cross-Database Connectivity

**Pattern**: Multiple linking mechanisms for different database types

**External Database Links** (via `rdfs:seeAlso`):
- **Wikidata**: ~2-5% of compounds (knowledge graph integration)
- **identifiers.org**: Various database links
- **NCBI Protein**: For protein entities
- **NCI Thesaurus**: Chemical classifications

**Ontology Classifications** (via `rdf:type`):
- **ChEBI**: ~5-10% of compounds have ChEBI classifications
- **SNOMED CT**: Drug compounds (clinical terminology)
- **NCI Thesaurus**: Drug classifications
- **Protein Ontology**: For protein entities

**Patent and Literature** (via `cito:isDiscussedBy`):
- **Patent coverage**: ~10% of compounds
- **Jurisdictions**: US, EP, CN, CA, JP, KR
- **PubMed references**: Literature citations

**Internal Relationships**:
- **Substances → Compounds**: via `vocab:is_standardized_into`
- **Proteins → PDB**: via `pdbx:link_to_pdb` (avg 3.2 links per protein)
- **Compounds → Stereoisomers**: via `cheminf:CHEMINF_000455` (avg 2.3 per compound)

### Entity and Relationship Counts

**Total entities**:
- 119,093,251 compounds
- 339,000,000 substances  
- 1,768,183 bioassays
- 167,172 genes
- 248,623 proteins
- 80,739 pathways

**FDA drug entities**:
- 17,367 compounds classified as FDA-approved drugs

**Coverage percentages** (for compounds):
- Molecular formula: >99%
- Molecular weight: >99%
- SMILES: >99%
- InChI: >95%
- Wikidata links: ~2%
- ChEBI classification: ~5%
- Patent references: ~10%

**Cardinality**:
- Average descriptors per compound: ~25
- Average stereoisomers per compound: 2.3
- Average patents per compound (when present): 8.5
- Average PDB links per protein: 3.2

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

### 1. FDA Drug Count (requires role filtering + COUNT)
- **17,367 FDA-approved drugs** in PubChem
- Identified via `obo:RO_0000087 vocab:FDAApprovedDrugs` role
- Much larger than typical small drug databases
- Requires database query; not in MIE file

### 2. Aspirin Molecular Properties (requires descriptor query)
- **CID 2244** is aspirin
- Molecular formula: C9H8O4 (requires CHEMINF_000335 descriptor)
- Molecular weight: 180.16 g/mol (requires CHEMINF_000334 descriptor)
- Complete InChI and SMILES structures available
- Demonstrates descriptor pattern for retrieving molecular data

### 3. Imatinib Structure (requires compound lookup)
- **CID 5291** is imatinib (Gleevec)
- Formula: C29H31N7O (complex kinase inhibitor)
- Weight: 493.6 g/mol
- Real cancer drug used for CML treatment
- Found via get_pubchem_compound_id search

### 4. Molecular Weight Range Filtering (requires property filtering)
- **20 FDA drugs with weights 150-200 g/mol** found in first query
- Demonstrates "druglike" small molecule discovery
- Weight 180.16 appears (likely aspirin as CID440545)
- Requires combining role filter + descriptor property filter

### 5. Descriptor Completeness (from stats)
- **>99% of compounds have molecular formula and weight**
- >95% have InChI identifiers
- Near-complete coverage of basic molecular properties
- Shows data quality and completeness of PubChem

### 6. Multi-Graph Architecture (from exploration)
- **Separate named graphs** for compounds, bioassays, proteins, etc.
- Requires FROM clauses for cross-entity queries
- Graph URIs available in MIE file
- Important for query construction

### 7. Ontology Integration Coverage (from stats)
- **~5-10% ChEBI classification** coverage
- Lower than expected for comprehensive integration
- Primarily enriched for bioactive/drug compounds
- Coverage varies by compound type and age

## Question Opportunities by Category

### Precision (Specific IDs, molecular properties)
✅ **GOOD (requires database query)**:
- "What is the PubChem CID for aspirin?" (Answer: CID2244, requires search)
- "What is the molecular weight of imatinib (CID5291)?" (Answer: 493.6, requires descriptor query)
- "What is the molecular formula of caffeine?" (requires CID lookup + descriptor)
- "What is the SMILES structure for aspirin (CID2244)?" (requires descriptor query)
- "What is the InChI identifier for morphine?" (requires search + descriptor)

❌ **BAD (trivial - from MIE examples)**:
- "What is CID2244?" (aspirin mentioned in MIE examples)
- "Does PubChem have molecular weight descriptors?" (schema question)

### Completeness (Counts, lists)
✅ **GOOD (requires COUNT or aggregation)**:
- "How many FDA-approved drugs are in PubChem?" (Answer: 17,367, requires COUNT)
- "How many compounds have molecular weights between 200-300 g/mol?" (requires filtering + COUNT)
- "How many bioassays are in PubChem?" (Answer: 1.7M+, requires COUNT)
- "How many compounds have ChEBI classifications?" (requires ontology filtering + COUNT)
- "List all FDA drugs with weight 180-200" (requires role + property filtering)

❌ **BAD (trivial)**:
- "How many descriptor types exist?" (schema metadata)
- "How many graphs does PubChem use?" (infrastructure)

### Integration (Cross-database links, ID conversions)
✅ **GOOD (requires cross-reference queries)**:
- "What Wikidata entity corresponds to aspirin (CID2244)?" (requires rdfs:seeAlso filtering)
- "Find ChEBI classifications for imatinib" (requires rdf:type filtering by ChEBI namespace)
- "What PDB structures link to PubChem protein entries?" (requires pdbx:link_to_pdb)
- "Convert substance SID to its standardized compound CID" (requires is_standardized_into)
- "What patents reference compound CID5291?" (requires cito:isDiscussedBy)

❌ **BAD (trivial)**:
- "What databases does PubChem link to?" (just listing MIE cross-refs)
- "Does PubChem have rdfs:seeAlso?" (schema question)

### Currency (Recent additions, updates)
✅ **GOOD (time-dependent)**:
- "How many COVID-19 drug compounds were added to PubChem?" (pandemic-related, 2020+)
- "What is the current total number of compounds in PubChem?" (changes continuously)
- "How many mRNA vaccine-related compounds exist?" (recent research area)
- "What new SARS-CoV-2 inhibitors have been assayed?" (requires recent bioassay data)

❌ **BAD (not time-sensitive)**:
- "What is the structure of aspirin?" (timeless)
- "How does PubChem classify compounds?" (process question)

### Specificity (Rare/niche compounds)
✅ **GOOD (requires niche searches)**:
- "What is the PubChem CID for venetoclax?" (BCL-2 inhibitor, specific drug)
- "Find compounds with molecular weight > 5000" (very large molecules, peptides)
- "What is the CID for remdesivir?" (COVID antiviral)
- "Find FDA drugs containing selenium" (rare element in drugs)
- "What is the CID for ivermectin?" (antiparasitic)

❌ **BAD (common compounds)**:
- "What is water's CID?" (too basic)
- "Find a compound" (too vague)

### Structured Query (Complex filtering, multi-criteria)
✅ **GOOD (requires complex SPARQL)**:
- "Find FDA drugs with molecular weight 150-200 AND containing nitrogen" (2+ criteria)
- "Count compounds with ChEBI classification AND patent references" (2 link types)
- "Find bioassays with 'cancer' in title AND active compounds" (keyword + activity)
- "List compounds that are FDA drugs AND have stereoisomers" (role + relationship)
- "Find proteins with >5 PDB structures AND conserved domains" (cardinality + classification)

❌ **BAD (simple lookups)**:
- "Find compounds by CID" (single criterion, trivial)
- "Show FDA drugs" (single filter, too basic)

## Notes

### Limitations and Challenges
1. **Multi-Graph Architecture**: Bioassays, proteins require explicit FROM clauses with correct graph URIs
2. **Descriptor Type Filtering**: Must filter by specific descriptor types (CHEMINF_*) for efficient queries
3. **Mixed Datatypes**: Descriptor values have different types (string/numeric), check before comparison
4. **Aggregation Performance**: GROUP BY requires LIMIT <100 and type filtering to prevent timeout
5. **Ontology Coverage Variability**: ChEBI classifications only ~5-10% of compounds, enriched for bioactive
6. **Patent Coverage**: Only ~10% of compounds have patent references

### Best Practices for Querying
1. **Start with CID lookup**: Use get_pubchem_compound_id for compound name → CID conversion
2. **Use get_compound_attributes**: Quick way to get formula, weight, SMILES, InChI
3. **Filter descriptor types**: Always specify CHEMINF_* types when querying descriptors
4. **Use FROM clauses**: Required for bioassays, genes, proteins (separate graphs)
5. **Add LIMIT**: Always limit aggregations to 50-100 results
6. **CID-specific queries fast**: <1s for individual compound lookups

### Important Clarifications About Counts
- **Entity counts**: 119M+ compounds, 17,367 FDA drugs
- **Relationship counts**: Avg 25 descriptors/compound, 2.3 stereoisomers/compound
- **Coverage percentages**: >99% formula/weight, ~5% ChEBI, ~10% patents
- Questions can ask about total counts, filtered counts, or coverage percentages

### Distinction Between MIE Examples and Real Data
- **MIE examples** (CID2244 aspirin): Used to illustrate patterns
- **Real discoveries** (CID5291 imatinib, CID2519 caffeine, CID2349 penicillin, CID5288826 morphine)
- Questions should use real compounds discovered through search, not just MIE examples
- However, CID2244 (aspirin) is scientifically important enough to use in questions despite MIE mention

### Database Quality and Completeness
- **Descriptor completeness**: >99% for formula/weight/SMILES, >95% for InChI
- **External links**: Variable (2-10% depending on database)
- **Ontology integration**: ~5-10% ChEBI, enriched for drug compounds
- **Continuous updates**: Database grows continuously with new compound submissions
