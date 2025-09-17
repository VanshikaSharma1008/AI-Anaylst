import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

class Visualizer:
    """
    Class for creating interactive visualizations of data.
    Includes distribution plots, scatter plots, box plots, and bar charts.
    """
    
    def __init__(self):
        """Initialize the Visualizer class."""
        # Set default template for dark theme
        self.template = "plotly_dark"
        self.color_scale = "Viridis"
    
    def create_distribution_plot(self, df, column):
        """
        Create a distribution plot for a numeric column.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            column (str): The column to visualize
            
        Returns:
            plotly.graph_objects.Figure: The distribution plot
        """
        if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
            # Return empty figure if column is not valid
            return go.Figure()
        
        # Create histogram with density curve
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Histogram(
            x=df[column],
            name='Histogram',
            opacity=0.7,
            marker_color='rgba(73, 160, 181, 0.7)',
            nbinsx=30,
            histnorm='probability density'
        ))
        
        # Add kernel density estimate
        try:
            # Calculate KDE
            kde_x = np.linspace(df[column].min(), df[column].max(), 1000)
            kde_y = df[column].plot.kde().get_lines()[0].get_ydata()
            kde_x_actual = np.linspace(df[column].min(), df[column].max(), len(kde_y))
            
            # Add KDE trace
            fig.add_trace(go.Scatter(
                x=kde_x_actual,
                y=kde_y,
                mode='lines',
                name='Density',
                line=dict(color='rgba(231, 107, 243, 1)', width=2)
            ))
            
            # Add mean line
            mean_val = df[column].mean()
            fig.add_vline(
                x=mean_val,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mean: {mean_val:.2f}",
                annotation_position="top right"
            )
            
            # Add median line
            median_val = df[column].median()
            fig.add_vline(
                x=median_val,
                line_dash="dot",
                line_color="green",
                annotation_text=f"Median: {median_val:.2f}",
                annotation_position="top left"
            )
        except:
            # Skip KDE if it fails
            pass
        
        # Update layout
        fig.update_layout(
            title={
                'text': f'Distribution of {column}',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title=column,
            yaxis_title='Density',
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        return fig
    
    def create_scatter_matrix(self, df, columns):
        """
        Create a scatter plot matrix for selected numeric columns.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            columns (list): The columns to include in the scatter matrix
            
        Returns:
            plotly.graph_objects.Figure: The scatter plot matrix
        """
        if not columns or not all(col in df.columns for col in columns):
            # Return empty figure if columns are not valid
            return go.Figure()
        
        # Filter DataFrame to include only selected columns
        plot_df = df[columns].copy()
        
        # Create scatter matrix
        fig = px.scatter_matrix(
            plot_df,
            dimensions=columns,
            color_discrete_sequence=['rgba(73, 160, 181, 0.7)'],
            opacity=0.7
        )
        
        # Update layout
        fig.update_layout(
            title='Scatter Plot Matrix',
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Update traces
        fig.update_traces(diagonal_visible=False)
        
        return fig
    
    def create_box_plot(self, df, column):
        """
        Create a box plot for a numeric column.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            column (str): The column to visualize
            
        Returns:
            plotly.graph_objects.Figure: The box plot
        """
        if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
            # Return empty figure if column is not valid
            return go.Figure()
        
        # Create box plot
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=df[column],
            name=column,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=-1.8,
            boxmean=True,
            fillcolor='rgba(73, 160, 181, 0.7)',
            line=dict(color='rgba(73, 160, 181, 1)'),
            marker=dict(
                color='rgba(231, 107, 243, 0.7)',
                line=dict(color='rgba(231, 107, 243, 1)', width=1)
            )
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Box Plot of {column}',
            yaxis_title=column,
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_bar_chart(self, df, column):
        """
        Create a bar chart for a categorical column.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            column (str): The column to visualize
            
        Returns:
            plotly.graph_objects.Figure: The bar chart
        """
        if column not in df.columns:
            # Return empty figure if column is not valid
            return go.Figure()
        
        # Count values
        value_counts = df[column].value_counts().reset_index()
        value_counts.columns = [column, 'count']
        
        # Limit to top 20 categories if there are too many
        if len(value_counts) > 20:
            value_counts = value_counts.head(20)
            title = f'Top 20 Categories in {column}'
        else:
            title = f'Categories in {column}'
        
        # Create bar chart
        fig = px.bar(
            value_counts,
            x=column,
            y='count',
            color_discrete_sequence=['rgba(73, 160, 181, 0.7)'],
            opacity=0.9
        )
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title=column,
            yaxis_title='Count',
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_correlation_heatmap(self, df):
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            
        Returns:
            plotly.graph_objects.Figure: The correlation heatmap
        """
        # Get numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty or numeric_df.shape[1] < 2:
            # Return empty figure if not enough numeric columns
            return go.Figure()
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1,
            text_auto='.2f'
        )
        
        # Update layout
        fig.update_layout(
            title='Correlation Heatmap',
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_grouped_bar_chart(self, df, cat_column, num_column):
        """
        Create a grouped bar chart for a categorical and numeric column.
        
        Args:
            df (pandas.DataFrame): The DataFrame containing the data
            cat_column (str): The categorical column
            num_column (str): The numeric column
            
        Returns:
            plotly.graph_objects.Figure: The grouped bar chart
        """
        if cat_column not in df.columns or num_column not in df.columns:
            # Return empty figure if columns are not valid
            return go.Figure()
        
        # Group by categorical column and calculate mean of numeric column
        grouped_df = df.groupby(cat_column)[num_column].mean().reset_index()
        
        # Limit to top 15 categories if there are too many
        if len(grouped_df) > 15:
            grouped_df = grouped_df.sort_values(num_column, ascending=False).head(15)
            title = f'Top 15 {cat_column} by Average {num_column}'
        else:
            title = f'Average {num_column} by {cat_column}'
        
        # Create bar chart
        fig = px.bar(
            grouped_df,
            x=cat_column,
            y=num_column,
            color_discrete_sequence=['rgba(73, 160, 181, 0.7)'],
            opacity=0.9
        )
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title=cat_column,
            yaxis_title=f'Average {num_column}',
            template=self.template,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig