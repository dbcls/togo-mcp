# Rhea Exploration Report

## Database Overview
Rhea is a comprehensive expert-curated database of biochemical reactions:
- **17,078 master reactions** (unspecified direction)
- **34,156 directional reactions** (left-to-right, right-to-left)
- **17,078 bidirectional reactions** (reversible)
- **11,763 small molecule compounds** (all with ChEBI IDs)
- **254 polymer structures** (with polymerization indices)
- **5,984 transport reactions** (with cellular location annotations)
- All approved reactions are atom-balanced and charge-balanced
- Serves as reference reaction resource for UniProtKB enzyme annotations

## Schema Analysis (from MIE file)

### Main Properties Available
- **Reactions**: Accession (RHEA:XXXXX), equation (text and HTML), status (Approved/Preliminary/Obsolete)
- **Chemical Balance**: isChemicallyBalanced (boolean), all approved reactions are balanced
- **Transport**: isTransport flag, location annotations (In/Out for cellular compartments)
- **Reaction Variants**: Master reaction links to directional (L→R, R→L) and bidirectional forms
- **Reaction Sides**: Left and right sides with participants
- **Stoichiometry**: Encoded in property names (contains1, contains2, contains3, containsN)
- **Compounds**: Small molecules with formula, charge, name, HTML name, ChEBI cross-reference
- **Polymers**: Polymerization index (n, n-1), formula with index notation, underlying ChEBI
- **EC Numbers**: Enzyme Commission classification via http://purl.uniprot.org/enzyme/
- **Cross-References**: GO (molecular function), KEGG, MetaCyc, Reactome, MACiE

### Important Relationships
- `rhea:directionalReaction` - Links master to L→R and R→L forms
- `rhea:bidirectionalReaction` - Links master to reversible form
- `rhea:side` - Links reaction to left/right sides
- `rhea:contains` - Links side to all participants
- `rhea:contains1/2/3/N` - Stoichiometry-specific participant links
- `rhea:compound` - Links participant to compound entity
- `rhea:location` - For transport reactions (rhea:In or rhea:Out)
- `rhea:chebi` - Links compound to ChEBI ontology
- `rhea:ec` - Links reaction to EC enzyme classification
- `rdfs:seeAlso` - Cross-references to GO, KEGG, MetaCyc, etc.
- `rhea:transformableTo` - Links left side to right side (reaction direction)

### Query Patterns Observed
- **Keyword search**: MUST use `bif:contains` on equation or labels (not FILTER)
- **Boolean operators**: Supports AND, OR, NOT in bif:contains
- **Reaction quartet**: Each ID has 4 forms (e.g., 10000 master, 10001 L→R, 10002 R→L, 10003 bidirectional)
- **Status filter**: Always filter by `rhea:status rhea:Approved` for production queries
- **Transport queries**: Filter by `rhea:isTransport 1` and check participant locations
- **Stoichiometry**: Use containsN properties for compounds appearing multiple times

## Search Queries Performed

1. **Query: "ATP"** → Results: 10 ATP-involving reactions including ion pumps (K+, Na+), transport reactions, DNA methylation
2. **Query: "glucose phosphate"** → Results: 10 reactions including glucose-6-phosphate hydrolysis, phosphotransfer, complex glycosylation
3. **Query: "transport"** (keyword search)** → Results: Got mixed results, better to use isTransport flag
4. **Transport reactions (SPARQL)** → Results: 10 transport reactions including ATP-dependent ion pumps, metabolite transporters
5. **ATP + ADP reactions with EC** → Results: 10 kinase reactions with EC numbers (2.7.x.x phosphotransferases)

## SPARQL Queries Tested

```sparql
# Query 1: Find transport reactions
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT ?reaction ?equation ?accession
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:equation ?equation ;
            rhea:accession ?accession ;
            rhea:isTransport 1 ;
            rhea:status rhea:Approved .
}
LIMIT 10
# Results: Retrieved ATP-dependent Zn2+ pump, guanine transporter, H+ pump, 
# Na+ transporter, glycerol-3-phosphate transporter, molybdate transporter, K+ pump, etc.
```

```sparql
# Query 2: Search reactions with ATP and ADP, get EC numbers
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT ?reaction ?equation ?ec
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:equation ?equation ;
            rhea:ec ?ec ;
            rhea:status rhea:Approved .
  ?equation bif:contains "'ATP' AND 'ADP'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Kinase reactions (EC 2.7.x.x) - xylitol kinase, viomycin kinase, 
# erythritol kinase, GMP kinase, adenosine kinase, etc.
```

```sparql
# Query 3: Find reactions with GO molecular function annotations
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT ?reaction ?accession ?equation ?goTerm
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:accession ?accession ;
            rhea:equation ?equation ;
            rdfs:seeAlso ?goTerm .
  FILTER(STRSTARTS(STR(?goTerm), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 10
# Results: Reactions with specific GO molecular function terms like retinyl-palmitate esterase,
# flavonol 3-O-xylosyltransferase, long-chain-fatty-acyl-CoA biosynthesis, etc.
```

```sparql
# Query 4: Get compound details for ATP
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT ?compound ?name ?formula ?charge ?chebi
WHERE {
  ?compound rdfs:subClassOf rhea:SmallMolecule ;
            rhea:name ?name ;
            rhea:formula ?formula ;
            rhea:charge ?charge ;
            rhea:chebi ?chebi .
  FILTER(?name = "ATP")
}
# Results: ATP - formula C10H12N5O13P3, charge -4, ChEBI:30616
```

## Interesting Findings

### Specific Entities for Questions
- **RHEA:10000**: Pentanamide hydrolysis - well-documented example reaction
- **ATP reactions**: Hundreds involving ATP (ion pumps, kinases, transporters)
- **Transport reactions**: 5,984 total with cellular location annotations
- **Reaction quartets**: Each reaction has 4 IDs (master + 2 directional + bidirectional)
- **ATP compound**: Rhea ID 6372, formula C10H12N5O13P3, charge -4, CHEBI:30616

### Unique Properties
- **Reaction directionality**: Systematic representation of all directions
- **Atom-balanced**: All approved reactions chemically validated
- **Location annotations**: Transport reactions specify In/Out compartments
- **Polymer notation**: Specialized (n), (n-1) notation in formulas
- **Stoichiometry encoding**: Property names (contains1, contains2, etc.)
- **EC classification**: ~45% reactions have enzyme commission numbers
- **Status tracking**: Approved (66,740), Preliminary (452), Obsolete (1,120)

### Connections to Other Databases
- **ChEBI**: 100% small molecules have ChEBI IDs
- **GO**: ~55% reactions have molecular function annotations
- **KEGG Reaction**: ~35% metabolic pathway coverage
- **MetaCyc/BioCyc**: Comprehensive metabolic pathway links
- **Reactome**: Selected pathway links
- **UniProt EC**: Enzyme classification links
- **MACiE**: Enzyme mechanism annotations

### Specific Verifiable Facts
- **17,078 master reactions** total
- **5,984 transport reactions** (35% of total)
- **11,763 small molecules** with ChEBI links
- **254 polymer structures**
- **ATP formula**: C10H12N5O13P3
- **ATP charge**: -4
- **ATP ChEBI ID**: CHEBI:30616
- **Reaction RHEA:22044**: K+ pump (K+ out + ATP → K+ in + ADP)

## Question Opportunities by Category

### Precision
- "What is the molecular formula of ATP in Rhea?" → C10H12N5O13P3
- "What is the charge on ATP?" → -4
- "What is the ChEBI ID for ATP in Rhea?" → CHEBI:30616
- "What is the equation for reaction RHEA:10000?" → Specific pentanamide hydrolysis
- "What EC number is associated with RHEA:20780?" → EC 2.7.4.8 (GMP kinase)

### Completeness
- "How many reactions are in Rhea?" → 17,078 master reactions
- "How many transport reactions exist?" → 5,984
- "How many reactions involve ATP?" → Large count from search
- "How many reactions have EC numbers?" → ~45% (based on coverage)
- "How many reactions have GO annotations?" → ~55%

### Integration
- "What is the ChEBI ID for ATP as used in Rhea?" → CHEBI:30616
- "Find GO terms associated with reaction RHEA:19697" → GO:0047520
- "What KEGG reactions correspond to Rhea reactions?" → Via rdfs:seeAlso
- "Link Rhea reactions to UniProt EC numbers" → Via rhea:ec property
- "Convert Rhea reaction to MetaCyc identifiers" → Cross-reference query

### Currency
- "How many reactions are in approved status?" → 66,740
- "How many reactions are preliminary?" → 452 (recently added)
- "What reactions were recently added?" → Filter by status
- "Are there new transport reactions?" → Query recent updates

### Specificity
- "What is the stoichiometry of ATP in reaction RHEA:22044?" → 1 (from contains1)
- "Find reactions with polymerization index n-1" → Polymer queries
- "What cellular location does Zn2+ go to in RHEA:20621?" → Out
- "Find reactions with charge-balanced equations" → All approved reactions
- "What is the polymerization index of polymer 10035?" → n-1

### Structured Query
- "Find approved transport reactions involving ATP and ADP" → Multiple filters
- "List kinase reactions (EC 2.7.x.x) with stoichiometry > 1 for ATP" → Complex
- "Find reactions with GO annotations AND EC numbers" → Cross-references
- "Search for reactions with glucose AND phosphate but NOT transport" → Boolean
- "Find bidirectional reactions involving NADH/NAD+" → Direction + participants

## Notes

### Limitations
- **Reaction quartet complexity**: Same reaction represented 4 ways (can be confusing)
- **Stoichiometry encoding**: Property names (contains1, contains2) not standard
- **Polymer notation**: Specialized (n), (n-1) requires parsing
- **Literature citations**: In rdfs:comment field, requires text parsing
- **Not all reactions have EC numbers**: Only ~45% coverage
- **Transport location**: Only for transport reactions, not general localization

### Best Practices
1. **ALWAYS use bif:contains** for text searches in equations/labels
2. **Filter by rhea:status rhea:Approved** for production queries
3. **Use LIMIT clauses** to prevent timeouts on exploratory queries
4. **Start from master reactions** and navigate to directional forms if needed
5. **For transport**: Check both isTransport flag and location properties
6. **Boolean operators**: Use 'ATP' AND 'ADP' in bif:contains for complex searches
7. **ORDER BY DESC(?sc)** after bif:contains for relevance ranking
8. **Cross-references**: Use STRSTARTS to filter by database namespace

### Performance Notes
- Simple reaction lookups by accession: <1 second
- Keyword searches with bif:contains: <1 second for 20 results
- Complex joins (reaction-side-participant-compound): 2-5 seconds with LIMIT
- Full graph traversals may timeout without LIMIT
- Boolean operators in bif:contains are very efficient
- Status and transport filters are well-indexed
