"""
Debug script to understand the git parsing issue.
"""

import subprocess
from pathlib import Path
import json
import sys

def debug_git_output(repo_path):
    try:
        print(f"Checking repository at: {repo_path}")
        
        # Check if path exists
        if not Path(repo_path).exists():
            print(f"ERROR: Path does not exist: {repo_path}")
            return
        
        # Check if it's a git repository
        git_path = Path(repo_path) / '.git'
        if not git_path.exists():
            print(f"ERROR: Not a git repository: {repo_path}")
            return
        
        # Try to run git command
        cmd = f"git -C {repo_path} log --since='1 week ago' --format='%H|||%an|||%ad|||%s'"
        print(f"Running command: {cmd}")
        
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        print(f"Raw output: {repr(output)}")
        print(f"Output length: {len(output)}")
        
        # Split and analyze lines
        lines = output.strip().split('\n')
        print(f"Number of lines: {len(lines)}")
        
        for i, line in enumerate(lines):
            print(f"Line {i}: {repr(line)}")
            parts = line.split('|||')
            print(f"  Parts count: {len(parts)}")
            if len(parts) >= 4:
                print(f"  Hash: {parts[0]}")
                print(f"  Author: {parts[1]}")
                print(f"  Date: {parts[2]}")
                print(f"  Message: {parts[3]}")
            else:
                print(f"  WARNING: Line has fewer than 4 parts!")
    
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Error output: {e.output}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/Users/carlyleong/Desktop/test-repo"
    
    debug_git_output(repo_path)
