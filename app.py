import pandas as pd
import streamlit as st

# Custom module imports from boq datastore & logic layer
from boq_data import get_extra_works_df, get_site_models_df
from boq_extra_works import calculate_ew_item_cost

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Project Plus | Telecom Infrastructure PMO",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- GLOBAL DATA INITIALIZATION ---
df_models = get_site_models_df()
df_ew = get_extra_works_df()

if "pmo_data" not in st.session_state:
    st.session_state.pmo_data = {
        # Dynamically linked to boq_data master site models
        "price_book": (
            df_models
            if not df_models.empty
            else pd.DataFrame(
                [
                    {
                        "Code": "MOD_01",
                        "Model": "45m Monopole - Standard",
                        "Unit": "site",
                        "Rate": 42500.00,
                    },
                    {
                        "Code": "MOD_02",
                        "Model": "60m Lattice - Heavy Duty",
                        "Unit": "site",
                        "Rate": 68000.00,
                    },
                    {
                        "Code": "MOD_03",
                        "Model": "Rooftop Micro Pole",
                        "Unit": "site",
                        "Rate": 22000.00,
                    },
                ]
            )
        ),
        "extra_works_catalog": df_ew,
        "sites": pd.DataFrame(
            [
                {
                    "Site ID": "RIY-101",
                    "Region": "Riyadh",
                    "Status": "Implementation",
                    "Tower Model": "45m Monopole - Standard",
                    "Budget (SAR)": 42500,
                    "PO Number": "PO-2026-ABR-001",
                    "PO Value (SAR)": 42500,
                    "Vendor": "Abrar Telecom",
                    "latitude": 24.7136,
                    "longitude": 46.6753,
                    "Design Approved": True,
                },
                {
                    "Site ID": "JED-204",
                    "Region": "Jeddah",
                    "Status": "Pending PM Site Approval",
                    "Tower Model": "60m Lattice - Heavy Duty",
                    "Budget (SAR)": 68000,
                    "PO Number": "Unassigned",
                    "PO Value (SAR)": 0,
                    "Vendor": "Red Sea Infra",
                    "latitude": 21.5433,
                    "longitude": 39.1728,
                    "Design Approved": False,
                },
                {
                    "Site ID": "DAM-302",
                    "Region": "Dammam",
                    "Status": "Pending PO Approval",
                    "Tower Model": "45m Monopole - Standard",
                    "Budget (SAR)": 42500,
                    "PO Number": "Pending FM Approval",
                    "PO Value (SAR)": 41000,
                    "Vendor": "Gulf Fiber Tech",
                    "latitude": 26.4207,
                    "longitude": 50.0888,
                    "Design Approved": False,
                },
            ]
        ),
        "purchase_orders": [
            {
                "PO Number": "PO-2026-ABR-001",
                "Vendor": "Abrar Telecom",
                "Site ID": "RIY-101",
                "PO Value (SAR)": 42500,
                "Status": "Approved by FM",
                "Created By": "PMO",
            },
            {
                "PO Number": "PO-REQ-002",
                "Vendor": "Gulf Fiber Tech",
                "Site ID": "DAM-302",
                "PO Value (SAR)": 41000,
                "Status": "Pending FM Approval",
                "Created By": "PMO",
            },
        ],
        "site_documents": {
            "RIY-101": {
                "1. Documents": [
                    {
                        "Filename": "Approved_Structural_Drawing_v1.pdf",
                        "Uploaded By": "Project Engineer",
                        "Date": "2026-08-10",
                        "Category": "Engineering",
                    },
                    {
                        "Filename": "Soil_Test_Report.pdf",
                        "Uploaded By": "Vendor (Abrar)",
                        "Date": "2026-08-05",
                        "Category": "Survey",
                    },
                ],
                "2. Implementation": [
                    {
                        "Filename": "Foundation_Pouring_Photo_1.jpg",
                        "Uploaded By": "Site Supervisor",
                        "Date": "2026-08-15",
                        "Category": "Site Photo",
                    }
                ],
                "3. Finance Data": [
                    {
                        "Filename": "PO_PO-2026-ABR-001.pdf",
                        "Uploaded By": "Finance Manager",
                        "Date": "2026-08-01",
                        "Category": "Purchase Order",
                    }
                ],
            }
        },
        "design_reviews": [
            {
                "Site ID": "RIY-101",
                "Vendor": "Abrar Telecom",
                "Drawing Ref": "DWG-RIY101-REV2",
                "PE Review": "Approved",
                "PM Signoff": "Approved",
                "Comments": "Soil capacity verified.",
            }
        ],
        "milestones": [
            {
                "Milestone ID": "M01",
                "Milestone Name": (
                    "Technical Site Survey (TSS) & Design Approval"
                ),
                "Department": "Design",
                "Dependencies": "Site Acquisition Signed",
                "Invoiceable": "Optional",
                "Vendor Status": "Submitted",
                "Engineer Verification": "Verified",
                "PM Approval": "Approved",
            },
            {
                "Milestone ID": "M02",
                "Milestone Name": "Permitting & Regulatory Clearance",
                "Department": "N/A",
                "Dependencies": "M01 Approved",
                "Invoiceable": "Optional",
                "Vendor Status": "In Progress",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M03",
                "Milestone Name": "Site Clearing & Excavation",
                "Department": "Implementation",
                "Dependencies": "M02 Approved",
                "Invoiceable": "Yes - Mobilization",
                "Vendor Status": "In Progress",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M04",
                "Milestone Name": "Foundation Pouring & Curing",
                "Department": "Implementation",
                "Dependencies": "M03 Completed",
                "Invoiceable": "No",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M05",
                "Milestone Name": "Tower Erection & Structural Assembly",
                "Department": "Implementation",
                "Dependencies": "M04 Cured (7-14 Days)",
                "Invoiceable": "Yes - RFI",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M06",
                "Milestone Name": "Compound Infrastructure & Grounding",
                "Department": "Implementation",
                "Dependencies": "M04 Completed",
                "Invoiceable": "No",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M07",
                "Milestone Name": "Trenching & Duct Laying",
                "Department": "Implementation",
                "Dependencies": "M03 Completed",
                "Invoiceable": "No",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M08",
                "Milestone Name": "Civil Acceptance & Handover",
                "Department": "Acceptance",
                "Dependencies": "M05, M06, M07 Completed",
                "Invoiceable": "YES - PAT",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
            {
                "Milestone ID": "M09",
                "Milestone Name": "Final Payment",
                "Department": "Acceptance",
                "Dependencies": "M08 Completed",
                "Invoiceable": "YES - FAT",
                "Vendor Status": "Not Started",
                "Engineer Verification": "Pending",
                "PM Approval": "Pending",
            },
        ],
        "invoices": [
            {
                "Invoice #": "INV-ABR-01",
                "Site ID": "RIY-101",
                "Milestone": "Civil Foundation & Anchor Bolts",
                "Amount (SAR)": 12750.00,
                "Status": "Pending FM Audit",
                "Vendor": "Abrar Telecom",
            }
        ],
        "extra_works": [
            {
                "Site ID": "RIY-101",
                "Description": "Hard Rock Excavation Beyond Depth",
                "Requested (SAR)": 5000.00,
                "Cap Limit (10%)": 4250.00,
                "Over Cap": True,
                "Status": "Pending Executive PM Review",
            }
        ],
        "vendors": pd.DataFrame(
            [
                {
                    "Vendor Name": "Abrar Telecom",
                    "Active Sites": 1,
                    "Completed Sites": 14,
                    "Status": "Active Qualified",
                },
                {
                    "Vendor Name": "Red Sea Infra",
                    "Active Sites": 1,
                    "Completed Sites": 8,
                    "Status": "Active Qualified",
                },
                {
                    "Vendor Name": "Gulf Fiber Tech",
                    "Active Sites": 1,
                    "Completed Sites": 5,
                    "Status": "Active Qualified",
                },
            ]
        ),
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = True  # Set default auth for workspace

if "user_role" not in st.session_state:
    st.session_state.user_role = "Project Manager (PMO)"

# --- SIDEBAR CONTROL & NAVIGATION ---
st.sidebar.image(
    "https://img.icons8.com/color/96/antenna.png", width=64
)
st.sidebar.title("GEView PMO System")
st.sidebar.caption("Enterprise Telecom Infrastructure Governance")

# Role Switcher
role = st.sidebar.selectbox(
    "Active System Role",
    [
        "Project Manager (PMO)",
        "Project Engineer",
        "Finance Manager",
        "Subcontractor / Vendor",
    ],
    index=0,
)
st.session_state.user_role = role

st.sidebar.markdown("---")
navigation = st.sidebar.radio(
    "PMO Modules",
    [
        "Portfolio Overview",
        "Site Management & Map",
        "Master BOQ & Price Book",
        "Extra Works (EW) Governance",
        "Milestones & Invoicing",
        "Document Repository",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric(
    "Active Site Models", len(st.session_state.pmo_data["price_book"])
)
st.sidebar.metric(
    "Loaded EW Items",
    len(st.session_state.pmo_data["extra_works_catalog"]),
)

# --- MAIN NAVIGATION ROUTING ---

# 1. PORTFOLIO OVERVIEW
if navigation == "Portfolio Overview":
    st.title("📡 Portfolio Executive Dashboard")
    sites_df = st.session_state.pmo_data["sites"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Active Sites", len(sites_df))
    c2.metric(
        "Total Budget (SAR)", f"{sites_df['Budget (SAR)'].sum():,.2f}"
    )
    c3.metric(
        "Approved POs",
        len(
            [
                p
                for p in st.session_state.pmo_data["purchase_orders"]
                if p["Status"] == "Approved by FM"
            ]
        ),
    )
    c4.metric(
        "Pending Extra Works",
        len(st.session_state.pmo_data["extra_works"]),
    )

    st.markdown("---")
    st.subheader("Site Distribution & Status")
    st.dataframe(sites_df, use_container_width=True)

# 2. SITE MANAGEMENT & MAP
elif navigation == "Site Management & Map":
    st.title("🗺️ Regional Site Tracking & GIS")
    sites_df = st.session_state.pmo_data["sites"]

    if "latitude" in sites_df.columns and "longitude" in sites_df.columns:
        st.map(sites_df[["latitude", "longitude"]])

    st.subheader("Site Directory")
    st.dataframe(sites_df, use_container_width=True)

# 3. MASTER BOQ & PRICE BOOK
elif navigation == "Master BOQ & Price Book":
    st.title("📋 Master BOQ & Vendor Unit Price Catalog")

    tab1, tab2 = st.tabs(["Base Site Models Catalog", "Master UPL / EW Items"])

    with tab1:
        st.subheader("Loaded Site Models Baseline")
        st.dataframe(
            st.session_state.pmo_data["price_book"],
            use_container_width=True,
        )

    with tab2:
        st.subheader("Extra Works Line Item Pricing")
        st.dataframe(
            st.session_state.pmo_data["extra_works_catalog"],
            use_container_width=True,
        )

# 4. EXTRA WORKS GOVERNANCE
elif navigation == "Extra Works (EW) Governance":
    st.title("⚖️ Extra Works Claims & Variation Approval Gate")

    ew_df = pd.DataFrame(st.session_state.pmo_data["extra_works"])
    st.subheader("Pending Variation Requests")
    st.dataframe(ew_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Calculate New Extra Work Line Item")
    c1, c2 = st.columns(2)

    catalog = st.session_state.pmo_data["extra_works_catalog"]
    if not catalog.empty and "EW_Code" in catalog.columns:
        selected_code = c1.selectbox("Select EW Item", catalog["EW_Code"].unique())
        qty = c2.number_input("Quantity", min_value=1.0, value=1.0)

        calc_cost = calculate_ew_item_cost(selected_code, qty)
        st.info(f"Calculated Estimated Value: **{calc_cost:,.2f} USD / SAR**")

# 5. MILESTONES & INVOICING
elif navigation == "Milestones & Invoicing":
    st.title("💳 Milestone Sign-off & Vendor Invoicing Gate")

    st.subheader("Project Milestones Workflow")
    st.dataframe(
        pd.DataFrame(st.session_state.pmo_data["milestones"]),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Submitted Invoices")
    st.dataframe(
        pd.DataFrame(st.session_state.pmo_data["invoices"]),
        use_container_width=True,
    )

# 6. DOCUMENT REPOSITORY
elif navigation == "Document Repository":
    st.title("📁 Site Civil Document Repository")

    selected_site = st.selectbox(
        "Select Site ID", st.session_state.pmo_data["sites"]["Site ID"]
    )
    docs = st.session_state.pmo_data["site_documents"].get(selected_site, {})

    if docs:
        for category, file_list in docs.items():
            with st.expander(f"{category} ({len(file_list)} files)"):
                st.dataframe(pd.DataFrame(file_list), use_container_width=True)
    else:
        st.info(f"No documents currently uploaded for {selected_site}.")