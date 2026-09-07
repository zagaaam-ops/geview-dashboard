import streamlit as st
import pandas as pd
from modules.db import save_data_to_db

def render_editor_module(df, user_role):
    st.subheader("📝 Master Data Editor & Excel Bulk Sync")
    st.caption("Update site attributes directly in the grid or bulk upload a Master Excel file to sync with Supabase.")

    if user_role not in ["👔 Regional Project Manager", "👷 Field Supervisor / Contractor"]:
        st.warning("⚠️ You are currently in Executive View. Switch persona roles in the sidebar to modify site data.")

    # Tabbed Interface: Grid Editor vs Bulk Excel Sync
    tab_editor, tab_bulk = st.tabs(["✏️ Interactive Grid Editor", "📤 Bulk Excel Upload Sync"])

    with tab_editor:
        st.write("Edit individual site metrics directly below:")
        
        # Format dates as strings for st.data_editor compatibility
        display_df = df.copy()
        for date_col in ['Start Date', 'Baseline Finish', 'Forecast Finish']:
            if date_col in display_df.columns:
                display_df[date_col] = display_df[date_col].dt.strftime('%Y-%m-%d')

        column_config = {
            "Overall Progress": st.column_config.NumberColumn(
                "Progress",
                help="Progress percentage (0.0 to 1.0)",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.2f"
            ),
            "Risk": st.column_config.SelectboxColumn(
                "Risk Level",
                options=["Low", "Medium", "High", "Critical"]
            ),
            "Budget": st.column_config.NumberColumn("Budget ($)", format="$%d"),
            "Actual": st.column_config.NumberColumn("Actual Spend ($)", format="$%d")
        }

        edited_df = st.data_editor(
            display_df,
            column_config=column_config,
            use_container_width=True,
            num_rows="dynamic",
            key="grid_data_editor"
        )

    with tab_bulk:
        st.markdown("### 📤 Bulk Upload Master Excel File")
        st.write("Upload an updated `.xlsx` or `.csv` spreadsheet to overwrite/sync the central cloud database.")

        uploaded_file = st.file_uploader("Choose a Master Rollout Excel file", type=["xlsx", "xls", "csv"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    imported_df = pd.read_csv(uploaded_file)
                else:
                    imported_df = pd.read_excel(uploaded_file)

                st.success(f"Successfully loaded `{uploaded_file.name}` ({len(imported_df)} rows). Preview below:")
                st.dataframe(imported_df.head(), use_container_width=True)

                required_cols = {'Site ID', 'Name', 'Region', 'Contractor', 'Overall Progress', 'Budget', 'Actual', 'Risk'}
                if required_cols.issubset(set(imported_df.columns)):
                    if st.button("🚀 Confirm & Sync Excel to Supabase Database", type="primary"):
                        db_engine = st.session_state.get('db_engine', None)
                        
                        # Re-fetch engine if available in app context
                        from modules.db import get_db_engine
                        db_engine = get_db_engine()

                        if db_engine:
                            if save_data_to_db(db_engine, imported_df):
                                st.success("✅ Supabase Database updated successfully! Refreshing dashboard...")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("❌ Failed to write Excel data to Supabase PostgreSQL database.")
                        else:
                            st.warning("⚠️ Cloud Database engine not available. Unable to sync.")
                else:
                    missing = required_cols - set(imported_df.columns)
                    st.error(f"Missing required columns in uploaded Excel file: {missing}")

            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

    return edited_df
