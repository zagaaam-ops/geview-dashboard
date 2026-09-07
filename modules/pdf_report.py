import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_pdf_report(df):
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Header
    story.append(Paragraph("PROJECT PLUS — EXECUTIVE STATUS REPORT", title_style))
    story.append(Paragraph("Telecom Infrastructure PMIS | Confidential & Proprietary", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceAfter=15))

    # Executive KPI Summary Table
    total_sites = len(df)
    avg_progress = (df['Overall Progress'].mean() * 100) if total_sites > 0 else 0
    total_budget = df['Budget'].sum() if 'Budget' in df.columns else 0
    total_actual = df['Actual'].sum() if 'Actual' in df.columns else 0
    avg_cpi = df['CPI'].mean() if 'CPI' in df.columns else 1.0

    kpi_data = [
        ["Total Active Sites", "Average Progress", "Total Budget", "Total Actual Spend", "Average CPI"],
        [f"{total_sites}", f"{avg_progress:.1f}%", f"${total_budget:,.0f}", f"${total_actual:,.0f}", f"{avg_cpi:.2f}"]
    ]

    kpi_table = Table(kpi_data, colWidths=[108]*5)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#0284C7')),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 11),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(Paragraph("Portfolio Overview", section_heading))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # Detailed Site Rollout Table
    story.append(Paragraph("Site Breakdown & Performance", section_heading))

    table_data = [["Site ID", "Site Name", "Region", "Contractor", "Progress", "Budget ($)", "Actual ($)", "Risk"]]
    
    for _, row in df.iterrows():
        table_data.append([
            str(row.get('Site ID', '')),
            str(row.get('Name', ''))[:18],
            str(row.get('Region', '')),
            str(row.get('Contractor', ''))[:15],
            f"{row.get('Overall Progress', 0)*100:.0f}%",
            f"{row.get('Budget', 0):,.0f}",
            f"{row.get('Actual', 0):,.0f}",
            str(row.get('Risk', ''))
        ])

    site_table = Table(table_data, colWidths=[60, 110, 60, 90, 50, 65, 65, 40])
    site_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (4,0), (6,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(site_table)
    story.append(Spacer(1, 20))

    # Footer Notice
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
    story.append(Paragraph("Generated automatically by Project Plus PMIS | Author: Rana Muhammad Zagham - PMP®", body_style))

    doc.build(story)
    return buffer.getvalue()
