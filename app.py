import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="Personal Insights Analyzer", page_icon="📊", layout="wide")

st.sidebar.title("📊 Dashboard Controls")
st.sidebar.write("Upload your file and explore the data")

st.title("📊 Personal Insights Analyzer")
st.markdown("Analyze your Excel data in seconds")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "csv"])

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.sidebar.success("File uploaded successfully")

    st.subheader("📋 Data Preview")
    st.dataframe(df)

    c1, c2 = st.columns(2)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])

    st.subheader("📈 Basic Statistics")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:

        st.subheader("📊 Dataset Quality Score")

        missing_values = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())
        total_cells = max(df.shape[0] * df.shape[1], 1)

        quality_score = round(
            100 - ((missing_values / total_cells) * 100),
            1
        )

        q1, q2, q3 = st.columns(3)
        q1.metric("Missing Values", missing_values)
        q2.metric("Duplicate Rows", duplicate_rows)
        q3.metric("Quality Score", f"{quality_score}%")

        st.subheader("🏆 Advanced Insights")

        column_means = df[numeric_columns].mean()

        top_column = column_means.idxmax()
        low_column = column_means.idxmin()

        a1, a2 = st.columns(2)

        with a1:
            st.success(
                f"🏆 Top Performing Column\n\n{top_column}\n\nAverage: {column_means[top_column]:.2f}"
            )

        with a2:
            st.warning(
                f"📉 Lowest Performing Column\n\n{low_column}\n\nAverage: {column_means[low_column]:.2f}"
            )

        corr_matrix = df[numeric_columns].corr().abs()
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
        corr_pairs = corr_pairs[corr_pairs < 1]

        if len(corr_pairs) > 0:
            strongest_pair = corr_pairs.index[0]
            strongest_value = corr_pairs.iloc[0]

            st.info(
                f"🔥 Strongest Correlation: {strongest_pair[0]} ↔ {strongest_pair[1]} ({strongest_value:.2f})"
            )

        st.subheader("📊 Column Selection")

        selected_column = st.selectbox(
            "Choose a column",
            numeric_columns
        )

        st.subheader("📌 Key Metrics")

        k1, k2, k3 = st.columns(3)
        avg_value = df[selected_column].mean()
        max_value = df[selected_column].max()
        min_value = df[selected_column].min()

        k1.metric("Average", round(avg_value, 2))
        k2.metric("Maximum", round(max_value, 2))
        k3.metric("Minimum", round(min_value, 2))

        st.subheader("📉 Visualizations")

        ch1, ch2 = st.columns(2)

        with ch1:
            fig_line = px.line(df, y=selected_column, title=f"{selected_column} Trend")
            st.plotly_chart(fig_line, use_container_width=True)

        with ch2:
            fig_bar = px.bar(df, y=selected_column, title=f"{selected_column} Distribution")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("🥧 Pie Chart")

        fig_pie = px.pie(
            df,
            values=selected_column,
            names=df.index.astype(str)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("🔗 Correlation Analysis")

        col_a = st.selectbox("Select First Column", numeric_columns, key="a")
        col_b = st.selectbox("Select Second Column", numeric_columns, key="b")

        correlation = df[col_a].corr(df[col_b])

        st.metric("Correlation", round(correlation, 2))

        st.subheader("🎯 Scatter Plot")

        fig_scatter = px.scatter(df, x=col_a, y=col_b)
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.subheader("🚨 Outlier Detection")

        Q1 = df[selected_column].quantile(0.25)
        Q3 = df[selected_column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outliers = df[
            (df[selected_column] < lower_bound) |
            (df[selected_column] > upper_bound)
        ]

        st.metric("Outliers Found", len(outliers))

        if len(outliers) > 0:
            st.dataframe(outliers)
        else:
            st.success("No significant outliers detected.")

        st.subheader("🤖 Smart Insights")

        growth = (
            (df[selected_column].iloc[-1] - df[selected_column].iloc[0])
            / max(abs(df[selected_column].iloc[0]), 1)
        ) * 100

        st.info(
            f"""
Average: {avg_value:.2f}

Highest Value: {max_value}

Lowest Value: {min_value}

Growth: {growth:.1f}%
"""
        )

        st.subheader("📄 Executive Summary")

        if st.button("Generate Executive Summary"):
            summary = f"""
Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.

Quality Score: {quality_score}%

Selected Metric: {selected_column}

Average: {avg_value:.2f}

Highest: {max_value}

Lowest: {min_value}

Outliers: {len(outliers)}

Correlation ({col_a}, {col_b}): {correlation:.2f}
"""
            st.text_area("Executive Summary", summary, height=250)

        st.subheader("💡 Business Recommendations")

        if st.button("Generate Recommendations"):
            recommendations = []

            if len(outliers) > 0:
                recommendations.append("Investigate detected outliers.")

            if abs(correlation) > 0.7:
                recommendations.append("Monitor strongly correlated metrics.")

            if growth > 0:
                recommendations.append("Positive growth detected.")
            else:
                recommendations.append("Investigate negative growth trend.")

            for rec in recommendations:
                st.success(rec)

        st.subheader("🤖 AI Insights")

        if st.button("Generate AI Insights"):
            insights = []
            for col in numeric_columns:
                insights.append(
                    f"• {col}: Avg={df[col].mean():.2f}, Max={df[col].max()}, Min={df[col].min()}"
                )
            st.markdown("\n".join(insights))

        st.subheader("📄 Export PDF Report")

        if st.button("Generate PDF Report"):

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()

            content = [
                Paragraph("Personal Insights Analyzer Report", styles["Title"]),
                Spacer(1, 12),
                Paragraph(f"Rows: {df.shape[0]}", styles["BodyText"]),
                Paragraph(f"Columns: {df.shape[1]}", styles["BodyText"]),
                Paragraph(f"Quality Score: {quality_score}%", styles["BodyText"]),
                Paragraph(f"Selected Metric: {selected_column}", styles["BodyText"]),
            ]

            doc.build(content)

            st.download_button(
                "⬇️ Download PDF Report",
                buffer.getvalue(),
                "analysis_report.pdf",
                "application/pdf"
            )

        st.subheader("⬇️ Download Data")

        csv = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )