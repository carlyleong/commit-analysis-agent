// Enhanced Dashboard for non-technical users

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeEnhancedDashboard();
});

function initializeEnhancedDashboard() {
    loadRecentReports();
    initializeCharts();
    initializeFeatures();
}

// New features for enhanced dashboard
function initializeFeatures() {
    // Add tab navigation
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });
    
    // Add filter controls
    const filterControls = document.querySelector('#filterControls');
    if (filterControls) {
        filterControls.innerHTML = `
            <select id="categoryFilter" class="p-2 border rounded mr-2">
                <option value="all">All Categories</option>
                <option value="feature">Features</option>
                <option value="bugfix">Bug Fixes</option>
                <option value="documentation">Documentation</option>
                <option value="security">Security</option>
            </select>
            <select id="impactFilter" class="p-2 border rounded mr-2">
                <option value="all">All Impacts</option>
                <option value="high">High Impact</option>
                <option value="medium">Medium Impact</option>
                <option value="low">Low Impact</option>
            </select>
        `;
    }
}

function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Show selected tab content
    const selectedTab = document.getElementById(`${tabName}Tab`);
    if (selectedTab) {
        selectedTab.classList.remove('hidden');
    }
    
    // Update tab button styles
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    const activeButton = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

async function displayEnhancedReport(report) {
    const reportContainer = document.getElementById('reportContent');
    if (!reportContainer) return;
    
    // Create tabbed interface
    reportContainer.innerHTML = `
        <div class="mb-6">
            <div class="border-b border-gray-200">
                <nav class="flex space-x-4">
                    <button class="tab-button active px-3 py-2 text-sm font-medium" data-tab="executive">
                        Executive Summary
                    </button>
                    <button class="tab-button px-3 py-2 text-sm font-medium" data-tab="timeline">
                        Timeline
                    </button>
                    <button class="tab-button px-3 py-2 text-sm font-medium" data-tab="technical">
                        Technical Details
                    </button>
                    <button class="tab-button px-3 py-2 text-sm font-medium" data-tab="visual">
                        Visual Analytics
                    </button>
                </nav>
            </div>
        </div>
        
        <!-- Tab Contents -->
        <div id="executiveTab" class="tab-content">
            ${renderExecutiveSummary(report.dashboard_summary)}
        </div>
        
        <div id="timelineTab" class="tab-content hidden">
            ${renderTimeline(report.non_technical_summaries)}
        </div>
        
        <div id="technicalTab" class="tab-content hidden">
            ${renderTechnicalDetails(report.non_technical_summaries)}
        </div>
        
        <div id="visualTab" class="tab-content hidden">
            <div id="visualAnalyticsContainer">
                ${renderVisualAnalytics(report.dashboard_summary)}
            </div>
        </div>
    `;
    
    // Initialize tab functionality
    initializeFeatures();
    
    // Update charts with new data - make sure this happens after content is in DOM
    setTimeout(() => {
        updateEnhancedCharts(report);
    }, 100);
}

function renderExecutiveSummary(summary) {
    if (!summary) return '<p>No summary available</p>';
    
    return `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-blue-50 p-6 rounded-lg">
                <h3 class="text-lg font-semibold text-blue-800">Total Updates</h3>
                <p class="text-3xl font-bold text-blue-900">${summary.total_commits || 0}</p>
                <p class="text-sm text-blue-600">Over ${summary.time_span_days || 0} days</p>
            </div>
            
            <div class="bg-green-50 p-6 rounded-lg">
                <h3 class="text-lg font-semibold text-green-800">Team Activity</h3>
                <p class="text-3xl font-bold text-green-900">${summary.active_contributors || 0}</p>
                <p class="text-sm text-green-600">Active contributors</p>
            </div>
            
            <div class="bg-purple-50 p-6 rounded-lg">
                <h3 class="text-lg font-semibold text-purple-800">High Impact</h3>
                <p class="text-3xl font-bold text-purple-900">${summary.impact_distribution?.high || 0}</p>
                <p class="text-sm text-purple-600">Critical changes</p>
            </div>
        </div>
        
        <div class="prose max-w-none">
            <h2>Key Highlights</h2>
            <ul>
                <li><strong>Most Active Contributor:</strong> ${summary.most_active_contributor || 'N/A'}</li>
                <li><strong>Visual Changes:</strong> ${summary.visual_changes_count || 0} updates affecting the user interface</li>
                <li><strong>Risk Areas:</strong> ${summary.high_risk_commits || 0} changes requiring careful review</li>
            </ul>
            
            <h2>Activity Breakdown</h2>
            ${renderCategoryBreakdown(summary.commit_categories)}
        </div>
    `;
}

function renderCategoryBreakdown(categories) {
    if (!categories) return '';
    
    const total = Object.values(categories).reduce((a, b) => a + b, 0);
    if (total === 0) return '<p>No categories available</p>';
    
    return `
        <div class="mt-4">
            ${Object.entries(categories).map(([category, count]) => `
                <div class="mb-2">
                    <div class="flex justify-between">
                        <span class="font-medium">${category.charAt(0).toUpperCase() + category.slice(1)}</span>
                        <span>${count} commits</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${(count / total) * 100}%"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderTimeline(summaries) {
    if (!summaries || summaries.length === 0) return '<p>No timeline data available</p>';
    
    return `
        <div class="space-y-8">
            ${summaries.map(commit => `
                <div class="border-l-4 ${getCategoryColor(commit.category)} pl-4">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-semibold text-lg">${commit.message}</h3>
                            <p class="text-sm text-gray-600">${commit.author} • ${commit.date}</p>
                        </div>
                        <div class="text-right">
                            <span class="px-2 py-1 rounded text-sm ${getImpactBadgeClass(commit.impact_score)}">
                                ${getImpactLevel(commit.impact_score)}
                            </span>
                        </div>
                    </div>
                    
                    <div class="mt-2">
                        <p class="text-gray-700">${commit.overall_impact}</p>
                    </div>
                    
                    ${renderFileExplanations(commit.file_explanations)}
                    
                    <div class="mt-2 text-sm text-gray-500">
                        Risk: ${commit.risk_level}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderFileExplanations(explanations) {
    if (!explanations || explanations.length === 0) return '';
    
    return `
        <div class="mt-3 bg-gray-50 rounded p-3">
            <h4 class="font-medium text-sm mb-2">Files Modified:</h4>
            <ul class="text-sm space-y-2">
                ${explanations.map(exp => {
                    const filePath = exp?.file_path || 'unknown';
                    const codeSummary = exp?.code_summary || exp?.non_technical_summary || 'No summary available';
                    const changesExplanation = exp?.changes_explanation || '';
                    const language = exp?.language || 'Unknown';
                    const complexityLevel = exp?.complexity_level || '';
                    
                    return `
                        <li class="border-b border-gray-200 pb-2">
                            <div class="font-mono bg-gray-200 px-2 py-1 rounded inline-block mb-1">
                                ${filePath}
                            </div>
                            <div class="text-gray-700 ml-4">
                                <p class="mb-1">${codeSummary}</p>
                                <p class="text-xs text-gray-500">${changesExplanation}</p>
                                <p class="text-xs text-gray-400 mt-1">Language: ${language} | ${complexityLevel}</p>
                            </div>
                        </li>
                    `;
                }).join('')}
            </ul>
        </div>
    `;
}

function getCategoryColor(category) {
    const colors = {
        'feature': 'border-green-500',
        'bugfix': 'border-red-500',
        'documentation': 'border-blue-500',
        'security': 'border-yellow-500',
        'performance': 'border-purple-500',
        'style': 'border-pink-500',
        'test': 'border-orange-500',
        'configuration': 'border-gray-500',
        'dependency': 'border-teal-500'
    };
    return colors[category] || 'border-gray-500';
}

function getImpactBadgeClass(impactScore) {
    if (!impactScore) return 'bg-gray-100 text-gray-800';
    if (impactScore.includes('High')) return 'bg-red-100 text-red-800';
    if (impactScore.includes('Medium')) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
}

function getImpactLevel(impactScore) {
    if (!impactScore) return 'Unknown Impact';
    if (impactScore.includes('High')) return 'High Impact';
    if (impactScore.includes('Medium')) return 'Medium Impact';
    return 'Low Impact';
}

function renderTechnicalDetails(summaries) {
    if (!summaries || summaries.length === 0) return '<p>No technical details available</p>';
    
    // Group by file type
    const fileTypeGroups = {};
    summaries.forEach(commit => {
        if (commit.files_by_type) {
            Object.entries(commit.files_by_type).forEach(([fileType, files]) => {
                if (!fileTypeGroups[fileType]) {
                    fileTypeGroups[fileType] = [];
                }
                fileTypeGroups[fileType] = fileTypeGroups[fileType].concat(files);
            });
        }
    });
    
    return `
        <div class="space-y-6">
            <h3 class="text-lg font-semibold">Technology Breakdown</h3>
            ${Object.entries(fileTypeGroups).map(([fileType, files]) => `
                <div class="bg-gray-50 p-4 rounded">
                    <h4 class="font-semibold">${fileType} Files</h4>
                    <p class="text-sm text-gray-600">Total changes: ${files.length}</p>
                    <ul class="mt-2 space-y-2">
                        ${files.slice(0, 5).map(file => `
                            <li class="text-sm border-b border-gray-200 pb-2">
                                <div><code class="bg-gray-200 px-1 rounded">${file.file_path || 'unknown'}</code></div>
                                <div class="mt-1 ml-4">
                                    <p class="text-gray-700">${file.code_summary || file.non_technical_summary || 'No summary available'}</p>
                                    <p class="text-xs text-gray-500">${file.changes_explanation || ''}</p>
                                </div>
                            </li>
                        `).join('')}
                        ${files.length > 5 ? `<li class="text-sm text-gray-500">...and ${files.length - 5} more</li>` : ''}
                    </ul>
                </div>
            `).join('')}
        </div>
    `;
}

function renderVisualAnalytics(summary) {
    if (!summary) return '<p>No visual analytics available</p>';
    
    return `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4">Activity Distribution</h3>
                <canvas id="enhancedCommitChart"></canvas>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4">Impact Analysis</h3>
                <canvas id="enhancedImpactChart"></canvas>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4">Risk Distribution</h3>
                <canvas id="enhancedRiskChart"></canvas>
            </div>
            
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-lg font-semibold mb-4">Category Trends</h3>
                <canvas id="categoryTrendChart"></canvas>
            </div>
        </div>
    `;
}

function updateEnhancedCharts(report) {
    const summary = report.dashboard_summary;
    if (!summary) return;
    
    // Activity Distribution Chart
    const commitCanvas = document.getElementById('enhancedCommitChart');
    if (commitCanvas) {
        const commitCtx = commitCanvas.getContext('2d');
        const categories = summary.commit_categories || {};
        
        new Chart(commitCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(categories).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
                datasets: [{
                    data: Object.values(categories),
                    backgroundColor: [
                        '#4CAF50', '#2196F3', '#FFC107', '#FF5722', 
                        '#9C27B0', '#00BCD4', '#795548', '#607D8B'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Impact Analysis Chart
    const impactCanvas = document.getElementById('enhancedImpactChart');
    if (impactCanvas) {
        const impactCtx = impactCanvas.getContext('2d');
        const impacts = summary.impact_distribution || {high: 0, medium: 0, low: 0};
        
        new Chart(impactCtx, {
            type: 'doughnut',
            data: {
                labels: ['High Impact', 'Medium Impact', 'Low Impact'],
                datasets: [{
                    data: [impacts.high, impacts.medium, impacts.low],
                    backgroundColor: ['#EF4444', '#F59E0B', '#10B981']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Risk Distribution Chart
    const riskCanvas = document.getElementById('enhancedRiskChart');
    if (riskCanvas) {
        const riskCtx = riskCanvas.getContext('2d');
        
        // Calculate risk distribution from commits
        let highRisk = 0, mediumRisk = 0, lowRisk = 0;
        if (report.non_technical_summaries) {
            report.non_technical_summaries.forEach(commit => {
                if (commit.risk_level.includes('High')) highRisk++;
                else if (commit.risk_level.includes('Medium')) mediumRisk++;
                else lowRisk++;
            });
        }
        
        new Chart(riskCtx, {
            type: 'bar',
            data: {
                labels: ['High Risk', 'Medium Risk', 'Low Risk'],
                datasets: [{
                    label: 'Number of Commits',
                    data: [highRisk, mediumRisk, lowRisk],
                    backgroundColor: ['#EF4444', '#F59E0B', '#10B981']
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    // Category Trends Chart
    const trendsCanvas = document.getElementById('categoryTrendChart');
    if (trendsCanvas) {
        const trendsCtx = trendsCanvas.getContext('2d');
        const timeline = summary.activity_timeline || [];
        
        const datasets = [];
        const categories = ['feature', 'bugfix', 'documentation', 'security'];
        const colors = ['#4CAF50', '#F44336', '#2196F3', '#FF9800'];
        
        categories.forEach((category, index) => {
            datasets.push({
                label: category.charAt(0).toUpperCase() + category.slice(1),
                data: timeline.map(day => day.category_breakdown?.[category] || 0),
                borderColor: colors[index],
                tension: 0.1
            });
        });
        
        new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: timeline.map(day => day.date),
                datasets: datasets
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
}
