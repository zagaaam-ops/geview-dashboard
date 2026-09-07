import streamlit as st

def render_editor_module(df, user_role):
    st.subheader("📝 Interactive Site Data Editor")
    st.caption("Edit progress or schedule dates directly in the grid below.")
    
    if user_role == "👷 Field Supervisor / Contractor":
        field_cols = ['Site ID', 'Name', 'Region', 'Contractor', 'Overall Progress', 'Risk', 'Start Date', 'Forecast Finish']
        edited_df = st.data_editor(df[field_cols], num_rows="fixed", use_container_width=True)
    else:
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    return edited_df
