"""
Simple API server for the commit analysis dashboard.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
from main import CommitAnalysisApp

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Global app instance
analysis_app = None

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/api/analyze', methods=['POST'])
def analyze_repo():
    global analysis_app
    
    data = request.json
    repo_path = data.get('repoPath')
    timeframe = data.get('timeframe', 'week')
    
    try:
        if not os.path.exists(repo_path):
            return jsonify({'success': False, 'error': f'Repository path does not exist: {repo_path}'})
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return jsonify({'success': False, 'error': f'Not a git repository: {repo_path}'})
        
        analysis_app = CommitAnalysisApp(repo_path)
        result = analysis_app.run_analysis(timeframe)
        
        return jsonify({
            'success': True,
            'report_id': result['report_id'],
            'summary': result['summary'],
            'commit_count': result['commit_count']
        })
    except IndexError as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'success': False, 'error': f'Index error while parsing git data: {str(e)}', 'details': error_details})
    except subprocess.CalledProcessError as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'success': False, 'error': f'Git command failed: {str(e)}', 'details': error_details})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'success': False, 'error': str(e), 'details': error_details})

@app.route('/api/reports/recent', methods=['GET'])
def get_recent_reports():
    global analysis_app
    
    if not analysis_app:
        return jsonify([])
    
    reports = analysis_app.get_recent_reports()
    return jsonify(reports)

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    global analysis_app
    
    if not analysis_app:
        return jsonify({'error': 'No analysis app initialized'}), 404
    
    report = analysis_app.get_report(report_id)
    if report:
        return jsonify(report)
    else:
        return jsonify({'error': 'Report not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
