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

    info1.metric("Rows", df.shape[0])
    info2.metric("Columns", df.shape[1])

    # Statistics
    st.subheader("📈 Basic Statistics")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:

        # Dataset Quality Score
        st.subheader("📊 Dataset Quality Score")

        missing_values = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        total_cells = df.shape[0] * df.shape[1]

        quality_score = max(
            0,
            round(
                100 - ((missing_values / max(total_cells, 1)) * 100),
                1
            )
        )

        q1, q2, q3 = st.columns(3)

        q1.metric("Missing Values", missing_values)
        q2.metric("Duplicate Rows", duplicate_rows)
        q3.metric("Quality Score", f"{quality_score}%")

        if quality_score >= 90:
            st.success("Excellent data quality detected.")
        elif quality_score >= 70:
            st.warning("Moderate data quality detected.")
        else:
            st.error("Poor data quality detected.")

        # Advanced Insights
        st.subheader("🏆 Advanced Insights")

        column_means = df[numeric_columns].mean()

        top_column = column_means.idxmax()
        top_value = column_means.max()

        low_column = column_means.idxmin()
        low_value = column_means.min()

        a1, a2 = st.columns(2)

        with a1:
            st.success(
                f"""
🏆 Top Performing Column

{top_column}

Average: {top_value:.2f}
"""
            )

        with a2:
            st.warning(
                f"""
📉 Lowest Performing Column

{low_column}

Average: {low_value:.2f}
"""
            )

        corr_matrix = df[numeric_columns].corr().abs()
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
        corr_pairs = corr_pairs[corr_pairs < 1]

        if len(corr_pairs) > 0:
            strongest_pair = corr_pairs.index[0]
            strongest_value = corr_pairs.iloc[0]

            st.info(
                f"""
🔥 Strongest Correlation

{strongest_pair[0]} ↔ {strongest_pair[1]}

Correlation: {strongest_value:.2f}
"""
            )

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

        # Visualizations
        st.subheader("📉 Visualizations")

        chart1, chart2 = st.columns(2)

        with chart1:
            fig_line = px.line(
                df,
                y=selected_column,
                title=f"{selected_column} Trend"
            )

            st.plotly_chart(
                fig_line,
                use_container_width=True
            )

        with chart2:
            fig_bar = px.bar(
                df,
                y=selected_column,
                title=f"{selected_column} Distribution"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        # Pie Chart
        st.subheader("🥧 Pie Chart")

        fig_pie = px.pie(
            df,
            values=selected_column,
            names=df.index.astype(str),
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

        correlation = df[col_a].corr(df[col_b])

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

        # Smart Insights
        st.subheader("🤖 Smart Insights")

        max_value = df[selected_column].max()
        min_value = df[selected_column].min()
        avg_value = df[selected_column].mean()

        growth = (
            (
                df[selected_column].iloc[-1]
                - df[selected_column].iloc[0]
            )
            / max(abs(df[selected_column].iloc[0]), 1)
        ) * 100

        insight_text = f"""
📊 Average {selected_column}: {avg_value:.2f}

📈 Highest value: {max_value}

📉 Lowest value: {min_value}

🚀 Growth from first record to last record: {growth:.1f}%
"""

        if growth > 0:
            st.success(insight_text)
        else:
            st.warning(insight_text)

        # AI Insights
        st.subheader("🤖 AI Insights")

        if st.button("Generate AI Insights"):

            insights = []

            for col in numeric_columns:
                avg = df[col].mean()
                maximum = df[col].max()
                minimum = df[col].min()

                insights.append(
                    f"• {col}: Average = {avg:.2f}, Max = {maximum}, Min = {minimum}"
                )

            st.success("AI Analysis Complete")
            st.markdown("\n".join(insights))

        # Download
        st.subheader("⬇️ Download Data")

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )