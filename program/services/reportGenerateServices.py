import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from utils import resourcePath
from Constant.fileKeywords import CONSENT_FORM_KEYWORD
from Constant.appConstant import FONT_REPORT



# Register fonts
pdfmetrics.registerFont(TTFont("Soho-Regular", str(FONT_REPORT["SOHO_REGULAR"])))
pdfmetrics.registerFont(TTFont("Soho-Bold", str(FONT_REPORT["SOHO_BOLD"])))
pdfmetrics.registerFont(TTFont("NotoSansCJK", str(FONT_REPORT["SOHO"])))  # Chinese support


def generateCustomerConsentForm(customerModel, customerId):
    """
    Generate a professional PDF consent form containing customer details.
    """
    file_name = f"{customerModel.customerName}{CONSENT_FORM_KEYWORD}-FORM.pdf"
    attachment_type = "Customer"
    save_path = resourcePath(os.path.join("data", "attachment", str(customerId), attachment_type, "Consent", file_name))
    
    # Ensure save directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Styles
    styles = getSampleStyleSheet()

    title = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Soho-Bold",
        fontSize=22,
        textColor=colors.HexColor("#003B73"),
        spaceAfter=18,
    )

    header_label = ParagraphStyle(
        "HeaderLabel",
        parent=styles["Normal"],
        fontName="Soho-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#003B73"),
    )

    field_style = ParagraphStyle(
        "FieldStyle",
        parent=styles["Normal"],
        fontName="Soho-Regular",
        fontSize=12,
        leading=16,
        spaceAfter=3,
    )

    body_text = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontName="NotoSansCJK",     # Chinese support
        fontSize=11,
        leading=16,
        spaceAfter=10,
    )

    signature_style = ParagraphStyle(
        "Signature",
        parent=styles["Normal"],
        fontName="Soho-Regular",
        fontSize=12,
        leading=18,
    )

    # ------------------------------------------
    # Consent text (bilingual polished version)
    # ------------------------------------------
    CONSENT_TEXT = """
    <b>CONSENT FOR TREATMENT</b> <br/><br />
    
    I understand that I can ask any questions pertaining to the therapy before filling this form. 
    I could, if the need arises, withdraw my consent to stop the therapy at any time throughout the procedure. <br/><br/>
    
    The procedure, its risks and benefits have been explained to me, and I understand the explanation given. <br/><br/>
    I hereby agree for the therapy to be carried out on me. <br/><br/>
    
    I also understand that a record of the therapy 
    given shall be kept. This record is confidential and will not be disclosed to an outside party, unless it 
    has been authorised by me, or my representative, or as ordered by the court of law to do so.
    """

    story = []

    # ----------------------------------------------------
    # Title section with spacing
    # ----------------------------------------------------
    story.append(Paragraph("Customer Consent Statement", title))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # Customer Details Table (clean layout)
    # ----------------------------------------------------
    customer_data = [
        [Paragraph("<b>Name</b>", header_label), Paragraph(customerModel.customerName, field_style)],
        [Paragraph("<b>IC</b>", header_label), Paragraph(customerModel.ic, field_style)],
        [Paragraph("<b>Gender</b>", header_label), Paragraph(customerModel.gender, field_style)],
        [Paragraph("<b>Race</b>", header_label), Paragraph(customerModel.race, field_style)],
        [Paragraph("<b>Address</b>", header_label), Paragraph(customerModel.address, field_style)],
        [Paragraph("<b>Phone</b>", header_label), Paragraph(customerModel.handphone, field_style)],
    ]

    table = Table(customer_data, colWidths=[40 * mm, 120 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 14))

    # ----------------------------------------------------
    # Consent Text Block
    # ----------------------------------------------------
    story.append(Paragraph(CONSENT_TEXT, body_text))
    story.append(Spacer(1, 20))

    # ----------------------------------------------------
    # Signature Section
    # ----------------------------------------------------
    story.append(Paragraph("Signature / 签名： _______________________________", signature_style))
    story.append(Spacer(1, 10))

    today_str = datetime.now().strftime("%Y-%m-%d")
    story.append(Paragraph(f"Name / 名字： _______________________________", signature_style))
    story.append(Spacer(1, 20))

    # ----------------------------------------------------
    # Build PDF
    # ----------------------------------------------------
    doc = SimpleDocTemplate(
        save_path,
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc.build(
        story,
        onFirstPage=lambda canvas, doc: add_footer(canvas, doc, generated_date),
        onLaterPages=lambda canvas, doc: add_footer(canvas, doc, generated_date),
    )

    return save_path


def generateAppointmentPdf(appointments_by_date, save_path):
    """
    Generate a PDF report for selected appointments.
    appointments_by_date: dict { "YYYY-MM-DD": [ {dict of appt info}, ... ] }
    save_path: final PDF path to save to.
    """
    # Create directory if not exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName="Soho-Bold",
        fontSize=22,
        textColor=colors.HexColor("#003B73"),
        spaceAfter=20,
    )

    normal = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontName="Soho-Regular",
        fontSize=12,
        leading=16,
        spaceAfter=6,
    )

    markdown_bold = ParagraphStyle(
        "BoldText",
        parent=styles["Normal"],
        fontName="Soho-Bold",
        fontSize=12,
        leading=16,
        spaceAfter=6,
    )

    story = []
    story.append(Paragraph("Appointment Details", title_style))
    story.append(Spacer(1, 12))

    # -------- Build content --------
    for date_str in sorted(appointments_by_date.keys(), reverse=True):
        
        # Determine day name
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%A")
        except:
            day_name = ""

        # Day + date title
        story.append(Paragraph(f"<b>{day_name} {date_str}</b>", markdown_bold))
        story.append(Paragraph("=" * 16, normal))
        story.append(Spacer(1, 6))

        # Appointment entries
        for appt in appointments_by_date[date_str]:

            story.append(Paragraph(f"{appt['time']} ({appt['customer_id']})", normal))
            story.append(Paragraph(f"<b>{appt['name']} {appt['contact']}</b>", markdown_bold))
            story.append(Paragraph(f"<i>{appt['condition']}</i>", normal))
            story.append(Paragraph(f"<i>{appt['treatment']}</i>", normal))

            story.append(Spacer(1, 14))   # blank space between appointments

    # -------- Build PDF --------
    doc = SimpleDocTemplate(
        save_path,
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    generated_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc.build(
        story,
        onFirstPage=lambda canvas, doc: add_footer(canvas, doc, generated_date),
        onLaterPages=lambda canvas, doc: add_footer(canvas, doc, generated_date),
    )

    return save_path


def add_footer(canvas, doc, generated_date):
    canvas.saveState()
    canvas.setFont("Soho-Regular", 9)

    # ---- Footer Content ----
    company_name = "杨式龙跌打馆 Yeoh Sek Leong Tuinalogy Center"
    created_text = f"Created on: {generated_date}"

    page_width = doc.pagesize[0]

    # Left-aligned company name (20 pts from left edge)
    canvas.drawString(20, 15, company_name)

    # Right-aligned created date (20 pts from right edge)
    canvas.drawRightString(page_width - 20, 15, created_text)

    canvas.restoreState()