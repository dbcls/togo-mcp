# TogoMCP Database Exploration Summary

## Overview

**Exploration Status**: COMPLETE ✅  
**Total Databases Explored**: 23 of 23  
**Total Exploration Reports**: 23 comprehensive reports  
**Exploration Method**: Real database queries + MIE file analysis  
**Quality Standard**: All findings from actual queries, not MIE examples

---

## All Explored Databases

### Protein & Gene Databases (4)
1. **UniProt** - 444M proteins (923K Swiss-Prot curated), extensive cross-references to 200+ databases
2. **NCBI Gene** - 57M+ gene entries, cross-species comparative genomics, orthology relationships
3. **Ensembl** - Genome annotations for 100+ species, transcript variants, exon boundaries
4. **DDBJ** - Nucleotide sequences from INSDC, genomic features, prokaryotic genomes

### Chemical & Drug Databases (4)
5. **PubChem** - 119M compounds, 339M substances, 1.7M bioassays, drug classifications
6. **ChEMBL** - 2.4M+ compounds, 20M bioactivity measurements, drug mechanisms
7. **ChEBI** - 217K+ chemical entities, hierarchical ontology, biological roles
8. **Rhea** - 17,078 biochemical reactions, enzyme classifications, metabolic pathways

### Structure & Pathway Databases (2)
9. **PDB** - 204K+ 3D structures, X-ray/NMR/cryo-EM, protein/nucleic acid complexes
10. **Reactome** - 22K+ pathways, 30+ species, molecular interactions, disease associations

### Clinical & Variant Databases (3)
11. **ClinVar** - 3.5M+ variant records, clinical interpretations, gene-disease associations
12. **MedGen** - 233K+ clinical concepts, integrates OMIM/Orphanet/HPO/MONDO
13. **NANDO** - 2,777 Japanese intractable diseases, government-designated, MONDO cross-references

### Literature & Text Mining (2)
14. **PubMed** - 37M+ biomedical citations, MeSH annotations, author/journal metadata
15. **PubTator** - 10M+ entity annotations, gene/disease text mining, literature-based discovery

### Ontology Databases (4)
16. **GO** - Gene Ontology with 48K+ terms, biological process/molecular function/cellular component
17. **MeSH** - Medical Subject Headings, 30K+ descriptors, PubMed literature indexing
18. **MONDO** - 30,230 disease classes, integrates 39+ databases, rare disease focus
19. **NCBI Taxonomy** - 2.7M+ organisms, hierarchical classification, genetic codes

### Microbiology Databases (3)
20. **BacDive** - 97K+ bacterial/archaeal strains, phenotypes, cultivation conditions
21. **MediaDive** - 3,289 culture media recipes, 1,489 ingredients, strain-media linking
22. **AMR Portal** - 1.7M phenotypic resistance tests, 1.1M genotypic AMR features

### Glycoscience Database (1)
23. **GlyCosmos** - Glycan structures (GlyTouCan), glycoproteins, glycosylation sites, 100+ named graphs

---

## Database Coverage Plan for 120 Questions

### Recommended Distribution

**Tier 1: High-Richness Databases** (60 questions total)
- **UniProt** (12 questions): Protein diversity, Swiss-Prot curation quality, cross-references
- **PubChem** (10 questions): Compound library scale, bioassay data, substance relationships
- **MONDO** (10 questions): Disease ontology integration, cross-database hub, rare diseases
- **PubMed** (10 questions): Literature corpus, MeSH indexing, cross-database integration
- **ChEMBL** (8 questions): Bioactivity measurements, drug development, target-compound relationships
- **GO** (10 questions): Ontology hierarchy, gene annotations, transitive relationships

**Tier 2: Medium-Richness Databases** (45 questions total)
- **NCBI Gene** (8 questions): Gene metadata, cross-references, comparative genomics
- **ClinVar** (8 questions): Variant classification, clinical significance, pathogenicity
- **Reactome** (6 questions): Pathway hierarchy, species coverage, molecular interactions
- **PDB** (6 questions): Structure quality, experimental methods, resolution records
- **MeSH** (5 questions): Medical terminology, descriptor hierarchy, qualifier usage
- **NCBI Taxonomy** (4 questions): Organism classification, genetic codes, lineage
- **PubTator** (4 questions): Text mining annotations, gene-disease co-mentions
- **NANDO** (4 questions): Japanese rare diseases, notification numbers, multilingual

**Tier 3: Specialized Databases** (15 questions total)
- **Rhea** (3 questions): Biochemical reactions, EC numbers, transport reactions
- **ChEBI** (3 questions): Chemical ontology, molecular properties, biological roles
- **Ensembl** (2 questions): Genome annotations, transcript variants
- **MediaDive** (2 questions): Culture media recipes, extreme growth conditions
- **BacDive** (2 questions): Bacterial phenotypes, oxygen tolerance
- **AMR Portal** (1 question): Resistance mechanisms, MIC distributions
- **GlyCosmos** (1 question): Glycan structures, glycoprotein sites
- **MedGen** (1 question): Clinical concepts, terminology integration

---

## Database Characteristics

### Rich Content (Good for Multiple Questions)

**UniProt**:
- 444M proteins (923K Swiss-Prot manually curated)
- Cross-references to 200+ databases
- Sequences, functions, domains, variants
- Critical: Filter by reviewed=1 for quality and performance

**PubChem**:
- 119M compounds, 339M substances, 1.7M bioassays
- Molecular descriptors (SMILES, InChI, properties)
- Drug classifications, patent information
- Central hub for compound-gene-pathway linking

**MONDO**:
- 30,230 disease classes
- Integrates 39+ databases (OMIM, Orphanet, MeSH, ICD, NANDO)
- Average 6.5 cross-references per disease
- Essential hub for cross-database disease queries

**PubMed**:
- 37M+ biomedical citations
- MeSH annotations (~95% coverage, avg 12.8 terms/article)
- Cross-database integration via shared article URIs
- Enables literature-based discovery

**ChEMBL**:
- 2.4M+ compounds, 20M bioactivity measurements
- Drug mechanisms, target-compound relationships
- Cross-references to UniProt, PDB, PubChem, DrugBank

**GO**:
- 48,165 terms (30,804 biological process, 12,793 molecular function, 4,568 cellular component)
- Hierarchical ontology with transitive relationships
- Gene annotations enable systematic functional analysis

### Specialized Content (Good for Specificity)

**NANDO**:
- 2,777 Japanese intractable diseases
- Notification numbers, government designation
- 84% map to MONDO (2,341 diseases)
- Multilingual labels (Japanese kanji, hiragana, English)

**BacDive**:
- 97,334 bacterial/archaeal strains
- Phenotypic data (oxygen tolerance, temperature ranges)
- 73% of MediaDive strains have BacDive links
- Morphology, physiology, cultivation metadata

**MediaDive**:
- 3,289 culture media recipes
- Extreme thermophiles (Pyrolobus fumarii 103°C)
- 73% strain-BacDive cross-references (33,226 strains)
- Ingredient-level granularity with chemical cross-references

**AMR Portal**:
- 1.7M phenotypic resistance tests
- 1.1M genotypic AMR features
- Geographic and temporal surveillance
- Genotype-phenotype correlations

**GlyCosmos**:
- Glycan structures from GlyTouCan
- Glycoproteins, glycosylation sites
- 100+ named graphs for multi-species glycobiology
- Lectin-glycan interactions

### Well-Connected (Good for Integration)

**Cross-Database Hubs**:
- **MONDO**: Links 39+ disease databases
- **PubChem**: Connects compounds to genes, proteins, pathways, diseases
- **UniProt**: References 200+ databases for protein data
- **MeSH**: Indexes PubMed literature, links to MONDO diseases
- **NCBI Gene**: Central for gene-centric integration

**Shared Endpoints Enable Efficient Queries**:

**Primary Endpoint** (bacdive, mediadive, taxonomy, mesh, go, mondo, nando):
- MediaDive + BacDive: Strain phenotypes + culture conditions
- MONDO + MeSH: Disease ontology + literature indexing
- MONDO + NANDO: International + Japanese rare diseases

**SIB Endpoint** (uniprot, rhea):
- UniProt + Rhea: Protein enzymes + biochemical reactions

**NCBI Endpoint** (pubmed, pubtator, clinvar, ncbigene, medgen):
- PubMed + PubTator: Literature + text mining annotations
- PubTator + NCBI Gene: Annotations + gene metadata
- ClinVar + MedGen: Variants + disease concepts

**ChEMBL Endpoint** (chembl):
- ChEMBL + UniProt: Compounds + target proteins (via API)

**EBI Endpoint** (reactome, ensembl):
- Reactome + Ensembl: Pathways + genomic context

---

## Cross-Database Integration Opportunities

### High-Value Multi-Database Questions

**1. MediaDive + BacDive** (Shared Primary Endpoint):
- "What culture medium is used for thermophilic Bacillus species with BacDive phenotypes?"
- Enables: Strain characterization + cultivation protocols
- Optimization: Genus pre-filter reduces 97K strains to ~5K (95% reduction)

**2. MONDO + MeSH + NANDO** (Shared Primary Endpoint):
- "Map Japanese rare disease NANDO:1200214 through MONDO to MeSH literature terms"
- Enables: Japanese healthcare + international research + literature integration
- Three-way query: NANDO → MONDO → MeSH descriptor

**3. PubMed + PubTator + NCBI Gene** (Shared NCBI Endpoint):
- "What genes are annotated in COVID-19 vaccine articles with official gene symbols?"
- Enables: Literature + text mining + gene nomenclature
- Double pre-filtering: bif:contains (37M→100) + entity type filter

**4. UniProt + ChEMBL + PDB**:
- "Find protein structures (PDB) for kinase targets (UniProt) with low-IC50 inhibitors (ChEMBL)"
- Enables: Structure-activity relationships for drug discovery
- Cross-endpoint integration via UniProt accessions

**5. ClinVar + MedGen + NCBI Gene**:
- "Link pathogenic BRCA1 variants (ClinVar) to disease concepts (MedGen) and gene function (NCBI Gene)"
- Enables: Clinical genetics + molecular biology integration
- Shared NCBI endpoint enables efficient queries

**6. GO + NCBI Gene + UniProt**:
- "Find human kinases (UniProt) with DNA repair GO annotations and their gene IDs (NCBI Gene)"
- Enables: Functional genomics + protein characterization
- Cross-endpoint: GO primary, Gene NCBI, UniProt SIB

**7. Rhea + ChEBI + UniProt** (SIB Endpoint):
- "What enzymes (UniProt) catalyze ATP-dependent reactions (Rhea) with substrate structures (ChEBI)?"
- Enables: Enzyme-reaction-substrate networks
- SIB endpoint efficiency for UniProt-Rhea queries

**8. Reactome + Ensembl**:
- "Map BRCA1 transcripts (Ensembl) to DNA repair pathways (Reactome)"
- Enables: Genomic context + pathway biology
- Shared EBI endpoint for pathway-genome integration

---

## Key Findings by Category

### Precision Findings
- **UniProt reviewed filter critical**: reviewed=1 reduces 444M to 923K for quality/performance
- **PDB resolution records**: 0.48 Å highest resolution achieved (PDB exploration)
- **Extreme thermophile data**: Pyrolobus fumarii 103°C (MediaDive/BacDive)
- **MONDO cross-reference density**: Average 6.5 external database links per disease
- **Parkinson genetic heterogeneity**: 10+ distinct subtypes with unique OMIM IDs

### Completeness Findings
- **PubMed scale**: 37M+ citations, 23,437 CRISPR articles, 16,101 BRCA1+cancer articles
- **ChEMBL bioactivity**: 20M measurements, 2.4M compounds, 1.6M assays
- **GO ontology size**: 48,165 terms (30,804 BP, 12,793 MF, 4,568 CC)
- **NCBI Taxonomy scope**: 2.7M+ organisms from bacteria to mammals
- **BacDive strain coverage**: 97,334 strains with phenotypic characterizations

### Integration Findings
- **MONDO integration hub**: Links 39+ databases (70% UMLS, 33% OMIM, 34% Orphanet, 28% MeSH, 8% NANDO)
- **PubChem connectivity**: Links compounds to 167K genes, 249K proteins, 81K pathways
- **MediaDive-BacDive**: 73% overlap (33,226 strains with BacDive IDs)
- **Article URI standardization**: PubMed/PubTator use identical URIs enabling seamless joins
- **identifiers.org adoption**: PubTator, Rhea, ChEBI use standardized namespace

### Currency Findings
- **PubMed updates**: Daily additions, future dates for "in press" articles (2026-2027 found)
- **COVID-19 research**: Massive literature (PubMed), pathway additions (Reactome), vaccine developments
- **mRNA vaccine expansion**: Beyond COVID-19 to influenza, PRRSV, monkeypox, bronchitis
- **Database version tracking**: Most databases provide version/update metadata

### Specificity Findings
- **NANDO specialization**: 2,777 Japanese designated intractable diseases, multilingual support
- **Rare disease coverage**: MONDO, NANDO, Orphanet cross-references
- **Extreme phenotypes**: MediaDive thermophiles (103°C), psychrophiles (4°C)
- **AMR mechanisms**: Efflux pumps most common resistance mechanism (AMR Portal)
- **Specialized ontologies**: GlyCosmos glycans, ChEBI chemical roles, GO cellular components

### Structured Query Findings
- **SPARQL optimization critical**: bif:contains provides 10-100x speedup over REGEX
- **Cross-database pre-filtering**: 99.97-99.999999% reduction before joins prevents timeouts
- **Transitive relationships**: GO ancestry (rdfs:subClassOf+), Reactome hierarchy
- **Aggregation patterns**: Gene-disease co-occurrence, pathway member counts, variant distributions
- **Multi-criteria filtering**: ChEMBL (target + IC50 + approval status), ClinVar (gene + clinical significance + review status)

---

## Performance Optimization Patterns

### Successful Strategies Documented

**Strategy 1: Explicit GRAPH Clauses**
- Mandatory for cross-database queries
- Prevents cross-contamination of data
- Example: `GRAPH <http://rdfportal.org/dataset/pubmed> { ... }`

**Strategy 2: Pre-Filtering Within GRAPH**
- Apply filters BEFORE cross-database joins
- Typical reduction: 99.97-99.999999%
- Example: bif:contains in PubMed (37M→100 articles) before PubTator join

**Strategy 4: bif:contains for Text Search**
- 10-100x faster than REGEX or FILTER CONTAINS
- Uses Virtuoso full-text index with relevance scoring
- Example: `?title bif:contains "'cancer'" option (score ?sc)`

**Strategy 7: OPTIONAL Ordering**
- Required patterns first, OPTIONAL patterns last
- Improves query performance
- Example: Get gene symbol (required) then description (optional)

**Strategy 10: Always LIMIT**
- Prevents timeout on large result sets
- Essential for all exploratory queries
- Typical limits: 10-50 for exploration, 100+ for comprehensive retrieval

**Strategy 5: URI Conversion**
- Convert between database ID formats using BIND
- Example: MONDO "MESH:D######" → MeSH URI with SUBSTR + CONCAT

**Performance Tiers Observed**:
- **Tier 1 (1-3s)**: Simple lookups, two-way cross-database with pre-filtering
- **Tier 2 (3-10s)**: Three-way cross-database, aggregations with pre-filtering
- **Timeout risk**: No pre-filtering, no LIMIT, full dataset aggregations

---

## Critical Requirements for Question Generation

### Anti-Trivial Question Design

**✅ Good Questions (Require Actual Queries)**:
- "What is the UniProt ID for human BRCA1?" (requires search)
- "How many kinase structures are in PDB?" (requires COUNT query)
- "Convert UniProt P38398 to NCBI Gene ID" (requires cross-database lookup)
- "What are the ingredients in LB medium 381?" (requires composition query)

**❌ Bad Questions (Just Reading MIE/Docs)**:
- "What properties does UniProt have?" (schema info)
- "What is an example protein in UniProt?" (MIE example)
- "How do I query UniProt?" (methodology)
- "What databases does MONDO cross-reference?" (documentation)

### Focus on Biological Content

**✅ Expert-Relevant Questions**:
- "What is the IC50 of imatinib for EGFR?" (drug development)
- "How many pathogenic BRCA1 variants are in ClinVar?" (clinical genetics)
- "What resistance mechanisms are most common for E. coli?" (epidemiology)
- "Which kinases are targeted by approved drugs in ChEMBL?" (pharmacology)

**❌ Infrastructure/Metadata Questions**:
- "What is the current database version?" (IT metadata)
- "What are the MeSH tree numbers?" (organizational codes)
- "What is the SPARQL endpoint URL?" (infrastructure)
- "How many triples are in the database?" (technical metadata)

### Coverage Requirements

**Question Distribution Across 23 Databases**:
- All databases represented (at minimum 1 question each)
- High-richness databases: 8-12 questions each
- Medium-richness: 4-8 questions each
- Specialized: 1-3 questions each

**Category Distribution (20 questions each)**:
- Precision (20): Exact IDs, measurements, sequences
- Completeness (20): Counts, comprehensive lists
- Integration (20): Cross-database linking, ID conversions
- Currency (20): Recent data, time-sensitive information
- Specificity (20): Rare entities, specialized content
- Structured Query (20): Multi-criteria filtering, complex queries

---

## Next Steps

**Phase 1 Complete**: ✅ All 23 databases thoroughly explored

**Ready for Phase 2: Question Generation**
1. Create 120 questions following QUESTION_DESIGN_GUIDE.md
2. Use exploration reports as knowledge base
3. Ensure all questions require actual database queries (not MIE reading)
4. Distribute across databases according to coverage plan
5. Balance across 6 categories (20 questions each)
6. Focus on expert-relevant biological questions
7. Avoid infrastructure/metadata questions

**Quality Standards**:
- Every question verifiable with expected answer
- Every question requires database access (not baseline knowledge)
- Every question biologically realistic (real researcher use case)
- Every question documented with database(s), category, rationale

---

**Exploration Phase: COMPLETE** ✅  
**Token Usage: 130K / 190K (68%)** - Healthy budget for question generation  
**Quality: All findings from real queries, comprehensive coverage**  
**Next: Begin Phase 2 - Question Generation (120 questions)**
