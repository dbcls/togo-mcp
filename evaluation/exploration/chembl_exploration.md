# ChEMBL Exploration Report

## Database Overview
ChEMBL is a manually curated bioactive molecule database for drug discovery containing:
- **2.4M+ compounds** with drug-like properties
- **1.6M assays** (binding, functional, ADMET)
- **20M bioactivity measurements** (IC50, EC50, Ki, etc.)
- **13K targets** (proteins, protein complexes, cell lines)
- Cross-references to UniProt, PDB, PubChem, DrugBank

**Core model**: Molecule → Activity → Assay → Target pathway for structure-activity relationships

## Schema Analysis (from MIE file)

### Main Properties
**Molecules**:
- `cco:SmallMolecule` - Drug-like compounds
- `cco:chemblId` - ChEMBL identifier (e.g., "CHEMBL25")
- `cco:highestDevelopmentPhase` - Clinical status (0-4, where 4=marketed)
- `cco:atcClassification` - Anatomical Therapeutic Chemical codes
- `cco:substanceType` - Molecule classification
- `cco:moleculeXref` - External database links
- `skos:exactMatch` - ChEBI/ontology mappings

**Activities**:
- `cco:Activity` - Bioactivity measurements
- `cco:standardType` - Measurement type (IC50, EC50, Ki, etc.)
- `cco:standardValue` - Numeric value
- `cco:standardUnits` - Units (nM, uM, %, etc.)
- `cco:pChembl` - Normalized potency (-log molar)

**Targets**:
- `cco:SingleProtein`, `cco:ProteinComplex`, `cco:ProteinFamily`
- `cco:targetType` - Classification
- `cco:organismName` - Source organism
- `cco:hasTargetComponent` - Links to UniProt

### Important Relationships
- Molecules → Activities: via `cco:hasActivity`
- Activities → Assays: via `cco:hasAssay`
- Assays → Targets: via `cco:hasTarget`
- Targets → UniProt: via TargetComponent/`skos:exactMatch`
- Molecules → ChEBI: via `skos:exactMatch`
- Drug Mechanisms: via `cco:hasMechanism`
- Drug Indications: via `cco:hasDrugIndication` linking to MeSH

### Query Patterns
1. **Use FROM clause**: `<http://rdf.ebi.ac.uk/dataset/chembl>`
2. **Use bif:contains** for keyword searches (10-100x faster than REGEX)
3. **Filter by development phase** for marketed/clinical drugs
4. **Always check standardUnits** when comparing activity values
5. **Pre-filter before joins** (Strategy 2) for cross-database queries

## Search Queries Performed

### 1. Query: "imatinib" → **CHEMBL941**
Results: Found 5 imatinib-related entries:
- CHEMBL941: IMATINIB (base molecule, score 36.0)
- CHEMBL1642: IMATINIB MESYLATE (salt form, score 36.0)
- CHEMBL2386595, CHEMBL3040018, CHEMBL56904 (related structures)

### 2. Query: "aspirin" → **CHEMBL25**
Results: Found 52 aspirin-related entries:
- CHEMBL25: ASPIRIN (score 36.0)
- CHEMBL5314595: ASPIRIN TRELAMINE (combination, score 35.0)
- CHEMBL1697753: ASPIRIN DL-LYSINE (salt, score 31.0)
- CHEMBL2260549: ASPIRIN EUGENOL ESTER (derivative, score 29.0)
- Plus 48 other related compounds

### 3. Query: "EGFR human" → **CHEMBL203**
Results: Found 134 EGFR-related targets:
- CHEMBL203: Epidermal growth factor receptor (Homo sapiens, SINGLE PROTEIN, score 12.0)
- CHEMBL3608: EGFR (Mus musculus, score 16.0)
- CHEMBL4523747: EGFR/PPP1CA (protein-protein interaction, score 16.0)
- CHEMBL5465557: CCN2-EGFR (protein-protein interaction, score 16.0)
- Plus 130 other EGFR-related entities

## SPARQL Queries Tested

```sparql
# Query: Count marketed drugs (development phase 4)
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>

SELECT (COUNT(DISTINCT ?molecule) as ?count)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule a cco:SmallMolecule ;
            cco:highestDevelopmentPhase 4 .
}
# Results: 3,678 marketed drugs
```

**Significance**: Quantifies FDA/EMA-approved drugs in ChEMBL. Phase 4 = marketed status.

## Cross-Reference Analysis

### ChEMBL Cross-Database Connectivity

**Molecular Cross-References** (via `cco:moleculeXref`):
- **PubChem**: 2.2M+ molecules
- **ZINC**: 1.2M+ molecules
- **ChEBI**: 35K molecules
- **DrugBank**: 8.4K drugs
- **FDA SRS**: 32K substances
- **HMDB**: 12K metabolites
- **SureChEMBL**: 540K patent compounds
- **Wikipedia**: Selected molecules

**Target Cross-References** (via TargetComponent/`skos:exactMatch`):
- **UniProt**: 11K targets (~85% coverage)
- **Ensembl**: Gene-level links
- **PDB**: 64K structure links

**Disease Cross-References** (via DrugIndication):
- **MeSH**: 51K drug-disease links
- **EFO**: Subset of indications

**Literature Cross-References**:
- **PubMed**: 88K documents
- **DOI**: Cross-referencing

### Shared SPARQL Endpoint

ChEMBL shares the **"ebi" endpoint** with:
- **ChEBI** (chemical ontology)
- **Reactome** (pathways)
- **Ensembl** (genomes)
- **AMR Portal** (resistance)

Enables powerful integration:
- ChEMBL drugs → ChEBI chemical structures
- ChEMBL targets → Reactome pathways  
- ChEMBL → UniProt → Reactome pathway context

## Interesting Findings

### 1. Marketed Drugs Count (requires development phase filtering)
- **3,678 marketed drugs** (highestDevelopmentPhase = 4)
- Much smaller than total 2.4M compounds
- Represents FDA/EMA-approved medicines
- Requires specific phase filter query

### 2. Imatinib Discovery (requires molecule search)
- **CHEMBL941** is the base imatinib molecule
- **CHEMBL1642** is imatinib mesylate (Gleevec salt form)
- Multiple related structures and derivatives
- Demonstrates salt/formulation variations

### 3. Aspirin Breadth (requires search)
- **52 aspirin-related compounds** in ChEMBL
- CHEMBL25 is the canonical aspirin
- Includes combinations, salts, esters, derivatives
- Shows extensive bioactivity testing history

### 4. EGFR Target Variants (requires target search)
- **CHEMBL203**: Human EGFR (canonical, SINGLE PROTEIN)
- **134 total EGFR-related entries** including:
  - Mouse EGFR (CHEMBL3608)
  - Protein-protein interactions
  - Mutant forms
- Major cancer drug target with extensive bioactivity data

### 5. Cross-Reference Coverage (from statistics)
- **~90% molecules have PubChem links**
- **~85% targets have UniProt mappings**
- **~80% molecules have bioactivity data**
- Demonstrates comprehensive database integration

### 6. Activity Data Completeness (from statistics)
- **20M bioactivity measurements** total
- **~70% activities have standardized values**
- Average 8.5 activities per molecule
- Enables SAR (structure-activity relationship) analysis

## Question Opportunities by Category

### Precision
✅ "What is the ChEMBL ID for imatinib?" (Answer: CHEMBL941)
✅ "What is the ChEMBL ID for human EGFR?" (Answer: CHEMBL203)
✅ "What is the development phase of aspirin (CHEMBL25)?" (Answer: 4/marketed)

### Completeness
✅ "How many marketed drugs are in ChEMBL?" (Answer: 3,678)
✅ "How many targets have UniProt mappings?" (requires COUNT)
✅ "How many compounds have IC50 measurements?" (requires activity type filtering)

### Integration
✅ "What UniProt ID corresponds to ChEMBL target CHEMBL203?" (requires cross-reference)
✅ "Find PubChem CID for ChEMBL25" (requires moleculeXref)
✅ "Link imatinib to ChEBI classification" (requires skos:exactMatch)

### Currency
✅ "How many COVID-19 drug candidates are in ChEMBL?" (pandemic drugs, 2020+)
✅ "What recent kinase inhibitors reached phase 3?" (recent approvals)

### Specificity
✅ "What is the ChEMBL ID for venetoclax?" (BCL-2 inhibitor)
✅ "Find ChEMBL entries for PARP inhibitors" (niche target class)

### Structured Query
✅ "Find marketed kinase inhibitors with IC50 < 100 nM" (3+ criteria)
✅ "List drugs with MeSH indication 'Melanoma' in phase 3+" (disease + phase filtering)
✅ "Find molecules targeting EGFR with mechanism 'INHIBITOR'" (target + mechanism)

## Notes

### Limitations
1. **Activity units critical**: Must filter by standardUnits (nM vs uM causes 1000x error)
2. **Not all molecules have activities**: ~80% have bioactivity data
3. **Target coverage variable**: Non-human organisms may lack UniProt mappings
4. **Development phase gaps**: Most complete for marketed drugs (phase 4)

### Best Practices
1. **Use search tools first**: search_chembl_molecule, search_chembl_target before SPARQL
2. **Use bif:contains**: 10-100x faster than REGEX
3. **Pre-filter before joins**: Development phase, organism, target type
4. **Check units**: Always include standardUnits when comparing values
5. **Use FROM clause**: Required for all ChEMBL queries

### Important Clarifications
- **Phase 4** = marketed drugs (3,678)
- **Phase 3** = late-stage clinical trials
- **Phase 0-2** = early development
- **Activity measurements**: IC50 (inhibition), EC50 (activation), Ki (binding)
- **pChembl**: Normalized potency metric (-log molar), enables cross-assay comparison

### Cross-Database Integration
- **ChEBI integration**: Via skos:exactMatch for chemical ontology
- **UniProt integration**: Via TargetComponent for protein sequences
- **Reactome integration**: Via UniProt bridge for pathway context
- **MeSH integration**: Via DrugIndication for disease associations
- Performance: Tier 1 (1-3s) for ChEBI, Tier 2 (3-8s) for Reactome with property paths
