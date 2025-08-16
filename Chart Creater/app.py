import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Web Data Analysis Dashboard", layout="wide")

st.title("📊 Web-Based Data Analysis Dashboard")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # File load
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.write("### 📋 Data Preview", df.head())

    # Step 2: Chart Type
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line", "Bar", "Scatter", "Pie"]
    )

    # Step 3: Select X and Y Axis
    x_axis = st.selectbox("Select X-axis", df.columns)
    y_axis = st.selectbox("Select Y-axis", df.columns)

    # Step 4: Generate Chart Button
    if st.button("Generate Chart"):
        fig, ax = plt.subplots(figsize=(8, 5))

        try:
            if chart_type == "Line":
                ax.plot(df[x_axis], df[y_axis], marker="o")
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                ax.set_title(f"{chart_type} Chart")
                plt.xticks(rotation=45, ha="right")

            elif chart_type == "Bar":
                # group duplicates if needed
                grouped = df.groupby(x_axis)[y_axis].sum().reset_index()
                ax.bar(grouped[x_axis].astype(str), grouped[y_axis])
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                ax.set_title(f"{chart_type} Chart")
                plt.xticks(rotation=45, ha="right")

            elif chart_type == "Scatter":
                ax.scatter(df[x_axis], df[y_axis])
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                ax.set_title(f"{chart_type} Chart")
                plt.xticks(rotation=45, ha="right")

            elif chart_type == "Pie":
                grouped = df.groupby(x_axis)[y_axis].sum()
                grouped.plot.pie(autopct="%1.1f%%", ax=ax)
                ax.set_ylabel("")
                ax.set_title(f"{chart_type} Chart")

            st.pyplot(fig)

            # Step 5: Download Chart
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="⬇️ Download Chart",
                data=buf,
                file_name="chart.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
