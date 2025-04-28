"""
Debug script to check commit details parsing.
"""

import subprocess
from pathlib import Path
import sys

def debug_commit_details(repo_path, commit_hash):
    try:
        print(f"Checking commit details for: {commit_hash}")
        
        cmd = f"git -C {repo_path} show --stat {commit_hash}"
        print(f"Running command: {cmd}")
        
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        print(f"Raw output:\n{output}\n")
        
        lines = output.strip().split('\n')
        print(f"Number of lines: {len(lines)}")
        
        for i, line in enumerate(lines):
            print(f"Line {i}: {repr(line)}")
            
            # Check if this is a file changes line
            if '|' in line and (' +' in line or ' -' in line):
                print(f"  This looks like a file stats line")
                parts = line.split('|')
                print(f"  Parts count: {len(parts)}")
                if len(parts) >= 2:
                    print(f"  File: {parts[0].strip()}")
                    print(f"  Stats: {parts[1].strip()}")
    
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Error output: {e.output}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        repo_path = sys.argv[1]
        commit_hash = sys.argv[2]
    else:
        repo_path = "/Users/carlyleong/Desktop/test-repo"
        # Use the first commit hash from your output
        commit_hash = "5b599a791f83d74118387b6ce4b65fba19cf15be"
    
    debug_commit_details(repo_path, commit_hash)
