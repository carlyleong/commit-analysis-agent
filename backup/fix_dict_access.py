"""
Script to fix all dictionary access issues throughout the project.
"""

import os
import re

def fix_file_access_pattern(content):
    """Fix patterns where we're trying to access attributes on dictionaries."""
    
    # Fix file_exp.file_path pattern
    content = re.sub(
        r'file_exp\.file_path',
        "file_exp.get('file_path', 'unknown') if isinstance(file_exp, dict) else getattr(file_exp, 'file_path', 'unknown')",
        content
    )
    
    # Fix file_exp.language pattern
    content = re.sub(
        r'file_exp\.language',
        "file_exp.get('language', 'Unknown') if isinstance(file_exp, dict) else getattr(file_exp, 'language', 'Unknown')",
        content
    )
    
    # Fix file_exp.code_summary pattern
    content = re.sub(
        r'file_exp\.code_summary',
        "file_exp.get('code_summary', '') if isinstance(file_exp, dict) else getattr(file_exp, 'code_summary', '')",
        content
    )
    
    # Fix file_exp.non_technical_summary pattern
    content = re.sub(
        r'file_exp\.non_technical_summary',
        "file_exp.get('non_technical_summary', '') if isinstance(file_exp, dict) else getattr(file_exp, 'non_technical_summary', '')",
        content
    )
    
    return content

def update_file(filepath):
    """Update a single file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        if '.file_path' in content or '.language' in content or '.code_summary' in content:
            new_content = fix_file_access_pattern(content)
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error updating {filepath}: {e}")

def main():
    project_dir = "/Users/carlyleong/Desktop/commit-analysis-agent"
    
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.js'):
                filepath = os.path.join(root, file)
                update_file(filepath)

if __name__ == "__main__":
    main()
