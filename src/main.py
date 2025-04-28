"""
Main application orchestrating the commit analysis workflow.
"""
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional  # Add this line
from agents.commit_analyzer import CommitAnalyzerAgent
from storage.document_store import DocumentStore


class CommitAnalysisApp:
    """
    Main application class that orchestrates the entire workflow.
    """
    
    def __init__(self, repo_path: str, storage_path: str = "./data"):
        self.repo_path = Path(repo_path)
        self.storage = DocumentStore(storage_path)
        self.analyzer = CommitAnalyzerAgent(repo_path)
    
    def run_analysis(self, timeframe: str = "week") -> Dict[str, Any]:
        """
        Run complete analysis workflow.
        """
        print(f"Starting commit analysis for timeframe: {timeframe}")
        
        # Step 1: Run analysis
        analysis_result = self.analyzer.process(timeframe)
        
        # Step 2: Store results
        report_id = self.storage.store_analysis_report(analysis_result)
        
        # Store individual commit analyses
        for commit_analysis in analysis_result['detailed_analysis']:
            self.storage.store_commit_analysis(commit_analysis)
        
        print(f"Analysis complete. Report ID: {report_id}")
        
        return {
            'report_id': report_id,
            'summary': analysis_result['report'],
            'commit_count': analysis_result['commits_analyzed']
        }
    
    def get_recent_reports(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recently generated reports."""
        return self.storage.get_recent_reports(limit)
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific report."""
        return self.storage.retrieve_report(report_id)


def main():
    parser = argparse.ArgumentParser(description='Commit Analysis Agent')
    parser.add_argument('repo_path', help='Path to the git repository')
    parser.add_argument('--timeframe', default='week', 
                        help='Analysis timeframe (week, month, or specific date range)')
    parser.add_argument('--storage', default='./data',
                        help='Path to store analysis results')
    
    args = parser.parse_args()
    
    app = CommitAnalysisApp(args.repo_path, args.storage)
    result = app.run_analysis(args.timeframe)
    
    print("\n=== Analysis Summary ===")
    print(result['summary'])
    print(f"\nDetailed report saved with ID: {result['report_id']}")


if __name__ == "__main__":
    main()
