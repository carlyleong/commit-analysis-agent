# Commit Analyzer Agent

An intelligent system that analyzes git repository commits and provides comprehensive insights using AI-powered agents.

## Overview

The Commit Analyzer Agent uses a multi-stage workflow with Claude API to analyze code repository commits and generate detailed reports. It leverages agentic workflows with evaluator-optimizer patterns to continuously improve the quality of analysis and reporting.

This tool helps development teams:
- Understand the impact and risk of code changes
- Generate both technical and non-technical summaries
- Visualize commit trends and patterns
- Get actionable insights from code changes

## Features

- **Intelligent Commit Analysis**: Classifies commits by type and analyzes their impact and risk
- **Multi-Step Processing**: Sequential workflow for analyzing, summarizing, and reporting
- **Customizable Reports**: Creates executive, technical, and non-technical summaries
- **Web Dashboard**: Interactive visualization of commit data and metrics
- **Self-Improving Reports**: Uses evaluator-optimizer pattern to refine analysis quality

## Architecture

The system follows a modular architecture based on the agent workflow patterns:

- **Base Agent Framework**: Core agent functionality with workflow patterns
- **Specialized Agents**: Commit analyzers and report generators
- **Storage System**: Hybrid approach with files and database 
- **API Layer**: REST API for integration with other systems
- **Dashboard**: Web interface for exploring results

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/commit-analyzer-agent.git
cd commit-analyzer-agent
```

2. **Set up environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure API keys**:
```bash
cp .env.example .env
# Edit .env with your Claude API key
```

## Usage

### Command Line Interface

Analyze a repository with default settings:
```bash
python src/main.py /path/to/your/repository
```

Specify timeframe and other options:
```bash
python src/main.py /path/to/your/repository --timeframe month --output ./reports
```

Available options:
- `--timeframe`: 'week' (default), 'month', or specific date range (e.g., '2023-01-01..2023-02-01')
- `--output`: Directory to save reports (default: './reports')
- `--model`: Claude model to use (default: claude-3-opus)

### Web Dashboard

Start the web server:
```bash
python src/api_server.py
```

Access the dashboard at http://localhost:5000

### Python API

```python
from src.agents.commit_analyzer import CommitAnalyzerAgent

# Initialize the agent
agent = CommitAnalyzerAgent("/path/to/repository")

# Process commits from last week
result = agent.process(timeframe="week")

# Access the generated report
print(result['report'])

# Access detailed analysis
for commit in result['detailed_analysis']:
    print(f"Commit: {commit.commit_hash}")
    print(f"Impact: {commit.impact_score}")
    print(f"Risk: {commit.risk_assessment}")
```

## Report Types

The system generates several types of reports:

1. **Executive Summary**: High-level overview for managers and stakeholders
2. **Technical Deep-Dive**: Detailed technical analysis for developers
3. **Timeline View**: Chronological view of repository activity
4. **Dashboard Summary**: Metrics and charts for visualization

## Configuration

System settings can be adjusted in `config.json`:

```json
{
  "models": {
    "default": "claude-3-opus-20240229"
  },
  "analysis": {
    "max_commits_per_request": 50,
    "default_timeframe": "week"
  }
}
```

## License

MIT License
