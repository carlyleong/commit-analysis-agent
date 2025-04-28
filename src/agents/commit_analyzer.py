"""
Commit Analysis Agent implementing advanced workflow patterns.
"""

from datetime import datetime
import subprocess
import json
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from .base_agent import AgentWorkflow, CommitAnalysis
from .advanced_analyzer import AdvancedCommitAnalyzer
from .enhanced_report_generator import EnhancedReportGenerator


class CommitAnalyzerAgent(AgentWorkflow):
    """
    Agent specialized in analyzing code commits with multi-step LLM workflow.
    """
    
    def __init__(self, repo_path: str, model_name: str = "claude-3-opus-20240229"):
        super().__init__(model_name)
        self.repo_path = Path(repo_path)
        self.advanced_analyzer = AdvancedCommitAnalyzer()
        self.report_generator = EnhancedReportGenerator()
    
    def process(self, timeframe: str = "week") -> Dict[str, Any]:
        """
        Process commits within specified timeframe.
        
        Args:
            timeframe: 'week', 'month', or specific date range
        
        Returns:
            Comprehensive analysis report
        """
        # Step 1: Fetch commits
        commits = self._fetch_commits(timeframe)
        
        if not commits:
            return {
                'timeframe': timeframe,
                'commits_analyzed': 0,
                'report': "No commits found in the specified timeframe.",
                'detailed_analysis': []
            }
        
        # Step 2: Parse and analyze each commit
        analyzed_commits = []
        for commit in commits:
            analysis = self._analyze_commit(commit)
            analyzed_commits.append(analysis)
        
        # Step 3: Generate non-technical summaries
        non_technical_summaries = []
        for analysis in analyzed_commits:
            non_tech_summary = self.advanced_analyzer.generate_non_technical_summary(analysis)
            non_technical_summaries.append(non_tech_summary)
        
        # Step 4: Generate comprehensive reports
        dashboard_summary = self.report_generator.generate_dashboard_summary(non_technical_summaries)
        executive_summary = self.report_generator.generate_executive_summary(dashboard_summary, non_technical_summaries)
        timeline_report = self.report_generator.generate_commit_timeline(non_technical_summaries)
        technical_report = self.report_generator.generate_technical_deep_dive(non_technical_summaries)
        
        # Combine all reports
        full_report = f"{executive_summary}\n\n{timeline_report}\n\n{technical_report}"
        
        # Step 5: Optimize report using evaluator-optimizer pattern
        criteria = {
            'clarity': 'Is the report clear and well-structured?',
            'completeness': 'Does the report cover all important aspects?',
            'insights': 'Does the report provide valuable insights?',
            'actionability': 'Are the recommendations actionable?',
            'non_technical': 'Is the report understandable for non-technical users?'
        }
        
        final_report = self.evaluator_optimizer_flow(full_report, criteria)
        
        return {
            'timeframe': timeframe,
            'commits_analyzed': len(analyzed_commits),
            'report': final_report,
            'detailed_analysis': analyzed_commits,
            'dashboard_summary': dashboard_summary,
            'non_technical_summaries': non_technical_summaries
        }
    
    def _fetch_commits(self, timeframe: str) -> List[Dict[str, Any]]:
        """Fetch commits from git repository."""
        try:
            if timeframe == "week":
                since_date = "1 week ago"
            elif timeframe == "month":
                since_date = "1 month ago"
            else:
                since_date = timeframe
            
            cmd = f"git -C {self.repo_path} log --since='{since_date}' --format='%H|||%an|||%ad|||%s'"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            
            # Check if output is empty
            if not output:
                return []
            
            commits = []
            for line in output.split('\n'):
                if line:
                    parts = line.split('|||')
                    if len(parts) >= 4:  # Ensure we have all expected parts
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1],
                            'date': parts[2],
                            'message': parts[3]
                        })
            
            return commits
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e}")
            return []
        except Exception as e:
            print(f"Error fetching commits: {e}")
            return []
    
    def _analyze_commit(self, commit: Dict[str, Any]) -> CommitAnalysis:
        """Analyze a single commit."""
        try:
            cmd = f"git -C {self.repo_path} show --stat {commit['hash']}"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            
            # Parse file changes and stats
            files_changed = []
            insertions = 0
            deletions = 0
            
            lines = output.strip().split('\n')
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # File changes line pattern
                if '|' in line and (' +' in line or ' -' in line):
                    try:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            file_path = parts[0].strip()
                            files_changed.append(file_path)
                            
                            # Extract insertions/deletions
                            stats = parts[1].strip()
                            plus_count = stats.count('+')
                            minus_count = stats.count('-')
                            insertions += plus_count
                            deletions += minus_count
                    except Exception as e:
                        print(f"Error parsing line: {line}, error: {e}")
                        continue
            
            # Sometimes git show doesn't have file stats, try a different format
            if not files_changed:
                try:
                    cmd = f"git -C {self.repo_path} diff-tree --no-commit-id --name-only -r {commit['hash']}"
                    diff_output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
                    files_changed = [f.strip() for f in diff_output.strip().split('\n') if f.strip()]
                except:
                    files_changed = ['unknown']
            
            # Use LLM patterns for advanced analysis
            classification = self.classify_and_route(commit)
            
            # Generate summary and analysis
            summary = self._generate_commit_summary(commit, files_changed, output)
            impact_score = self._calculate_impact_score(insertions, deletions, len(files_changed))
            risk_assessment = self._assess_risk(commit, files_changed)
            
            return CommitAnalysis(
                commit_hash=commit['hash'],
                author=commit['author'],
                date=self._parse_date(commit['date']),
                message=commit['message'],
                files_changed=files_changed,
                insertions=insertions,
                deletions=deletions,
                summary=summary,
                category=classification,
                impact_score=impact_score,
                risk_assessment=risk_assessment
            )
        except subprocess.CalledProcessError:
            return CommitAnalysis(
                commit_hash=commit['hash'],
                author=commit['author'],
                date=datetime.now(),
                message=commit['message'],
                files_changed=[],
                insertions=0,
                deletions=0,
                summary="Unable to analyze commit",
                category="unknown",
                impact_score=0.0,
                risk_assessment="unknown"
            )
    
    def _generate_commit_summary(self, commit: Dict[str, Any], files_changed: List[str], raw_output: str) -> str:
        """Generate a natural language summary of the commit."""
        # In real implementation, this would use an LLM
        if not files_changed or files_changed == ['unknown']:
            return f"Commit with message: {commit.get('message', 'No message')}"
        
        file_types = self._classify_file_types(files_changed)
        dominant_type = max(file_types, key=file_types.get) if file_types else "general"
        
        return f"This commit modifies {len(files_changed)} files, primarily affecting {dominant_type} components. The changes appear to {commit.get('message', 'perform unspecified modifications').lower()}."
    
    def _classify_file_types(self, files: List[str]) -> Dict[str, int]:
        """Classify files by type."""
        types = {}
        for file in files:
            ext = file.split('.')[-1] if '.' in file else 'other'
            types[ext] = types.get(ext, 0) + 1
        return types
    
    def _calculate_impact_score(self, insertions: int, deletions: int, files_changed: int) -> float:
        """Calculate impact score based on change metrics."""
        # Simple heuristic for impact
        total_changes = insertions + deletions
        if total_changes == 0:
            return 0.0
        
        # Normalize score between 0 and 1
        base_score = (total_changes + files_changed * 10) / 1000
        return min(1.0, base_score)
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string with fallback."""
        try:
            # Try standard git date format
            return datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
        except ValueError:
            try:
                # Try alternative formats
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # If all parsing fails, return current date
                return datetime.now()
    
    def _assess_risk(self, commit: Dict[str, Any], files_changed: List[str]) -> str:
        """Assess risk level of the commit."""
        # Mock risk assessment - would use LLM in real implementation
        risky_patterns = ['config', 'security', 'auth', 'database', 'schema']
        
        risk_level = "low"
        for file in files_changed:
            for pattern in risky_patterns:
                if pattern in file.lower():
                    risk_level = "high"
                    break
        
        return risk_level
    
    def _generate_report(self, analyzed_commits: List[CommitAnalysis]) -> str:
        """Generate a comprehensive report from analyzed commits."""
        total_commits = len(analyzed_commits)
        total_insertions = sum(c.insertions for c in analyzed_commits)
        total_deletions = sum(c.deletions for c in analyzed_commits)
        
        # Group by category
        categories = {}
        for commit in analyzed_commits:
            if commit.category not in categories:
                categories[commit.category] = []
            categories[commit.category].append(commit)
        
        # Find high impact commits
        high_impact = [c for c in analyzed_commits if c.impact_score > 0.7]
        high_risk = [c for c in analyzed_commits if c.risk_assessment == "high"]
        
        report = f"""
# Code Commit Analysis Report

## Summary
- Total commits analyzed: {total_commits}
- Lines added: {total_insertions}
- Lines removed: {total_deletions}
- Net change: {total_insertions - total_deletions}

## Activity by Category
"""
        
        for category, commits in categories.items():
            report += f"- {category}: {len(commits)} commits\n"
        
        report += f"""
## High Impact Changes
Found {len(high_impact)} high-impact commits:
"""
        
        for commit in high_impact[:5]:  # Top 5
            report += f"- {commit.commit_hash[:8]}: {commit.summary}\n"
        
        report += f"""
## Risk Assessment
Identified {len(high_risk)} high-risk commits:
"""
        
        for commit in high_risk:
            report += f"- {commit.commit_hash[:8]}: {commit.message} (Files: {', '.join(commit.files_changed[:3])})\n"
        
        report += """
## Recommendations
1. Review high-risk commits for potential security implications
2. Consider code review for high-impact changes
3. Update documentation for significant changes
4. Run comprehensive tests on affected areas
"""
        
        return report
    
    def _handle_code_change(self, input_data: Any) -> str:
        """Handle code change commits."""
        return "code_change"
    
    def _handle_documentation(self, input_data: Any) -> str:
        """Handle documentation commits."""
        return "documentation"
    
    def _handle_configuration(self, input_data: Any) -> str:
        """Handle configuration commits."""
        return "configuration"
    
    def _handle_general(self, input_data: Any) -> str:
        """Handle general commits."""
        return "general"
