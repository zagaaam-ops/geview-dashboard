import streamlit as st
import pandas as pd

def render_site_survey():
    st.title("📋 Site Survey & BOQ Generation Engine")
    st.caption("Capture field civil engineering parameters and generate site-level BOQ against standard contract rates.")

    # --- MASTER PRICE BOOK DATA (DEFAULTS) ---
    PRICE_BOOK = {
        "EXC_01": {"description": "Site Excavation & Backfilling (Class A Soil)", "unit": "m³", "rate": 45.00},
        "CON_01": {"description": "Reinforced Concrete Foundation (C35/40)", "unit": "m³", "rate": 350.00},
        "TOW_01": {"description": "45m Monopole Tower Supply & Erection", "unit": "lot", "rate": 18500.00},
        "TOW_02": {"description": "4-Legged Self-Supporting Tower (60m)", "unit": "lot", "rate": 32000.00},
        "FEN_01": {"description": "Chain Link Perimeter Fencing with Gate (12x12m)", "unit": "m", "rate": 85.00},
        "GND_01": {"description": "Copper Earth Ring & Grounding Pit Installation", "unit": "system", "rate": 1200.00},
        "PWR_01": {"description": "Commercial AC Power Hookup & DB Cabinet", "unit": "lot", "rate": 4500.00},
    }

    # --- FORM SECTIONS ---
    st.subheader("1. General Site Identification")
    c1, c2, c3 = st.columns(3)
    with c1:
        site_id = st.text_input("Site ID / Candidate Code", value="RIY-CIV-104")
    with c2:
        region = st.selectbox("Region / Zone", ["Riyadh Central", "Jeddah West", "Dammam East", "Southern Zone"])
    with c3:
        surveyor = st.text_input("Field Engineer / Surveyor", value="Rana M. Zagham")

    st.subheader("2. Civil Engineering & Tower Parameters")
    col_a, col_b = st.columns(2)
    
    with col_a:
        tower_type = st.selectbox("Tower Structure Required", ["45m Monopole", "60m 4-Legged Lattice"])
        soil_type = st.selectbox("Soil Classification", ["Class A (Standard Soil)", "Class B (Soft Soil / Excavation Expansion)", "Class C (Hard Rock)"])
        excavation_vol = st.number_input("Estimated Excavation Volume (m³)", min_value=10.0, max_value=500.0, value=65.0, step=5.0)
    
    with col_b:
        concrete_vol = st.number_input("Foundation Concrete Volume (m³)", min_value=5.0, max_value=200.0, value=28.0, step=2.0)
        fencing_len = st.number_input("Perimeter Fencing Length (m)", min_value=0.0, max_value=200.0, value=48.0, step=4.0)
        power_required = st.checkbox("Requires Commercial Grid Connection", value=True)

    st.markdown("---")
    
    # --- AUTOMATED BOQ CALCULATION ---
    if st.button("⚙️ Generate Site BOQ", type="primary", use_container_width=True):
        boq_items = []
        
        # 1. Excavation Adjustment based on Soil Class
        exc_multiplier = 1.0
        if "Class B" in soil_type:
            exc_multiplier = 1.25
        elif "Class C" in soil_type:
            exc_multiplier = 1.60
            
        exc_rate = PRICE_BOOK["EXC_01"]["rate"] * exc_multiplier
        exc_amount = excavation_vol * exc_rate
        boq_items.append({
            "Item Code": "EXC_01",
            "Description": f"{PRICE_BOOK['EXC_01']['description']} ({soil_type})",
            "Unit": "m³",
            "Qty": excavation_vol,
            "Unit Rate (SAR)": round(exc_rate, 2),
            "Total Amount (SAR)": round(exc_amount, 2)
        })

        # 2. Foundation Concrete
        conc_amount = concrete_vol * PRICE_BOOK["CON_01"]["rate"]
        boq_items.append({
            "Item Code": "CON_01",
            "Description": PRICE_BOOK["CON_01"]["description"],
            "Unit": "m³",
            "Qty": concrete_vol,
            "Unit Rate (SAR)": PRICE_BOOK["CON_01"]["rate"],
            "Total Amount (SAR)": round(conc_amount, 2)
        })

        # 3. Tower Structure
        tow_code = "TOW_01" if "45m" in tower_type else "TOW_02"
        boq_items.append({
            "Item Code": tow_code,
            "Description": PRICE_BOOK[tow_code]["description"],
            "Unit": "lot",
            "Qty": 1.0,
            "Unit Rate (SAR)": PRICE_BOOK[tow_code]["rate"],
            "Total Amount (SAR)": PRICE_BOOK[tow_code]["rate"]
        })

        # 4. Fencing
        if fencing_len > 0:
            fence_amount = fencing_len * PRICE_BOOK["FEN_01"]["rate"]
            boq_items.append({
                "Item Code": "FEN_01",
                "Description": PRICE_BOOK["FEN_01"]["description"],
                "Unit": "m",
                "Qty": fencing_len,
                "Unit Rate (SAR)": PRICE_BOOK["FEN_01"]["rate"],
                "Total Amount (SAR)": round(fence_amount, 2)
            })

        # 5. Grounding System
        boq_items.append({
            "Item Code": "GND_01",
            "Description": PRICE_BOOK["GND_01"]["description"],
            "Unit": "system",
            "Qty": 1.0,
            "Unit Rate (SAR)": PRICE_BOOK["GND_01"]["rate"],
            "Total Amount (SAR)": PRICE_BOOK["GND_01"]["rate"]
        })

        # 6. Power Hookup
        if power_required:
            boq_items.append({
                "Item Code": "PWR_01",
                "Description": PRICE_BOOK["PWR_01"]["description"],
                "Unit": "lot",
                "Qty": 1.0,
                "Unit Rate (SAR)": PRICE_BOOK["PWR_01"]["rate"],
                "Total Amount (SAR)": PRICE_BOOK["PWR_01"]["rate"]
            })

        df_boq = pd.DataFrame(boq_items)
        total_site_cost = df_boq["Total Amount (SAR)"].sum()

        st.session_state["generated_boq"] = {
            "site_id": site_id,
            "region": region,
            "surveyor": surveyor,
            "items": df_boq,
            "total_cost": total_site_cost
        }

        st.success(f"Site BOQ generated successfully for **{site_id}**!")

    # --- DISPLAY GENERATED BOQ RESULT ---
    if "generated_boq" in st.session_state:
        boq_data = st.session_state["generated_boq"]
        st.subheader(f"📊 Generated BOQ — Site: {boq_data['site_id']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Site ID", boq_data["site_id"])
        m2.metric("Region", boq_data["region"])
        m3.metric("Total Civil Cost", f"{boq_data['total_cost']:,.2f} SAR")

        st.dataframe(boq_data["items"], use_container_width=True)

        st.download_button(
            label="📥 Download BOQ (CSV)",
            data=boq_data["items"].to_csv(index=False),
            file_name=f"BOQ_{boq_data['site_id']}.csv",
            mime="text/csv"
        )

# Execute entrypoint
render_site_survey()
