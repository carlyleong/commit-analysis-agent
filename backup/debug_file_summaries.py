"""
Debug script to check file summary generation.
"""

import json
from agents.commit_analyzer import CommitAnalyzerAgent
from agents.advanced_analyzer import AdvancedCommitAnalyzer
import sys
from datetime import datetime

def debug_file_summaries(repo_path):
    print(f"Debugging file summaries for repository: {repo_path}")
    
    # Initialize analyzers
    commit_analyzer = CommitAnalyzerAgent(repo_path)
    advanced_analyzer = AdvancedCommitAnalyzer()
    
    # Get commits
    commits = commit_analyzer._fetch_commits("week")
    print(f"\nFound {len(commits)} commits")
    
    if not commits:
        print("No commits found")
        return
    
    # Analyze first commit
    commit = commits[0]
    print(f"\nAnalyzing commit: {commit['hash'][:8]} - {commit['message']}")
    
    # Basic analysis
    analyzed = commit_analyzer._analyze_commit(commit)
    print(f"\nFiles changed: {analyzed.files_changed}")
    
    # Advanced analysis
    non_tech_summary = advanced_analyzer.generate_non_technical_summary(analyzed)
    
    print("\nNon-technical summary structure:")
    print(json.dumps({
        'commit_id': non_tech_summary.get('commit_id'),
        'author': non_tech_summary.get('author'),
        'file_explanations_count': len(non_tech_summary.get('file_explanations', [])),
        'files_by_type_keys': list(non_tech_summary.get('files_by_type', {}).keys())
    }, indent=2))
    
    # Check file explanations
    print("\nFile explanations:")
    for i, exp in enumerate(non_tech_summary.get('file_explanations', [])):
        print(f"\nFile {i + 1}:")
        if isinstance(exp, dict):
            print(f"  Type: Dict")
            print(f"  Keys: {list(exp.keys())}")
            print(f"  Path: {exp.get('file_path')}")
            print(f"  Code Summary: {exp.get('code_summary')}")
            print(f"  Non-tech Summary: {exp.get('non_technical_summary')}")
        else:
            print(f"  Type: {type(exp)}")
            if hasattr(exp, '__dict__'):
                print(f"  Attributes: {exp.__dict__}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/Users/carlyleong/Desktop/test-repo"
    
    debug_file_summaries(repo_path)
