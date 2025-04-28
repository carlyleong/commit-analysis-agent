"""
Enhanced report generator that creates comprehensive, non-technical reports.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict


class EnhancedReportGenerator:
    """
    Generates beautiful, comprehensive reports that non-technical users can understand.
    """
    
    def generate_dashboard_summary(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate dashboard summary with key metrics."""
        if not commits:
            return {
                'total_commits': 0,
                'time_span_days': 0,
                'active_contributors': 0,
                'most_active_contributor': 'None',
                'commit_categories': {},
                'impact_distribution': {'high': 0, 'medium': 0, 'low': 0},
                'high_risk_commits': 0,
                'visual_changes_count': 0,
                'activity_timeline': []
            }
        
        total_commits = len(commits)
        
        # Author statistics
        authors = defaultdict(int)
        for commit in commits:
            authors[commit['author']] += 1
        
        # Time analysis
        dates = []
        for commit in commits:
            try:
                date_str = commit['date']
                # Handle different date formats
                if ' at ' in date_str:
                    date_obj = datetime.strptime(date_str, "%B %d, %Y at %I:%M %p")
                else:
                    date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
                dates.append(date_obj)
            except ValueError:
                # If date parsing fails, use current date
                dates.append(datetime.now())
        
        if dates:
            earliest_date = min(dates)
            latest_date = max(dates)
            time_span = (latest_date - earliest_date).days + 1  # Include both start and end days
        else:
            time_span = 0
        
        # Category analysis
        categories = defaultdict(int)
        for commit in commits:
            categories[commit['category']] += 1
        
        # Impact analysis
        high_impact = sum(1 for commit in commits if 'High impact' in commit.get('impact_score', ''))
        medium_impact = sum(1 for commit in commits if 'Medium impact' in commit.get('impact_score', ''))
        low_impact = sum(1 for commit in commits if 'Low impact' in commit.get('impact_score', ''))
        
        # Risk analysis
        high_risk = sum(1 for commit in commits if 'High risk' in commit.get('risk_level', ''))
        
        return {
            'total_commits': total_commits,
            'time_span_days': time_span,
            'active_contributors': len(authors),
            'most_active_contributor': max(authors.items(), key=lambda x: x[1])[0] if authors else 'None',
            'commit_categories': dict(categories),
            'impact_distribution': {
                'high': high_impact,
                'medium': medium_impact,
                'low': low_impact
            },
            'high_risk_commits': high_risk,
            'visual_changes_count': sum(1 for commit in commits if commit.get('visual_changes', False)),
            'activity_timeline': self._generate_activity_timeline(commits)
        }
    
    def generate_executive_summary(self, summary: Dict[str, Any], commits: List[Dict[str, Any]]) -> str:
        """Generate an executive summary for non-technical stakeholders."""
        report = "# Development Activity Executive Summary\n\n"
        
        # Overview
        report += "## Overview\n"
        report += f"During this period, the development team made {summary['total_commits']} updates to the application "
        report += f"over {summary['time_span_days']} days. "
        report += f"These changes involved {summary['active_contributors']} team member{'s' if summary['active_contributors'] != 1 else ''}.\n\n"
        
        # Key Metrics
        report += "## Key Metrics\n"
        report += f"- **Most Active Contributor**: {summary['most_active_contributor']}\n"
        report += f"- **High Impact Changes**: {summary['impact_distribution']['high']}\n"
        report += f"- **Features Added**: {summary['commit_categories'].get('feature', 0)}\n"
        report += f"- **Bugs Fixed**: {summary['commit_categories'].get('bugfix', 0)}\n"
        report += f"- **Visual Updates**: {summary['visual_changes_count']}\n\n"
        
        # Risk Assessment
        if summary['high_risk_commits'] > 0:
            report += "## Risk Areas\n"
            report += f"There were {summary['high_risk_commits']} high-risk changes that require careful attention. "
            report += "These updates affect critical components of the application and should be thoroughly tested.\n\n"
        
        # Activity Breakdown
        report += "## Activity Breakdown\n"
        categories = summary['commit_categories']
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / summary['total_commits']) * 100
            report += f"- **{category.title()}**: {count} updates ({percentage:.1f}%)\n"
        
        return report
    
    def generate_commit_timeline(self, commits: List[Dict[str, Any]]) -> str:
        """Generate a timeline view of commits."""
        if not commits:
            return "# Development Timeline\n\nNo commits available for the selected timeframe."
        
        timeline = "# Development Timeline\n\n"
        
        # Group commits by date
        commits_by_date = defaultdict(list)
        for commit in commits:
            try:
                date_str = commit['date']
                if ' at ' in date_str:
                    date_obj = datetime.strptime(date_str, "%B %d, %Y at %I:%M %p")
                else:
                    date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
                date_key = date_obj.strftime("%B %d, %Y")
            except (ValueError, AttributeError):
                date_key = datetime.now().strftime("%B %d, %Y")
            
            commits_by_date[date_key].append(commit)
        
        # Sort dates properly
        date_keys = sorted(commits_by_date.keys(), 
                          key=lambda x: datetime.strptime(x, "%B %d, %Y"), 
                          reverse=True)
        
        # Generate timeline
        for date in date_keys:
            timeline += f"## {date}\n\n"
            
            for commit in commits_by_date[date]:
                # Commit header
                timeline += f"### {commit['author']} - {commit['message']}\n"
                timeline += f"- **Type**: {commit['category'].title()} - {commit.get('category_explanation', 'General change')}\n"
                timeline += f"- **Impact**: {commit.get('impact_score', 'Unknown')}\n"
                timeline += f"- **Risk**: {commit.get('risk_level', 'Unknown')}\n\n"
                
                # Files changed explanation
                if commit.get('file_explanations'):
                    timeline += "**Changes Made:**\n"
                    for file_exp in commit['file_explanations']:
                        if isinstance(file_exp, dict):
                            file_path = file_exp.get('file_path', 'unknown')
                            code_summary = file_exp.get('code_summary', '')
                            if not code_summary:
                                code_summary = file_exp.get('non_technical_summary', 'No summary available')
                        else:
                            file_path = getattr(file_exp, 'file_path', 'unknown')
                            code_summary = getattr(file_exp, 'code_summary', '')
                            if not code_summary:
                                code_summary = getattr(file_exp, 'non_technical_summary', 'No summary available')
                        timeline += f"- `{file_path}`: {code_summary}\n"
                    timeline += "\n"
                
                # Overall impact
                timeline += f"**Overall Impact:** {commit.get('overall_impact', 'No impact information available')}\n\n"
                timeline += "---\n\n"
        
        return timeline
    
    def generate_technical_deep_dive(self, commits: List[Dict[str, Any]]) -> str:
        """Generate a technical deep dive for developers."""
        deep_dive = "# Technical Deep Dive\n\n"
        
        # File statistics
        all_files = defaultdict(lambda: {'changes': 0, 'commits': 0})
        for commit in commits:
            for file_exp in commit.get('file_explanations', []):
                # Handle both dict and object formats
                if isinstance(file_exp, dict):
                    file_path = file_exp.get('file_path', 'unknown')
                else:
                    file_path = getattr(file_exp, 'file_path', 'unknown')
                    
                all_files[file_path]['changes'] += 1
                all_files[file_path]['commits'] += 1
        
        # Most changed files
        deep_dive += "## Most Changed Files\n"
        for file_path, stats in sorted(all_files.items(), 
                                     key=lambda x: x[1]['changes'], 
                                     reverse=True)[:10]:
            deep_dive += f"- `{file_path}`: {stats['changes']} changes across {stats['commits']} commits\n"
        deep_dive += "\n"
        
        # Language breakdown
        language_stats = defaultdict(int)
        for commit in commits:
            for file_exp in commit.get('file_explanations', []):
                if isinstance(file_exp, dict):
                    language = file_exp.get('language', 'Unknown')
                else:
                    language = getattr(file_exp, 'language', 'Unknown')
                language_stats[language] += 1
        
        deep_dive += "## Language Distribution\n"
        for language, count in sorted(language_stats.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True):
            deep_dive += f"- **{language}**: {count} file changes\n"
        deep_dive += "\n"
        
        # High impact commits
        high_impact_commits = [c for c in commits if 'High impact' in c['impact_score']]
        if high_impact_commits:
            deep_dive += "## High Impact Changes\n"
            for commit in high_impact_commits:
                deep_dive += f"### {commit['commit_id']} - {commit['message']}\n"
                deep_dive += f"- **Author**: {commit['author']}\n"
                deep_dive += f"- **Date**: {commit['date']}\n"
                deep_dive += f"- **Files Changed**: {len(commit['file_explanations'])}\n"
                deep_dive += f"- **Impact**: {commit['overall_impact']}\n\n"
        
        return deep_dive
    
    def _generate_activity_timeline(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate activity timeline data for visualization."""
        timeline_data = []
        
        # Group by date
        commits_by_date = defaultdict(lambda: {'count': 0, 'categories': defaultdict(int)})
        for commit in commits:
            try:
                date_str = commit['date']
                if ' at ' in date_str:
                    date_obj = datetime.strptime(date_str, "%B %d, %Y at %I:%M %p")
                else:
                    date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z")
                date_key = date_obj.strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                # Use today's date if parsing fails
                date_key = datetime.now().strftime("%Y-%m-%d")
            
            commits_by_date[date_key]['count'] += 1
            commits_by_date[date_key]['categories'][commit.get('category', 'other')] += 1
        
        # Convert to list format
        for date, data in commits_by_date.items():
            timeline_data.append({
                'date': date,
                'total_commits': data['count'],
                'category_breakdown': dict(data['categories'])
            })
        
        return sorted(timeline_data, key=lambda x: x['date'])
