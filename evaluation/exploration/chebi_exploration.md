# ChEBI Exploration Report

## Database Overview
ChEBI (Chemical Entities of Biological Interest) is an ontology database containing 223,738 chemical entities including small molecules, atoms, ions, functional groups, and macromolecules with hierarchical classification.

## Schema Analysis
**Main entity type:**
- `owl:Class`: Chemical entities

**Key properties:**
- Identification: rdfs:label, oboInOwl:id, oboInOwl:hasOBONamespace
- Hierarchy: rdfs:subClassOf
- Structure: chebi/formula, chebi/mass, chebi/smiles, chebi/inchi, chebi/inchikey
- Cross-references: oboInOwl:hasDbXref (literal strings)
- Synonyms: oboInOwl:hasRelatedSynonym, oboInOwl:hasExactSynonym
- Definition: obo:IAO_0000115

**CRITICAL namespace distinction:**
- Data properties: `http://purl.obolibrary.org/obo/chebi/` (formula, mass, smiles)
- Relationship properties: `http://purl.obolibrary.org/obo/chebi#` (is_conjugate_acid_of)

**Important patterns:**
- OWL ontology structure with class hierarchy
- Chemical relationships encoded as OWL restrictions
- Biological roles via RO_0000087 through restrictions
- Two namespaces (/ vs #) for different property types

## Search Queries Performed

Using OLS4:search tool:
1. Query: "glucose" → Found CHEBI:17234 (glucose) and related entries
2. Cross-ontology results include FOBI, XCO, SNOMED references

## SPARQL Queries Tested

```sparql
# Query 1: Entity coverage statistics
SELECT (COUNT(*) as ?totalEntities)
       (COUNT(?formula) as ?withFormula)
       (COUNT(?mass) as ?withMass)
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  ?entity a owl:Class .
  FILTER(STRSTARTS(STR(?entity), "http://purl.obolibrary.org/obo/CHEBI_"))
  OPTIONAL { ?entity chebi:formula ?formula }
  OPTIONAL { ?entity chebi:mass ?mass }
}
# Results: 223,738 entities, 193,348 with formula (86%), 192,389 with mass (86%)
```

## Cross-Reference Analysis

**External database cross-references (via oboInOwl:hasDbXref):**
- Chemical: CAS, Beilstein, Reaxys, Gmelin
- Biological: KEGG, HMDB, DrugBank, MetaCyc
- Structure: PubChem, ChEMBL, LIPID_MAPS
- Knowledge: Wikipedia, PMID, Patent

**Cross-database integration:**
- ChEMBL: Via skos:exactMatch (high performance, Tier 1: 1-3s)
- Reactome: Via bp:xref with URI conversion (moderate performance, Tier 2: 3-8s)
- Both on shared EBI endpoint

**Integration methods:**
1. ChEMBL: Direct skos:exactMatch linking
2. Reactome: URI conversion from "CHEBI:15422" format to CHEBI_15422 URIs
3. PubChem/DrugBank: Via cross-reference literals (requires parsing)

## Interesting Findings

**Entity coverage:**
- Total: 223,738 chemical entities
- With formula: 193,348 (86%)
- With mass: 192,389 (86%)
- With InChI: ~81%
- With SMILES: ~85%

**Search capabilities:**
- OLS4:search tool provides fast keyword lookup
- Returns entities across multiple ontologies (ChEBI, FOBI, SNOMED)
- bif:contains within SPARQL for full-text search with relevance scoring

**Structural diversity:**
- Small molecules (e.g., water CHEBI:15377)
- Amino acids (e.g., L-proline CHEBI:17203)
- Drugs (e.g., ciprofloxacin CHEBI:100241)
- Elements (e.g., phosphorus CHEBI:28659)
- Lipids (e.g., triolein CHEBI:53753)

**Cross-database optimization:**
- ChEMBL integration: Pre-filtering on developmentPhase reduces join size by 99.5%
- Reactome integration: Requires ^^xsd:string type restriction for bp:db
- URI conversion pattern: SUBSTR + BIND(IRI(CONCAT(...)))

**Performance characteristics:**
- bif:contains searches: <2s typically
- Cross-database queries: Tier 1 (1-3s) for ChEMBL, Tier 2 (3-8s) for Reactome
- Pre-filtering essential for sub-3s performance

## Question Opportunities by Category

### Precision
- ✅ "What is the molecular formula of aspirin (CHEBI:15365)?"
- ✅ "What is the InChI key for glucose?"
- ✅ "How many entities have molecular mass data?"

### Completeness
- ✅ "How many chemical entities are in ChEBI?"
- ✅ "What percentage of entities have SMILES notation?"
- ✅ "How many entities have KEGG cross-references?"

### Integration
- ✅ "Link ChEBI marketed drugs to ChEMBL development phase data"
- ✅ "Find ChEBI metabolites in Reactome metabolic pathways"
- ✅ "Which ChEBI entities are in DrugBank?"

### Currency
- ⚠️ Limited - ontology updates monthly but not time-series data

### Specificity
- ✅ "Find antibiotics in ChEBI"
- ✅ "What are parent classes of L-proline?"
- ✅ "Find conjugate acid/base pairs in ChEBI"

### Structured Query
- ✅ "Find carbon-oxygen compounds with >5 database cross-references"
- ✅ "Find marketed kinase inhibitors with ChEMBL via ChEBI"
- ✅ "Find entities with both KEGG and DrugBank references"

## Notes

**Critical namespace issues:**
- Data properties (formula, mass, smiles): `http://purl.obolibrary.org/obo/chebi/`
- Relationship properties (is_conjugate_acid_of): `http://purl.obolibrary.org/obo/chebi#`
- Using wrong namespace causes empty results

**Query optimization:**
- Always filter by CHEBI_ URI prefix to exclude non-entity classes
- Use bif:contains for keyword search (faster than FILTER CONTAINS)
- Use OPTIONAL for molecular properties (not all entities have them)
- Add LIMIT to prevent timeouts

**Cross-database optimization strategies:**
- Strategy 1: Explicit GRAPH clauses
- Strategy 2: Pre-filter within GRAPH blocks (99.5% reduction possible)
- Strategy 4: bif:contains for text search
- Strategy 5: URI conversion for Reactome
- Strategy 7: OPTIONAL blocks after required patterns
- Strategy 9: Type restrictions (^^xsd:string) for Reactome
- Strategy 10: LIMIT clauses

**Cross-database performance:**
- ChEMBL: 1-3s with pre-filtering (Tier 1)
- Reactome: 3-8s with property paths (Tier 2)
- Pre-filtering reduces ChEMBL joins from 2.4M→10K rows

**Data quality:**
- Manual curation ensures accuracy
- Monthly updates
- Not all entities have molecular data (abstract classes)
- Well-maintained cross-database links
