import jinja2
import pdfkit
from datetime import datetime
import os
from Constant.converterFunctions import convertTimeStampToId
from Constant.treatmentDatabaseFunctions import getAllTreatmentByCustomerId
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")


def generate_customer_pdf(customerModel):
    customer_name = customerModel.customerName
    customer_id = convertTimeStampToId(customerModel.customerId)

    customer_ic_passport = customerModel.ic  
    gender = customerModel.gender
    race = customerModel.race
    cus_phone_number = customerModel.handphone
    address = customerModel.address
    date =datetime.today().strftime("%d %b, %Y")
    treatment_list = getAllTreatmentByCustomerId(customer_id)  # A list of treatmentModel objects

    context = {"customer_name": customer_name,
               "customer_id": customer_id,
                "customer_ic_passport": customer_ic_passport,
                "gender": gender,
                "race": race,
                "cus_phone_number": cus_phone_number,
                "address": address,
                "date_generated": date,
                "treatments": treatment_list,
                
               }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the templates folder
    template_dir = os.path.join(base_dir, 'templates')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    template = env.get_template('customer_details_template.html')
    options = {
    'enable-local-file-access': ''
    }

    output_text = template.render(context)    
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    options = {
        'enable-local-file-access': ''
    }
    pdfkit.from_string(output_text, f'{DESKTOP_PATH}/{customer_name}_{customer_id}_report.pdf', configuration=config, options=options)
    print(f"PDF generated for customer {customer_id}")
    print(f'treatment_list0: {treatment_list[len(treatment_list)-1]}')