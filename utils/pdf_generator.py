import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_ipc_pdf(ipc_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], fontSize=18, leading=22, textColor=colors.HexColor("#1E3A8A"))
    story.append(Paragraph("INTERIM PAYMENT CERTIFICATE (IPC)", title_style))
    story.append(Spacer(1, 12))

    details = [
        [Paragraph(f"<b>IPC Number:</b> {ipc_data["IPC_Number"]}"), Paragraph(f"<b>Date:</b> {ipc_data["Payment_Date"]}")],
        [Paragraph(f"<b>Client:</b> {ipc_data["Client"]}"), Paragraph(f"<b>Project ID:</b> {ipc_data["Project_ID"]}")],
        [Paragraph(f"<b>Status:</b> {ipc_data["Status"]}"), Paragraph("<b>Currency:</b> SAR")]
    ]
    t_header = Table(details, colWidths=[270, 270])
    t_header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F3F4F6")),
        ("PADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 18))

    financial_data = [
        ["Description", "Amount (SAR)"],
        ["Gross Value of Work Executed", f"{ipc_data["Gross_Amount_SAR"]:,.2f}"],
        ["Saudi VAT Rate", "15%"],
        ["VAT Amount", f"{ipc_data["VAT_15_Percent"]:,.2f}"],
        ["Net Payable Amount", f"{ipc_data["Net_Amount_SAR"]:,.2f}"]
    ]
    t_finance = Table(financial_data, colWidths=[360, 180])
    t_finance.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (1,0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0,0), (1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D1D5DB")),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#FEF08A")),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ]))
    story.append(t_finance)
    story.append(Spacer(1, 30))

    sig_data = [
        ["Prepared By:", "Approved By (Client):"],
        ["\n\n_______________________\nProject Manager", "\n\n_______________________\nAuthorized Signatory"]
    ]
    t_sig = Table(sig_data, colWidths=[270, 270])
    story.append(t_sig)

    doc.build(story)
    buffer.seek(0)
    return buffer
