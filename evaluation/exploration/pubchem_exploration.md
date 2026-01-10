# PubChem Exploration Report

## Database Overview
PubChem is a comprehensive public database of chemical molecules and biological activities containing:
- **119 million compounds** with molecular descriptors (SMILES, InChI, molecular properties)
- **339 million substances**
- **1.7 million bioassays** with activity data
- **167K genes, 249K proteins, 81K pathways**
- **17,367 FDA-approved drugs**
- Integration with chemical ontologies (ChEBI, SNOMED CT, NCI), patent information, drug classifications, stereoisomer relationships

## Schema Analysis (from MIE file)

### Main Properties Available
- **Molecular Descriptors**: Formula, weight, SMILES, InChI, TPSA
- **Drug Roles**: FDA approval status, biological roles
- **Ontology Classifications**: ChEBI, SNOMED CT, NCI classifications
- **External Links**: Wikidata (~2% compounds), identifiers.org
- **Patent References**: US, EP, CN, CA, JP, KR jurisdictions (~10% compounds)
- **Bioactivity Data**: Cell line assays, screening results
- **Protein-Structure Links**: PDB cross-references

### Important Relationships
- `sio:SIO_000008` - Links compound to descriptors
- `sio:SIO_000300` - Descriptor values
- `obo:RO_0000087` - Drug roles (e.g., FDA approval)
- `cheminf:CHEMINF_000455` - Stereoisomer relationships
- `vocab:is_standardized_into` - Substance to compound mapping
- `pdbx:link_to_pdb` - Protein to PDB structure links
- `cito:isDiscussedBy` - Patent and literature references

### Query Patterns Observed
- **CID-based queries**: Very efficient (<1s)
- **Descriptor filtering**: Requires type specification
- **Weight range queries**: Efficient up to 10K results
- **Multi-graph queries**: Need explicit FROM clauses for bioassays, proteins
- **Aggregations**: Must use LIMIT <100 and type filters

## Search Queries Performed

1. **Query: "aspirin"** → Result: CID2244, molecular formula C9H8O4, MW 180.16, full SMILES and InChI
2. **Query: "imatinib"** → Result: CID5291, cancer drug, molecular formula C29H31N7O, MW 493.6
3. **Query: "caffeine"** → Result: CID2519, stimulant compound
4. **Query: "resveratrol"** → Result: CID445154, polyphenol, C14H12O3, MW 228.24
5. **FDA drugs MW 150-200** → Result: 20 FDA-approved drugs in this range (aspirin, morphine derivatives, etc.)

## SPARQL Queries Tested

```sparql
# Query 1: Get molecular descriptors for aspirin
PREFIX compound: <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/>
PREFIX sio: <http://semanticscience.org/resource/>

SELECT ?descriptorType ?value
WHERE {
  compound:CID2244 sio:SIO_000008 ?descriptor .
  ?descriptor a ?descriptorType ;
              sio:SIO_000300 ?value .
  FILTER(?descriptorType IN (
    sio:CHEMINF_000335,  # Formula
    sio:CHEMINF_000334,  # Weight
    sio:CHEMINF_000376,  # SMILES
    sio:CHEMINF_000396   # InChI
  ))
}
# Results: Retrieved C9H8O4, 180.16, SMILES, InChI for aspirin
```

```sparql
# Query 2: Find FDA drugs by molecular weight range
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
# Results: 20 FDA-approved drugs including aspirin (CID440545), morphine derivatives, etc.
```

```sparql
# Query 3: List bioassays with titles
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?bioassay ?title
FROM <http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay>
WHERE {
  ?bioassay a vocab:BioAssay ;
            dcterms:title ?title .
}
LIMIT 5
# Results: Anti-inflammatory assays in RAW264.7 cells testing TNFα, COX-2, NF-κB, iNOS, NO production
```

## Interesting Findings

### Specific Entities for Questions
- **CID2244**: Aspirin - classic drug with all descriptors
- **CID5291**: Imatinib - cancer drug with complex structure
- **CID445154**: Resveratrol - polyphenol with biological activity
- **FDA drugs in specific MW ranges**: Useful for structured queries
- **Bioassays AID1932045-1932049**: Anti-inflammatory activity assays

### Unique Properties
- **Stereoisomer tracking**: Can query related stereoisomers
- **Multi-jurisdiction patent coverage**: US, EP, JP, etc.
- **Layered descriptor system**: SIO ontology for all molecular properties
- **Separated named graphs**: Requires FROM clauses for bioassays, proteins
- **Ontology integration**: ChEBI, SNOMED CT classifications for drugs

### Connections to Other Databases
- **ChEBI**: ~5-10% compounds have ChEBI classifications
- **Wikidata**: ~2% compounds linked
- **NCBI Protein**: Via identifiers.org
- **PDB**: Protein structures linked via pdbx:link_to_pdb
- **UniProt**: Through protein cross-references

### Specific Verifiable Facts
- **119,093,251 total compounds**
- **17,367 FDA-approved drugs**
- **1,768,183 bioassays**
- Aspirin MW exactly 180.16 g/mol
- Imatinib formula C29H31N7O (cancer drug)

## Question Opportunities by Category

### Precision
- "What is the PubChem CID for aspirin?" → CID2244
- "What is the molecular weight of imatinib (CID5291)?" → 493.6
- "What is the molecular formula of resveratrol?" → C14H12O3
- "What is the SMILES notation for caffeine?" → From descriptors
- "What is the InChI for aspirin?" → From descriptors

### Completeness
- "How many FDA-approved drugs are in PubChem?" → 17,367
- "How many compounds have molecular weight between 100-150?" → Count query
- "How many bioassays are in PubChem?" → 1,768,183
- "List all FDA drugs with MW exactly 180.16" → Multiple compounds
- "How many compounds have ChEBI classifications?" → ~5-10% of total

### Integration
- "What is the ChEBI ID for aspirin in PubChem?" → Via rdf:type
- "Find PubChem compounds linked to UniProt protein P04637" → Via cross-refs
- "Convert PubChem CID2244 to Wikidata entity" → Via rdfs:seeAlso
- "What PDB structures are linked to PubChem protein 10GS_A?" → Via pdbx links

### Currency
- "How many COVID-19 related bioassays are in PubChem?" → Search recent assays
- "What are the most recently added FDA drugs?" → Recent compounds
- "How many SARS-CoV-2 related compounds?" → Current count

### Specificity
- "What is the molecular weight of the rare drug gefitinib?" → Specific CID
- "Find PubChem CID for the niche compound shikonin" → Rare natural product
- "What are the stereoisomers of thalidomide?" → Specific relationship

### Structured Query
- "Find FDA drugs with MW 150-200 and ChEBI classification" → Complex filter
- "List compounds with IC50 values <100nM in kinase bioassays" → Multi-criteria
- "Find all compounds that are both FDA drugs AND have patent references" → AND logic
- "Search for compounds with molecular formula C9H8O4 AND MW 180-190" → Multiple filters

## Notes

### Limitations
- **Multi-graph architecture**: Must use explicit FROM clauses for bioassays, proteins, genes
- **Large dataset**: Aggregations require LIMIT constraints
- **Mixed datatypes**: Descriptor values can be strings, doubles, or integers
- **Coverage variation**: External links vary from 2% (Wikidata) to >99% (basic descriptors)

### Best Practices
1. **Always specify CID** for compound queries when possible
2. **Use descriptor type filters** (CHEMINF_000334, etc.) to target specific properties
3. **Add LIMIT 100** to exploratory queries
4. **Use FROM clauses** for bioassay, protein, gene graphs
5. **Filter by namespace** for ontology queries (STRSTARTS)
6. **Type filter first**: Filter by vocab:Compound before other criteria

### Performance Notes
- CID-based queries: <1 second
- Weight range filtering: Efficient up to 10K results
- Bioassay queries: Fast with FROM clause
- Aggregations: Require LIMIT and type filters
- Cross-graph joins: Slow without specific entity IDs
