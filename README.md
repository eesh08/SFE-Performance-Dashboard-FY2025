# Call Report Dashboard 📊

A comprehensive dashboard application for analyzing call reports and generating insights about representatives meeting doctors across divisions. This tool helps solve business problems by providing actionable insights from your data.

## Features

✨ **Key Capabilities:**
- 📁 Upload CSV or Excel files
- 📈 Automatic data validation and processing
- 📊 Interactive visualizations using Plotly
- 💡 AI-powered business insights generation
- 🎯 Multiple analysis perspectives:
  - Representative performance tracking
  - Doctor engagement patterns
  - Division-wise analysis
  - Time-series trends
  - Cross-dimensional heatmaps
- 💾 Export processed data and summary statistics

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eesh08/CallReportDashboard.git
cd CallReportDashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Dashboard

Launch the dashboard using Streamlit:
```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Data Format

Your CSV or Excel file should contain the following columns:

**Required columns:**
- `representative` - Name of the sales representative
- `doctor` - Name of the doctor visited
- `division` - Medical division/specialty
- `date` - Date of the call/visit

**Optional columns:**
- `call_type` - Type of call (In-person, Virtual, Phone, etc.)
- `outcome` - Call outcome (Positive, Neutral, Follow-up needed, etc.)
- `product` - Product discussed during the call
- `location` - Location of the call

### Sample Data

A sample data file (`sample_data.csv`) is included in the repository. You can use this to test the dashboard functionality.

## Dashboard Sections

### 1. Key Metrics
- Total number of calls
- Number of unique representatives
- Number of unique doctors
- Number of divisions

### 2. Key Insights
- Average calls per representative
- Top performing representative
- Average visits per doctor
- Most active division
- Time-based trends

### 3. Visualizations
- **Representative Performance**: Bar chart showing top performers
- **Division Analysis**: Pie chart showing call distribution by division
- **Time Trends**: Line chart showing call patterns over time
- **Doctor Engagement**: Bar chart showing most visited doctors
- **Cross Analysis**: Heatmap showing division vs representative activity

### 4. Data Export
- Download summary statistics as CSV
- Download processed data as CSV

## Technology Stack

- **Streamlit**: Web application framework
- **Pandas**: Data processing and analysis
- **Plotly**: Interactive visualizations
- **openpyxl**: Excel file support
- **NumPy**: Numerical computations

## Use Cases

This dashboard is ideal for:
- 🏥 Pharmaceutical sales teams tracking doctor visits
- 📊 Sales managers monitoring team performance
- 📈 Business analysts identifying trends and patterns
- 🎯 Strategic planning based on engagement metrics
- 📉 Identifying underperforming divisions or representatives
- 🔍 Discovering high-value doctor relationships

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub. 
