import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_vendor_comparison_module(fx_rate):
    st.subheader("⚖️ Vendor Price Book & Rate Comparison Matrix")
    st.caption("Side-by-side cost variance analysis between Vendor 1 (Ven1) and Vendor 2 (Ven2).")

    v1_towers = [
        {"Model": "MODEL 1-RT 6m Pole (Type I)", "V1_USD": 21782.03, "V2_USD": 16678.33},
        {"Model": "MODEL 2-RT 9m Pole (Type I)", "V1_USD": 22593.16, "V2_USD": 18295.00},
        {"Model": "MODEL 3-RT 9m Square Tower (Type II)", "V1_USD": 23369.42, "V2_USD": 19426.67},
        {"Model": "Model 4-RT 12m Square Tower (Type II)", "V1_USD": 25220.86, "V2_USD": 18929.19},
        {"Model": "Model 5- RT 9m Penetrating (Type III)", "V1_USD": 24167.37, "V2_USD": 18241.00}
    ]

    comp_df = pd.DataFrame(v1_towers)
    comp_df["V1_SAR"] = comp_df["V1_USD"] * fx_rate
    comp_df["V2_SAR"] = comp_df["V2_USD"] * fx_rate
    comp_df["Variance (SAR)"] = comp_df["V1_SAR"] - comp_df["V2_SAR"]
    comp_df["Variance %"] = ((comp_df["V1_SAR"] - comp_df["V2_SAR"]) / comp_df["V1_SAR"]) * 100

    st.markdown("### 🗼 Tower Model Cost Comparison (SAR)")
    st.dataframe(
        comp_df.style.format({
            "V1_USD": "${:,.2f}",
            "V2_USD": "${:,.2f}",
            "V1_SAR": "SAR {:,.2f}",
            "V2_SAR": "SAR {:,.2f}",
            "Variance (SAR)": "SAR {:,.2f}",
            "Variance %": "{:.1f}%"
        }),
        use_container_width=True
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(x=comp_df["Model"], y=comp_df["V1_SAR"], name="Vendor 1 (Ven1)", marker_color="#0284C7"))
    fig.add_trace(go.Bar(x=comp_df["Model"], y=comp_df["V2_SAR"], name="Vendor 2 (Ven2)", marker_color="#10B981"))

    fig.update_layout(
        title="Tower Model Pricing Comparison (SAR)",
        barmode='group',
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#1E293B",
        font_color="#F8FAFC",
        height=400,
        xaxis=dict(gridcolor="#334155"),
        yaxis=dict(title="Price (SAR)", gridcolor="#334155")
    )
    st.plotly_chart(fig, use_container_width=True)
