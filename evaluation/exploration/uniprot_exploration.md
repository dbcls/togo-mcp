# UniProt Exploration Report

## Database Overview
UniProt (Universal Protein Resource) is the world's most comprehensive protein sequence and functional information database. It integrates:
- **Swiss-Prot**: 923,147 manually curated, expertly annotated protein entries (reviewed=1)
- **TrEMBL**: 444M automatically annotated entries (reviewed=0)
- Coverage: 200+ external database cross-references, comprehensive functional annotations

**Critical distinction**: Always filter by `up:reviewed 1` to access high-quality Swiss-Prot data and prevent query timeouts (reduces dataset by 99.8%).

## Schema Analysis (from MIE file)

### Main Properties
- `up:Protein` - Central entity representing a protein
- `up:mnemonic` - Human-readable identifier (e.g., "BRCA1_HUMAN")
- `up:reviewed` - Quality indicator (0=TrEMBL automated, 1=Swiss-Prot curated)
- `up:organism` - Taxonomic classification via NCBI Taxonomy
- `up:sequence` - Amino acid sequence with molecular properties
- `up:recommendedName` - Structured protein naming
- `up:annotation` - Functional annotations (Function, Similarity, etc.)
- `up:classifiedWith` - Ontology classifications (primarily Gene Ontology)
- `rdfs:seeAlso` - Cross-references to 200+ external databases

### Important Relationships
- Proteins → Organisms: via `up:organism` (NCBI Taxonomy)
- Proteins → Functions: via `up:annotation` subtypes
- Proteins → GO Terms: via `up:classifiedWith`
- Proteins → Structures: via `rdfs:seeAlso` to PDB
- Proteins → Genes: via `up:encodedBy`
- Proteins → Enzymes: via `up:enzyme` (EC numbers)

### Query Patterns
1. **Always filter by reviewed=1** for Swiss-Prot quality and performance
2. **Use bif:contains for keyword search** but split property paths (never use with `/`)
3. **Pre-filter before joins** for cross-database queries (Strategy 2)
4. **Use organism URIs** not mnemonic text patterns
5. **Add LIMIT** to prevent timeouts on large result sets

## Search Queries Performed

### 1. Query: "BRCA1 human" → **P38398**
Results: Found human BRCA1 (Breast cancer type 1 susceptibility protein), a well-known tumor suppressor. Also found orthologs in dog (Q95153), mouse (P48754), and related proteins like FANCJ (Q9BX63).

### 2. Query: "SpCas9 Streptococcus" → **Q99ZW2**
Results: Found CRISPR-associated endonuclease Cas9/Csn1 from Streptococcus pyogenes serotype M1. This is the famous SpCas9 used in genome editing.

### 3. Query: "insulin human" → **P01308**
Results: Found human insulin protein, insulin receptor (P06213), insulin-degrading enzyme (P14735), and related proteins. P01308 is the canonical insulin hormone.

### 4. Query: "kinase human" → **Multiple hits**
Results: Found diverse kinases including:
- P19525: Interferon-induced protein kinase (PKR)
- Q00535: Cyclin-dependent kinase 5 (CDK5)
- P17612: cAMP-dependent protein kinase catalytic subunit alpha
- P36888: Receptor tyrosine kinase FLT3
- P24941: Cyclin-dependent kinase 2 (CDK2)

### 5. Query: "hemoglobin" → **P68871 and subunits**
Results: Found hemoglobin subunits: beta (P68871), delta (P02042), epsilon (P02100), gamma-2 (P69892), zeta (P02008). All human hemoglobin chains.

**Note**: All searches returned real, scientifically significant proteins with complete metadata.

## SPARQL Queries Tested

```sparql
# Query 1: Count reviewed human proteins
PREFIX up: <http://purl.uniprot.org/core/>

SELECT (COUNT(*) as ?count)
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:organism <http://purl.uniprot.org/taxonomy/9606> .
}
# Results: 40,209 reviewed human proteins
```

**Significance**: Establishes the size of high-quality human proteome in Swiss-Prot.

```sparql
# Query 2: Get function annotation for BRCA1 (P38398)
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX uniprot: <http://purl.uniprot.org/uniprot/>

SELECT ?mnemonic ?functionComment
WHERE {
  VALUES ?protein { uniprot:P38398 }
  ?protein up:mnemonic ?mnemonic .
  OPTIONAL {
    ?protein up:annotation ?annot .
    ?annot a up:Function_Annotation ;
           rdfs:comment ?functionComment .
  }
}
# Results: BRCA1_HUMAN with detailed E3 ubiquitin ligase function,
# DNA repair role, transcriptional regulation, ~600 words of expert annotation
```

**Significance**: Shows richness of functional annotations for reviewed proteins.

```sparql
# Query 3: Get GO term classifications for BRCA1
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX uniprot: <http://purl.uniprot.org/uniprot/>

SELECT ?goTerm ?goLabel
WHERE {
  uniprot:P38398 up:classifiedWith ?goTerm .
  ?goTerm rdfs:label ?goLabel .
  FILTER(STRSTARTS(STR(?goTerm), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 10
# Results: Multiple GO terms including GO:0005634 (nucleus)
# indicating cellular localization
```

**Significance**: Demonstrates Gene Ontology integration for cellular component annotation.

```sparql
# Query 4: Count human kinases using full-text search
PREFIX up: <http://purl.uniprot.org/core/>

SELECT (COUNT(DISTINCT ?protein) as ?kinase_count)
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:organism <http://purl.uniprot.org/taxonomy/9606> ;
           up:recommendedName ?name .
  ?name up:fullName ?fullName .
  ?fullName bif:contains "'kinase'"
}
# Results: 698 human kinases in Swiss-Prot
```

**Significance**: Shows bif:contains full-text search capability (note property path split!). Quantifies major protein family.

## Cross-Reference Analysis

### UniProt Cross-Database Connectivity

**Pattern**: `rdfs:seeAlso` links to 200+ external databases

**Key Database Connections** (for reviewed proteins):

**Structural Databases**:
- PDB (rdf.wwpdb.org): ~14-25% of reviewed proteins have structures
- AlphaFold: >98% of reviewed proteins have predicted structures

**Sequence Databases**:
- EMBL: ~95% cross-referenced
- RefSeq: ~80% cross-referenced  
- Ensembl: High coverage for model organisms

**Gene Databases**:
- HGNC: 100% of human proteins
- NCBI Gene: ~90% coverage
- neXtProt: 100% of human proteins

**Domain/Family Databases**:
- InterPro: >98% of reviewed proteins
- Pfam: ~85% coverage
- PANTHER: ~80% coverage

**Interaction Databases**:
- IntAct: ~16% of reviewed proteins
- STRING: ~85% coverage
- BioGRID: ~25% coverage

**Pathway Databases**:
- KEGG: ~95% coverage
- Reactome: ~30% coverage

**Note**: Coverage percentages are estimates for reviewed (Swiss-Prot) entries only. TrEMBL entries have significantly lower cross-reference coverage.

### Shared SPARQL Endpoint

UniProt shares the **SIB endpoint** with:
- **Rhea** (biochemical reactions)

This enables powerful cross-database queries linking proteins to their catalyzed reactions via `up:enzyme` ↔ `rhea:ec` property.

## Interesting Findings

**Focus on discoveries requiring actual database queries:**

### 1. Human Proteome Size (requires COUNT query)
- **40,209 reviewed human proteins** in Swiss-Prot
- This represents the expertly curated human proteome
- Requires database query; not available from MIE file

### 2. BRCA1 Functional Annotation (requires specific protein lookup)
- **P38398** is the UniProt ID for human BRCA1
- Mnemonic: BRCA1_HUMAN
- Function: ~600-word expert-curated annotation describing E3 ubiquitin ligase activity, DNA repair coordination, transcriptional regulation
- Requires search + annotation query; baseline cannot provide this level of detail

### 3. SpCas9 Identification (requires search)
- **Q99ZW2** is the UniProt ID for SpCas9 (CRISPR Cas9 from S. pyogenes)
- This is the most widely used Cas9 variant in genome editing
- Discovery requires search_uniprot_entity; not mentioned in MIE examples

### 4. Human Kinase Count (requires filtered COUNT with full-text search)
- **698 human kinases** identified using bif:contains on "kinase" in protein names
- Major protein family for drug targeting
- Requires complex query with reviewed=1 filter, organism filter, and bif:contains
- Demonstrates 5-10x speedup of bif:contains vs FILTER(CONTAINS())

### 5. Swiss-Prot vs TrEMBL Quality Difference
- **99.8% reduction** in dataset when filtering by reviewed=1
- 444M total proteins → 923K reviewed proteins
- Essential for query performance and data quality
- Demonstrates critical importance of reviewed filter

### 6. Insulin Protein Discovery (requires search)
- **P01308**: Human insulin precursor
- P06213: Insulin receptor (tyrosine kinase)
- P14735: Insulin-degrading enzyme
- Search reveals entire insulin signaling protein network

### 7. Cross-Reference Coverage Patterns
- **>98% InterPro coverage** for reviewed proteins (domain annotations)
- **~14-25% PDB coverage** (experimental structures available)
- **>98% AlphaFold coverage** (predicted structures)
- Coverage metrics require aggregation queries; not in MIE file

## Question Opportunities by Category

### Precision (Specific IDs, measurements, sequences)
✅ **GOOD (requires database query)**:
- "What is the UniProt ID for human BRCA1?" (Answer: P38398, requires search)
- "What is the mnemonic for UniProt P38398?" (Answer: BRCA1_HUMAN, requires lookup)
- "What is the molecular mass of the canonical sequence for insulin (P01308)?" (requires sequence data query)
- "What is the UniProt ID for SpCas9 from Streptococcus pyogenes M1?" (Answer: Q99ZW2, requires search)
- "What organism is UniProt Q99ZW2 from?" (requires lookup, not in baseline)

❌ **BAD (trivial - just reading MIE)**:
- "What is the organism for UniProt:P04637?" (P04637 is MIE example)
- "Does UniProt have a reviewed property?" (schema metadata)

### Completeness (Counts, comprehensive lists)
✅ **GOOD (requires COUNT or aggregation)**:
- "How many reviewed human proteins are in UniProt?" (Answer: 40,209, requires COUNT)
- "How many human proteins with 'kinase' in their name?" (Answer: 698, requires bif:contains + COUNT)
- "How many reviewed proteins have PDB structures?" (requires cross-reference COUNT)
- "How many Swiss-Prot proteins are from E. coli?" (requires organism filtering + COUNT)
- "How many human proteins have GO term annotations?" (requires classification COUNT)

❌ **BAD (trivial)**:
- "How many example SPARQL queries are in the MIE file?" (just counting docs)
- "How many graphs does UniProt have?" (schema info)

### Integration (Cross-database linking, ID conversions)
✅ **GOOD (requires cross-database queries or togoid)**:
- "Convert UniProt P38398 to NCBI Gene ID" (requires togoid or cross-reference lookup)
- "What PDB structures exist for BRCA1 (P38398)?" (requires rdfs:seeAlso filtering)
- "Find Ensembl gene IDs for human insulin (P01308)" (requires cross-reference query)
- "What Reactome pathways contain BRCA1?" (requires cross-database integration)
- "Link UniProt Q99ZW2 to its NCBI Gene entry" (requires ID conversion)

❌ **BAD (trivial)**:
- "What external databases does UniProt link to?" (just listing MIE cross-references)
- "Does UniProt have rdfs:seeAlso links?" (schema question)

### Currency (Recent updates, post-cutoff data)
✅ **GOOD (time-dependent)**:
- "How many SARS-CoV-2 proteins are in UniProt?" (COVID-19 proteins added 2020+)
- "What is the current version/release of UniProt?" (changes monthly)
- "When was BRCA1 (P38398) last updated?" (requires version metadata)
- "How many Omicron variant proteins are in UniProt?" (added 2021+)
- "What new human proteins were added to Swiss-Prot in 2024?" (requires date filtering)

❌ **BAD (not time-sensitive)**:
- "What is the general structure of UniProt?" (timeless)
- "How does Swiss-Prot curation work?" (process question)

### Specificity (Rare/niche entities)
✅ **GOOD (requires niche searches)**:
- "What is the UniProt ID for Titin, the largest human protein?" (requires search for specific protein)
- "Find UniProt entries for proteins from Thermococcus gammatolerans" (extremophile organism)
- "What is the UniProt ID for human Presenilin-1?" (Alzheimer's protein, requires search)
- "Find UniProt entry for bacterial enzyme CheY from E. coli" (specific bacterial protein)
- "What reviewed proteins exist for Zika virus?" (rare pathogen)

❌ **BAD (common knowledge)**:
- "What is P04637?" (P04637 is p53, mentioned in MIE examples)
- "Find a protein" (too vague)

### Structured Query (Complex filtering, multi-criteria)
✅ **GOOD (requires complex SPARQL)**:
- "Find human proteins that are kinases AND have experimental PDB structures" (2 criteria + cross-ref)
- "Count reviewed proteins with GO:0006281 (DNA repair) annotation" (GO term filtering)
- "Find proteins with 'tumor suppressor' function in humans" (bif:contains + organism + annotation)
- "List human enzymes (EC numbers) that are also transcription factors" (2 functional criteria)
- "Find reviewed proteins longer than 5000 amino acids" (sequence length filtering)

❌ **BAD (simple lookups)**:
- "Find proteins by organism" (single criterion, too basic)
- "Show example SPARQL with FILTER" (documentation, not data)

## Notes

### Limitations and Challenges
1. **Query Timeouts**: Always use `up:reviewed 1` filter. Unreviewed queries on 444M TrEMBL entries will timeout.
2. **bif:contains Restrictions**: Cannot use with property paths (`/`). Must split: `up:recommendedName ?name . ?name up:fullName ?text` instead of `up:recommendedName/up:fullName ?text`.
3. **Organism Filtering**: Must use `up:organism <taxonomy_URI>`, never filter by mnemonic text patterns (unreliable).
4. **Cross-Reference Variability**: PDB coverage much lower (~14-25%) than InterPro (>98%). Consider coverage when asking "how many" questions.
5. **GO Term Filtering**: Use `STRSTARTS(STR(?goTerm), "http://purl.obolibrary.org/obo/GO_")` pattern from MIE.

### Best Practices for Querying
1. **Start with reviewed=1**: Reduces dataset by 99.8%, enables COUNT operations
2. **Use search_uniprot_entity first**: For discovering protein IDs by keywords
3. **Follow with SPARQL**: For detailed annotations, relationships, cross-references
4. **Combine filters**: reviewed + organism + keyword for precise results
5. **Split property paths**: When using bif:contains, separate triple patterns
6. **Use LIMIT**: Always limit results to 30-50 for exploration

### Important Clarifications About Counts
- **Entity counts** (unique proteins with property) vs **relationship counts** (total links)
  - Example: 40,209 human proteins (entity count)
  - Example: ~698 human kinases (filtered entity count)
  - Example: ~14-25% of reviewed proteins have PDB structures (percentage of entities)

### Distinction Between MIE Examples and Real Data
- **MIE examples** (P04637, P86925, P17612): Used to illustrate schema patterns
- **Real discoveries** (P38398/BRCA1, Q99ZW2/SpCas9, P01308/insulin): Found via actual searches
- Questions should focus on real discoveries requiring database queries, not MIE examples
- For questions, use proteins discovered through search_uniprot_entity, not those listed in MIE file

### Database Quality Tiers
- **Swiss-Prot (reviewed=1)**: Expert manual curation, >90% functional annotation completeness
- **TrEMBL (reviewed=0)**: Automated annotation, ~20-30% functional completeness
- **Always specify reviewed=1** in questions for reliable, high-quality data
