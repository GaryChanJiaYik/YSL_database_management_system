import os
import customtkinter as ctk
import subprocess
import platform
from utils import resourcePath
from datetime import datetime
from Constant.treatmentDatabaseFunctions import getTreatmentByID
from Constant.appConstant import FONT_REPORT
from Components.popupModal import renderPopUpModal
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from services.attachmentFilesServices import saveAttachmentFile, HasAttachment, ERROR, SUCCESS

# Register fonts
pdfmetrics.registerFont(TTFont('Soho-Regular', str(FONT_REPORT["SOHO_REGULAR"])))
pdfmetrics.registerFont(TTFont('Soho-Bold', str(FONT_REPORT["SOHO_BOLD"])))
pdfmetrics.registerFont(TTFont('NotoSansCJK', str(FONT_REPORT["SOHO"])))  # For Chinese

ATTACHMENT_TYPE = "Treatment"
CONSENT_TEXT = ''' 
I understand that I can ask any questions pertaining to the therapy before filling this form proceed treament with my signature above.
I could, if the need arises, withdraw my consent to stop the therapy at any time throughout the procedure. 
The procedure, its risks and benefits have been explained to me, and I understand the explanation given.
'''

class ViewGenerateReportView(ctk.CTkFrame):
    def __init__(self, parent, controller, customerModel, conditionModel, treatmentID):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.customerModel = customerModel
        self.conditionModel = conditionModel
        self.treatmentModel = getTreatmentByID(treatmentID)

        self.customerId = self.getFormattedId(self.customerModel.customerId)
        treatment_date_str = self.treatmentModel.treatmentDate
        if isinstance(treatment_date_str, str):
            try:
                dt_obj = datetime.fromisoformat(treatment_date_str)
            except ValueError:
                dt_obj = datetime.strptime(treatment_date_str, "%Y-%m-%d %H:%M:%S")
        else:
            dt_obj = treatment_date_str
        self.default_filename = f"{dt_obj.strftime('%Y%m%d%H%M%S')}_YSLReport.pdf"

        # --- UI ---
        self.title_label = ctk.CTkLabel(self, text="Patient Report", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.preview_textbox = ctk.CTkTextbox(self, width=600, height=400)
        self.preview_textbox.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        # Auto-generate preview
        self.preview_report()
        # Render Save/View buttons
        self.renderReportOptionButtons(row=0, column=0)

    # -------------------
    # Generate Report Text
    # -------------------
    def generate_report_text(self):
        c = self.customerModel
        cond = self.conditionModel
        t = self.treatmentModel

        treatment_date_str = self.format_datetime(t.treatmentDate)
        appointment_date_str = self.format_datetime(t.appointmentDate)

        report_lines = [
            "=== Customer Details ===",
            f"Old Customer ID: {c.oldCustomerId}",
            f"Name: {c.customerName}",
            f"IC: {c.ic}",
            f"Gender: {c.gender}",
            f"Race: {c.race}",
            f"Address: {c.address}",
            f"Handphone: {c.handphone}",
            "",
            "=== Condition & Treatment Details ===",
            f"Condition Description: {cond.conditionDescription}",
            f"Treatment Date: {treatment_date_str}",
            f"Appointment Date: {appointment_date_str}",
            f"Treatment Description: {t.treatmentDescription}",
            "",
            "Pain Levels (Before / After)",
            f"Pain: {t.painLevel} / {t.painLevelAfter}",
            f"Tense: {t.tenseLevel} / {t.tenseLevelAfter}",
            f"Sore: {t.soreLevel} / {t.soreLevelAfter}",
            f"Numb: {t.numbLevel} / {t.numbLevelAfter}",
            "",
            "=== Consent Statement ===",
            CONSENT_TEXT
        ]
        return "\n".join(report_lines)

    # -------------------
    # Format DateTime
    # -------------------
    def format_datetime(self, dt_value):
        if isinstance(dt_value, str):
            try:
                dt_obj = datetime.fromisoformat(dt_value)
            except ValueError:
                dt_obj = datetime.strptime(dt_value, "%Y-%m-%d %H:%M:%S")
        else:
            dt_obj = dt_value
        return dt_obj.strftime("%d/%m/%Y %I:%M %p")  # No seconds, AM/PM
    
    # -------------------
    # Get Customer Formatted ID
    # -------------------
    def getFormattedId(self, customerId):
        dt = datetime.strptime(customerId, '%m/%d/%Y %H:%M:%S')
        formatted_id = f"{dt.month}{dt.day}{dt.year}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
        return formatted_id

    # -------------------
    # Preview in Textbox
    # -------------------
    def preview_report(self):
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("1.0", self.generate_report_text())
        
    # -------------------
    # Render Save/View Buttons
    # -------------------
    def renderReportOptionButtons(self, row, column):
        # Clear old buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # View Report Button first (if exists)
        if HasAttachment(self.customerId, ATTACHMENT_TYPE, entity_id=self.treatmentModel.treatmentID , filename_contains="_YSLReport"):
            ctk.CTkButton(
                master=self.button_frame,
                text="View Report",
                command=self.view_report
            ).grid(row=row, column=column, sticky="w", padx=(10,5), pady=5)

        # Save Report Button (green)
        ctk.CTkButton(
            master=self.button_frame,
            text="Save Report",
            command=self.save_report,
            fg_color="green"
        ).grid(row=row, column=column+1, sticky="w", padx=(10,5), pady=5)

    # -------------------
    # Save Report PDF
    # -------------------
    def save_report(self):
        default_path = resourcePath(os.path.join("data","attachment", self.getFormattedId(self.customerModel.customerId), ATTACHMENT_TYPE, self.treatmentModel.treatmentID, self.default_filename))
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        
        try:
            # Generate PDF directly to default path
            self.generate_pdf_report(default_path)

            # Save via saveAttachmentFile to customer's folder (optional backup)
            # result = saveAttachmentFile(self.customerId, default_path, ATTACHMENT_TYPE, entity_id=self.treatmentModel.treatmentID)
            if os.path.isfile(default_path):
                result = SUCCESS

            if result == SUCCESS:
                # Refresh buttons to show "View Report" if not already
                for widget in self.button_frame.winfo_children():
                    widget.destroy()
                self.renderReportOptionButtons(row=0, column=0)

               # Show success popup using custom modal
                renderPopUpModal(
                    self.parent,
                    f"Report saved successfully.",
                    "Save Report",
                    "Success"
                )
            else:
                renderPopUpModal(
                    self.parent,
                    "Error saving report file.",
                    "Save Report",
                    "Error"
                )
        except Exception as e:
            renderPopUpModal(
                self.parent,
                # f"Failed to generate report.\nClose any open PDF viewers and try again.",
                f"Failed to generate report.\n{str(e)}",
                "Save Report",
                "Error"
            )


    # -------------------
    # View Report PDF
    # -------------------
    def view_report(self):
        customer_folder = resourcePath(os.path.join("data","attachment", self.customerId, ATTACHMENT_TYPE, self.treatmentModel.treatmentID))
        if os.path.isdir(customer_folder):
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{customer_folder}"')
            elif platform.system() == "Darwin":
                subprocess.call(["open", customer_folder])
            else:
                subprocess.call(["xdg-open", customer_folder])


    # -------------------
    # Generate PDF (ReportLab)
    # -------------------
    def generate_pdf_report(self, file_path):
        c = self.customerModel
        cond = self.conditionModel
        t = self.treatmentModel

        treatment_date_str = self.format_datetime(t.treatmentDate)
        appointment_date_str = self.format_datetime(t.appointmentDate)

        # Document setup
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=25*mm,
            leftMargin=25*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )

        # Styles
        styles = getSampleStyleSheet()
        BLUE = colors.HexColor("#0070C0")  # Custom blue

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Soho-Bold',
            fontSize=20,
            textColor=BLUE,
            leading=24,
            spaceAfter=12
        )

        section_header = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Soho-Bold',
            fontSize=14,
            textColor=BLUE,
            spaceBefore=15,
            spaceAfter=8
        )

        normal = ParagraphStyle(
            'NormalCJK',
            parent=styles['Normal'],
            fontName='Soho-Regular',
            fontSize=10,
            textColor=colors.black  # ensure text is black
        )

        story = []

        # --- Title ---
        story.append(Paragraph("Patient Treatment Report", title_style))
        story.append(Spacer(1, 12))

        # --- Customer Details Table ---
        story.append(Paragraph("Customer Details", section_header))
        data_customer = [
            ["Old Customer ID", c.oldCustomerId],
            ["Name", c.customerName],
            ["IC", c.ic],
            ["Gender", c.gender],
            ["Race", c.race],
            ["Address", c.address],
            ["Handphone", c.handphone]
        ]
        customer_table = Table(data_customer, colWidths=[130, 350])
        customer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),  # header row
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),  # body rows
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (0,-1), 'Soho-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Soho-Regular'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 0.5, BLUE),
            ('INNERGRID', (0,0), (-1,-1), 0.25, BLUE),
            ('BACKGROUND', (0,1), (0,-1), colors.whitesmoke)  # first column light gray
        ]))
        story.append(customer_table)
        story.append(Spacer(1, 15))

        # --- Condition & Treatment Table ---
        story.append(Paragraph("Condition & Treatment Details", section_header))
        data_treatment = [
            ["Condition Description", cond.conditionDescription],
            ["Treatment Date", treatment_date_str],
            ["Appointment Date", appointment_date_str],
            ["Treatment Description", t.treatmentDescription],
            ["Pain (Before/After)", f"{t.painLevel} / {t.painLevelAfter}"],
            ["Tense (Before/After)", f"{t.tenseLevel} / {t.tenseLevelAfter}"],
            ["Sore (Before/After)", f"{t.soreLevel} / {t.soreLevelAfter}"],
            ["Numb (Before/After)", f"{t.numbLevel} / {t.numbLevelAfter}"]
        ]
        treatment_table = Table(data_treatment, colWidths=[150, 330])
        treatment_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), BLUE),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),  # header row
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),  # body rows
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (0,-1), 'Soho-Bold'),
            ('FONTNAME', (1,0), (1,-1), 'Soho-Regular'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOX', (0,0), (-1,-1), 0.5, BLUE),
            ('INNERGRID', (0,0), (-1,-1), 0.25, BLUE),
            ('BACKGROUND', (0,1), (0,-1), colors.whitesmoke)  # first column light gray
        ]))
        story.append(treatment_table)
        story.append(Spacer(1, 20))

        # --- Consent Statement ---
        story.append(Paragraph("Consent Statement", section_header))
        consent_text = CONSENT_TEXT
        story.append(Paragraph(consent_text, normal))

        # --- Signature Section ---
        story.append(Spacer(1, 40))
        story.append(Paragraph("Patient Signature: ___________________________", normal))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Name: ________________________________", normal))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Date: ________________________________", normal))

        # Build PDF
        doc.build(
            story,
            onFirstPage=self.add_footer,
            onLaterPages=self.add_footer
        )
        
        
    def add_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Soho-Regular", 9)

        company_name = "杨式龙跌打馆 Yeoh Sek Leong Tuinalogy Center"

        # Left-aligned footer (20 pt from the left)
        canvas.drawString(20, 15, company_name)

        canvas.restoreState()


