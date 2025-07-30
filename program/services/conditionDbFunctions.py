import csv
import os
import Model.conditionModel as CM
from datetime import datetime
from utils import resource_path

DB_PATH = resource_path('./data/conditionDb.csv')


import Constant.dbColumn as dbCol

def getAllConditionsByCustomerId(customerId):
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdConditionDb)
        condition_id = header.index(dbCol.conditionId)
        condition_description = header.index(dbCol.conditionDescription)
        undergoing_treatment = header.index(dbCol.undergoingTreatment)
        condition_date = header.index(dbCol.conditionDate)
      

        result = []

        for line in csvFile:
            if line != []:

                print(f'{line[customer_id_index]} == {customerId} --> {line[customer_id_index] == customerId}')
                if line[customer_id_index] == customerId:
                    condition = CM.ConditionModel(
                        customerId=customerId,
                        condition_id=line[condition_id],
                        conditionDescription=line[condition_description],
                        undergoingTreatment=line[undergoing_treatment],
                        conditionDate=line[condition_date]
                    )
                    result.append(condition)
        sorted_result = sorted(result, key=lambda x: parse_date_safe(x.conditionDate), reverse=True)  # Sort by conditionDate in descending order
        return sorted_result


def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return datetime.min  # or datetime.max if sorting descending


def insertConditionToDb(conditionModel):
    with open(DB_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  

        writer_object = csv.writer(file)
        data = [value for key, value in vars(conditionModel).items()]
        writer_object.writerow(data)

    
def updateTreatmentStatus(customer_id, condition_id, is_treated):
    print(f"Updating treatment status for customer {customer_id}, condition {condition_id}")
    temp_file_path = DB_PATH + ".tmp"
    updated = False

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        customer_idx = header.index("customerId")
        condition_idx = header.index("conditionId")
        treatment_status_idx = header.index("undergoingTreatment")

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[customer_idx] == str(customer_id) and row[condition_idx] == condition_id:
                row[treatment_status_idx] = "False" if is_treated else "True"
                updated = True

            writer.writerow(row)

    if updated:
        os.replace(temp_file_path, DB_PATH)
        print("Treatment status updated successfully.")
    else:
        os.remove(temp_file_path)
        print("No matching treatment found. Status not updated.")

    return updated
        

def getTreatmentStatus(customer_id, condition_id):
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)

        customer_idx = header.index("customerId")
        condition_idx = header.index("conditionId")
        treatment_status_idx = header.index("undergoingTreatment")

        for row in csvFile:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[customer_idx] == str(customer_id) and row[condition_idx] == condition_id:
                return row[treatment_status_idx] == "False"  # "False" = treated

    return False  # Default to not treated if no match found


def updateConditionByID(condition_id, new_description, new_datetime):
    temp_file_path = DB_PATH + ".tmp"
    updated = False

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)

        condition_id_idx = header.index('conditionId')
        description_idx = header.index('conditionDescription')
        datetime_idx = header.index('conditionDate')  # Make sure this column exists

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[condition_id_idx].strip() == condition_id:
                print("Updating condition:", condition_id)
                row[description_idx] = new_description
                row[datetime_idx] = new_datetime
                updated = True

            writer.writerow(row)

    if updated:
        os.replace(temp_file_path, DB_PATH)
    else:
        os.remove(temp_file_path)

    return updated


def deleteCondition(condition_id):
    temp_file_path = DB_PATH + ".tmp"
    deleted = False

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)

        condition_id_idx = header.index('conditionId')

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[condition_id_idx].strip() == condition_id:
                print("Deleting condition:", condition_id)
                deleted = True
                continue  # skip writing this row (deleting it)

            writer.writerow(row)

    if deleted:
        os.replace(temp_file_path, DB_PATH)
    else:
        os.remove(temp_file_path)

    return deleted