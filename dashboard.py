import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Call Report Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data(file):
    """Load data from CSV or Excel file"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def validate_data(df):
    """Validate that the dataframe has expected columns"""
    required_columns = ['representative', 'doctor', 'division', 'date']
    missing_columns = [col for col in required_columns if col not in [c.lower() for c in df.columns]]
    
    if missing_columns:
        st.warning(f"Note: Some recommended columns are missing: {missing_columns}")
        st.info("The dashboard will work best with columns: representative, doctor, division, date, and optionally: call_type, outcome, product, location")
    
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower().str.strip()
    return df

def get_key_metrics(df):
    """Calculate key metrics from the data"""
    metrics = {}
    
    # Total calls
    metrics['total_calls'] = len(df)
    
    # Unique representatives
    if 'representative' in df.columns:
        metrics['total_reps'] = df['representative'].nunique()
    
    # Unique doctors
    if 'doctor' in df.columns:
        metrics['total_doctors'] = df['doctor'].nunique()
    
    # Unique divisions
    if 'division' in df.columns:
        metrics['total_divisions'] = df['division'].nunique()
    
    return metrics

def create_rep_performance_chart(df):
    """Create representative performance chart"""
    if 'representative' not in df.columns:
        return None
    
    rep_counts = df['representative'].value_counts().reset_index()
    rep_counts.columns = ['Representative', 'Number of Calls']
    
    fig = px.bar(rep_counts.head(10), 
                 x='Representative', 
                 y='Number of Calls',
                 title='Top 10 Representatives by Number of Calls',
                 color='Number of Calls',
                 color_continuous_scale='Blues')
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_division_analysis_chart(df):
    """Create division-wise analysis chart"""
    if 'division' not in df.columns:
        return None
    
    division_counts = df['division'].value_counts().reset_index()
    division_counts.columns = ['Division', 'Number of Calls']
    
    fig = px.pie(division_counts, 
                 values='Number of Calls', 
                 names='Division',
                 title='Call Distribution by Division',
                 hole=0.4)
    return fig

def create_time_trend_chart(df):
    """Create time trend chart"""
    if 'date' not in df.columns:
        return None
    
    try:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        if len(df) == 0:
            return None
        
        daily_calls = df.groupby(df['date'].dt.date).size().reset_index()
        daily_calls.columns = ['Date', 'Number of Calls']
        
        fig = px.line(daily_calls, 
                     x='Date', 
                     y='Number of Calls',
                     title='Call Trend Over Time',
                     markers=True)
        fig.update_traces(line_color='#1f77b4')
        return fig
    except Exception as e:
        st.warning(f"Could not create time trend chart: {str(e)}")
        return None

def create_doctor_engagement_chart(df):
    """Create doctor engagement chart"""
    if 'doctor' not in df.columns:
        return None
    
    doctor_counts = df['doctor'].value_counts().reset_index()
    doctor_counts.columns = ['Doctor', 'Number of Visits']
    
    # Top 15 doctors
    fig = px.bar(doctor_counts.head(15), 
                 x='Number of Visits', 
                 y='Doctor',
                 orientation='h',
                 title='Top 15 Most Visited Doctors',
                 color='Number of Visits',
                 color_continuous_scale='Greens')
    return fig

def create_cross_analysis(df):
    """Create cross-analysis between divisions and representatives"""
    if 'division' not in df.columns or 'representative' not in df.columns:
        return None
    
    cross_tab = pd.crosstab(df['division'], df['representative'])
    
    fig = px.imshow(cross_tab,
                    labels=dict(x="Representative", y="Division", color="Calls"),
                    title='Calls Heatmap: Division vs Representative',
                    color_continuous_scale='YlOrRd')
    return fig

def generate_insights(df, metrics):
    """Generate business insights from the data"""
    insights = []
    
    # Representative productivity insights
    if 'representative' in df.columns:
        avg_calls_per_rep = metrics['total_calls'] / metrics['total_reps']
        insights.append(f"📊 Average calls per representative: {avg_calls_per_rep:.1f}")
        
        # Top performer
        top_rep = df['representative'].value_counts().index[0]
        top_rep_calls = df['representative'].value_counts().values[0]
        insights.append(f"🏆 Top performer: {top_rep} with {top_rep_calls} calls")
    
    # Doctor engagement insights
    if 'doctor' in df.columns:
        avg_visits_per_doctor = metrics['total_calls'] / metrics['total_doctors']
        insights.append(f"👨‍⚕️ Average visits per doctor: {avg_visits_per_doctor:.1f}")
    
    # Division insights
    if 'division' in df.columns:
        top_division = df['division'].value_counts().index[0]
        top_division_calls = df['division'].value_counts().values[0]
        insights.append(f"🏢 Most active division: {top_division} with {top_division_calls} calls")
    
    # Time-based insights
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            if len(df) > 0:
                date_range = (df['date'].max() - df['date'].min()).days
                insights.append(f"📅 Data covers {date_range} days")
                
                # Calculate daily average
                daily_avg = len(df) / max(date_range, 1)
                insights.append(f"📈 Average daily calls: {daily_avg:.1f}")
        except:
            pass
    
    return insights

def main():
    # Title and description
    st.title("📊 Call Report Dashboard")
    st.markdown("""
    This dashboard analyzes call reports to generate insights about representatives meeting doctors across divisions.
    Upload your CSV or Excel file to get started.
    """)
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload your call report file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a CSV or Excel file containing call report data"
        )
        
        st.markdown("---")
        st.markdown("### 📋 Expected Columns")
        st.markdown("""
        - **representative**: Name of the representative
        - **doctor**: Name of the doctor
        - **division**: Division name
        - **date**: Date of the call
        - *call_type* (optional): Type of call
        - *outcome* (optional): Call outcome
        - *product* (optional): Product discussed
        - *location* (optional): Location
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This dashboard helps analyze:
        - Representative performance
        - Doctor engagement patterns
        - Division-wise trends
        - Time-series analysis
        """)
    
    # Main content
    if uploaded_file is not None:
        # Load data
        df = load_data(uploaded_file)
        
        if df is not None:
            # Validate data
            df = validate_data(df)
            
            # Display file info
            st.success(f"✅ File loaded successfully: {uploaded_file.name}")
            
            # Show data preview
            with st.expander("🔍 View Data Preview", expanded=False):
                st.dataframe(df.head(100), use_container_width=True)
                st.info(f"Dataset contains {len(df)} rows and {len(df.columns)} columns")
            
            # Calculate metrics
            metrics = get_key_metrics(df)
            
            # Display key metrics
            st.header("📈 Key Metrics")
            cols = st.columns(4)
            
            col_idx = 0
            if 'total_calls' in metrics:
                cols[col_idx].metric("Total Calls", f"{metrics['total_calls']:,}")
                col_idx += 1
            
            if 'total_reps' in metrics:
                cols[col_idx % 4].metric("Representatives", f"{metrics['total_reps']:,}")
                col_idx += 1
            
            if 'total_doctors' in metrics:
                cols[col_idx % 4].metric("Doctors", f"{metrics['total_doctors']:,}")
                col_idx += 1
            
            if 'total_divisions' in metrics:
                cols[col_idx % 4].metric("Divisions", f"{metrics['total_divisions']:,}")
            
            # Generate and display insights
            st.header("💡 Key Insights")
            insights = generate_insights(df.copy(), metrics)
            for insight in insights:
                st.markdown(f"- {insight}")
            
            # Visualizations
            st.header("📊 Visualizations")
            
            # Representative performance
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_rep_performance_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_division_analysis_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Time trend
            fig = create_time_trend_chart(df.copy())
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Doctor engagement and cross analysis
            col3, col4 = st.columns(2)
            
            with col3:
                fig = create_doctor_engagement_chart(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col4:
                fig = create_cross_analysis(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Data export
            st.header("💾 Export Data")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                # Export summary statistics
                summary_df = df.describe(include='all').reset_index()
                csv_summary = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Summary Statistics (CSV)",
                    data=csv_summary,
                    file_name="call_report_summary.csv",
                    mime="text/csv"
                )
            
            with col_export2:
                # Export processed data
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Processed Data (CSV)",
                    data=csv_data,
                    file_name="call_report_processed.csv",
                    mime="text/csv"
                )
    
    else:
        # Show instructions when no file is uploaded
        st.info("👆 Please upload a CSV or Excel file using the sidebar to get started.")
        
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. Prepare your call report data with the following columns:
           - `representative`, `doctor`, `division`, `date`
        2. Upload the file using the sidebar
        3. View automatic insights and visualizations
        4. Export results for further analysis
        """)
        
        # Show sample data structure
        st.markdown("### 📝 Sample Data Structure")
        sample_data = pd.DataFrame({
            'representative': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Williams'],
            'doctor': ['Dr. Smith', 'Dr. Jones', 'Dr. Brown', 'Dr. Davis'],
            'division': ['Cardiology', 'Oncology', 'Cardiology', 'Neurology'],
            'date': ['2024-01-15', '2024-01-16', '2024-01-16', '2024-01-17'],
            'call_type': ['In-person', 'Virtual', 'In-person', 'Phone'],
            'outcome': ['Positive', 'Positive', 'Follow-up needed', 'Positive']
        })
        st.dataframe(sample_data, use_container_width=True)

if __name__ == "__main__":
    main()
