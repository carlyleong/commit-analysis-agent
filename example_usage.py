"""
Example usage of the Commit Analysis Agent system.
"""

from src.main import CommitAnalysisApp
import json
from datetime import datetime

def run_example():
    """Run an example analysis workflow."""
    
    # Initialize the application
    repo_path = "/path/to/your/repo"  # Replace with actual repo path
    app = CommitAnalysisApp(repo_path)
    
    # Run analysis for the last week
    print("Running commit analysis for the last week...")
    result = app.run_analysis("week")
    
    # Display summary
    print("\n=== Analysis Summary ===")
    print(result['summary'])
    
    # Get recent reports
    print("\n=== Recent Reports ===")
    recent_reports = app.get_recent_reports(5)
    for report in recent_reports:
        print(f"- {report['timeframe']} analysis from {report['created_at']}")
        print(f"  Commits analyzed: {report['commit_count']}")
    
    # Get detailed report
    if recent_reports:
        latest_report_id = recent_reports[0]['metadata']['report_id']
        full_report = app.get_report(latest_report_id)
        
        if full_report:
            print(f"\n=== Full Report ({latest_report_id}) ===")
            print(json.dumps(full_report, indent=2, default=str))
    
    # Demonstrate the evaluator-optimizer workflow
    print("\n=== Optimization History ===")
    if hasattr(app.analyzer, 'optimization_history'):
        for iteration in app.analyzer.optimization_history:
            print(f"Iteration {iteration['iteration']}:")
            print(f"  Score: {iteration['evaluation']['score']}")
            print(f"  Feedback: {iteration['evaluation']['feedback']}")

if __name__ == "__main__":
    run_example()
