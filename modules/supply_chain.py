import streamlit as st
import pandas as pd

def render_supply_chain_module(user_role):
    st.subheader("📦 Supply Chain & Material Inventory Tracking")
    st.caption("Track warehouse inventory, manage heavy equipment, and log Purchase Orders (POs).")

    if "inventory_stock" not in st.session_state:
        st.session_state["inventory_stock"] = pd.DataFrame([
            {"Item_Code": "MAT-STL-001", "Material_Description": "Galvanized Steel Tower Angles (40m Tower)", "Warehouse": "Riyadh Central Hub", "Quantity": 150, "Unit": "Tons", "Status": "In Stock"},
            {"Item_Code": "MAT-FBR-204", "Material_Description": "Single Mode Underground Fiber Cable (96 Core)", "Warehouse": "Jeddah Depot", "Quantity": 45, "Unit": "Spools (1km)", "Status": "Low Stock"},
            {"Item_Code": "MAT-CON-501", "Material_Description": "C40 Ready-Mix Structural Concrete Base", "Warehouse": "Dammam Field Yard", "Quantity": 320, "Unit": "m³", "Status": "In Stock"}
        ])

    if "equipment_assets" not in st.session_state:
        st.session_state["equipment_assets"] = pd.DataFrame([
            {"Asset_ID": "EQP-CRN-01", "Equipment_Type": "50-Ton Mobile Hydraulic Crane", "Assigned_Site": "RIY-5G-102 (Riyadh)", "Operator": "Sultan Al-Otaibi", "Status": "Active Field Deployment"},
            {"Asset_ID": "EQP-EXC-04", "Equipment_Type": "Heavy Trenching Excavator", "Assigned_Site": "JED-FBR-045 (Jeddah)", "Operator": "Subcontractor Allocated", "Status": "Under Maintenance"}
        ])

    inv_df = st.session_state["inventory_stock"]
    eqp_df = st.session_state["equipment_assets"]

    tabs = st.tabs(["🏭 Warehouse Inventory", "🚜 Equipment & Heavy Machinery", "📝 Raise Material Request / PO"])

    with tabs[0]:
        st.markdown("### 🏭 Regional Warehouse Stock Levels")
        st.dataframe(inv_df, use_container_width=True)

    with tabs[1]:
        st.markdown("### 🚜 Heavy Machinery & Asset Dispatch")
        st.dataframe(eqp_df, use_container_width=True)
        if len(eqp_df) > 0:
            c1, c2 = st.columns([2, 2])
            asset = c1.selectbox("Select Equipment Asset:", eqp_df["Asset_ID"].tolist())
            site = c2.text_input("New Target Site ID / City:", "DAM-TWR-309 (Dammam)")
            if st.button("🚜 Reassign & Dispatch", type="primary"):
                st.session_state["equipment_assets"].loc[st.session_state["equipment_assets"]["Asset_ID"] == asset, "Assigned_Site"] = site
                st.success(f"Asset {asset} dispatched to {site}!")
                st.rerun()

    with tabs[2]:
        st.markdown("### 📝 Raise Purchase Order (PO) / Material Request")
        with st.form("po_request_form"):
            col1, col2 = st.columns(2)
            desc = col1.text_input("Material / Item Description:", "HDPE Conduit Pipes (110mm)")
            wh = col2.selectbox("Target Warehouse:", ["Riyadh Central Hub", "Jeddah Depot", "Dammam Field Yard"])
            col3, col4 = st.columns(2)
            qty = col3.number_input("Quantity:", min_value=1, value=100)
            u = col4.text_input("Unit of Measure:", "Meters")
            if st.form_submit_button("📦 Submit Purchase Order Request"):
                code = f"MAT-REQ-00{len(inv_df) + 1}"
                row = {"Item_Code": code, "Material_Description": desc, "Warehouse": wh, "Quantity": qty, "Unit": u, "Status": "Pending Delivery"}
                st.session_state["inventory_stock"] = pd.concat([inv_df, pd.DataFrame([row])], ignore_index=True)
                st.success("PO Request submitted!")
                st.rerun()
