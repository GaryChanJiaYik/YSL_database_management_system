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
    file_name = f"{customerModel.customerName}{CONSENT_FORM_KEYWORD}-TEMPLATE.pdf"
    entity_id = "CUSTOMER"
    save_path = resourcePath(os.path.join("data", "attachment", str(customerId), entity_id, file_name))

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
    <b>CONSENT FOR TREATMENT</b><br/>
    <b>治疗同意书</b><br/><br/>

    I understand that I may ask any questions pertaining to the therapy before completing this form. 
    I acknowledge that I may withdraw my consent and stop the therapy at any time during the procedure.<br/><br/>

    我明白在填写此表格之前，我可以询问与治疗相关的任何问题。  
    我也了解在治疗进行过程中，我有权随时撤回同意并终止治疗。<br/><br/>

    The procedure, including its risks and benefits, has been clearly explained to me, and I confirm 
    that I understand the explanation given.<br/><br/>

    治疗的程序、风险及益处已向我清楚说明，我确认已充分理解相关内容。<br/><br/>

    I hereby agree to undergo the therapy. I also understand that a record of the treatment provided 
    to me will be kept. This record is confidential and will not be disclosed to any external party 
    unless authorised by me, my representative, or required by an order of the court of law.<br/><br/>

    我在此同意接受治疗。我也明白治疗记录将被保存，并会受到严格保密，除非经由本人、  
    我的代表授权，或根据法院指令，否则不会向任何外部人士披露。
    """

    story = []

    # ----------------------------------------------------
    # Title section with spacing
    # ----------------------------------------------------
    story.append(Paragraph("Customer Consent Form / 客户治疗同意书", title))
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
    story.append(Paragraph(f"Date / 日期： _______________________________", signature_style))
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

def add_footer(canvas, doc, generated_date):
    canvas.saveState()
    canvas.setFont("Soho-Regular", 9)

    footer_text = f"Generated on: {generated_date}"

    page_width = doc.pagesize[0]

    # Right-aligned footer (20 pts from right edge)
    canvas.drawRightString(page_width - 20, 15, footer_text)

    canvas.restoreState()