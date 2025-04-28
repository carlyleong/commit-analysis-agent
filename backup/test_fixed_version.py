"""
Test script to verify the fixed version works properly.
"""

import json
from src.agents.commit_analyzer import CommitAnalyzerAgent
from src.storage.document_store import DocumentStore
import sys

def test_analyzer(repo_path):
    print(f"Testing analyzer with repo: {repo_path}")
    
    # Create analyzer
    analyzer = CommitAnalyzerAgent(repo_path)
    
    # Process commits
    print("Processing commits...")
    result = analyzer.process("week")
    
    # Print results
    print("\nResult structure:")
    print(f"Commits analyzed: {result['commits_analyzed']}")
    print(f"Non-technical summaries: {len(result.get('non_technical_summaries', []))}")
    
    # Check first commit summary if available
    if result.get('non_technical_summaries'):
        first_summary = result['non_technical_summaries'][0]
        print("\nFirst commit summary:")
        print(f"Message: {first_summary.get('message')}")
        print(f"Author: {first_summary.get('author')}")
        print(f"Files: {len(first_summary.get('file_explanations', []))}")
        
        # Check first file explanation
        if first_summary.get('file_explanations'):
            first_file = first_summary['file_explanations'][0]
            print("\nFirst file explanation:")
            print(f"Path: {first_file.get('file_path')}")
            print(f"Language: {first_file.get('language')}")
            print(f"Code summary: {first_file.get('code_summary')}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/Users/carlyleong/Desktop/test-repo"
    
    test_analyzer(repo_path)
