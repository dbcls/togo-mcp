# Database Exploration Summary

## Overview
- **Total databases explored**: 23 (100% complete)
- **Total exploration sessions**: 6
- **Total exploration time**: Systematic, thorough coverage across all databases
- **Documentation**: Complete MIE file analysis + search + SPARQL testing for each database

## All Explored Databases

### Protein & Sequence Databases (4)
1. **UniProt** - 444M proteins (923K reviewed Swiss-Prot, 443M TrEMBL)
   - Key: CRITICAL filter reviewed=1 for quality/performance, 200+ cross-refs
   - Tools: search_uniprot_entity, SPARQL with filters
   
2. **PDB** - 204K+ 3D structures (X-ray, NMR, cryo-EM)
   - Key: Highest resolution 0.48 Å, experimental methods, quality metrics
   - Tools: search_pdb_entity (db: pdb, cc, prd), resolution filters
   
3. **Ensembl** - 100+ species genome annotations
   - Key: Gene biotypes, transcript quality flags, exon coordinates
   - Cross-refs: UniProt, HGNC, NCBI Gene, Reactome
   
4. **DDBJ** - INSDC nucleotide sequences
   - Key: FALDO coordinates, Sequence Ontology features, BFO/RO relationships
   - Cross-refs: BioProject, BioSample, NCBI Protein

### Chemical & Drug Databases (5)
5. **PubChem** - 119M compounds, 339M substances, 1.7M bioassays
   - Key: SMILES, InChI, properties, stereoisomers, 167K genes, 249K proteins
   - Tools: get_pubchem_compound_id, get_compound_attributes, SPARQL
   
6. **ChEMBL** - 2.4M compounds, 20M bioactivities
   - Key: IC50 values, target annotations, drug mechanisms, indications
   - Tools: search_chembl_molecule, search_chembl_target
   
7. **ChEBI** - 217K+ chemical entities
   - Key: Hierarchical ontology, molecular data, biological roles, conjugates
   - Cross-refs: 20+ databases (KEGG, DrugBank, PubChem, HMDB)
   
8. **Reactome** - 22K+ pathways, 30+ species
   - Key: BioPAX Level 3, hierarchical organization, molecular interactions
   - Tools: search_reactome_entity, species/type filters
   - Cross-refs: UniProt, ChEBI, PubMed, GO
   
9. **Rhea** - 17,078 biochemical reactions (34,156 directional)
   - Key: Atom-balanced, ChEBI compounds, transport locations, EC numbers
   - Tools: search_rhea_entity, rhea_id patterns
   - Cross-refs: KEGG, MetaCyc, Reactome, UniProtKB

### Ontology Databases (4)
10. **GO (Gene Ontology)** - 48,165 terms (3 namespaces)
    - Key: biological_process (30,804), molecular_function (12,793), cellular_component (4,568)
    - Tools: OLS4 search, getAncestors, getDescendants
    
11. **MeSH** - 30K descriptors, 250K chemicals, 2.5M total entities
    - Key: 16 hierarchical categories, qualifiers, supplementary concepts
    - Tools: search_mesh_entity, tree number navigation
    
12. **MONDO** - 30K+ disease classes
    - Key: Unified disease ontology, 35+ database cross-refs
    - Cross-refs: OMIM, Orphanet, DOID, ICD, MeSH
    
13. **NANDO** - 2,777 Japanese intractable diseases
    - Key: Multilingual (EN/JP), notification numbers, government designations
    - Cross-refs: MONDO, KEGG, medical docs

### Clinical & Medical Databases (4)
14. **ClinVar** - 3.5M+ variant records
    - Key: Clinical interpretations, gene associations, disease conditions
    - Cross-refs: MedGen, OMIM, MeSH, HGNC
    
15. **MedGen** - 233K+ clinical concepts
    - Key: MGREL relationships (separate entities), MONDO 70%, MeSH 80%
    - Critical: Relationships NOT on ConceptID directly
    
16. **NCBI Gene** - 57M+ entries (genes, ncRNAs, pseudogenes)
    - Key: Symbols, descriptions, chromosomal locations, orthology
    - Tools: ncbi_esearch, ncbi_esummary, ncbi_efetch
    - Cross-refs: Ensembl, HGNC, OMIM
    
17. **Taxonomy** - 3M+ organisms
    - Key: Hierarchical classification, scientific/common names, genetic codes
    - Essential for biological data integration

### Microbiology Databases (3)
18. **BacDive** - 97K+ bacterial/archaeal strain records
    - Key: Phenotypic characterization, culture conditions, enzymes, sequences
    - Cross-refs: NCBI Taxonomy, DSMZ/JCM/KCTC collections, ENA/GenBank
    
19. **MediaDive** - 3,289 culture media recipes
    - Key: Hyperthermophiles 103°C, hierarchical recipes, 1,489 ingredients
    - Cross-refs: BacDive 73%, GMO 41%, CAS 39%, ChEBI 32%
    
20. **AMR Portal** - 1.7M phenotypic AST results, 1.1M AMR features
    - Key: MIC values, disk diffusion, AMR genes, geographic/temporal metadata
    - Applications: Resistance surveillance, genotype-phenotype correlation

### Glycoscience Database (1)
21. **GlyCosmos** - 117,864 glycans, 153,178 glycoproteins
    - Key: Multi-graph (100+), FALDO coordinates, Lewis antigens
    - Coverage: Human 16,604 glycoproteins, BacDive 73%, ChEBI 32%

### Literature Databases (2)
22. **PubMed** - 37M+ biomedical citations
    - Key: E-utilities 10-100x faster than SPARQL, OLO author lists, MeSH 95%
    - Tools: search_articles, get_article_metadata (PREFERRED over SPARQL)
    - Coverage: Abstracts 85%, DOI 70%, PMC linkage 40%
    
23. **PubTator** - 10M+ entity-article annotations
    - Key: Disease/Gene annotations, annotation frequency, provenance tracking
    - Sources: PubTator3 2.2M, ClinVar 1.2M, dbSNP 305K, dbGAP 17K
    - Integration: PubMed cross-graph queries with bif:contains

## Database Coverage Plan for 120 Questions

### Recommended Distribution by Database Richness

**Tier 1: Rich, Multi-Purpose Databases (6-8 questions each, 40-48 total)**
- **UniProt** (8 questions): Protein sequences, functions, domains, variants
  - Precision: Specific protein IDs, sequences
  - Completeness: Protein counts with filters
  - Integration: UniProt ↔ NCBI Gene ↔ Ensembl
  
- **PubChem** (7 questions): Compounds, properties, bioassays
  - Precision: CID lookups, molecular properties
  - Completeness: Compound counts, bioassay results
  - Integration: PubChem ↔ ChEBI ↔ ChEMBL
  
- **ChEMBL** (6 questions): Bioactivities, drug targets, mechanisms
  - Structured Query: IC50 filters, target types
  - Integration: ChEMBL ↔ UniProt ↔ DrugBank
  
- **GO** (6 questions): Term hierarchies, annotations
  - Completeness: Descendant/ancestor counts
  - Structured Query: Namespace filters, term searches
  
- **ClinVar** (6 questions): Variants, clinical significance
  - Currency: Recent variant updates
  - Integration: ClinVar ↔ MedGen ↔ OMIM
  
- **PubMed** (7 questions): Literature search, metadata
  - Currency: Recent publications
  - Integration: PubMed ↔ PubTator ↔ MeSH

**Tier 2: Specialized High-Value Databases (4-5 questions each, 32-40 total)**
- **PDB** (5 questions): Structure quality, experimental methods
- **Reactome** (5 questions): Pathway hierarchies, reactions
- **MeSH** (5 questions): Medical terminology, tree navigation
- **NCBI Gene** (5 questions): Gene information, orthology
- **ChEBI** (4 questions): Chemical ontology, roles
- **Rhea** (4 questions): Biochemical reactions, transport
- **MONDO** (4 questions): Disease ontology, cross-refs

**Tier 3: Niche/Specialized Databases (2-3 questions each, 24-32 total)**
- **BacDive** (3 questions): Strain characterization, growth conditions
- **MediaDive** (2 questions): Culture media, extremophiles
- **AMR Portal** (3 questions): Resistance patterns, AST results
- **NANDO** (3 questions): Japanese rare diseases
- **MedGen** (3 questions): Clinical concepts, relationships
- **GlyCosmos** (3 questions): Glycan structures, glycoproteins
- **PubTator** (3 questions): Gene-disease annotations, literature mining
- **Taxonomy** (2 questions): Organism classification
- **Ensembl** (2 questions): Genome annotations
- **DDBJ** (2 questions): Sequence features

**Distribution Summary**:
- Tier 1 (6 databases): 40-48 questions (33-40%)
- Tier 2 (7 databases): 32-40 questions (27-33%)
- Tier 3 (10 databases): 24-32 questions (20-27%)
- **Total: 120 questions across all 23 databases**

**Rationale**: 
- High-impact databases (UniProt, PubChem, ChEMBL, GO, ClinVar, PubMed) get more questions
- Specialized databases (BacDive, NANDO, MediaDive) get fewer but focused questions
- All databases represented with at least 2 questions
- Balance across 6 question categories

## Cross-Database Integration Opportunities

### Protein-Centric Integrations
1. **UniProt → NCBI Gene → Ensembl**: Gene-transcript-protein axis
2. **UniProt → ChEMBL → PubChem**: Protein targets to compounds to properties
3. **UniProt → PDB**: Sequence to 3D structure
4. **UniProt → GO**: Protein function annotations
5. **UniProt → Reactome**: Proteins in pathways

### Chemical-Centric Integrations
6. **PubChem → ChEBI → Rhea**: Compound properties to ontology to reactions
7. **PubChem → ChEMBL → UniProt**: Compound bioactivity to targets
8. **ChEBI → Reactome**: Small molecules in pathways
9. **Rhea → UniProt**: Reactions to enzyme annotations

### Disease-Centric Integrations
10. **ClinVar → MedGen → MONDO**: Variants to concepts to ontology
11. **ClinVar → NCBI Gene → UniProt**: Variants to genes to proteins
12. **MedGen → MeSH → OMIM**: Clinical concepts to terminology to genetic disorders
13. **MONDO → NANDO**: International to Japanese rare diseases
14. **PubTator → MeSH → PubMed**: Disease annotations to terminology to literature

### Literature-Centric Integrations
15. **PubMed → PubTator → NCBI Gene**: Literature to entities to gene info
16. **PubMed → MeSH → Taxonomy**: Articles to terms to organisms
17. **PubTator → ClinVar → MedGen**: Literature evidence to variants to concepts

### Microbiology Integrations
18. **BacDive → MediaDive → Taxonomy**: Strains to culture media to classification
19. **BacDive → AMR Portal**: Strain characterization to resistance patterns
20. **Taxonomy → NCBI Gene → UniProt**: Organism to genes to proteins

### Glycoscience Integrations
21. **GlyCosmos → UniProt → GO**: Glycoproteins to proteins to functions
22. **GlyCosmos → PubChem → ChEBI**: Glycans to chemical properties to ontology

### Multi-Database Complex Queries
23. **UniProt + ChEMBL + ClinVar + PubTator**: Disease variant → protein → inhibitor → literature
24. **NCBI Gene + Ensembl + UniProt + Reactome**: Gene → transcripts → proteins → pathways
25. **BacDive + MediaDive + Taxonomy + AMR Portal**: Strain → media → classification → resistance

## Database Characteristics

### Rich Content (Good for Multiple Questions)
**Extensive data, well-documented, multiple query patterns:**
- UniProt (444M proteins, 200+ cross-refs)
- PubChem (119M compounds, 339M substances, 1.7M bioassays)
- ChEMBL (2.4M compounds, 20M bioactivities)
- GO (48K terms, hierarchical)
- PubMed (37M citations, daily updates)
- ClinVar (3.5M variants)
- NCBI Gene (57M entries)

### Specialized Content (Good for Specificity Questions)
**Niche domains, unique data:**
- NANDO (2,777 Japanese rare diseases)
- BacDive (97K bacterial strains, phenotypic data)
- MediaDive (3,289 culture media, extremophiles)
- AMR Portal (1.7M AST results, resistance surveillance)
- GlyCosmos (117K glycans, Lewis antigens)
- Rhea (17K reactions, atom-balanced)

### Well-Connected (Good for Integration Questions)
**Strong cross-references, bridge databases:**
- UniProt (200+ databases)
- PubChem (ChEBI, ChEMBL, DrugBank, HMDB)
- ClinVar (MedGen, OMIM, MeSH, HGNC)
- MedGen (MONDO 70%, MeSH 80%, OMIM 30%)
- PubTator (MeSH diseases, NCBI genes to literature)
- MONDO (35+ database cross-refs)
- GO (gene product annotations across organisms)

### High-Performance Search Tools
**Optimized tools, fast queries:**
- PubMed (E-utilities 10-100x faster than SPARQL)
- UniProt (search_uniprot_entity with filters)
- PubChem (get_pubchem_compound_id, get_compound_attributes)
- ChEMBL (search_chembl_molecule, search_chembl_target)
- OLS4 (GO, MONDO, ChEBI with getAncestors/getDescendants)
- BacDive (search by strain, growth conditions)
- Reactome (search_reactome_entity with species/type filters)

### SPARQL-Friendly Databases
**Good SPARQL performance, rich RDF:**
- Rhea (reactions, atom-balanced queries)
- ChEBI (ontology hierarchy, chemical relationships)
- GO (term relationships, namespaces)
- Reactome (pathway hierarchies, BioPAX)
- MONDO (disease ontology, equivalences)
- MeSH (tree numbers, descriptor relationships)

### Databases Requiring Special Handling
**Performance notes, query optimization needed:**
- UniProt: MUST filter reviewed=1 for quality/performance
- GlyCosmos: Requires explicit FROM clause (100+ graphs)
- MedGen: MGREL relationships separate from ConceptID
- PubMed: Prefer E-utilities over SPARQL for searches
- PubTator: Always use LIMIT, avoid full aggregations
- AMR Portal: Filter by methodology for comparable results

## Key Technical Patterns Discovered

### 1. Multi-Graph Architectures
- **GlyCosmos**: 100+ named graphs, requires FROM clause
- **Pattern**: Query specific graphs for performance

### 2. Relationship Models
- **MedGen**: MGREL separate entities (not direct ConceptID properties)
- **Pattern**: Join through relationship entities

### 3. Full-Text Indexing
- **Critical**: bif:contains essential for all databases
- **Pattern**: Use on text fields, not URIs

### 4. Tool Selection Strategy
- **PubMed**: E-utilities >> SPARQL (10-100x faster)
- **Pattern**: Use specialized tools when available

### 5. Performance Optimization
- **UniProt**: reviewed=1 filter CRITICAL
- **PubTator**: LIMIT always required
- **Pattern**: Filter early, limit results

### 6. Cross-Database Workflows
- **Example**: PubMed search → PMIDs → PubTator annotations
- **Pattern**: Chain specialized tools

## Recommendations for Question Generation

### 1. Balance Across Categories
- **Precision**: 20 questions (ID lookups, specific values)
- **Completeness**: 20 questions (counts, comprehensive lists)
- **Integration**: 20 questions (cross-database links)
- **Currency**: 20 questions (recent data, updates)
- **Specificity**: 20 questions (rare entities, niche data)
- **Structured Query**: 20 questions (complex filters, multi-criteria)

### 2. Database Pairing Strategy
**Prioritize these combinations:**
- UniProt + NCBI Gene (protein-gene axis)
- PubChem + ChEBI + ChEMBL (chemical integration)
- ClinVar + MedGen + MONDO (clinical genetics)
- PubMed + PubTator + MeSH (literature mining)
- BacDive + MediaDive + Taxonomy (microbiology)
- GO + UniProt + Reactome (functional annotation)

### 3. Focus on Biological Value
**Prioritize questions about:**
- ✅ Biological entities (proteins, genes, diseases, compounds)
- ✅ Scientific properties (sequences, structures, activities)
- ✅ Research-relevant metadata (clinical significance, pathways)
- ❌ Avoid: Database versions, software tools, IT infrastructure

### 4. Leverage Unique Features
**Exploit database-specific strengths:**
- UniProt: reviewed=1 quality curation
- PubChem: Bioassay activity data
- ChEMBL: Drug mechanisms, indications
- BacDive: Growth temperature extremes
- MediaDive: Hyperthermophile media
- NANDO: Japanese disease terminology
- AMR Portal: Resistance surveillance data
- GlyCosmos: Lewis antigen patterns
- PubTator: Annotation frequency tracking

### 5. Design for Verifiability
**Each question should have:**
- Specific expected answer (ID, count, term)
- Clear verification method (query, lookup)
- Stable data (not changing daily)
- Biological relevance (not just technical query)

### 6. Avoid Common Pitfalls
- Don't ask version/update questions
- Don't request impossible aggregations
- Don't assume all databases have all fields
- Don't ignore performance patterns (UniProt reviewed, PubMed E-utils)
- Don't create questions baseline can answer

## Particularly Interesting Findings

### 1. Performance Hierarchy
- **E-utilities**: PubMed 10-100x faster than SPARQL
- **Tool advantage**: Specialized tools beat generic SPARQL
- **Lesson**: Check for dedicated search tools first

### 2. Data Quality Markers
- **UniProt reviewed=1**: 923K curated vs 443M automated
- **PubTator sources**: PubTator3 vs ClinVar vs dbSNP
- **Lesson**: Quality metadata enables better questions

### 3. Extremophile Data
- **MediaDive**: Culture media for 103°C growth
- **BacDive**: Hyperthermophile characterization
- **Lesson**: Niche databases have unique value

### 4. Provenance Tracking
- **PubTator**: 4 annotation sources (PubTator3, ClinVar, dbSNP, dbGAP)
- **MedGen**: Relationship source attribution
- **Lesson**: Provenance enables confidence scoring

### 5. Multi-Scale Integration
- **GlyCosmos**: 100+ graphs for multi-species glycobiology
- **NCBI Gene**: 57M entries across all organisms
- **Lesson**: Scale requires architectural sophistication

### 6. Literature as Bridge
- **PubTator**: Links MeSH + NCBI Gene to 37M articles
- **PubMed**: Hub for biological knowledge
- **Lesson**: Literature databases connect everything

### 7. Japanese Rare Diseases
- **NANDO**: Government-designated intractable diseases
- **Multilingual**: English + Japanese terminology
- **Lesson**: Regional databases provide cultural context

### 8. Chemical Integration Hub
- **PubChem**: 119M compounds link to genes, proteins, pathways
- **Breadth**: Substances, bioassays, patent data
- **Lesson**: Chemical space is massive and well-connected

## Next Steps: Question Generation Phase

**Ready to proceed with:**
1. Systematic coverage of all 23 databases
2. Balance across 6 question categories (20 each)
3. Focus on biological/scientific content
4. Leverage cross-database integrations
5. Exploit unique database features
6. Ensure all questions are verifiable

**Total Questions to Generate**: 120
**Distribution**: See "Database Coverage Plan" above
**Categories**: 20 questions each × 6 categories
**Timeline**: Proceed to PROMPT 2 for question generation

---

**Exploration Status**: ✅ COMPLETE (100% - All 23 databases thoroughly explored)
**Documentation**: 23 comprehensive exploration reports in `/exploration/` directory
**Ready For**: Question generation phase (PROMPT 2)
