import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_site_boq_pdf(site_id, site_name, vendor_name, tower_item, ew_items, total_usd, total_sar, fx_rate):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0F172A'))
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#64748B'))
    sec_style = ParagraphStyle('Sec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#1E293B'), spaceBefore=10, spaceAfter=6)

    story = []

    # Header
    story.append(Paragraph("PROJECT PLUS — OFFICIAL SITE BOQ BREAKDOWN", title_style))
    story.append(Paragraph(f"Site ID: {site_id} | Site Name: {site_name} | Assigned Vendor: {vendor_name}", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=12))

    # Meta Table
    meta_data = [
        ["FX Rate Applied:", f"1 USD = {fx_rate:.2f} SAR", "Total BOQ (USD):", f"${total_usd:,.2f}"],
        ["Generated Date:", "Current Status: Approved", "Total BOQ (SAR):", f"SAR {total_sar:,.2f}"]
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 110, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#334155')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Line Items Table
    story.append(Paragraph("Line Itemized Rate Schedule", sec_style))
    items_data = [["Category", "Description / Spec", "Unit", "Rate (USD)", "Rate (SAR)"]]

    if tower_item:
        items_data.append(["Tower Model", tower_item['Model'], "Unit", f"${tower_item['USD']:,.2f}", f"SAR {tower_item['USD']*fx_rate:,.2f}"])

    for ew in ew_items:
        items_data.append(["Extra Work", ew['Item'], ew['Unit'], f"${ew['USD']:,.2f}", f"SAR {ew['USD']*fx_rate:,.2f}"])

    items_data.append(["TOTAL", "Combined BOQ Total Allocation", "-", f"${total_usd:,.2f}", f"SAR {total_sar:,.2f}"])

    boq_table = Table(items_data, colWidths=[80, 240, 40, 90, 90])
    boq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E0F2FE')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))

    story.append(boq_table)
    doc.build(story)
    return buffer.getvalue()
