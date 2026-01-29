# PubTator Central Exploration Report

## Database Overview
PubTator Central is a biomedical text mining database containing >10 million entity annotations extracted from PubMed literature using automated methods (PubTator3), manual curation (ClinVar), and genomic databases (dbSNP). It provides Disease and Gene annotations linked to PubMed articles with identifiers from MeSH and NCBI Gene databases. Each annotation includes mention frequency counts (annotation_count) indicating how many times an entity appears in an article. The RDF representation uses the Web Annotation Ontology (oa:Annotation) to model entity-article relationships, enabling literature-based biomedical discovery, gene-disease association networks, and knowledge graph construction.

Key data types:
- **Disease Annotations**: MeSH disease terms (identifiers.org/mesh/) linked to PubMed articles
- **Gene Annotations**: NCBI Gene IDs (identifiers.org/ncbigene/) linked to PubMed articles
- **Annotation Metadata**: Mention counts (1-9+), source attribution (PubTator3, ClinVar, dbSNP)
- **Article Links**: Connections to PubMed (http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid})

## Schema Analysis (from MIE file)

**Main Properties:**
- `oa:Annotation`: Core entity representing text mining annotations
- `dcterms:subject`: Entity type classification ("Disease" or "Gene")
- `oa:hasBody`: External identifier (MeSH term URI or NCBI Gene URI via identifiers.org)
- `oa:hasTarget`: Link to PubMed article (http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid})
- `pubtator:annotation_count`: Integer indicating mention frequency in article (typically 1-2, occasionally 9+)
- `dcterms:source`: Optional provenance (PubTator3, ClinVar, dbSNP) - ~50% coverage

**Important Relationships:**
- Disease annotations: oa:hasBody → identifiers.org/mesh/{mesh_id} (e.g., D000544 for Alzheimer Disease)
- Gene annotations: oa:hasBody → identifiers.org/ncbigene/{gene_id}
- Article linking: oa:hasTarget → shared article URI pattern with PubMed, enabling seamless cross-database joins
- Cross-database integration: identifiers.org namespace enables direct compatibility with NCBI Gene, MeSH databases

**Query Patterns:**
- Entity type filtering: `dcterms:subject` with "Disease" or "Gene" literal
- Specific entity lookup: Filter on `oa:hasBody` with full identifiers.org URI
- Article-specific annotations: Filter on `oa:hasTarget` with PubMed article URI
- High-frequency mentions: Filter `pubtator:annotation_count > N`
- Gene-disease co-mentions: Join two annotations via shared `oa:hasTarget`
- Cross-database enrichment: Join with PubMed (titles/abstracts) or NCBI Gene (gene symbols/descriptions)

## Search Queries Performed

1. **Query: Alzheimer Disease annotations (MeSH D000544)** → Found 5 articles with Alzheimer Disease mentions including PMIDs 1893564, 18936138, 18936150, 18936242, 18936252. Demonstrates disease-specific literature linkage.

2. **Query: Unique gene identifiers** → Retrieved 10 distinct NCBI Gene IDs: 11820, 12359, 1233, 20299, 207, 2185, 21943, 25819, 5594, 6367, showing diverse gene coverage from text mining.

3. **Query: High-frequency gene mentions (count >5)** → Found 10 genes with 8-9 mentions per article, including NCBI Gene IDs 28964 (9 mentions in PMID 15383276), 81848, 79760, 8856, 1616, 10605, 51135, 1540, 6867, 4089 (all 8 mentions). Identifies highly discussed genes in specific publications.

## SPARQL Queries Tested

```sparql
# Query 1: Find all disease annotations for specific article - adapted for PMID 18935173
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?ann ?diseaseId
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Disease" ;
       oa:hasBody ?diseaseId ;
       oa:hasTarget <http://rdf.ncbi.nlm.nih.gov/pubmed/18935173> .
}
# Results: Retrieved all disease annotations for specific article (demonstrates article-centric query)
```

```sparql
# Query 2: Find articles mentioning diabetes mellitus (MeSH D003920) - adapted with provenance
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX pubtator: <http://purl.jp/bio/10/pubtator-central/ontology#>

SELECT ?ann ?article ?count ?source
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Disease" ;
       oa:hasBody <http://identifiers.org/mesh/D003920> ;
       oa:hasTarget ?article ;
       pubtator:annotation_count ?count .
  OPTIONAL { ?ann dcterms:source ?source }
}
ORDER BY DESC(?count)
LIMIT 20
# Results: Found diabetes articles with annotation counts and optional source attribution (PubTator3, ClinVar, dbSNP)
```

```sparql
# Query 3: Gene-disease co-mentions - adapted for Parkinson Disease (D010300) with gene enrichment
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?article ?geneId ?diseaseId
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?geneAnn dcterms:subject "Gene" ;
           oa:hasBody ?geneId ;
           oa:hasTarget ?article .
  ?diseaseAnn dcterms:subject "Disease" ;
              oa:hasBody <http://identifiers.org/mesh/D010300> ;
              oa:hasTarget ?article .
}
LIMIT 50
# Results: Retrieved articles mentioning both Parkinson Disease and genes, enabling gene-disease association discovery
```

```sparql
# Query 4: Cross-database integration with PubMed - adapted for BRCA1 research
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX pubtator: <http://purl.jp/bio/10/pubtator-central/ontology#>

SELECT ?pmid ?title ?geneId ?count
WHERE {
  GRAPH <http://rdfportal.org/dataset/pubmed> {
    ?article bibo:pmid ?pmid ;
             dct:title ?title .
    ?title bif:contains "'BRCA1' AND 'cancer'" .
  }
  GRAPH <http://rdfportal.org/dataset/pubtator_central> {
    ?ann dcterms:subject "Gene" ;
         oa:hasBody ?geneId ;
         oa:hasTarget ?article ;
         pubtator:annotation_count ?count .
  }
}
ORDER BY DESC(?count)
LIMIT 20
# Results: Found BRCA1 cancer articles with gene annotations and mention frequencies (demonstrates PubMed-PubTator integration)
```

```sparql
# Query 5: High-frequency entity mentions - adapted for genes with multiple mentions
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX pubtator: <http://purl.jp/bio/10/pubtator-central/ontology#>

SELECT ?geneId (AVG(?count) as ?avg_mentions) (COUNT(?article) as ?article_count)
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann dcterms:subject "Gene" ;
       oa:hasBody ?geneId ;
       oa:hasTarget ?article ;
       pubtator:annotation_count ?count .
  FILTER(?count > 3)
}
GROUP BY ?geneId
ORDER BY DESC(?avg_mentions)
LIMIT 20
# Results: Identified genes with consistently high mention rates across articles (indicates important research genes)
```

## Cross-Reference Analysis

**Entity counts** (unique entities with mappings):

PubTator Annotations → External Databases:
- Majority: Disease annotations using MeSH identifiers (identifiers.org/mesh/)
- Substantial: Gene annotations using NCBI Gene identifiers (identifiers.org/ncbigene/)
- All: Article links to PubMed (http://rdf.ncbi.nlm.nih.gov/pubmed/)

**MeSH Disease Coverage:**
- Extensive coverage of MeSH disease terms across biomedical literature
- Disease annotations represent majority of PubTator content
- MeSH namespace: identifiers.org/mesh/{mesh_id}

**NCBI Gene Coverage:**
- Broad coverage of gene identifiers from text mining
- Gene annotations less frequent than disease annotations
- NCBI Gene namespace: identifiers.org/ncbigene/{gene_id}

**Relationship counts** (total mappings):

Annotation Frequency Distribution:
- Typical annotation_count: 1-2 mentions per article
- High-frequency: 3-5 mentions (genes central to article topic)
- Very high-frequency: 6-9+ mentions (highly focused articles on specific genes)
- Maximum observed: 9 mentions (NCBI Gene 28964 in PMID 15383276)

**Distribution:**
- Average 1-5 annotations per article (variable by article type and topic)
- ~50% of annotations include dcterms:source provenance
- Source attribution: PubTator3 (automated), ClinVar (curated), dbSNP (genomic)

## Interesting Findings

**Discoveries requiring actual database queries:**

1. **High-frequency gene mentions identify focal topics**: Gene NCBI:28964 appears 9 times in PMID 15383276, indicating the article focuses extensively on this specific gene. Requires querying annotation_count property.

2. **Alzheimer Disease literature linkage**: MeSH D000544 (Alzheimer Disease) annotations found in PMIDs 1893564, 18936138, 18936150, 18936242, 18936252. Requires disease-specific filtering on oa:hasBody.

3. **Gene annotation diversity**: First 10 gene IDs span range from 207 to 28964, showing broad coverage from yeast (20299) to human genes. Requires DISTINCT query on gene annotations.

4. **Provenance tracking incomplete**: Only ~50% of annotations include dcterms:source, meaning provenance unknown for half of annotations. Requires OPTIONAL pattern analysis.

5. **Disease annotations dominate**: Disease annotations appear more frequently than gene annotations in query results, suggesting text mining emphasis on disease mentions. Requires comparing entity type distributions.

6. **Annotation count distribution**: Most annotations have count=1-2, with rare cases of 8-9 mentions indicating highly focused articles. Requires annotation_count aggregation analysis.

7. **Cross-database integration via shared URIs**: Article URIs (http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid}) identical in PubTator and PubMed enable seamless joins without URI conversion. Requires cross-database query testing.

8. **Gene-disease co-mentions enable association discovery**: Articles with both gene and disease annotations (via shared oa:hasTarget) provide evidence for gene-disease relationships. Requires co-occurrence queries.

9. **identifiers.org namespace standardization**: All external references use identifiers.org URIs (mesh/, ncbigene/) enabling direct compatibility with other databases. Requires examining oa:hasBody URI patterns.

## Question Opportunities by Category

### Precision Questions ✅
- "What is the annotation count for gene NCBI:28964 in PMID 15383276?" (requires specific annotation query - answer: 9)
- "What MeSH disease ID is annotated in PubMed article 18935173?" (requires disease annotation lookup)
- "What is the source attribution for disease annotation D000544 in PMID 1893564?" (requires dcterms:source retrieval)
- "How many times is gene NCBI:207 mentioned in its most frequently annotated article?" (requires MAX(annotation_count) query)

### Completeness Questions ✅
- "How many articles in PubTator have Alzheimer Disease (D000544) annotations?" (requires COUNT on disease filter)
- "List all gene IDs annotated in PubMed article 12345678" (requires gene annotation enumeration)
- "How many distinct diseases are annotated across all PubTator?" (requires COUNT DISTINCT on disease oa:hasBody)
- "What are all the PubMed articles mentioning gene NCBI:1233?" (requires article enumeration via oa:hasTarget)

### Integration Questions ✅
- "What genes are annotated in PubMed articles about 'CRISPR'?" (requires PubTator→PubMed keyword integration)
- "Link PubTator disease annotations to MeSH term labels in MeSH database" (requires PubTator→MeSH cross-reference)
- "What are the gene symbols for genes annotated in diabetes articles?" (requires PubTator→PubMed→NCBI Gene three-way integration)
- "Convert PubTator gene annotations to Ensembl IDs via NCBI Gene" (requires multi-database ID conversion)

### Currency Questions ✅
- "What genes are newly annotated in 2025 COVID-19 publications?" (requires temporal PubMed filter + PubTator annotations)
- "How many disease annotations have been added for recent mRNA vaccine articles?" (requires recent PubMed + annotation count)
- "What is the most recently annotated article for Parkinson Disease?" (requires temporal sorting with disease filter)

### Specificity Questions ✅
- "What genes are co-mentioned with Erdheim-Chester disease (rare disorder)?" (requires rare disease gene co-occurrence)
- "Which articles discuss both BRCA1 gene and Fanconi anemia disease?" (requires specific gene-disease co-mention)
- "What is the annotation count for SARS-CoV-2 spike protein gene in its most discussed article?" (requires specific gene mention frequency)
- "Find articles with >5 mentions of gene TP53 (NCBI:7157)" (requires high-frequency annotation filtering)

### Structured Query Questions ✅
- "Find genes co-occurring with Alzheimer Disease in >10 articles" (requires gene-disease aggregation with threshold)
- "Identify articles with both gene and disease annotations where annotation_count >3 for both" (requires dual entity type + frequency filtering)
- "List genes mentioned in Nature journals about cancer (via PubMed integration)" (requires PubMed journal filter + keyword + PubTator annotations)
- "Find disease-gene pairs with highest co-occurrence counts across literature" (requires co-mention aggregation with ranking)

## Notes

**Web Annotation Ontology usage**: PubTator uses W3C Web Annotation Ontology standard (oa:Annotation, oa:hasBody, oa:hasTarget) making it interoperable with other annotation systems and enabling semantic integration.

**Entity type limitation**: Database primarily contains "Disease" and "Gene" entity types. Other types (Chemical, Species, Mutation) mentioned in documentation may have limited or no coverage. Always filter by dcterms:subject to ensure correct entity type.

**Cross-database optimization**: Shares "ncbi" endpoint with PubMed, NCBI Gene, ClinVar, MedGen. Cross-database queries require:
- **Strategy 1**: Explicit GRAPH clauses for each database (MANDATORY)
- **Strategy 2**: Pre-filtering within source GRAPH before joins (99.9997-99.999999% reduction)
- **Strategy 4**: bif:contains for PubMed keyword search (10-100x speedup over REGEX)
- **Strategy 7**: OPTIONAL ordering (required patterns first, optional patterns last)
- **Strategy 10**: LIMIT clauses to prevent timeouts (essential for all queries)
- **Critical MIE consultation**: Always retrieve MIE files for co-located databases BEFORE creating cross-database queries

**Performance tiers**:
- Single-database entity lookup: Fast (<1s)
- Entity-specific queries with filters: Moderate (1-5s)
- Cross-database (PubTator-PubMed): Tier 1 (1-3s with bif:contains pre-filtering)
- Three-way (PubTator-PubMed-NCBI Gene): Tier 2 (5-8s with double pre-filtering)
- Aggregations (gene-disease co-occurrence): Tier 2 (5-10s with disease pre-filtering)

**Annotation count interpretation**:
- count=1: Entity mentioned once (typical)
- count=2-3: Multiple mentions (moderate focus)
- count=4-5: High focus (central to article)
- count=6-9+: Very high focus (article specifically about this entity)
- Use for relevance ranking: Higher counts = more central to article topic

**Provenance tracking**:
- ~50% of annotations have dcterms:source
- Sources: PubTator3 (automated text mining), ClinVar (manual curation), dbSNP (genomic database)
- Use OPTIONAL for dcterms:source to capture all annotations

**Article URI compatibility**:
- PubTator uses http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid} pattern
- Identical to PubMed's article URI pattern
- No URI conversion needed for PubTator↔PubMed joins
- Enables seamless cross-database integration

**identifiers.org standardization**:
- Disease: identifiers.org/mesh/{mesh_id} directly compatible with MeSH database
- Gene: identifiers.org/ncbigene/{gene_id} directly compatible with NCBI Gene database
- No namespace conversion needed for cross-database queries
- Follows Identifiers.org registry standards for biological databases

**Gene-disease association discovery**:
- Co-mention queries identify articles discussing both entities
- Co-occurrence counts indicate association strength in literature
- Higher co-occurrence = stronger literature-based evidence
- Useful for hypothesis generation, candidate gene identification, systematic reviews

**Data quality considerations**:
- Automated text mining may have false positives
- Entity disambiguation not always perfect (gene symbols, disease names)
- Annotation counts represent mentions, not biological significance
- Provenance (when available) indicates data source and reliability

**Cross-database integration patterns**:
- PubTator→PubMed: Shared article URI, keyword search via bif:contains in PubMed GRAPH
- PubTator→NCBI Gene: identifiers.org/ncbigene URIs directly compatible, enrichment via rdfs:label and dct:description
- PubTator→MeSH: identifiers.org/mesh URIs for disease term metadata
- Three-way (PubTator→PubMed→NCBI Gene): Double pre-filtering (bif:contains + entity type) required

**Unique value**: PubTator Central provides automated biomedical entity recognition linking millions of genes and diseases to their PubMed literature mentions. Essential for literature-based discovery, gene-disease association networks, systematic reviews, and knowledge graph construction. The RDF representation with Web Annotation Ontology enables semantic integration with other biomedical resources.

**Limitations**:
- Entity types limited to primarily Disease and Gene (Chemical, Species, Mutation coverage unclear)
- Provenance incomplete (~50% have dcterms:source)
- Automated text mining may have accuracy issues
- Large aggregation queries timeout without LIMIT
- Cross-database queries require pre-filtering to avoid timeouts
- MIE file consultation mandatory to avoid wrong properties/URIs in cross-database queries
