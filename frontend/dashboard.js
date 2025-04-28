// Dashboard JavaScript for Commit Analysis

let commitChart = null;
let impactChart = null;
let riskChart = null;
let categoryTrendChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadRecentReports();
    initializeCharts();
});

// Run new analysis
async function runAnalysis() {
    const repoPath = document.getElementById('repoPath').value;
    const timeframe = document.getElementById('timeframe').value;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ repoPath, timeframe })
        });
        
        const result = await response.json();
        
        if (result.success) {
            if (result.commit_count === 0) {
                showNotification('No commits found in the specified timeframe.', 'warning');
            } else {
                showNotification('Analysis completed successfully!', 'success');
                loadRecentReports();
                viewReport(result.report_id);
            }
        } else {
            showNotification('Analysis failed: ' + result.error, 'error');
            console.error('Detailed error:', result.details);
        }
    } catch (error) {
        showNotification('Error running analysis: ' + error.message, 'error');
    }
}

// Load recent reports
async function loadRecentReports() {
    try {
        const response = await fetch('/api/reports/recent');
        const reports = await response.json();
        
        const container = document.getElementById('recentReports');
        container.innerHTML = '';
        
        reports.forEach(report => {
            const card = createReportCard(report);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

// Create report card element
function createReportCard(report) {
    const card = document.createElement('div');
    card.className = 'bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition';
    
    const date = new Date(report.created_at).toLocaleString();
    
    card.innerHTML = `
        <div class="flex justify-between items-center">
            <div>
                <h3 class="font-semibold">${report.timeframe} Analysis</h3>
                <p class="text-sm text-gray-600">${date}</p>
                <p class="text-sm">Commits analyzed: ${report.commit_count}</p>
            </div>
            <button onclick="viewReport('${report.metadata.report_id}')" 
                    class="bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200">
                View
            </button>
        </div>
    `;
    
    return card;
}

// View detailed report
async function viewReport(reportId) {
    try {
        const response = await fetch(`/api/reports/${reportId}`);
        const report = await response.json();
        
        const reportView = document.getElementById('reportView');
        
        // Use enhanced display
        displayEnhancedReport(report);
        
        // Show report view
        reportView.classList.remove('hidden');
        
        // Scroll to report
        reportView.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showNotification('Error loading report: ' + error.message, 'error');
    }
}

// Close report view
function closeReport() {
    const reportView = document.getElementById('reportView');
    reportView.classList.add('hidden');
}

// Initialize charts
function initializeCharts() {
    const commitCtx = document.getElementById('commitChart').getContext('2d');
    const impactCtx = document.getElementById('impactChart').getContext('2d');
    const riskCtx = document.getElementById('riskChart').getContext('2d');
    const categoryTrendCtx = document.getElementById('categoryTrendChart').getContext('2d');
    
    commitChart = new Chart(commitCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Commits by Date',
                data: [],
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    impactChart = new Chart(impactCtx, {
        type: 'doughnut',
        data: {
            labels: ['High Impact', 'Medium Impact', 'Low Impact'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.7)',
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(34, 197, 94, 0.7)'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });
    
    riskChart = new Chart(riskCtx, {
        type: 'pie',
        data: {
            labels: ['High Risk', 'Medium Risk', 'Low Risk'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(34, 197, 94, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true
        }
    });
    
    categoryTrendChart = new Chart(categoryTrendCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Update charts with new data
function updateCharts(commits) {
    // Process commit data for charts
    const dateCounts = {};
    let highImpact = 0;
    let mediumImpact = 0;
    let lowImpact = 0;
    let highRisk = 0;
    let mediumRisk = 0;
    let lowRisk = 0;
    
    commits.forEach(commit => {
        // Date-based grouping
        const date = new Date(commit.date).toLocaleDateString();
        dateCounts[date] = (dateCounts[date] || 0) + 1;
        
        // Impact scoring
        if (commit.impact_score > 0.7) {
            highImpact++;
        } else if (commit.impact_score > 0.3) {
            mediumImpact++;
        } else {
            lowImpact++;
        }
        
        // Risk assessment
        if (commit.risk_assessment === 'high') {
            highRisk++;
        } else if (commit.risk_assessment === 'medium') {
            mediumRisk++;
        } else {
            lowRisk++;
        }
    });
    
    // Update commit chart
    commitChart.data.labels = Object.keys(dateCounts);
    commitChart.data.datasets[0].data = Object.values(dateCounts);
    commitChart.update();
    
    // Update impact chart
    impactChart.data.datasets[0].data = [highImpact, mediumImpact, lowImpact];
    impactChart.update();
    
    // Update risk chart
    riskChart.data.datasets[0].data = [highRisk, mediumRisk, lowRisk];
    riskChart.update();
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' :
        'bg-blue-500'
    }`;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
