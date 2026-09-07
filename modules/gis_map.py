import streamlit as st
import folium
from streamlit_folium import st_folium

def render_gis_map(df):
    st.subheader("🗺️ High-Resolution GIS Satellite & Topo Map")
    
    if 'lat' not in df.columns or 'lon' not in df.columns:
        st.warning("No GPS coordinates found in dataset.")
        return

    # Map Layer Selector
    map_provider = st.radio(
        "Select Basemap Tile Layer:",
        ["🛰️ Esri World Imagery (HD Satellite)", "🗺️ OpenStreetMap (Standard)", "⛰️ Esri World Topo"],
        horizontal=True
    )

    # Set initial center coordinates
    center_lat = df['lat'].mean() if len(df) > 0 else 24.7136
    center_lon = df['lon'].mean() if len(df) > 0 else 46.6753

    # Initialize Folium Map
    if "Satellite" in map_provider:
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        attr = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
    elif "Topo" in map_provider:
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
        attr = "Tiles &copy; Esri"
    else:
        tiles = "OpenStreetMap"
        attr = None

    m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles=tiles, attr=attr)

    # Add Color-coded Tower Markers
    risk_colors = {'Low': 'green', 'Medium': 'orange', 'Critical': 'red'}

    for _, row in df.iterrows():
        color = risk_colors.get(row['Risk'], 'blue')
        popup_html = f"""
            <div style="font-family: Arial; width: 180px;">
                <h4>{row['Site ID']}</h4>
                <b>Name:</b> {row['Name']}<br/>
                <b>Region:</b> {row['Region']}<br/>
                <b>Contractor:</b> {row['Contractor']}<br/>
                <b>Progress:</b> {int(row['Overall Progress']*100)}%<br/>
                <b>Risk Status:</b> <span style="color:{color}; font-weight:bold;">{row['Risk']}</span>
            </div>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{row['Site ID']} - {row['Name']} ({row['Risk']} Risk)",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85
        ).add_to(m)

    st_folium(m, width="100%", height=500)
