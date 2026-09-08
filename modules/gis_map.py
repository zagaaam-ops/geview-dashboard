import streamlit as st
import pandas as pd

def render_gis_map_module(user_role):
    st.subheader("🗺️ Interactive GIS Map & Site Location Portal")
    st.caption("Geospatial tracking of telecom towers, civil sites, and regional infrastructure across Saudi Arabia.")

    if "gis_sites" not in st.session_state:
        st.session_state["gis_sites"] = pd.DataFrame([
            {"Site_ID": "RIY-5G-102", "Client": "STC", "City": "Riyadh", "lat": 24.7136, "lon": 46.6753, "Status": "In Progress", "Tower_Type": "Rooftop Monopole"},
            {"Site_ID": "JED-FBR-045", "Client": "Mobily", "City": "Jeddah", "lat": 21.5433, "lon": 39.1728, "Status": "Completed", "Tower_Type": "Underground Fiber Trench"},
            {"Site_ID": "DAM-TWR-309", "Client": "Zain", "City": "Dammam", "lat": 26.4207, "lon": 50.0888, "Status": "Planning", "Tower_Type": "45m Lattice Tower"},
            {"Site_ID": "MED-5G-012", "Client": "STC", "City": "Madinah", "lat": 24.5247, "lon": 39.5692, "Status": "In Progress", "Tower_Type": "Rooftop Monopole"}
        ])

    df_sites = st.session_state["gis_sites"]

    c1, c2 = st.columns(2)
    sel_city = c1.multiselect("Filter by City:", df_sites["City"].unique(), default=df_sites["City"].unique())
    sel_client = c2.multiselect("Filter by Client:", df_sites["Client"].unique(), default=df_sites["Client"].unique())

    filtered_df = df_sites[(df_sites["City"].isin(sel_city)) & (df_sites["Client"].isin(sel_client))]

    st.markdown("### 📍 Active Site Map View")
    if not filtered_df.empty:
        st.map(filtered_df[["lat", "lon"]])
    else:
        st.warning("No site locations match the selected filters.")

    st.markdown("---")
    st.markdown("### 📋 Site Coordinates & Metadata Directory")
    st.dataframe(filtered_df, use_container_width=True)

    with st.expander("➕ Add New GIS Site Location"):
        with st.form("add_gis_site"):
            f1, f2, f3 = st.columns(3)
            new_id = f1.text_input("Site ID:", "RUH-5G-888")
            new_client = f2.selectbox("Client:", ["STC", "Mobily", "Zain", "Dawiyat"])
            new_city = f3.text_input("City:", "Riyadh")

            f4, f5, f6 = st.columns(3)
            new_lat = f4.number_input("Latitude:", value=24.77426, format="%.5f")
            new_lon = f5.number_input("Longitude:", value=46.73858, format="%.5f")
            new_type = f6.selectbox("Tower/Infrastructure Type:", ["Rooftop Monopole", "45m Lattice Tower", "Underground Fiber Trench"])

            if st.form_submit_button("📍 Register Site Location"):
                new_row = {"Site_ID": new_id, "Client": new_client, "City": new_city, "lat": new_lat, "lon": new_lon, "Status": "Planning", "Tower_Type": new_type}
                st.session_state["gis_sites"] = pd.concat([df_sites, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Site {new_id} registered!")
                st.rerun()
