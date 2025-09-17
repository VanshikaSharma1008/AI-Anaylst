# 🤖 DataAnalyst Pro
Your Autonomous Data Science Partner

DataAnalyst Pro is an intelligent, autonomous, AI-powered web application that works like a senior data analyst on demand. With just a dataset upload, it automatically cleans, explores, and analyzes your data — delivering actionable insights, interactive visualizations, and professional reports.

Think of it as your always-on analyst: fast, reliable, and built to uncover patterns you might miss.

## ✨ Key Features

- 📂 **Seamless Data Upload** – Instantly upload CSV or Excel files. The application validates and processes them without manual setup.
- 📊 **Autonomous Statistical Analysis** – Automated data profiling, descriptive stats, correlation mapping, and outlier detection.
- 📈 **Dynamic Visualizations** – Interactive, AI-suggested charts (histograms, heatmaps, scatter plots, distributions) tailored for your dataset.
- 🔍 **AI-Curated Insights** – Trend discovery, anomaly flags, and recommendations explained in natural language.
- 📑 **One-Click Reporting** – Export polished reports (PDF, CSV, XLSX) with embedded charts and insights.
- 🎨 **Professional UI/UX** – Responsive dark/light themes, modern design, and intuitive tab-based navigation.
- 🛡️ **Robust & Error-Resilient** – Handles messy datasets gracefully with built-in AI-driven error handling.

## 🚀 Why Use It?

- **For Businesses** – Spot sales trends, anomalies, and growth opportunities automatically.
- **For Researchers** – Simplify multi-variable statistical analysis and visualize results instantly.
- **For Data Quality Checks** – Detect missing values, duplicates, and data inconsistencies.
- **For Quick Decision-Making** – Get executive-ready summaries and reports in minutes.
- **For Learners** – Understand data science concepts through AI-explained insights.

## ⚡️ Quick Start

1. Clone the Repository
   ```
   git clone https://github.com/VanshikaSharma1008/AI-Anaylst.git
   cd Data_analyst_agent
   ```

2. Set Up Environment
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   # OR
   source venv/bin/activate  # Mac/Linux
   ```

3. Install Dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run DataAnalyst Pro
   ```
   python app.py
   ```

Then open: http://127.0.0.1:8050/ in your browser.

Upload your dataset → Explore tabs for analysis → Get insights, charts, and reports instantly.

## 🧩 Tech Stack

- **Frontend/UI**: Dash, Plotly (interactive dashboards)
- **Backend/Data Processing**: Python, Pandas, NumPy
- **AI Modules**: Automated analysis & insight generation
- **Exports**: ReportLab for PDFs, native CSV/XLSX outputs

## 📂 Project Structure

- `app.py`: Core application logic and dashboard.
- `modules/`: Modular components
  - `data_processor.py`: Data upload, validation, and processing
  - `statistical_analyzer.py`: Stats, correlations, and analysis
  - `visualizer.py`: Chart generation with Plotly
  - `report_generator.py`: PDF/CSV/XLSX export
  - `error_handler.py`: Error management
- `requirements.txt`: Dependencies
- `README.md`: You're here!

## UML Class Diagram

Here's a simple UML class diagram illustrating the main classes and their relationships in DataAnalyst Pro:\n\n```mermaid\nclassDiagram\n    class App {\n        +run()\n    }\n    class DataProcessor {\n        +process_data(df: DataFrame) : DataFrame\n    }\n    class StatisticalAnalyzer {\n        +get_numerical_statistics(df: DataFrame) : DataFrame\n        +calculate_correlation_matrix(df: DataFrame) : DataFrame\n        +identify_outliers(df: DataFrame, column: str) : Series\n    }\n    class Visualizer {\n        +create_distribution_plot(df: DataFrame, column: str) : Figure\n        +create_scatter_matrix(df: DataFrame) : Figure\n        +create_correlation_heatmap(corr_matrix: DataFrame) : Figure\n    }\n    class ReportGenerator {\n        +generate_pdf_report(df: DataFrame, analysis_results: dict) : str\n    }\n    class ErrorHandler {\n        +validate_file(file_path: str) : bool\n        +validate_dataframe(df: DataFrame) : bool\n        +handle_error(e: Exception) : str\n    }\n    App --> DataProcessor : uses\n    App --> StatisticalAnalyzer : uses\n    App --> Visualizer : uses\n    App --> ReportGenerator : uses\n    App --> ErrorHandler : uses\n```

## Contributing

Fork the repo and submit a PR with your enhancements to help evolve DataAnalyst Pro!

## License

MIT License. See LICENSE file for details.