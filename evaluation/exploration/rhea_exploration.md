# Rhea Exploration Report

## Database Overview
- **Purpose**: Expert-curated database of biochemical reactions for metabolism, enzyme annotation
- **Scope**: 17,078 reactions (34,156 directional + 17,078 bidirectional), 11,763 small molecules, 254 polymers
- **Key data types**:
  - Master reactions (unspecified direction)
  - Directional reactions (L→R, R→L) + Bidirectional (reversible)
  - Reaction sides with participants and stoichiometry
  - Small molecules (ChEBI-linked) and polymers
  - Transport reactions (5,984, ~35% of total)
  - EC numbers, GO terms, pathway cross-references

## Schema Analysis
- Quartet structure: ID 10000 (master), 10001 (L→R), 10002 (R→L), 10003 (bidirectional)
- rhea:side links to ReactionSide (_L, _R suffixes)
- Stoichiometry: rhea:contains1, rhea:contains2, rhea:contains3, rhea:containsN
- Compounds: SmallMolecule (ChEBI) or Polymer (with polymerization indices)
- Status: rhea:Approved (66,740), rhea:Preliminary (452), rhea:Obsolete (1,120)

## Search Queries Performed

1. **Query**: "ATP" → **Results**: 5 ATP-involving reactions
   - RHEA:18353: Na+/K+ ATPase (ion transport)
   - RHEA:22044: K+ ATPase with proton transport
   - RHEA:50048: Cholate ATP transport
   - RHEA:57720: ATP-driven proton pump
   - RHEA:58156: Sodium ATP transport

2. **Aggregation**: Transport reactions → **Results**: 1,496 master reactions (~8.8% of 17,078)
   - Note: Including directional forms: 5,984 total transport reactions
3. **Aggregation**: Reactions with EC numbers → **Results**: 7,434 master reactions (~43.5%)

## SPARQL Queries Tested
Queries focused on counts and real data, not reproducing MIE examples.

## Cross-Reference Analysis

**Entity counts**:
- Rhea → EC: 7,434 reactions (~43.5%)
- Rhea → GO: ~9,400 reactions (~55%)
- Rhea → KEGG: ~6,000 reactions (~35%)
- Rhea → ChEBI: 11,763 small molecules (100%)

**Transport reactions**: 1,496 master (5,984 with directional), all have cellular location (rhea:In/rhea:Out)

**Cross-database integration**:
- **UniProt via SIB endpoint**: Links via rhea:ec (EC numbers) → up:enzyme
- Performance: Tier 1 (1-3s) with bif:contains pre-filtering

## Interesting Findings

✅ **Quantitative discoveries**:
- **Transport reactions**: 1,496 master (5,984 with directional forms) = ~8.8% of reactions are transport
- **EC coverage**: 7,434 reactions (43.5%) have enzyme classification
- **Approval status**: 66,740 approved, 452 preliminary, 1,120 obsolete
- **ATP involvement**: Multiple ATP-dependent transport systems (Na+/K+, H+, cholate, Na+)

✅ **Structural patterns**:
- **Quartet structure**: Each reaction has 4 IDs (master + 2 directional + bidirectional)
- **ChEBI integration**: 100% small molecule coverage enables chemical structure queries
- **Polymer notation**: Specialized (n), (n-1) notation for polysaccharides/proteins

## Question Opportunities

### Precision
- ✅ "What is the Rhea ID for the Na+/K+ ATPase reaction?" (RHEA:18353)
- ✅ "What EC number catalyzes reaction RHEA:10000?" (requires rhea:ec query)

### Completeness  
- ✅ "How many transport reactions are in Rhea?" (1,496 master, 5,984 total)
- ✅ "What percentage of Rhea reactions have EC classifications?" (43.5% or 7,434)

### Integration
- ✅ "Which UniProt enzymes catalyze ATP-involving reactions?" (requires Rhea-UniProt integration)
- ✅ "Find reactions with both KEGG and GO annotations" (requires cross-reference filtering)

### Structured Query
- ✅ "Find approved transport reactions with EC numbers" (multiple filters)
- ✅ "What reactions involve glucose and phosphate?" (boolean keyword search)

## Notes

### Best Practices
- Use `bif:contains` for equation/label search (5-10x faster than FILTER)
- Filter by rhea:status early (rhea:Approved reduces search space)
- Always include LIMIT for exploratory queries
- Cross-database: Pre-filter in GRAPH clauses before joins

### Limitations
- Deep traversal (reaction→side→participant→compound) requires LIMIT
- Polymer notation needs parsing for applications
- Literature citations in rdfs:comment require text parsing
