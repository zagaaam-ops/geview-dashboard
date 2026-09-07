import streamlit as st
import plotly.graph_objects as go

def render_evm_module(df):
    st.subheader("💰 Earned Value Management Analysis")
    fig_evm = go.Figure()
    fig_evm.add_trace(go.Bar(x=df['Site ID'], y=df['Budget'], name='Budget', marker_color='#64748B'))
    fig_evm.add_trace(go.Bar(x=df['Site ID'], y=df['Actual'], name='Actual Cost', marker_color='#EF4444'))
    fig_evm.add_trace(go.Bar(x=df['Site ID'], y=df['Earned Value'], name='Earned Value', marker_color='#10B981'))
    fig_evm.update_layout(barmode='group', template="plotly_dark", height=400)
    st.plotly_chart(fig_evm, use_container_width=True)
