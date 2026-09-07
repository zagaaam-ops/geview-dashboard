import streamlit as st
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pat_pdf(site_id, site_name, contractor, region, checklist_results, engineer_name, remarks):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Title Block
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=1, # Center
        spaceAfter=15
    )
    story.append(Paragraph("<b>PROJECT PLUS - PROVISIONAL ACCEPTANCE CERTIFICATE (PAT)</b>", title_style))
    story.append(Spacer(1, 10))

    # Meta Information Table
    meta_data = [
        [Paragraph("<b>Site ID:</b>", styles['Normal']), Paragraph(site_id, styles['Normal']),
         Paragraph("<b>Date:</b>", styles['Normal']), Paragraph(datetime.now().strftime("%Y-%m-%d"), styles['Normal'])],
        [Paragraph("<b>Site Name:</b>", styles['Normal']), Paragraph(site_name, styles['Normal']),
         Paragraph("<b>Region:</b>", styles['Normal']), Paragraph(region, styles['Normal'])],
        [Paragraph("<b>Contractor:</b>", styles['Normal']), Paragraph(contractor, styles['Normal']),
         Paragraph("<b>Inspector:</b>", styles['Normal']), Paragraph(engineer_name, styles['Normal'])],
    ]
    meta_table = Table(meta_data, colWidths=[1.2*inch, 2.3*inch, 1.2*inch, 2.3*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Checklist Results
    story.append(Paragraph("<b>Inspection Checklist Verification</b>", styles['Heading2']))
    story.append(Spacer(1, 8))

    table_data = [["Category", "Inspection Item", "Status"]]
    for item in checklist_results:
        status_color = "#16A34A" if item["Status"] == "PASS" else "#DC2626"
        status_p = Paragraph(f"<font color='{status_color}'><b>{item['Status']}</b></font>", styles['Normal'])
        table_data.append([item["Category"], item["Item"], status_p])

    checklist_table = Table(table_data, colWidths=[2.0*inch, 4.0*inch, 1.0*inch])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(checklist_table)
    story.append(Spacer(1, 15))

    # Remarks & Sign-off
    story.append(Paragraph("<b>Inspector Remarks:</b>", styles['Heading3']))
    story.append(Paragraph(remarks if remarks else "All items inspected according to telecom civil and structural baseline standards.", styles['Normal']))
    story.append(Spacer(1, 25))

    sig_data = [
        ["___________________________________", "___________________________________"],
        ["Field Supervisor Signature", "Project Manager / Client Sign-off"]
    ]
    sig_table = Table(sig_data, colWidths=[3.5*inch, 3.5*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(sig_table)

    doc.build(story)
    return buffer.getvalue()

def render_acceptance_module(df):
    st.subheader("📋 Digital Site Acceptance & PAT/FAC Certificate Generator")
    st.caption("Perform digital punch list verification and issue formal site acceptance sign-offs.")

    selected_site_str = st.selectbox(
        "Select Site for Handover Inspection:",
        options=df['Site ID'] + " - " + df['Name']
    )
    
    site_id = selected_site_str.split(" - ")[0]
    site_row = df[df['Site ID'] == site_id].iloc[0]

    st.markdown(f"### Inspection Checklist: `{site_id}` ({site_row['Name']})")

    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.write(f"**Region:** {site_row['Region']}")
    col_info2.write(f"**Contractor:** {site_row['Contractor']}")
    col_info3.write(f"**Current Progress:** {int(site_row['Overall Progress']*100)}%")

    st.markdown("---")

    # Interactive Checklist Form
    with st.form(key="pat_form"):
        st.markdown("#### 1. Civil & Foundation Scope")
        c1 = st.checkbox("Foundation concrete strength test verified", value=True)
        c2 = st.checkbox("Tower anchor bolts torque & verticality alignment within tolerance", value=True)
        c3 = st.checkbox("Compound fencing, gate lock, and site drainage verified", value=True)

        st.markdown("#### 2. Tower Structure & Antennas")
        c4 = st.checkbox("Tower lattice steel structure galvanized & paint inspection cleared", value=True)
        c5 = st.checkbox("Antenna mounts azimuth & tilt aligned to design RF sheet", value=True)
        c6 = st.checkbox("Aviation warning light and lightning rod grounding installed", value=True)

        st.markdown("#### 3. Power & Telecom Grounding")
        c7 = st.checkbox("Earth pit resistance test <= 5 Ohms verified", value=True)
        c8 = st.checkbox("Rectifier unit, battery backup, and AC DB board tested", value=True)

        st.markdown("---")
        inspector_name = st.text_input("Inspector / Lead Engineer Name:", value="Rana Muhammad Zagham Ali - PMP®")
        remarks = st.text_area("Punch List / Handover Remarks:", value="Site civil and structural works verified. Ready for PAT sign-off.")

        submit_pat = st.form_submit_button("Generate Official PAT Certificate PDF")

    if submit_pat:
        checklist_items = [
            {"Category": "Civil", "Item": "Foundation concrete strength test", "Status": "PASS" if c1 else "FAIL"},
            {"Category": "Civil", "Item": "Tower anchor bolts & verticality", "Status": "PASS" if c2 else "FAIL"},
            {"Category": "Civil", "Item": "Compound fencing & drainage", "Status": "PASS" if c3 else "FAIL"},
            {"Category": "Structure", "Item": "Tower steel & galvanization", "Status": "PASS" if c4 else "FAIL"},
            {"Category": "Telecom RF", "Item": "Antenna mounts azimuth & tilt", "Status": "PASS" if c5 else "FAIL"},
            {"Category": "Safety", "Item": "Aviation light & lightning protection", "Status": "PASS" if c6 else "FAIL"},
            {"Category": "Power/Electrical", "Item": "Earth pit resistance <= 5 Ohms", "Status": "PASS" if c7 else "FAIL"},
            {"Category": "Power/Electrical", "Item": "Rectifier & battery backup system", "Status": "PASS" if c8 else "FAIL"},
        ]

        pdf_bytes = generate_pat_pdf(
            site_id=site_row['Site ID'],
            site_name=site_row['Name'],
            contractor=site_row['Contractor'],
            region=site_row['Region'],
            checklist_results=checklist_items,
            engineer_name=inspector_name,
            remarks=remarks
        )

        st.success(f"Provisional Acceptance Test Certificate generated for {site_id}!")
        st.download_button(
            label="📄 Download PAT Certificate (PDF)",
            data=pdf_bytes,
            file_name=f"PAT_Certificate_{site_id}.pdf",
            mime="application/pdf"
        )
