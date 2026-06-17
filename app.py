import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Personal Insights Analyzer",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.write("Upload your file and explore the data")

# Main Title
st.title("📊 Personal Insights Analyzer")
st.markdown("Analyze your Excel data in seconds")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "csv"]
)

if uploaded_file is not None:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.sidebar.success("File uploaded successfully")
    st.sidebar.info("Select columns and explore insights")

    # Data Preview
    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # Dataset Info
    info1, info2 = st.columns(2)

    info1.metric(
        "Rows",
        df.shape[0]
    )

    info2.metric(
        "Columns",
        df.shape[1]
    )

    # Statistics
    st.subheader("📈 Basic Statistics")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:

        # Column Selection
        st.subheader("📊 Column Selection")

        selected_column = st.selectbox(
            "Choose a column",
            numeric_columns
        )

        # KPIs
        st.subheader("📌 Key Metrics")

        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            "Average",
            round(df[selected_column].mean(), 2)
        )

        kpi2.metric(
            "Maximum",
            round(df[selected_column].max(), 2)
        )

        kpi3.metric(
            "Minimum",
            round(df[selected_column].min(), 2)
        )

        # Charts
        st.subheader("📉 Visualizations")

        chart1, chart2 = st.columns(2)

        with chart1:
            st.line_chart(df[selected_column])

        with chart2:
            st.bar_chart(df[selected_column])

        # Pie Chart
        st.subheader("🥧 Pie Chart")

        fig_pie = px.pie(
            df,
            values=selected_column,
            names=df.index,
            title=f"{selected_column} Distribution"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        # Correlation Analysis
        st.subheader("🔗 Correlation Analysis")

        col_a = st.selectbox(
            "Select First Column",
            numeric_columns,
            key="col_a"
        )

        col_b = st.selectbox(
            "Select Second Column",
            numeric_columns,
            key="col_b"
        )

        correlation = df[col_a].corr(
            df[col_b]
        )

        st.metric(
            "Correlation",
            round(correlation, 2)
        )

        if correlation > 0.5:
            st.success(
                f"There is a strong positive relationship between {col_a} and {col_b}"
            )

        elif correlation < -0.5:
            st.error(
                f"There is a strong negative relationship between {col_a} and {col_b}"
            )

        else:
            st.info(
                f"No strong relationship detected between {col_a} and {col_b}"
            )

        # Scatter Plot
        st.subheader("🎯 Scatter Plot")

        fig_scatter = px.scatter(
            df,
            x=col_a,
            y=col_b,
            title=f"{col_a} vs {col_b}"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        # Auto Insights
        st.subheader("🤖 Auto Insights")

        max_value = df[selected_column].max()
        min_value = df[selected_column].min()
        avg_value = df[selected_column].mean()

        st.success(
            f"""
Average: {avg_value:.2f}

Maximum: {max_value}

Minimum: {min_value}
"""
        )

        # Download
        st.subheader("⬇️ Download Data")

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )