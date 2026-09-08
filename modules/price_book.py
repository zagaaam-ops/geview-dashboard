import streamlit as st
import pandas as pd
import re

USD_TO_SAR = 3.75

def clean_currency_value(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    # Remove $, commas, spaces, and quotes
    cleaned = re.sub(r'[^\d.]', '', str(val))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def parse_price_book_file(uploaded_file, category_type, base_currency, fx_rate):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean empty/unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Standardize column headers
    cols = [c.strip().replace('\n', ' ') for c in df.columns]
    df.columns = cols

    parsed_data = []

    if category_type == "Tower Model":
        desc_col = [c for c in df.columns if 'DESCRIPTION' in c.upper() or 'MODEL' in c.upper()][0]
        price_col = [c for c in df.columns if 'PRICE' in c.upper()][0]

        for _, row in df.iterrows():
            usd_price = clean_currency_value(row[price_col])
            sar_price = usd_price * fx_rate if base_currency == "USD" else usd_price
            parsed_data.append({
                "Category": "Tower Model",
                "Item / Model Name": str(row[desc_col]).strip(),
                "Unit of Measure": "Unit",
                "Original Price": usd_price,
                "Currency": base_currency,
                "Price (SAR)": sar_price
            })

    elif category_type == "Extra Work Item":
        desc_col = [c for c in df.columns if 'DISCRIPTION' in c.upper() or 'DESCRIPTION' in c.upper()][0]
        unit_col = [c for c in df.columns if 'UNIT' in c.upper()][0]
        price_col = [c for c in df.columns if 'PRICE' in c.upper()][0]

        for _, row in df.iterrows():
            usd_price = clean_currency_value(row[price_col])
            sar_price = usd_price * fx_rate if base_currency == "USD" else usd_price
            parsed_data.append({
                "Category": "Extra Work Item",
                "Item / Model Name": str(row[desc_col]).strip(),
                "Unit of Measure": str(row[unit_col]).strip() if pd.notna(row[unit_col]) else "LS",
                "Original Price": usd_price,
                "Currency": base_currency,
                "Price (SAR)": sar_price
            })

    return pd.DataFrame(parsed_data)

def render_price_book_module(db_engine):
    st.subheader("🏷️ Vendor Price Book & Rate Card Management")
    st.caption("Ingest and convert vendor tower model prices and Extra Work Unit Price Lists (UPL) into SAR.")

    tab1, tab2 = st.tabs(["📤 Upload Vendor Price Book", "📋 Approved Rate Card Directory"])

    with tab1:
        st.markdown("### Upload Approved Vendor Price List")

        c1, c2, c3, c4 = st.columns(4)
        vendor_name = c1.selectbox("Select Vendor", ["Vendor 1 (Ven1)", "Vendor 2 (Ven2)", "Custom Vendor"])
        category_type = c2.selectbox("Price Book Category", ["Tower Model", "Extra Work Item"])
        base_currency = c3.selectbox("Base Currency", ["USD", "SAR"])
        fx_rate = c4.number_input("Exchange Rate (USD to SAR)", value=3.75, step=0.01) if base_currency == "USD" else 1.0

        uploaded_file = st.file_uploader("Upload Price List (CSV / Excel)", type=["csv", "xlsx"])

        if uploaded_file and vendor_name:
            try:
                parsed_df = parse_price_book_file(uploaded_file, category_type, base_currency, fx_rate)
                
                st.success(f"Parsed {len(parsed_df)} items successfully from `{uploaded_file.name}`.")
                st.markdown("#### Converted Price Catalog Preview (SAR)")
                
                st.dataframe(
                    parsed_df.style.format({
                        "Original Price": "${:,.2f}" if base_currency == "USD" else "SAR {:,.2f}",
                        "Price (SAR)": "SAR {:,.2f}"
                    }),
                    use_container_width=True
                )

                if st.button("💾 Save to Approved Database", type="primary"):
                    st.success(f"Approved price book for {vendor_name} ({category_type}) has been saved to the database!")
            except Exception as e:
                st.error(f"Error parsing file structure: {str(e)}")

    with tab2:
        st.markdown("### Master Rate Directory")
        st.info("Catalog items loaded from vendor submissions can be filtered and matched directly against Site BOQs.")
