import streamlit as st
import pandas as pd

def render_editor_module(df, user_role):
    st.subheader("📝 Interactive Site Data Editor & Excel Sync")
    st.caption("Edit progress directly in the table or upload a revised master rollout Excel sheet.")

    tab_edit, tab_upload = st.tabs(["✏️ Live Table Grid", "📤 Upload & Sync Excel Sheet"])

    with tab_edit:
        if user_role == "👷 Field Supervisor / Contractor":
            field_cols = ['Site ID', 'Name', 'Region', 'Contractor', 'Overall Progress', 'Risk', 'Start Date', 'Forecast Finish']
            edited_df = st.data_editor(df[field_cols], num_rows="fixed", use_container_width=True)
        else:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    with tab_upload:
        st.markdown("#### Sync Rollout Database from Excel File")
        uploaded_excel = st.file_uploader("Choose Master Excel Rollout File", type=["xlsx", "xls"])
        
        if uploaded_excel:
            try:
                new_df = pd.read_excel(uploaded_excel)
                st.write("Preview of Uploaded Excel File:")
                st.dataframe(new_df.head(), use_container_width=True)
                
                if st.button("🔄 Replace Database with Uploaded Excel Data"):
                    st.session_state['excel_sync_df'] = new_df
                    st.success("Excel data staged for synchronization! Click 'Save Grid Changes to Database' below.")
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")

    if 'excel_sync_df' in st.session_state:
        return st.session_state['excel_sync_df']
        
    return edited_df
