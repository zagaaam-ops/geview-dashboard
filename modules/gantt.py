import streamlit as st
import plotly.express as px
import pandas as pd

def render_gantt_module(df):
    st.subheader("📅 Interactive Schedule Timeline & Milestone Gantt")
    st.caption("Track baseline vs. forecast completion dates and monitor milestone progress across regions.")

    if df.empty:
        st.warning("No site data available for Gantt chart rendering.")
        return

    gantt_df = df.copy()
    gantt_df['Start Date'] = pd.to_datetime(gantt_df['Start Date'])
    gantt_df['Forecast Finish'] = pd.to_datetime(gantt_df['Forecast Finish'])

    # Create Plotly Timeline
    fig = px.timeline(
        gantt_df,
        x_start="Start Date",
        x_end="Forecast Finish",
        y="Site ID",
        color="Risk",
        hover_name="Name",
        hover_data=["Region", "Contractor", "Overall Progress", "Schedule Variance (Days)"],
        title="Site Execution Timeline (Forecast Finish Dates)",
        color_discrete_map={
            "Low": "#10B981",
            "Medium": "#F59E0B",
            "High": "#EF4444",
            "Critical": "#991B1B"
        }
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#1E293B",
        font_color="#F8FAFC",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(gridcolor="#334155")
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed Schedule Table
    st.markdown("### 📋 Schedule Variance Summary")
    st.dataframe(
        gantt_df[['Site ID', 'Name', 'Region', 'Contractor', 'Start Date', 'Baseline Finish', 'Forecast Finish', 'Schedule Variance (Days)', 'Risk']],
        use_container_width=True
    )
