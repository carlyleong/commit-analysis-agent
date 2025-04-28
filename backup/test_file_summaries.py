"""
Test file summary functionality.
"""

import json
from agents.advanced_analyzer import AdvancedCommitAnalyzer
from agents.base_agent import CommitAnalysis
from datetime import datetime

# Create a test analyzer
analyzer = AdvancedCommitAnalyzer()

# Create a test commit
test_commit = CommitAnalysis(
    commit_hash="abc123def456",
    author="Test User",
    date=datetime.now(),
    message="Add new feature",
    files_changed=["src/index.js", "styles/main.css", "config/database.yml"],
    insertions=30,
    deletions=10,
    summary="Test commit summary",
    category="feature",
    impact_score=0.5,
    risk_assessment="low"
)

# Generate explanations
summary = analyzer.generate_non_technical_summary(test_commit)

# Print results
print("Generated Summary:")
print(json.dumps(summary, indent=2, default=str))
