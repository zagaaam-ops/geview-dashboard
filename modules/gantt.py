import streamlit as st
import plotly.express as px

def render_gantt_module(df):
    st.subheader("📅 Tower Rollout Timeline (Gantt Chart)")
    if 'Start Date' in df.columns and 'Forecast Finish' in df.columns:
        fig_gantt = px.timeline(
            df, 
            x_start="Start Date", 
            x_end="Forecast Finish", 
            y="Site ID", 
            color="Risk",
            hover_name="Name",
            color_discrete_map={'Low': '#22C55E', 'Medium': '#EAB308', 'Critical': '#EF4444'},
            title="Schedule Overview (Start to Forecast Finish)"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("### Schedule Variance Analysis")
        st.dataframe(
            df[['Site ID', 'Name', 'Contractor', 'Baseline Finish', 'Forecast Finish', 'Schedule Variance (Days)', 'Risk']],
            column_config={
                "Schedule Variance (Days)": st.column_config.NumberColumn(
                    "Delay (Days)",
                    help="Positive numbers indicate delay beyond baseline target.",
                    format="%d days"
                )
            },
            use_container_width=True,
            hide_index=True
        )
