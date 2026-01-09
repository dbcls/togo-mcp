#!/usr/bin/env python3
"""
Verification script for TogoMCP evaluation questions
"""
import json
import os
from collections import Counter

def verify_questions():
    base_path = "/Users/arkinjo/work/GitHub/togo-mcp/evaluation/questions"
    files = [f"Q{i:02d}.json" for i in range(1, 11)]
    
    total_questions = 0
    all_categories = []
    all_ids = []
    databases_mentioned = set()
    
    print("=" * 70)
    print("TOGOMCP EVALUATION QUESTIONS VERIFICATION")
    print("=" * 70)
    
    for filename in files:
        filepath = os.path.join(base_path, filename)
        
        try:
            with open(filepath, 'r') as f:
                questions = json.load(f)
        except FileNotFoundError:
            print(f"\n❌ ERROR: {filename} not found!")
            continue
        except json.JSONDecodeError as e:
            print(f"\n❌ ERROR: {filename} has invalid JSON: {e}")
            continue
        
        print(f"\n{filename}:")
        print(f"  ✓ Questions: {len(questions)}")
        
        # Verify it's an array
        if not isinstance(questions, list):
            print(f"  ❌ ERROR: Root element is not an array!")
            continue
        
        # Check each question has required fields
        for i, q in enumerate(questions, 1):
            missing = []
            if 'question' not in q:
                missing.append('question')
            if 'id' not in q:
                missing.append('id')
            if 'category' not in q:
                missing.append('category')
            if 'expected_answer' not in q:
                missing.append('expected_answer')
            if 'notes' not in q:
                missing.append('notes')
            
            if missing:
                print(f"  ❌ Question {i} missing fields: {missing}")
        
        # Check categories
        cats = Counter(q['category'] for q in questions)
        print(f"  ✓ Categories: {dict(cats)}")
        
        # Verify each category appears exactly 2 times
        for cat, count in cats.items():
            if count != 2:
                print(f"  ⚠️  WARNING: {cat} appears {count} times (should be 2)")
        
        # Check IDs
        ids = [q['id'] for q in questions]
        print(f"  ✓ ID range: {min(ids)}-{max(ids)}")
        
        total_questions += len(questions)
        all_categories.extend(q['category'] for q in questions)
        all_ids.extend(ids)
        
        # Extract database mentions from notes
        for q in questions:
            notes = q.get('notes', '')
            if 'Database:' in notes:
                db_part = notes.split('Database:')[1].split('.')[0]
                dbs = [db.strip() for db in db_part.split(',')]
                databases_mentioned.update(dbs)
    
    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"\n✓ Total Questions: {total_questions}")
    
    if total_questions == 120:
        print(f"  ✓ PASS: Exactly 120 questions")
    else:
        print(f"  ❌ FAIL: Expected 120, got {total_questions}")
    
    print(f"\nCategory Distribution:")
    cat_counts = Counter(all_categories)
    valid_categories = {"Precision", "Completeness", "Integration", "Currency", "Specificity", "Structured Query"}
    
    for cat, count in sorted(cat_counts.items()):
        status = "✓" if count == 20 else "❌"
        valid = "✓" if cat in valid_categories else "❌"
        print(f"  {status} {cat}: {count} (valid: {valid})")
    
    print(f"\nID Verification:")
    print(f"  IDs used: {min(all_ids)} to {max(all_ids)}")
    print(f"  Unique IDs: {len(set(all_ids))}")
    
    if len(all_ids) == len(set(all_ids)):
        print(f"  ✓ PASS: No duplicate IDs")
    else:
        print(f"  ❌ FAIL: {len(all_ids) - len(set(all_ids))} duplicate IDs found")
        dupes = [id for id in all_ids if all_ids.count(id) > 1]
        print(f"  Duplicates: {set(dupes)}")
    
    if set(all_ids) == set(range(1, 121)):
        print(f"  ✓ PASS: All IDs 1-120 present")
    else:
        missing = set(range(1, 121)) - set(all_ids)
        if missing:
            print(f"  ❌ FAIL: Missing IDs: {sorted(missing)}")
    
    print(f"\nDatabases Mentioned ({len(databases_mentioned)}):")
    for db in sorted(databases_mentioned):
        print(f"  • {db}")
    
    print(f"\n{'=' * 70}")
    print("VERIFICATION COMPLETE")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    verify_questions()
