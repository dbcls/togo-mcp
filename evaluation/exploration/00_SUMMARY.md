# Database Exploration Summary

## Overview
- **Total databases explored**: 23
- **Total exploration sessions**: 2 (22 databases in session 1, 1 database in session 2)
- **Date completed**: January 2026

## All Explored Databases

### Molecular Biology & Genomics
1. **UniProt** - Protein sequences and functional annotations (444M proteins, Swiss-Prot vs TrEMBL)
2. **NCBI Gene** - Gene database (57M+ entries, protein-coding, ncRNA, pseudogenes)
3. **Ensembl** - Genome annotations for 100+ species (genes, transcripts, proteins, exons)
4. **PDB** - 3D protein structures (204K+ entries from X-ray, NMR, cryo-EM)
5. **DDBJ** - DNA sequence data from INSDC collaboration (nucleotide sequences, annotations)

### Chemical & Drug Databases
6. **PubChem** - Chemical molecules (119M compounds, 339M substances, bioactivity data)
7. **ChEBI** - Chemical entities of biological interest (217K+ entities, hierarchical classification)
8. **ChEMBL** - Bioactive molecules with drug-like properties (2.4M+ compounds, 20M bioactivity measurements)

### Pathway & Reaction Databases
9. **Reactome** - Biological pathways and processes (22K+ pathways, 30+ species)
10. **Rhea** - Biochemical reactions (17,078 reactions, atom-balanced, ChEBI-linked)
11. **Gene Ontology (GO)** - Controlled vocabulary for gene attributes (48,165 terms across 3 domains)

### Disease & Clinical Databases
12. **ClinVar** - Genomic variants and clinical interpretations (3.5M+ variant records)
13. **MedGen** - Medical genetics conditions (233K+ clinical concepts from OMIM, Orphanet, HPO)
14. **MONDO** - Disease ontology (30K+ disease classes, 35+ database cross-references)
15. **NANDO** - Japanese intractable/rare diseases (2,777 disease classes, multilingual)

### Literature & Annotations
16. **PubMed** - Biomedical literature (bibliographic information, MeSH annotations)
17. **PubTator** - Text-mining entity annotations (Disease and Gene annotations from PubMed)
18. **MeSH** - Medical subject headings (controlled vocabulary, ~30K descriptors)

### Microbiology & Specialized Databases
19. **BacDive** - Bacterial diversity (97K+ strain records, phenotypic/genotypic data)
20. **MediaDive** - Culture media recipes (3,289 standardized recipes from DSMZ)
21. **Taxonomy** - NCBI biological classification (3M+ organisms, hierarchical relationships)
22. **GlyCosmos** - Glycoscience portal (glycan structures, glycoproteins, glycosylation sites)
23. **AMR Portal** - Antimicrobial resistance surveillance (1.7M phenotypic AST results, 1.1M genotypic AMR features) ✨ NEW

## Database Coverage Plan for 120 Questions

### Recommended Distribution

**Tier 1 - Rich Content (8-12 questions each):**
- **UniProt** (12 questions) - Largest protein database, excellent search, cross-references
- **PubChem** (10 questions) - Massive chemical database, diverse properties, bioactivity
- **ChEMBL** (10 questions) - Drug discovery, bioactivity, target relationships
- **GO** (10 questions) - Ontology navigation, hierarchical queries, gene annotations
- **ClinVar** (10 questions) - Clinical variants, pathogenicity, temporal data
- **Reactome** (8 questions) - Pathways, molecular interactions, species coverage
- **PDB** (8 questions) - Structural data, experimental methods, resolution metrics

**Tier 2 - Specialized Content (4-6 questions each):**
- **AMR Portal** (6 questions) - Resistance surveillance, phenotype-genotype linkage, geographic trends ✨ NEW
- **NCBI Gene** (6 questions) - Gene IDs, orthology, cross-references
- **MeSH** (6 questions) - Medical terminology, rare diseases, hierarchical
- **Rhea** (6 questions) - Biochemical reactions, transport, EC numbers
- **ChEBI** (5 questions) - Chemical ontology, molecular properties, roles
- **MONDO** (5 questions) - Disease ontology, integration across sources
- **Ensembl** (5 questions) - Genome annotations, transcript variants

**Tier 3 - Niche Content (2-4 questions each):**
- **NANDO** (4 questions) - Japanese rare diseases, unique identifiers
- **BacDive** (4 questions) - Bacterial strains, growth conditions
- **MediaDive** (4 questions) - Culture media, ingredients, protocols
- **MedGen** (3 questions) - Clinical concepts, relationship tracking
- **PubMed** (3 questions) - Literature metadata, MeSH annotations
- **PubTator** (3 questions) - Entity annotations, text mining
- **GlyCosmos** (3 questions) - Glycans, glycoproteins, lectin interactions
- **Taxonomy** (3 questions) - Organism classification, genetic codes
- **DDBJ** (2 questions) - Nucleotide sequences, genomic features

**Total: 120 questions**

### Rationale
- **UniProt, PubChem, ChEMBL, GO, ClinVar**: Extremely rich datasets with diverse query opportunities, excellent tools, high research relevance
- **AMR Portal**: NEW database with unique surveillance data, phenotype-genotype correlation, geographic/temporal analysis - excellent for integration and currency questions
- **Reactome, PDB, Rhea**: Specialized but deep content with clear use cases
- **NANDO, BacDive, MediaDive**: Unique niche databases perfect for specificity questions
- **Integration opportunities**: Cross-database questions leverage ID conversion tools (TogoID) and shared identifiers

## Cross-Database Integration Opportunities

### High-Value Integration Pairs

1. **UniProt ↔ NCBI Gene**: Protein to gene ID conversion, orthology
2. **UniProt ↔ ChEMBL**: Protein targets with bioactivity data
3. **PubChem ↔ ChEBI**: Chemical entity standardization, ID conversion
4. **ClinVar ↔ MedGen**: Variant to clinical concept mapping
5. **ClinVar ↔ NCBI Gene**: Variant to gene associations
6. **Ensembl ↔ NCBI Gene**: Genome annotation cross-references
7. **ChEMBL ↔ PubChem**: Drug compounds across databases
8. **Reactome ↔ UniProt**: Pathway components to proteins
9. **Rhea ↔ ChEBI**: Reactions to chemical participants
10. **GO ↔ UniProt**: Gene ontology annotations on proteins
11. **AMR Portal ↔ Taxonomy**: Resistance data to organism classification ✨ NEW
12. **AMR Portal ↔ PubMed**: Surveillance data to literature citations ✨ NEW
13. **AMR Portal ↔ BioSample**: Phenotype-genotype linkage via samples ✨ NEW

### Multi-Database Query Examples

**Example 1**: "Find human kinases (UniProt) with bioactivity data (ChEMBL) and associated pathways (Reactome)"
- Databases: UniProt, ChEMBL, Reactome
- Integration: Protein IDs, target mapping, pathway components

**Example 2**: "Convert BRCA1 variant (ClinVar) to gene ID (NCBI Gene) to disease associations (MedGen)"
- Databases: ClinVar, NCBI Gene, MedGen
- Integration: Variant → Gene → Clinical concept

**Example 3**: "Find ATP-dependent reactions (Rhea) with chemical properties (ChEBI) in metabolic pathways (Reactome)"
- Databases: Rhea, ChEBI, Reactome
- Integration: Reaction participants, chemical entities, pathway context

**Example 4**: "Track carbapenem resistance genes (AMR Portal) in Klebsiella pneumoniae (Taxonomy) with geographic distribution and link to literature (PubMed)" ✨ NEW
- Databases: AMR Portal, Taxonomy, PubMed
- Integration: Genotype/phenotype data, organism classification, citations

## Database Characteristics

### Rich Content (Good for multiple questions)
**Excellent search tools, diverse data, high research value:**
- **UniProt**: search_uniprot_entity, 444M proteins, comprehensive annotations
- **PubChem**: get_pubchem_compound_id, get_compound_attributes, 119M compounds
- **ChEMBL**: search_chembl_molecule, search_chembl_target, 2.4M compounds, 20M bioactivities
- **GO**: searchClasses, getDescendants, getAncestors, 48K terms with rich hierarchy
- **ClinVar**: Via NCBI tools, 3.5M variants with clinical interpretations
- **AMR Portal**: SPARQL queries, 1.7M phenotypes + 1.1M genotypes, phenotype-genotype correlation ✨ NEW

### Specialized Content (Good for specificity questions)
**Niche domains, unique identifiers, expert curation:**
- **NANDO**: Japanese rare diseases, government-designated intractable diseases
- **BacDive**: Bacterial strain characterization, growth conditions, 97K strains
- **MediaDive**: Culture media recipes, hierarchical ingredients, DSMZ standardization
- **MeSH**: Medical terminology, rare disease descriptors, controlled vocabulary
- **GlyCosmos**: Glycoscience specialization, 100+ named graphs
- **Rhea**: Expert-curated reactions, atom-balanced, transport reactions
- **AMR Portal**: Resistance surveillance, quantitative MIC data, geographic/temporal tracking ✨ NEW

### Well-Connected (Good for integration questions)
**Strong cross-references, ID conversion capabilities:**
- **UniProt**: 200+ database cross-references, central hub for proteins
- **PubChem**: Links to ChEBI, DrugBank, patents, genes, proteins
- **ChEMBL**: Cross-references to UniProt, PDB, PubChem
- **ClinVar**: Links to MedGen, OMIM, MeSH, HGNC
- **NCBI Gene**: Cross-references to Ensembl, HGNC, OMIM
- **Reactome**: Links to UniProt, ChEBI, PubMed, GO
- **AMR Portal**: BioSample, SRA, INSDC, PubMed, ARO ontology, NCBI Taxonomy ✨ NEW

### Ontology-Based (Good for structured query questions)
**Hierarchical relationships, semantic queries:**
- **GO**: Three ontology domains, hierarchical navigation
- **ChEBI**: Chemical entity classification, role hierarchy
- **MONDO**: Disease ontology, cross-ontology integration
- **MeSH**: Tree number hierarchy, 16 categories
- **NANDO**: Japanese rare disease taxonomy
- **Taxonomy**: Biological classification hierarchy

### Temporal/Currency Content (Good for currency questions)
**Recent updates, time-sensitive data:**
- **ClinVar**: Last updated dates, current classifications
- **PDB**: Recent structure depositions, current resolution records
- **PubMed**: Latest publications, recent MeSH annotations
- **NCBI Gene**: Current gene symbols, recent annotations
- **AMR Portal**: Collection years 1911-2025, temporal resistance trends ✨ NEW

## Recommendations

### For Question Generation

1. **Leverage unique strengths**: 
   - UniProt for protein IDs and annotations
   - NANDO for rare Japanese diseases
   - AMR Portal for resistance surveillance and epidemiology ✨ NEW
   - BacDive/MediaDive for microbiology specifics
   - PDB for structural metrics

2. **Focus on integration**:
   - UniProt ↔ ChEMBL for drug-target questions
   - ClinVar ↔ MedGen for variant-disease mapping
   - AMR Portal ↔ BioSample/Taxonomy for resistance epidemiology ✨ NEW
   - Use TogoID for systematic ID conversion

3. **Exploit hierarchies**:
   - GO for ancestor/descendant queries
   - MeSH for medical terminology navigation
   - ChEBI for chemical classification
   - MONDO for disease relationships

4. **Test temporal capabilities**:
   - ClinVar update dates
   - PDB recent depositions
   - AMR Portal resistance trend analysis (2010-2025) ✨ NEW
   - PubMed recent literature

5. **Include specificity questions**:
   - NANDO Japanese identifiers
   - BacDive strain-specific growth conditions
   - MediaDive culture medium recipes
   - AMR Portal MIC measurements, MDR isolates ✨ NEW
   - Rare disease MeSH descriptors

### Databases That Pair Well Together

**Chemistry Focus:**
- PubChem + ChEBI + ChEMBL (compound properties, bioactivity, drug discovery)
- Rhea + ChEBI + Reactome (reactions, chemicals, pathways)

**Clinical Focus:**
- ClinVar + MedGen + MONDO (variants, clinical concepts, disease ontology)
- ClinVar + NCBI Gene + UniProt (variant → gene → protein)

**Pathway/Systems Biology:**
- Reactome + UniProt + GO (pathways, proteins, functions)
- Reactome + Rhea + ChEBI (pathways, reactions, chemicals)

**Structural Biology:**
- PDB + UniProt + ChEMBL (structures, sequences, ligands)

**Microbiology/AMR:** ✨ NEW
- AMR Portal + BacDive + Taxonomy (resistance, strains, classification)
- AMR Portal + PubMed + MedGen (surveillance, literature, clinical concepts)

**Literature/Annotation:**
- PubMed + PubTator + MeSH (articles, entity annotations, controlled vocabulary)

### Particularly Interesting Findings

1. **UniProt Swiss-Prot quality filter**: CRITICAL to use reviewed=1 for performance and quality
2. **AMR Portal phenotype-genotype linkage**: BioSample connects resistance phenotypes with AMR genes ✨ NEW
3. **AMR Portal extreme MDR**: Isolates resistant to 30+ antibiotics, public health concern ✨ NEW
4. **ChEMBL bioactivity scale**: Nanomolar IC50 values for kinase inhibitors
5. **GO hierarchy depth**: 25 descendant terms for autophagy (GO:0006914)
6. **ClinVar pathogenic variants**: BRCA1 c.5266dup with update timestamps
7. **PDB resolution record**: 0.48 Å achieved (atomic resolution)
8. **NANDO multilingual**: Japanese kanji, hiragana, and English labels
9. **BacDive temperature extremes**: Thermophiles >70°C documented
10. **MediaDive ingredient detail**: GMO 41%, CAS 39%, ChEBI 32% coverage
11. **Rhea transport reactions**: 5,984 cellular location-specific reactions
12. **GlyCosmos graph diversity**: 100+ named graphs for glycobiology
13. **AMR Portal geographic coverage**: 150+ countries, all continents represented ✨ NEW
14. **AMR Portal temporal span**: 92 years of data (1911-2025), concentrated post-2000 ✨ NEW

### Common Query Patterns Across Databases

**Search Tools:**
- `search_uniprot_entity`, `search_chembl_molecule`, `search_mesh_entity`, `search_pdb_entity`
- All support keyword-based queries with relevance scoring
- AMR Portal uses `bif:contains` in SPARQL for flexible text search ✨ NEW

**SPARQL Queries:**
- OLS4 databases: `searchClasses`, `getAncestors`, `getDescendants`
- TogoMCP databases: Direct SPARQL with `run_sparql`
- AMR Portal: Large dataset requires LIMIT clauses and organism filters ✨ NEW

**ID Conversion:**
- `togoid_convertId` for systematic cross-database ID mapping
- Common routes: UniProt ↔ NCBI Gene, PubChem ↔ ChEBI
- AMR Portal: BioSample as primary linkage key ✨ NEW

**Ontology Navigation:**
- Hierarchical queries in GO, ChEBI, MONDO, MeSH, NANDO
- Parent/child relationships, subsumption
- Tree number navigation in MeSH

### Performance Considerations

**Fast Queries:**
- UniProt Swiss-Prot (reviewed=1)
- ChEMBL targeted searches
- GO ontology navigation
- Small PDB result sets

**Requires Optimization:**
- UniProt TrEMBL (444M records - must filter)
- AMR Portal (1.7M phenotypes - must use organism/antibiotic filters + LIMIT) ✨ NEW
- PubChem comprehensive searches
- Complex multi-database joins

**Best Practices:**
- Use specific entity IDs when known
- Filter by organism, database section, or category
- Apply LIMIT to exploratory queries
- AMR Portal: Always specify FROM clause, use bif:contains for text ✨ NEW
- Prefer search tools over broad SPARQL when available

---

**Last Updated**: January 2026 (after AMR Portal exploration)  
**Total Databases**: 23 (all explored)  
**Ready for**: Question generation phase (PROMPT 2)  
**New Addition**: AMR Portal - antimicrobial resistance surveillance with unique phenotype-genotype correlation capabilities ✨
