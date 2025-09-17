import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

class ReportGenerator:
    """
    Class for generating PDF reports with analysis results and visualizations.
    """
    
    def __init__(self):
        """Initialize the ReportGenerator class."""
        self.styles = getSampleStyleSheet()
        # Create custom styles
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        self.styles.add(ParagraphStyle(
            name='ReportHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.darkblue
        ))
        self.styles.add(ParagraphStyle(
            name='ReportNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8
        ))
        
    def generate_pdf_report(self, df, analysis_results):
        """
        Generate a PDF report with analysis results and visualizations.
        
        Args:
            df (pandas.DataFrame): The processed DataFrame
            analysis_results (dict): Dictionary containing analysis results
            
        Returns:
            str: Path to the generated PDF report
        """
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Create report filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"reports/data_analysis_report_{timestamp}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(report_filename, pagesize=letter)
        
        # Create story (content)
        story = []
        
        # Add title
        story.append(Paragraph("Data Analysis Report", self.styles['ReportTitle']))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['ReportNormal']))
        story.append(Spacer(1, 0.25*inch))
        
        # Add executive summary
        story.append(Paragraph("Executive Summary", self.styles['ReportHeading2']))
        story.append(Paragraph(f"The dataset contains {df.shape[0]} records with {df.shape[1]} variables.", self.styles['ReportNormal']))
        story.append(Paragraph(f"Missing values: {analysis_results['missing_percentage']}% of the dataset", self.styles['ReportNormal']))
        story.append(Paragraph(f"Numeric columns: {len(analysis_results['numeric_columns'])}", self.styles['ReportNormal']))
        story.append(Paragraph(f"Categorical columns: {len(analysis_results['categorical_columns'])}", self.styles['ReportNormal']))
        story.append(Paragraph(f"Outliers detected: {analysis_results['outlier_count']} across all numeric variables", self.styles['ReportNormal']))
        
        if 'strongest_correlation' in analysis_results and analysis_results['strongest_correlation']['pair'] != 'N/A':
            corr_pair = analysis_results['strongest_correlation']['pair']
            corr_value = analysis_results['strongest_correlation']['value']
            story.append(Paragraph(f"Strongest correlation: {corr_pair} ({corr_value:.2f})", self.styles['ReportNormal']))
        
        story.append(Spacer(1, 0.25*inch))
        
        # Add data overview
        story.append(Paragraph("Data Overview", self.styles['ReportHeading2']))
        
        # Add descriptive statistics table
        if 'descriptive_stats' in analysis_results and analysis_results['descriptive_stats']:
            story.append(Paragraph("Descriptive Statistics", self.styles['ReportHeading2']))
            
            # Create descriptive statistics table
            desc_stats_df = df.describe().reset_index()
            desc_stats_data = [[''] + list(desc_stats_df.columns[1:])]
            for _, row in desc_stats_df.iterrows():
                row_data = [row['index']]
                for col in desc_stats_df.columns[1:]:
                    try:
                        row_data.append(f"{row[col]:.2f}")
                    except:
                        row_data.append(str(row[col]))
                desc_stats_data.append(row_data)
            
            # Create table
            desc_stats_table = Table(desc_stats_data)
            desc_stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(desc_stats_table)
            story.append(Spacer(1, 0.25*inch))
        
        # Add visualizations
        story.append(Paragraph("Data Visualizations", self.styles['ReportHeading2']))
        
        # Add distribution plots for numeric columns (up to 3)
        for i, col in enumerate(analysis_results['numeric_columns'][:3]):
            story.append(Paragraph(f"Distribution of {col}", self.styles['ReportNormal']))
            
            # Create distribution plot
            plt.figure(figsize=(6, 4))
            sns.histplot(df[col], kde=True)
            plt.title(f"Distribution of {col}")
            plt.tight_layout()
            
            # Save plot to BytesIO
            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            plt.close()
            
            # Add image to story
            img = Image(img_data, width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.25*inch))
        
        # Add correlation heatmap if there are numeric columns
        if len(analysis_results['numeric_columns']) >= 2:
            story.append(Paragraph("Correlation Heatmap", self.styles['Normal']))
            
            # Create correlation heatmap
            plt.figure(figsize=(7, 5))
            corr_matrix = df[analysis_results['numeric_columns']].corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title("Correlation Heatmap")
            plt.tight_layout()
            
            # Save plot to BytesIO
            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            plt.close()
            
            # Add image to story
            img = Image(img_data, width=7*inch, height=5*inch)
            story.append(img)
            story.append(Spacer(1, 0.25*inch))
        
        # Add insights and recommendations
        story.append(Paragraph("Insights & Recommendations", self.styles['Heading2']))
        
        # Add patterns
        if 'patterns' in analysis_results and analysis_results['patterns']:
            story.append(Paragraph("Identified Patterns:", self.styles['Normal']))
            for pattern in analysis_results['patterns']:
                story.append(Paragraph(f"• {pattern}", self.styles['Normal']))
            story.append(Spacer(1, 0.15*inch))
        
        # Add recommendations
        if 'recommendations' in analysis_results and analysis_results['recommendations']:
            story.append(Paragraph("Recommendations:", self.styles['Normal']))
            for recommendation in analysis_results['recommendations']:
                story.append(Paragraph(f"• {recommendation}", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return report_filename