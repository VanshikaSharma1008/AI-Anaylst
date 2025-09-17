import os
import io
import base64
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State, dash_table, callback
import dash_bootstrap_components as dbc
from flask import Flask, send_file
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid

# Import custom modules
from modules.data_processor import DataProcessor
from modules.statistical_analyzer import StatisticalAnalyzer
from modules.visualizer import Visualizer
from modules.report_generator import ReportGenerator
from modules.error_handler import ErrorHandler

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app with professional theme
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap",
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

# Custom CSS for professional UI
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>DataAnalyst Pro - Professional Data Analysis</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-color: #4361ee;
                --secondary-color: #3f37c9;
                --success-color: #4cc9f0;
                --info-color: #4895ef;
                --warning-color: #f72585;
                --danger-color: #e63946;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --background-color: #ffffff;
                --text-color: #212529;
                --border-color: #dee2e6;
                --card-bg: #ffffff;
                --sidebar-bg: #f8f9fa;
            }

            [data-theme="dark"] {
                --primary-color: #4cc9f0;
                --secondary-color: #4895ef;
                --success-color: #4361ee;
                --info-color: #3f37c9;
                --warning-color: #f72585;
                --danger-color: #e63946;
                --light-color: #343a40;
                --dark-color: #f8f9fa;
                --background-color: #212529;
                --text-color: #f8f9fa;
                --border-color: #495057;
                --card-bg: #343a40;
                --sidebar-bg: #343a40;
            }

            body {
                font-family: 'Poppins', sans-serif;
                background-color: var(--background-color);
                color: var(--text-color);
                transition: all 0.3s ease;
            }

            .card {
                background-color: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }

            .sidebar {
                background-color: var(--sidebar-bg);
                border-right: 1px solid var(--border-color);
                transition: all 0.3s ease;
            }

            .nav-link {
                color: var(--text-color);
            }

            .nav-link.active {
                background-color: var(--primary-color) !important;
                color: white !important;
            }

            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
            }

            .btn-secondary {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
            }

            .btn-success {
                background-color: var(--success-color);
                border-color: var(--success-color);
            }

            .btn-info {
                background-color: var(--info-color);
                border-color: var(--info-color);
            }

            .btn-warning {
                background-color: var(--warning-color);
                border-color: var(--warning-color);
            }

            .btn-danger {
                background-color: var(--danger-color);
                border-color: var(--danger-color);
            }

            .header {
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                padding: 2rem 0;
                margin-bottom: 2rem;
                border-radius: 0 0 1rem 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .metric-card {
                border-radius: 1rem;
                padding: 1.5rem;
                height: 100%;
                transition: transform 0.3s ease;
                border-left: 5px solid var(--primary-color);
            }

            .metric-card:hover {
                transform: translateY(-5px);
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }

            .metric-label {
                font-size: 1rem;
                color: var(--text-secondary);
                margin-bottom: 0;
            }

            .upload-area {
                border: 2px dashed var(--border-color);
                border-radius: 1rem;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
                background-color: rgba(0, 0, 0, 0.02);
            }

            .upload-area:hover {
                border-color: var(--primary-color);
                background-color: rgba(0, 0, 0, 0.05);
            }

            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner * {
                color: var(--text-color) !important;
            }

            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
                background-color: var(--primary-color) !important;
                color: white !important;
            }

            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td {
                background-color: var(--card-bg) !important;
            }

            .dash-dropdown .Select-control {
                background-color: var(--card-bg) !important;
                color: var(--text-color) !important;
                border-color: var(--border-color) !important;
            }

            .dash-dropdown .Select-menu-outer {
                background-color: var(--card-bg) !important;
                color: var(--text-color) !important;
                border-color: var(--border-color) !important;
            }

            .dash-dropdown .Select-value-label {
                color: var(--text-color) !important;
            }

            .theme-toggle {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                z-index: 1000;
                width: 3rem;
                height: 3rem;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }

            .theme-toggle:hover {
                transform: scale(1.1);
            }

            .tab-content {
                padding: 1.5rem;
                background-color: var(--card-bg);
                border-radius: 0 0 1rem 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .nav-tabs {
                border-bottom: none;
            }

            .nav-tabs .nav-link {
                border-radius: 1rem 1rem 0 0;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                border: 1px solid transparent;
            }

            .nav-tabs .nav-link.active {
                background-color: var(--card-bg);
                border-color: var(--border-color);
                border-bottom-color: transparent;
                color: var(--primary-color);
            }

            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: var(--primary-color);
            }

            .feature-card {
                text-align: center;
                padding: 2rem;
                border-radius: 1rem;
                height: 100%;
                transition: transform 0.3s ease;
            }

            .feature-card:hover {
                transform: translateY(-5px);
            }

            .export-options {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }

            .export-btn {
                flex: 1;
                text-align: center;
                padding: 1rem;
                border-radius: 0.5rem;
                transition: all 0.3s ease;
                cursor: pointer;
            }

            .export-btn:hover {
                transform: translateY(-5px);
            }

            .csv-btn {
                background-color: rgba(var(--success-color-rgb), 0.1);
                color: var(--success-color);
                border: 1px solid var(--success-color);
            }

            .excel-btn {
                background-color: rgba(var(--info-color-rgb), 0.1);
                color: var(--info-color);
                border: 1px solid var(--info-color);
            }

            .pdf-btn {
                background-color: rgba(var(--danger-color-rgb), 0.1);
                color: var(--danger-color);
                border: 1px solid var(--danger-color);
            }

            .loading-spinner {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                position: absolute;
                top: 0;
                left: 0;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                border-radius: 1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout with professional UI
app.layout = html.Div([
    # Theme store for dark/light mode
    dcc.Store(id='theme-store', data={'theme': 'light'}),

    # Session ID for tracking user sessions
    dcc.Store(id='session-id', data={'session_id': str(uuid.uuid4())}),

    # Data stores
    dcc.Store(id='stored-data'),
    dcc.Store(id='processed-data'),
    dcc.Store(id='analysis-results'),

    # Main container with theme attribute
    html.Div(
        id='main-container',
        children=[
            # Header
            html.Div(
                className='header text-center text-white',
                children=[
                    html.H1("DataAnalyst Pro", className="display-4 fw-bold"),
                    html.P(
                        "Professional Data Analysis & Visualization Platform", className="lead")
                ]
            ),

            # Main content
            dbc.Container(
                fluid=True,
                className='px-4',
                children=[
                    # Upload section
                    dbc.Card(
                        className='mb-4',
                        children=[
                            dbc.CardBody([
                                html.H3("Start Your Analysis",
                                        className="card-title mb-3"),
                                html.P(
                                    "Upload your dataset to begin analyzing your data with our professional tools.", className="card-text mb-4"),

                                # Upload area
                                html.Div(
                                    className='upload-area',
                                    children=[
                                        dcc.Upload(
                                            id='upload-data',
                                            children=[
                                                html.Div([
                                                    html.I(
                                                        className="fas fa-cloud-upload-alt fa-3x mb-3"),
                                                    html.H5(
                                                        "Drag and Drop or Click to Upload"),
                                                    html.P(
                                                        "Supported formats: CSV, Excel (.xlsx, .xls)")
                                                ])
                                            ],
                                            multiple=False
                                        )
                                    ]
                                ),

                                # Upload status
                                html.Div(id='upload-status', className='mt-3')
                            ])
                        ]
                    ),

                    # Metrics section (initially hidden)
                    html.Div(
                        id='metrics-section',
                        style={'display': 'none'},
                        children=[
                            html.H3("Dataset Overview", className="mb-4"),
                            dbc.Row([
                                # Total Records
                                dbc.Col([
                                    dbc.Card(
                                        className='metric-card',
                                        children=[
                                            html.Div([
                                                html.I(
                                                    className="fas fa-database feature-icon"),
                                                html.H2(
                                                    id="metric-records", className="metric-value text-primary"),
                                                html.P("Total Records",
                                                       className="metric-label")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=6, lg=3, className='mb-4'),

                                # Total Columns
                                dbc.Col([
                                    dbc.Card(
                                        className='metric-card',
                                        children=[
                                            html.Div([
                                                html.I(
                                                    className="fas fa-table feature-icon"),
                                                html.H2(
                                                    id="metric-columns", className="metric-value text-info"),
                                                html.P("Total Columns",
                                                       className="metric-label")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=6, lg=3, className='mb-4'),

                                # Numeric Fields
                                dbc.Col([
                                    dbc.Card(
                                        className='metric-card',
                                        children=[
                                            html.Div([
                                                html.I(
                                                    className="fas fa-hashtag feature-icon"),
                                                html.H2(
                                                    id="metric-numeric", className="metric-value text-success"),
                                                html.P("Numeric Fields",
                                                       className="metric-label")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=6, lg=3, className='mb-4'),

                                # Categorical Fields
                                dbc.Col([
                                    dbc.Card(
                                        className='metric-card',
                                        children=[
                                            html.Div([
                                                html.I(
                                                    className="fas fa-tags feature-icon"),
                                                html.H2(
                                                    id="metric-categorical", className="metric-value text-warning"),
                                                html.P("Categorical Fields",
                                                       className="metric-label")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=6, lg=3, className='mb-4')
                            ])
                        ]
                    ),

                    # Main analysis section (initially hidden)
                    html.Div(
                        id='analysis-section',
                        style={'display': 'none'},
                        children=[
                            # Tabs for different analysis views
                            dbc.Tabs(
                                id='analysis-tabs',
                                active_tab='tab-overview',
                                className='mb-4',
                                children=[
                                    # Data Overview Tab
                                    dbc.Tab(
                                        label="Data Overview",
                                        tab_id="tab-overview",
                                        label_class_name="d-flex align-items-center",
                                        label_style={"font-size": "1rem"},
                                        tab_class_name="rounded-top",
                                        children=[
                                            html.Div(
                                                className='tab-content',
                                                children=[
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.H4(
                                                                "Data Preview", className="mb-3"),
                                                            html.Div(
                                                                id="data-table-container")
                                                        ], width=12)
                                                    ]),
                                                    html.Hr(),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.H4(
                                                                "Data Summary", className="mb-3"),
                                                            html.Div(
                                                                id="data-summary-container")
                                                        ], width=12)
                                                    ])
                                                ]
                                            )
                                        ]
                                    ),

                                    # Statistical Analysis Tab
                                    dbc.Tab(
                                        label="Statistical Analysis",
                                        tab_id="tab-stats",
                                        label_class_name="d-flex align-items-center",
                                        label_style={"font-size": "1rem"},
                                        tab_class_name="rounded-top",
                                        children=[
                                            html.Div(
                                                className='tab-content',
                                                children=[
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.H4(
                                                                "Select Variables", className="mb-3"),
                                                            dcc.Dropdown(
                                                                id="stats-variable-selector",
                                                                multi=True,
                                                                placeholder="Select variables for analysis..."
                                                            )
                                                        ], width=12, className="mb-4")
                                                    ]),
                                                    html.Div(
                                                        id="stats-content")
                                                ]
                                            )
                                        ]
                                    ),

                                    # Visualizations Tab
                                    dbc.Tab(
                                        label="Visualizations",
                                        tab_id="tab-viz",
                                        label_class_name="d-flex align-items-center",
                                        label_style={"font-size": "1rem"},
                                        tab_class_name="rounded-top",
                                        children=[
                                            html.Div(
                                                className='tab-content',
                                                children=[
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.H4(
                                                                "Create Custom Visualizations", className="mb-3"),
                                                            dbc.Row([
                                                                dbc.Col([
                                                                    html.Label(
                                                                        "Chart Type"),
                                                                    dcc.Dropdown(
                                                                        id="chart-type-selector",
                                                                        options=[
                                                                            {"label": "Bar Chart",
                                                                                "value": "bar"},
                                                                            {"label": "Line Chart",
                                                                                "value": "line"},
                                                                            {"label": "Scatter Plot",
                                                                                "value": "scatter"},
                                                                            {"label": "Histogram",
                                                                                "value": "histogram"},
                                                                            {"label": "Box Plot",
                                                                                "value": "box"},
                                                                            {"label": "Heatmap",
                                                                                "value": "heatmap"}
                                                                        ],
                                                                        value="bar"
                                                                    )
                                                                ], width=4),
                                                                dbc.Col([
                                                                    html.Label(
                                                                        "X-Axis"),
                                                                    dcc.Dropdown(
                                                                        id="x-axis-selector",
                                                                        placeholder="Select variable..."
                                                                    )
                                                                ], width=4),
                                                                dbc.Col([
                                                                    html.Label(
                                                                        "Y-Axis"),
                                                                    dcc.Dropdown(
                                                                        id="y-axis-selector",
                                                                        placeholder="Select variable..."
                                                                    )
                                                                ], width=4)
                                                            ], className="mb-3"),
                                                            dbc.Button(
                                                                [html.I(
                                                                    className="fas fa-chart-bar me-2"), "Generate Chart"],
                                                                id="btn-generate-chart",
                                                                color="primary",
                                                                className="mb-4"
                                                            )
                                                        ], width=12)
                                                    ]),
                                                    html.Div(id="viz-content")
                                                ]
                                            )
                                        ]
                                    ),

                                    # Insights Tab
                                    dbc.Tab(
                                        label="Insights & Recommendations",
                                        tab_id="tab-insights",
                                        label_class_name="d-flex align-items-center",
                                        label_style={"font-size": "1rem"},
                                        tab_class_name="rounded-top",
                                        children=[
                                            html.Div(
                                                className='tab-content',
                                                children=[
                                                    dbc.Alert(
                                                        [
                                                            html.I(
                                                                className="fas fa-lightbulb me-2"),
                                                            "Automated insights are generated based on your data patterns."
                                                        ],
                                                        color="info",
                                                        className="mb-4"
                                                    ),
                                                    html.Div(
                                                        id="insights-content")
                                                ]
                                            )
                                        ]
                                    ),

                                    # Export Tab
                                    dbc.Tab(
                                        label="Export & Reports",
                                        tab_id="tab-export",
                                        label_class_name="d-flex align-items-center",
                                        label_style={"font-size": "1rem"},
                                        tab_class_name="rounded-top",
                                        children=[
                                            html.Div(
                                                className='tab-content',
                                                children=[
                                                    html.H4(
                                                        "Export Options", className="mb-4"),
                                                    dbc.Row([
                                                        # CSV Export
                                                        dbc.Col([
                                                            dbc.Card(
                                                                className='h-100',
                                                                children=[
                                                                    dbc.CardBody([
                                                                        html.Div(
                                                                            className='text-center',
                                                                            children=[
                                                                                html.I(
                                                                                    className="fas fa-file-csv fa-3x mb-3 text-success"),
                                                                                html.H5(
                                                                                    "CSV Export", className="mb-3"),
                                                                                html.P(
                                                                                    "Export your data as a CSV file for use in spreadsheet applications.", className="mb-4"),
                                                                                dbc.Button(
                                                                                    [html.I(
                                                                                        className="fas fa-download me-2"), "Download CSV"],
                                                                                    id="btn-export-csv",
                                                                                    color="success",
                                                                                    className="w-100"
                                                                                )
                                                                            ]
                                                                        )
                                                                    ])
                                                                ]
                                                            )
                                                        ], xs=12, sm=12, md=4, className="mb-4"),

                                                        # Excel Export
                                                        dbc.Col([
                                                            dbc.Card(
                                                                className='h-100',
                                                                children=[
                                                                    dbc.CardBody([
                                                                        html.Div(
                                                                            className='text-center',
                                                                            children=[
                                                                                html.I(
                                                                                    className="fas fa-file-excel fa-3x mb-3 text-primary"),
                                                                                html.H5(
                                                                                    "Excel Export", className="mb-3"),
                                                                                html.P(
                                                                                    "Export your data as an Excel file with formatting preserved.", className="mb-4"),
                                                                                dbc.Button(
                                                                                    [html.I(
                                                                                        className="fas fa-download me-2"), "Download Excel"],
                                                                                    id="btn-export-excel",
                                                                                    color="primary",
                                                                                    className="w-100"
                                                                                )
                                                                            ]
                                                                        )
                                                                    ])
                                                                ]
                                                            )
                                                        ], xs=12, sm=12, md=4, className="mb-4"),

                                                        # PDF Report
                                                        dbc.Col([
                                                            dbc.Card(
                                                                className='h-100',
                                                                children=[
                                                                    dbc.CardBody([
                                                                        html.Div(
                                                                            className='text-center',
                                                                            children=[
                                                                                html.I(
                                                                                    className="fas fa-file-pdf fa-3x mb-3 text-danger"),
                                                                                html.H5(
                                                                                    "PDF Report", className="mb-3"),
                                                                                html.P(
                                                                                    "Generate a comprehensive PDF report with visualizations and insights.", className="mb-4"),
                                                                                dbc.Button(
                                                                                    [html.I(
                                                                                        className="fas fa-file-pdf me-2"), "Generate Report"],
                                                                                    id="btn-generate-report",
                                                                                    color="danger",
                                                                                    className="w-100"
                                                                                )
                                                                            ]
                                                                        )
                                                                    ])
                                                                ]
                                                            )
                                                        ], xs=12, sm=12, md=4, className="mb-4")
                                                    ])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),

                    # Features section (shown when no data is uploaded)
                    html.Div(
                        id='features-section',
                        children=[
                            html.H3("Professional Data Analysis Features",
                                    className="text-center mb-5"),
                            dbc.Row([
                                # Statistical Analysis
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-chart-line feature-icon"),
                                                html.H4(
                                                    "Statistical Analysis", className="mb-3"),
                                                html.P(
                                                    "Comprehensive statistical analysis including descriptive statistics, correlation analysis, and hypothesis testing.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4"),

                                # Data Visualization
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-chart-bar feature-icon"),
                                                html.H4(
                                                    "Data Visualization", className="mb-3"),
                                                html.P(
                                                    "Interactive and customizable visualizations to explore and present your data effectively.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4"),

                                # Automated Insights
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-lightbulb feature-icon"),
                                                html.H4(
                                                    "Automated Insights", className="mb-3"),
                                                html.P(
                                                    "AI-powered insights and recommendations based on your data patterns and trends.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4"),

                                # Data Cleaning
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-broom feature-icon"),
                                                html.H4("Data Cleaning",
                                                        className="mb-3"),
                                                html.P(
                                                    "Automatic detection and handling of missing values, outliers, and inconsistencies in your data.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4"),

                                # Professional Reports
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-file-pdf feature-icon"),
                                                html.H4(
                                                    "Professional Reports", className="mb-3"),
                                                html.P(
                                                    "Generate comprehensive PDF reports with visualizations, insights, and recommendations.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4"),

                                # Multiple Export Options
                                dbc.Col([
                                    dbc.Card(
                                        className='feature-card h-100',
                                        children=[
                                            dbc.CardBody([
                                                html.I(
                                                    className="fas fa-file-export feature-icon"),
                                                html.H4(
                                                    "Multiple Export Options", className="mb-3"),
                                                html.P(
                                                    "Export your data and analysis results in various formats including CSV, Excel, and PDF.")
                                            ])
                                        ]
                                    )
                                ], xs=12, sm=6, md=4, className="mb-4")
                            ])
                        ]
                    )
                ]
            ),

            # Footer
            html.Footer(
                className='mt-5 py-4 text-center',
                children=[
                    html.P(
                        "DataAnalyst Pro - Professional Data Analysis & Visualization Platform", className="mb-0")
                ]
            ),

            # Theme toggle button
            html.Button(
                id='theme-toggle',
                className='theme-toggle btn btn-primary',
                children=[html.I(className="fas fa-moon")]
            ),

            # Download components
            dcc.Download(id="download-csv"),
            dcc.Download(id="download-excel"),
            dcc.Download(id="download-report")
        ]
    )
])

# Callback for theme toggle


@app.callback(
    Output('main-container', 'data-theme'),
    Output('theme-toggle', 'children'),
    Input('theme-toggle', 'n_clicks'),
    State('main-container', 'data-theme')
)
def toggle_theme(n_clicks, current_theme):
    if n_clicks is None:
        return None, html.I(className="fas fa-moon")

    if current_theme == 'dark' or current_theme is None:
        return 'light', html.I(className="fas fa-moon")
    else:
        return 'dark', html.I(className="fas fa-sun")

# Callback for file upload


@app.callback(
    [Output('stored-data', 'data'),
     Output('upload-status', 'children'),
     Output('metrics-section', 'style'),
     Output('analysis-section', 'style'),
     Output('features-section', 'style')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def process_upload(contents, filename):
    if contents is None:
        return None, None, {
            'display': 'none'}, {
            'display': 'none'}, {
            'display': 'block'}

    try:
        # Initialize error handler
        error_handler = ErrorHandler()

        # Process the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            # Determine file type and read accordingly
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return None, dbc.Alert(
                    [html.I(className="fas fa-exclamation-triangle me-2"),
                     "Unsupported file type. Please upload CSV or Excel file."],
                    color="danger",
                    className="mt-3"
                ), {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

            # Return success message and store data
            success_msg = dbc.Alert(
                [
                    html.I(className="fas fa-check-circle me-2"),
                    f"Successfully loaded {filename} with {df.shape[0]} rows and {df.shape[1]} columns."
                ],
                color="success",
                className="mt-3"
            )

            return df.to_json(
                date_format='iso', orient='split'), success_msg, {
                'display': 'block'}, {
                'display': 'block'}, {
                'display': 'none'}

        except Exception as e:
            error_msg = error_handler.handle_error(e, "Error processing file")
            return None, error_msg, {
                'display': 'none'}, {
                'display': 'none'}, {
                'display': 'block'}

    except Exception as e:
        error_msg = dbc.Alert(
            [html.I(className="fas fa-exclamation-triangle me-2"),
             f"Error processing file: {str(e)}"],
            color="danger",
            className="mt-3"
        )
        return None, error_msg, {
            'display': 'none'}, {
            'display': 'none'}, {
            'display': 'block'}

# Callback to update metric cards


@app.callback(
    [Output('metric-records', 'children'),
     Output('metric-columns', 'children'),
     Output('metric-numeric', 'children'),
     Output('metric-categorical', 'children')],
    Input('stored-data', 'data')
)
def update_metrics(data):
    if data is None:
        return "0", "0", "0", "0"

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Calculate metrics
        total_records = len(df)
        total_columns = len(df.columns)
        numeric_cols = len(df.select_dtypes(include=['number']).columns)
        categorical_cols = len(df.select_dtypes(
            include=['object', 'category']).columns)

        return f"{total_records:,}", f"{total_columns}", f"{numeric_cols}", f"{categorical_cols}"

    except Exception as e:
        print(f"Error updating metrics: {str(e)}")
        return "0", "0", "0", "0"

# Callback for data table


@app.callback(
    Output('data-table-container', 'children'),
    Input('stored-data', 'data')
)
def update_data_table(data):
    if data is None:
        return html.Div("No data uploaded yet.")

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Create data table
        table = dash_table.DataTable(
            data=df.head(50).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'var(--primary-color)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'backgroundColor': 'var(--card-bg)',
                'color': 'var(--text-color)',
                'textAlign': 'left',
                'padding': '8px'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgba(0, 0, 0, 0.05)'
                }
            ]
        )

        return table

    except Exception as e:
        return html.Div(f"Error displaying data: {str(e)}")

# Callback for data summary


@app.callback(
    Output('data-summary-container', 'children'),
    Input('stored-data', 'data')
)
def update_data_summary(data):
    if data is None:
        return html.Div("No data uploaded yet.")

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Create summary components
        summary_components = [
            # Data types
            dbc.Row([
                dbc.Col([
                    html.H5("Data Types", className="mb-3"),
                    dash_table.DataTable(
                        data=[{'Column': col,
                               'Type': str(dtype)} for col,
                              dtype in df.dtypes.items()],
                        columns=[
                            {'name': 'Column', 'id': 'Column'},
                            {'name': 'Type', 'id': 'Type'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'var(--primary-color)',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'var(--card-bg)',
                            'color': 'var(--text-color)',
                            'textAlign': 'left',
                            'padding': '8px'
                        }
                    )
                ], width=12, className="mb-4")
            ]),

            # Missing values
            dbc.Row([
                dbc.Col([
                    html.H5("Missing Values", className="mb-3"),
                    dash_table.DataTable(
                        data=[{'Column': col, 'Missing': int(df[col].isna().sum(
                        )), 'Percentage': f"{df[col].isna().mean() * 100:.2f}%"} for col in df.columns],
                        columns=[
                            {'name': 'Column', 'id': 'Column'},
                            {'name': 'Missing', 'id': 'Missing'},
                            {'name': 'Percentage', 'id': 'Percentage'}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'var(--primary-color)',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'var(--card-bg)',
                            'color': 'var(--text-color)',
                            'textAlign': 'left',
                            'padding': '8px'
                        }
                    )
                ], width=12, className="mb-4")
            ]),

            # Descriptive statistics
            dbc.Row([
                dbc.Col([
                    html.H5("Descriptive Statistics", className="mb-3"),
                    dash_table.DataTable(
                        data=df.describe().reset_index().rename(
                            columns={'index': 'Statistic'}).to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.describe().reset_index().rename(
                            columns={'index': 'Statistic'}).columns],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'var(--primary-color)',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'var(--card-bg)',
                            'color': 'var(--text-color)',
                            'textAlign': 'left',
                            'padding': '8px'
                        }
                    )
                ], width=12)
            ])
        ]

        return summary_components

    except Exception as e:
        return html.Div(f"Error generating data summary: {str(e)}")

# Callback for statistical analysis


@app.callback(
    Output('stats-variable-selector', 'options'),
    Input('stored-data', 'data')
)
def update_variable_options(data):
    if data is None:
        return []

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Create options for dropdown
        options = [{'label': col, 'value': col} for col in df.columns]

        return options

    except Exception as e:
        print(f"Error updating variable options: {str(e)}")
        return []

# Callback for statistical analysis content


@app.callback(
    Output('stats-content', 'children'),
    [Input('stats-variable-selector', 'value'),
     Input('stored-data', 'data')]
)
def update_stats_content(selected_vars, data):
    if data is None or not selected_vars:
        return html.Div("Please select variables for analysis.")

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Filter selected variables
        df_selected = df[selected_vars]

        # Initialize statistical analyzer
        statistical_analyzer = StatisticalAnalyzer()

        # Perform analysis
        analysis_results = statistical_analyzer.analyze(df_selected)

        # Create content components
        stats_components = []

        # Descriptive statistics
        stats_components.append(
            dbc.Row([
                dbc.Col([
                    html.H5("Descriptive Statistics", className="mb-3"),
                    dash_table.DataTable(
                        data=df_selected.describe().reset_index().rename(columns={'index': 'Statistic'}).to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df_selected.describe().reset_index().rename(columns={'index': 'Statistic'}).columns],
                        style_table={'overflowX': 'auto'},
                        style_header={
                            'backgroundColor': 'var(--primary-color)',
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_cell={
                            'backgroundColor': 'var(--card-bg)',
                            'color': 'var(--text-color)',
                            'textAlign': 'left',
                            'padding': '8px'
                        }
                    )
                ], width=12, className="mb-4")
            ])
        )

        # Correlation matrix for numeric variables
        numeric_vars = df_selected.select_dtypes(include=['number']).columns
        if len(numeric_vars) > 1:
            corr_matrix = df_selected[numeric_vars].corr()

            stats_components.append(
                dbc.Row([
                    dbc.Col([
                        html.H5("Correlation Matrix", className="mb-3"),
                        dcc.Graph(
                            figure=px.imshow(
                                corr_matrix,
                                color_continuous_scale='RdBu_r',
                                zmin=-1, zmax=1,
                                labels=dict(color="Correlation")
                            ).update_layout(
                                template="plotly_white",
                                height=500
                            )
                        )
                    ], width=12, className="mb-4")
                ])
            )

        return stats_components

    except Exception as e:
        return html.Div(f"Error generating statistical analysis: {str(e)}")

# Callbacks for visualization


@app.callback(
    [Output('x-axis-selector', 'options'),
     Output('y-axis-selector', 'options')],
    Input('stored-data', 'data')
)
def update_axis_options(data):
    if data is None:
        return [], []

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Create options for dropdown
        options = [{'label': col, 'value': col} for col in df.columns]

        return options, options

    except Exception as e:
        print(f"Error updating axis options: {str(e)}")
        return [], []

# Callback for generating chart


@app.callback(
    Output('viz-content', 'children'),
    [Input('btn-generate-chart', 'n_clicks')],
    [State('chart-type-selector', 'value'),
     State('x-axis-selector', 'value'),
     State('y-axis-selector', 'value'),
     State('stored-data', 'data')]
)
def generate_chart(n_clicks, chart_type, x_axis, y_axis, data):
    if n_clicks is None or data is None:
        return html.Div(
            "Select chart type and variables, then click 'Generate Chart'.")

    if x_axis is None:
        return html.Div("Please select an X-axis variable.")

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Initialize visualizer
        visualizer = Visualizer()

        # Generate chart based on type
        if chart_type == 'bar':
            if y_axis is None:
                fig = px.bar(df, x=x_axis)
            else:
                fig = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == 'line':
            if y_axis is None:
                fig = px.line(df, x=x_axis)
            else:
                fig = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == 'scatter':
            if y_axis is None:
                return html.Div(
                    "Scatter plots require both X and Y axis variables.")
            fig = px.scatter(df, x=x_axis, y=y_axis)
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_axis)
        elif chart_type == 'box':
            if y_axis is None:
                fig = px.box(df, x=x_axis)
            else:
                fig = px.box(df, x=x_axis, y=y_axis)
        elif chart_type == 'heatmap':
            if y_axis is None:
                return html.Div(
                    "Heatmaps require both X and Y axis variables.")
            # For heatmap, we need to pivot the data
            try:
                pivot_df = df.pivot_table(
                    index=x_axis, columns=y_axis, aggfunc='size', fill_value=0)
                fig = px.imshow(pivot_df, color_continuous_scale='Viridis')
            except Exception:
                return html.Div(
                    "Could not create heatmap with selected variables. Try different variables.")
        else:
            return html.Div("Unsupported chart type.")

        # Update layout
        fig.update_layout(
            template="plotly_white",
            height=600,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        return dcc.Graph(figure=fig)

    except Exception as e:
        return html.Div(f"Error generating chart: {str(e)}")

# Callback for insights


@app.callback(
    Output('insights-content', 'children'),
    Input('stored-data', 'data')
)
def update_insights(data):
    if data is None:
        return html.Div("No data uploaded yet.")

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Generate insights
        insights = []

        # Basic dataset insights
        insights.append(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Dataset Overview", className="card-title"),
                    html.P(f"Your dataset contains {df.shape[0]} records with {df.shape[1]} variables."),
                    html.P(f"There are {len(df.select_dtypes(include=['number']).columns)} numeric variables and {len(df.select_dtypes(exclude=['number']).columns)} categorical variables.")
                ]),
                className="mb-4"
            )
        )

        # Missing values insights
        missing_data = df.isna().sum()
        missing_cols = missing_data[missing_data > 0]
        if len(missing_cols) > 0:
            insights.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Missing Data", className="card-title"),
                        html.P(f"Your dataset contains missing values in {len(missing_cols)} columns."),
                        html.Ul([
                            html.Li(f"{col}: {missing_data[col]} missing values ({missing_data[col]/len(df)*100:.2f}%)")
                            for col in missing_cols.index
                        ])
                    ]),
                    className="mb-4"
                )
            )

        # Correlation insights
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.shape[1] > 1:
            corr_matrix = numeric_df.corr()
            # Get top 5 correlations
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    corr_pairs.append(
                        (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

            # Sort by absolute correlation
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

            if corr_pairs:
                insights.append(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Correlation Analysis", className="card-title"),
                            html.P("Top correlations between variables:"),
                            html.Ul([
                                html.Li(f"{pair[0]} and {pair[1]}: {pair[2]:.2f} ({interpret_correlation(pair[2])})")
                                for pair in corr_pairs[:5]
                            ])
                        ]),
                        className="mb-4"
                    )
                )

        # Recommendations
        recommendations = []

        # Check for missing values
        if missing_data.sum() > 0:
            recommendations.append(
                "Consider handling missing values using imputation techniques or removing rows/columns with excessive missing data.")

        # Check for outliers in numeric columns
        outlier_cols = []
        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = numeric_df[(numeric_df[col] < lower_bound) | (
                numeric_df[col] > upper_bound)][col]
            if len(outliers) > 0:
                outlier_cols.append((col, len(outliers)))

        if outlier_cols:
            recommendations.append(
                "Consider addressing outliers in the following columns: " +
                ", ".join(
                    [
                        f"{col} ({count} outliers)" for col,
                        count in outlier_cols]))

        # Check for high cardinality in categorical columns
        cat_df = df.select_dtypes(exclude=['number'])
        high_card_cols = []
        for col in cat_df.columns:
            if df[col].nunique() > 20:
                high_card_cols.append((col, df[col].nunique()))

        if high_card_cols:
            recommendations.append(
                "Consider grouping or encoding high cardinality categorical variables: " +
                ", ".join(
                    [
                        f"{col} ({count} unique values)" for col,
                        count in high_card_cols]))

        if recommendations:
            insights.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Recommendations", className="card-title"),
                        html.Ul([html.Li(rec) for rec in recommendations])
                    ]),
                    className="mb-4"
                )
            )

        return insights

    except Exception as e:
        return html.Div(f"Error generating insights: {str(e)}")

# Helper function to interpret correlation


def interpret_correlation(corr):
    if abs(corr) < 0.3:
        return "weak correlation"
    elif abs(corr) < 0.7:
        return "moderate correlation"
    else:
        return "strong correlation"

# Callback for CSV export


@app.callback(
    Output('download-csv', 'data'),
    Input('btn-export-csv', 'n_clicks'),
    State('stored-data', 'data')
)
def export_csv(n_clicks, data):
    if n_clicks is None or data is None:
        return None

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Return CSV for download
        return dcc.send_data_frame(
            df.to_csv,
            f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            index=False)

    except Exception as e:
        print(f"Error exporting CSV: {str(e)}")
        return None

# Callback for Excel export


@app.callback(
    Output('download-excel', 'data'),
    Input('btn-export-excel', 'n_clicks'),
    State('stored-data', 'data')
)
def export_excel(n_clicks, data):
    if n_clicks is None or data is None:
        return None

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Return Excel for download
        return dcc.send_data_frame(
            df.to_excel,
            f"data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            index=False,
            sheet_name="Data")

    except Exception as e:
        print(f"Error exporting Excel: {str(e)}")
        return None

# Callback for PDF report generation


@app.callback(
    Output('download-report', 'data'),
    Input('btn-generate-report', 'n_clicks'),
    State('stored-data', 'data')
)
def generate_report(n_clicks, data):
    if n_clicks is None or data is None:
        return None

    try:
        # Parse the stored data
        df = pd.read_json(data, orient='split')

        # Initialize report generator
        report_generator = ReportGenerator()

        # Generate report
        # Create analysis results dictionary for the report
        analysis_results = {}

        # Get statistical analyzer
        from modules.statistical_analyzer import StatisticalAnalyzer
        stat_analyzer = StatisticalAnalyzer()

        # Add basic statistics to analysis_results
        analysis_results['numeric_columns'] = df.select_dtypes(
            include=['number']).columns.tolist()
        analysis_results['categorical_columns'] = df.select_dtypes(
            exclude=['number']).columns.tolist()

        # Calculate missing values percentage
        missing_percentage = (df.isna().sum().sum() /
                              (df.shape[0] * df.shape[1]) * 100).round(2)
        analysis_results['missing_percentage'] = missing_percentage

        # Calculate descriptive statistics
        analysis_results['descriptive_stats'] = stat_analyzer.get_numerical_statistics(
            df).to_dict()

        # Calculate outliers
        outlier_count = 0
        for col in analysis_results['numeric_columns']:
            outliers = stat_analyzer.identify_outliers(df, col)
            outlier_count += outliers.sum()
        analysis_results['outlier_count'] = outlier_count

        # Calculate correlations
        corr_matrix = stat_analyzer.calculate_correlation_matrix(df)
        if not corr_matrix.empty:
            # Find strongest correlation
            strongest_corr = {'pair': 'N/A', 'value': 0}
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > abs(
                            strongest_corr['value']):
                        strongest_corr['pair'] = f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]}"
                        strongest_corr['value'] = corr_matrix.iloc[i, j]
            analysis_results['strongest_correlation'] = strongest_corr

        # Add patterns and recommendations
        analysis_results['patterns'] = []
        analysis_results['recommendations'] = []

        # Compute recommendations similar to insights
        missing_data = df.isna().sum().sum()
        if missing_data > 0:
            analysis_results['recommendations'].append(
                "Consider handling missing values using imputation techniques or removing rows/columns with excessive missing data.")

        # Check for outliers
        numeric_df = df.select_dtypes(include=['number'])
        outlier_cols = []
        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = numeric_df[(numeric_df[col] < lower_bound) | (
                numeric_df[col] > upper_bound)][col]
            if len(outliers) > 0:
                outlier_cols.append((col, len(outliers)))

        if outlier_cols:
            analysis_results['recommendations'].append(
                "Consider addressing outliers in the following columns: " +
                ", ".join(
                    [
                        f"{col} ({count} outliers)" for col,
                        count in outlier_cols]))

        # Check for high cardinality
        cat_df = df.select_dtypes(exclude=['number'])
        high_card_cols = []
        for col in cat_df.columns:
            if df[col].nunique() > 20:
                high_card_cols.append((col, df[col].nunique()))

        if high_card_cols:
            analysis_results['recommendations'].append(
                "Consider grouping or encoding high cardinality categorical variables: " +
                ", ".join(
                    [
                        f"{col} ({count} unique values)" for col,
                        count in high_card_cols]))

        # Add some patterns from correlations
        if 'strongest_correlation' in analysis_results and analysis_results[
                'strongest_correlation']['pair'] != 'N/A':
            pair = analysis_results['strongest_correlation']['pair']
            value = analysis_results['strongest_correlation']['value']
            analysis_results['patterns'].append(
                f"Strong correlation between {pair} ({value:.2f})")

        # Generate PDF report using the correct method name
        report_filename = report_generator.generate_pdf_report(
            df, analysis_results)

        # Return report for download
        with open(report_filename, 'rb') as f:
            report_bytes = f.read()

        return dcc.send_bytes(
            report_bytes,
            f"data_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return None


# Create necessary directories
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('reports'):
    os.makedirs('reports')

# Run the app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=False)
