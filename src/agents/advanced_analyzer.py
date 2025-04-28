"""
Advanced commit analyzer with comprehensive non-technical explanations.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import re
from datetime import datetime
from .base_agent import CommitAnalysis


@dataclass
class CodeExplanation:
    file_path: str
    language: str
    purpose: str
    complexity_level: str
    impact_description: str
    non_technical_summary: str
    changes_explanation: str
    code_summary: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class AdvancedCommitAnalyzer:
    """
    Advanced analyzer that provides comprehensive, non-technical explanations.
    """
    
    def __init__(self):
        self.file_type_explanations = {
            'py': ('Python', 'programming logic and automation'),
            'js': ('JavaScript', 'website interactivity and user experience'),
            'jsx': ('React', 'website user interface components'),
            'ts': ('TypeScript', 'enhanced JavaScript with type safety'),
            'html': ('HTML', 'website structure and content'),
            'css': ('CSS', 'website visual styling and layout'),
            'json': ('JSON', 'data storage and configuration'),
            'md': ('Markdown', 'documentation and readable text'),
            'yml': ('YAML', 'configuration and settings'),
            'yaml': ('YAML', 'configuration and settings'),
            'sh': ('Shell Script', 'automation and system commands'),
            'sql': ('SQL', 'database queries and data management'),
            'java': ('Java', 'application programming'),
            'cpp': ('C++', 'system and performance-critical code'),
            'rb': ('Ruby', 'web application backend'),
            'go': ('Go', 'server and cloud applications'),
            'rs': ('Rust', 'system programming with safety'),
            'php': ('PHP', 'web server programming'),
            'swift': ('Swift', 'iOS and Mac application development'),
            'kt': ('Kotlin', 'Android application development')
        }
        
        self.commit_category_explanations = {
            'feature': 'New functionality added to the application',
            'bugfix': 'Problems or errors fixed',
            'refactor': 'Code improvements without changing functionality',
            'documentation': 'Updates to help text or instructions',
            'performance': 'Changes to make the application faster',
            'security': 'Updates to protect the application',
            'style': 'Visual appearance improvements',
            'test': 'Updates to automated testing',
            'configuration': 'Changes to settings or environment',
            'dependency': 'Updates to external libraries or tools'
        }
        
        self.file_purposes = {
            'index': 'Main entry point or homepage',
            'config': 'Application settings and configuration',
            'auth': 'User authentication and login',
            'database': 'Data storage and retrieval',
            'api': 'Communication with external services',
            'utils': 'Helper functions and utilities',
            'components': 'Reusable UI elements',
            'styles': 'Visual design and layout',
            'tests': 'Automated testing code',
            'docs': 'Documentation and help files',
            'assets': 'Images, fonts, and other resources',
            'migrations': 'Database structure changes',
            'models': 'Data structure definitions',
            'controllers': 'Business logic and flow control',
            'views': 'User interface templates',
            'routes': 'URL path definitions',
            'middleware': 'Request processing functions',
            'services': 'Business logic services',
            'helpers': 'Utility functions',
            'layouts': 'Page structure templates'
        }
    
    def categorize_commit(self, message: str) -> str:
        """Categorize commit based on message patterns."""
        message_lower = message.lower()
        
        # Feature detection
        if any(word in message_lower for word in ['feature', 'add', 'implement', 'create', 'new']):
            return 'feature'
        
        # Bugfix detection
        if any(word in message_lower for word in ['fix', 'bug', 'issue', 'resolve', 'repair', 'patch']):
            return 'bugfix'
        
        # Refactor detection
        if any(word in message_lower for word in ['refactor', 'restructure', 'reorganize', 'cleanup', 'improve']):
            return 'refactor'
        
        # Documentation detection
        if any(word in message_lower for word in ['docs', 'documentation', 'readme', 'comment']):
            return 'documentation'
        
        # Performance detection
        if any(word in message_lower for word in ['performance', 'optimize', 'speed', 'faster', 'efficient']):
            return 'performance'
        
        # Security detection
        if any(word in message_lower for word in ['security', 'vulnerability', 'secure', 'auth', 'permission']):
            return 'security'
        
        # Style detection
        if any(word in message_lower for word in ['style', 'ui', 'ux', 'design', 'css', 'layout']):
            return 'style'
        
        # Test detection
        if any(word in message_lower for word in ['test', 'testing', 'spec', 'e2e', 'unit']):
            return 'test'
        
        # Configuration detection
        if any(word in message_lower for word in ['config', 'setting', 'environment', 'setup']):
            return 'configuration'
        
        # Dependency detection
        if any(word in message_lower for word in ['dependency', 'package', 'library', 'upgrade', 'version']):
            return 'dependency'
        
        return 'other'
    
    def _determine_file_purpose(self, file_path: str) -> str:
        """Determine the purpose of a file based on its path and name."""
        file_name = file_path.split('/')[-1].lower()
        file_base = file_name.split('.')[0]
        
        # Check for direct matches
        for key, purpose in self.file_purposes.items():
            if key in file_base:
                return purpose
        
        # Check path components
        path_parts = file_path.lower().split('/')
        for part in path_parts:
            for key, purpose in self.file_purposes.items():
                if key in part:
                    return purpose
        
        # Fallback based on extension
        extension = file_path.split('.')[-1] if '.' in file_path else ''
        if extension in ['css', 'scss', 'less']:
            return 'Visual design and layout'
        elif extension in ['js', 'ts', 'jsx', 'tsx']:
            return 'Application functionality code'
        elif extension in ['html', 'htm']:
            return 'Web page structure'
        elif extension in ['json', 'yml', 'yaml']:
            return 'Configuration or data'
        elif extension in ['py', 'rb', 'php', 'go', 'java']:
            return 'Server-side application code'
        elif extension in ['md', 'txt', 'rst']:
            return 'Documentation and text content'
        
        return 'General purpose file'
    
    def _generate_code_summary(self, file_path: str, language: str) -> str:
        """Generate a simple summary of what the code likely does."""
        file_purpose = self._determine_file_purpose(file_path)
        file_name = file_path.split('/')[-1]
        
        # Enhanced summaries based on file patterns
        if 'login' in file_path.lower() or 'auth' in file_path.lower():
            return f"This {language} file manages user login and authentication processes. It likely handles password verification, session management, and user credentials."
        elif 'database' in file_path.lower() or 'db' in file_path.lower():
            return f"This {language} file handles database operations like storing and retrieving information. It likely contains code for database connections and data queries."
        elif 'api' in file_path.lower():
            return f"This {language} file manages communication with external services and APIs. It likely handles data exchange with other applications or servers."
        elif 'component' in file_path.lower():
            return f"This {language} file defines a reusable UI component that can be used throughout the application. It likely contains visual elements and their behavior."
        elif 'style' in file_path.lower() or 'css' in file_path.lower():
            return f"This {language} file controls the visual appearance of the application. It likely defines colors, layouts, fonts, and other design elements."
        elif 'test' in file_path.lower():
            return f"This {language} file contains automated tests to ensure the application works correctly. It likely includes test cases and verification code."
        elif 'config' in file_path.lower():
            return f"This {language} file contains configuration settings for the application. It likely defines environment variables and application parameters."
        else:
            return f"This {language} file handles {file_purpose.lower()}. It contains code that contributes to the overall functionality of the application."
    
    def explain_file_change(self, file_path: str, insertions: int, deletions: int) -> CodeExplanation:
        """Generate non-technical explanation for file changes."""
        extension = file_path.split('.')[-1] if '.' in file_path else 'unknown'
        language, purpose = self.file_type_explanations.get(extension, ('Unknown', 'general purpose'))
        
        # Determine complexity level
        total_changes = insertions + deletions
        if total_changes > 200:
            complexity_level = "Large change"
        elif total_changes > 50:
            complexity_level = "Medium change"
        else:
            complexity_level = "Small change"
        
        # Generate impact description
        if insertions > deletions * 2:
            impact_description = "Significant additions to functionality"
        elif deletions > insertions * 2:
            impact_description = "Major code cleanup or feature removal"
        elif insertions == 0:
            impact_description = "Code removal or deletion only"
        elif deletions == 0:
            impact_description = "New code additions only"
        else:
            impact_description = "Balanced code updates"
        
        # Generate code summary
        code_summary = self._generate_code_summary(file_path, language)
        
        # Non-technical summary
        non_technical_summary = f"This {language} file handles {purpose}. The change made here is a {complexity_level.lower()} with {impact_description.lower()}."
        
        # Changes explanation
        changes_explanation = f"Added {insertions} lines and removed {deletions} lines of code. "
        if insertions > 0 and deletions == 0:
            changes_explanation += "This likely adds new features or functionality."
        elif insertions == 0 and deletions > 0:
            changes_explanation += "This removes code, possibly outdated features or unnecessary complexity."
        elif insertions > deletions:
            changes_explanation += "More code was added than removed, suggesting new features or expanded functionality."
        elif deletions > insertions:
            changes_explanation += "More code was removed than added, suggesting simplification or cleanup."
        else:
            changes_explanation += "Similar amounts of code were added and removed, suggesting code improvements or restructuring."
        
        return CodeExplanation(
            file_path=file_path,
            language=language,
            purpose=purpose,
            complexity_level=complexity_level,
            impact_description=impact_description,
            non_technical_summary=non_technical_summary,
            changes_explanation=changes_explanation,
            code_summary=code_summary
        )
    
    def generate_non_technical_summary(self, commit: CommitAnalysis) -> Dict[str, Any]:
        """Generate comprehensive non-technical summary for a commit."""
        category = self.categorize_commit(commit.message)
        category_explanation = self.commit_category_explanations.get(category, "General code change")
        
        # Analyze files
        file_explanations = []
        if commit.files_changed:
            for i, file in enumerate(commit.files_changed):
                if file != 'unknown':
                    # Distribute changes evenly if we don't have specific counts per file
                    file_insertions = commit.insertions // len(commit.files_changed) if commit.insertions else 0
                    file_deletions = commit.deletions // len(commit.files_changed) if commit.deletions else 0
                    
                    explanation = self.explain_file_change(
                        file,
                        file_insertions,
                        file_deletions
                    )
                    
                    # Convert explanation object to dict for JSON serialization
                    file_explanations.append(explanation.to_dict())
        
        # Group files by language/type
        files_by_type = {}
        for explanation in file_explanations:
            lang = explanation['language']
            if lang not in files_by_type:
                files_by_type[lang] = []
            files_by_type[lang].append(explanation)
        
        # Generate overall impact summary
        overall_impact = self._generate_overall_impact(commit, file_explanations)
        
        # Create timeline-friendly date
        try:
            formatted_date = commit.date.strftime("%B %d, %Y at %I:%M %p")
        except (AttributeError, ValueError):
            # If date formatting fails, use a fallback
            formatted_date = str(commit.date)
        
        return {
            'commit_id': commit.commit_hash[:8],
            'author': commit.author,
            'date': formatted_date,
            'category': category,
            'category_explanation': category_explanation,
            'message': commit.message,
            'overall_impact': overall_impact,
            'file_explanations': file_explanations,
            'files_by_type': files_by_type,
            'risk_level': self._humanize_risk_level(commit.risk_assessment),
            'impact_score': self._humanize_impact_score(commit.impact_score),
            'visual_changes': self._detect_visual_changes(commit),
            'insertions': commit.insertions,
            'deletions': commit.deletions
        }
    
    def _generate_overall_impact(self, commit: CommitAnalysis, file_explanations: List[Dict[str, Any]]) -> str:
        """Generate overall impact description."""
        total_files = len(commit.files_changed)
        total_changes = commit.insertions + commit.deletions
        
        impact = f"This update modified {total_files} file{'s' if total_files != 1 else ''} "
        impact += f"with a total of {total_changes} lines changed. "
        
        if commit.impact_score > 0.7:
            impact += "This is a significant change that may affect multiple parts of the application. "
        elif commit.impact_score > 0.3:
            impact += "This is a moderate change that updates specific functionality. "
        else:
            impact += "This is a small change with limited scope. "
        
        # Add language-specific insights
        languages = set()
        for exp in file_explanations:
            languages.add(exp.get('language', 'Unknown'))
        
        if len(languages) > 1:
            impact += f"It involves multiple types of code ({', '.join(languages)}) suggesting a cross-functional update."
        
        return impact
    
    def _humanize_risk_level(self, risk_level: str) -> str:
        """Convert risk level to human-friendly description."""
        risk_explanations = {
            'low': "Low risk - routine change that's unlikely to cause problems",
            'medium': "Medium risk - could affect some functionality and should be tested",
            'high': "High risk - affects critical components and requires careful review"
        }
        return risk_explanations.get(risk_level, "Risk level unknown")
    
    def _humanize_impact_score(self, impact_score: float) -> str:
        """Convert impact score to human-friendly description."""
        if impact_score > 0.7:
            return "High impact - major change to the application"
        elif impact_score > 0.3:
            return "Medium impact - noticeable change to functionality"
        else:
            return "Low impact - minor adjustment or fix"
    
    def _detect_visual_changes(self, commit: CommitAnalysis) -> bool:
        """Detect if commit includes visual changes."""
        visual_extensions = ['css', 'scss', 'sass', 'less', 'styl', 'html', 'jsx', 'tsx', 'vue']
        for file in commit.files_changed:
            if any(file.endswith(ext) for ext in visual_extensions):
                return True
        return False
