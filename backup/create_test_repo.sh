#!/bin/bash

# Create a test repository
cd /Users/carlyleong/Desktop
mkdir -p test-repo
cd test-repo

# Initialize git repository
git init

# Create initial commit
echo "# Test Repository" > README.md
git add README.md
git commit -m "Initial commit"

# Add some test files and commits
echo "Test file 1" > test1.txt
git add test1.txt
git commit -m "Add test file 1"

echo "Test file 2" > test2.txt
git add test2.txt
git commit -m "Add test file 2"

# Create a directory with source files
mkdir src
echo "function hello() { console.log('Hello!'); }" > src/index.js
git add src/index.js
git commit -m "Add source directory"

# Add configuration file
echo "{ \"name\": \"test-repo\", \"version\": \"1.0.0\" }" > package.json
git add package.json
git commit -m "Add package.json configuration"

# Make some more commits
echo "Additional content" >> README.md
git add README.md
git commit -m "Update README with more content"

echo "Another test file" > test3.txt
git add test3.txt
git commit -m "Add test file 3"

echo "Test repository created successfully at /Users/carlyleong/Desktop/test-repo"
