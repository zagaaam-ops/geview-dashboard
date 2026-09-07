import streamlit as st
import plotly.express as px

def render_analytics_module(df):
    st.subheader("📊 Executive Rollout Analytics")
    col1, col2 = st.columns(2)
    with col1:
        fig_reg = px.bar(
            df, x='Region', y='Overall Progress', color='Risk',
            color_discrete_map={'Low': '#22C55E', 'Medium': '#EAB308', 'Critical': '#EF4444'},
            title="Site Completion Progress by Region"
        )
        fig_reg.update_layout(template="plotly_dark", yaxis_tickformat='.0%')
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col2:
        fig_contractor = px.pie(
            df, names='Contractor', values='Budget', hole=0.4,
            title="Budget Allocation by Contractor"
        )
        fig_contractor.update_layout(template="plotly_dark")
        st.plotly_chart(fig_contractor, use_container_width=True)
