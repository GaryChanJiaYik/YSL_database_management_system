import csv
import os
import Model.conditionModel as CM
from datetime import datetime
from Constant.appConstant import DB_PATH
import Constant.dbColumn as dbCol



def getAllConditionsByCustomerId(customerId):
    predefined_lookup = loadPredefinedConditionLookup()

    with open(DB_PATH["CONDITION"], mode="r", encoding="utf-8") as file:
        csvFile = csv.reader(file)
        header = next(csvFile)

        customer_id_index = header.index(dbCol.customerIdConditionDb)
        condition_id_index = header.index(dbCol.conditionId)
        condition_description = header.index(dbCol.conditionDescription)
        undergoing_treatment = header.index(dbCol.undergoingTreatment)
        condition_date = header.index(dbCol.conditionDate)

        result = []

        for line in csvFile:
            if not line:
                continue

            if line[customer_id_index] == customerId:
                condition_id = line[condition_id_index]

                condition = CM.ConditionModel(
                    customerId=customerId,
                    condition_id=condition_id,
                    conditionDescription=line[condition_description],
                    undergoingTreatment=line[undergoing_treatment] == "True",
                    conditionDate=line[condition_date]
                )

                # 🔗 Attach predefined conditions
                flags = predefined_lookup.get((customerId, condition_id), {})

                for key, value in flags.items():
                    setattr(condition, key, value)

                result.append(condition)

    return sorted(
        result,
        key=lambda x: parse_date_safe(x.conditionDate),
        reverse=True
    )



def loadPredefinedConditionLookup():
    lookup = {}

    with open(DB_PATH["CONDITION2"], mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)

        idx_customer = header.index(dbCol.customerIdConditionDb)
        idx_condition = header.index(dbCol.conditionId)

        for row in reader:
            if not row:
                continue

            key = (row[idx_customer], row[idx_condition])

            lookup[key] = {
                dbCol.highBloodPressure: row[header.index(dbCol.highBloodPressure)] == "True",
                dbCol.bloodSugar: row[header.index(dbCol.bloodSugar)] == "True",
                dbCol.cholesterol: row[header.index(dbCol.cholesterol)] == "True",
                dbCol.uricAcid: row[header.index(dbCol.uricAcid)] == "True",
                dbCol.bloating: row[header.index(dbCol.bloating)] == "True",
                dbCol.heartDisease: row[header.index(dbCol.heartDisease)] == "True",
                dbCol.stroke: row[header.index(dbCol.stroke)] == "True",
                dbCol.cancer: row[header.index(dbCol.cancer)] == "True",
            }

    return lookup


def parse_date_safe(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return datetime.min  # or datetime.max if sorting descending


def insertConditionToDb(conditionModel):
    with open(DB_PATH["CONDITION"], mode='a', encoding='utf-8', newline='\n') as file:
        
        writer_object = csv.writer(file)
        row = [
            conditionModel.customerId,
            conditionModel.conditionId,
            conditionModel.conditionDescription,
            conditionModel.undergoingTreatment,
            conditionModel.conditionDate,
        ]
        writer_object.writerow(row)


def insertConditionToDb2(conditionModel):
    with open(DB_PATH["CONDITION2"], mode="a", encoding="utf-8", newline="\n") as file:
        writer = csv.writer(file)

        row = [
            conditionModel.customerId,
            conditionModel.conditionId,
            conditionModel.highBloodPressure,
            conditionModel.bloodSugar,
            conditionModel.cholesterol,
            conditionModel.uricAcid,
            conditionModel.bloating,
            conditionModel.heartDisease,
            conditionModel.stroke,
            conditionModel.cancer,
        ]

        writer.writerow(row)


def updateTreatmentStatus(customer_id, condition_id, is_treated):
    print(f"Updating treatment status for customer {customer_id}, condition {condition_id}")
    temp_file_path = DB_PATH["CONDITION"].with_suffix('.tmp')
    updated = False

    with open(DB_PATH["CONDITION"], mode='r', encoding='utf-8', newline='') as infile, \
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
        os.replace(temp_file_path, DB_PATH["CONDITION"])
        print("Treatment status updated successfully.")
    else:
        os.remove(temp_file_path)
        print("No matching treatment found. Status not updated.")

    return updated
        

def getTreatmentStatus(customer_id, condition_id):
    with open(DB_PATH["CONDITION"], mode='r', encoding='utf-8', newline='') as file:
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
    temp_file_path = DB_PATH["CONDITION"].with_suffix('.tmp')
    updated = False

    with open(DB_PATH["CONDITION"], mode='r', encoding='utf-8', newline='') as infile, \
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
        os.replace(temp_file_path, DB_PATH["CONDITION"])
    else:
        os.remove(temp_file_path)

    return updated


def updateCondition2ByID(condition_id, updated_conditions):
    temp_file_path = DB_PATH["CONDITION2"].with_suffix('.tmp')
    updated = False

    with open(DB_PATH["CONDITION2"], mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        condition_id_idx = header.index("conditionId")

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[condition_id_idx].strip() == condition_id:
                print("Updating predefined conditions:", condition_id)

                for attr_name, value in updated_conditions.items():
                    if attr_name in header:
                        col_idx = header.index(attr_name)
                        row[col_idx] = str(value)

                updated = True

            writer.writerow(row)

    if updated:
        os.replace(temp_file_path, DB_PATH["CONDITION2"])
    else:
        os.remove(temp_file_path)

    return updated



def deleteCondition(condition_id):
    temp_file_path = DB_PATH["CONDITION"].with_suffix('.tmp')
    deleted = False

    with open(DB_PATH["CONDITION"], mode='r', encoding='utf-8', newline='') as infile, \
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
        os.replace(temp_file_path, DB_PATH["CONDITION"])
    else:
        os.remove(temp_file_path)

    return deleted

def deleteCondition2(condition_id):
    temp_file_path = DB_PATH["CONDITION2"].with_suffix('.tmp')
    deleted = False

    with open(DB_PATH["CONDITION2"], mode='r', encoding='utf-8', newline='') as infile, \
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
        os.replace(temp_file_path, DB_PATH["CONDITION2"])
    else:
        os.remove(temp_file_path)

    return deleted