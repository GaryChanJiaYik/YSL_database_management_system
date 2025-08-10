import csv
import os
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
from Model.customerObjectModel import CustomerModel
from Constant.converterFunctions import convertTimeStampToId
from utils import resourcePath
from datetime import datetime
from collections import defaultdict


DB_PATH = resourcePath('./data/db.csv')
TREATMENT_DB_PATH = resourcePath('./data/treatmentDb.csv')
CONDITION_DB_PATH = resourcePath('./data/conditionDb.csv')


def searchForSingleUser( userId):
    print("from searching constant function")
    print(userId)
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        
        if dbCol.customerId in header:
            customer_id = header.index(dbCol.customerId)
            ic_index = header.index(dbCol.ic)
            name_index = header.index(dbCol.name)
            email_index = header.index(dbCol.email)
            handphone_index = header.index(dbCol.handPhoneNumber)
            gender_index = header.index(dbCol.gender)
            address_index = header.index(dbCol.address)
            insta_index = header.index(dbCol.instagram)
            knowUsMethod_index = header.index(dbCol.knowUsMethod)
            race_index = header.index(dbCol.race)  
            old_cus_id_index = header.index(dbCol.oldCustomerId)
            consent = header.index(dbCol.consent)
          
            for lines in csvFile:
                if convertTimeStampToId(lines[customer_id]) == userId:
                    print(lines[old_cus_id_index])

                    customer = CustomerModel(
                        pCustomerId=lines[customer_id],
                        pOldCustomerId= lines[old_cus_id_index],
                        pIc=lines[ic_index],
                        pCustomerName=lines[name_index],
                        pEmail= lines[email_index],
                        pHandphoneNum= lines[handphone_index],
                        pGender=lines[gender_index],
                        pAddress=lines[address_index],
                        pInstagram=lines[insta_index],
                        pHowDidYouFindUs= lines[knowUsMethod_index],
                        pRace=lines[race_index],
                        pConsent=lines[consent]
                    )
                    return customer          
        else:
            return errorCode.NO_USER_FOUND

def searchForUserBasedOn_ID_IC_Name_Contact_oldCustomerId(userId):
    # Step 1: Build treatment mapping (customerId -> latest treatment date)
    condition_to_customer = {}
    with open(CONDITION_DB_PATH, mode='r', encoding='utf-8') as condition_file:
        reader = csv.DictReader(condition_file)
        for row in reader:
            condition_id = row.get("conditionId")
            customer_id = row.get("customerId")
            if condition_id and customer_id:
                condition_to_customer[condition_id] = customer_id

    customer_latest_treatment = defaultdict(lambda: datetime.min)
    with open(TREATMENT_DB_PATH, mode='r', encoding='utf-8') as treatment_file:
        reader = csv.DictReader(treatment_file)
        for row in reader:
            condition_id = row.get("conditionId")
            treatment_date_str = row.get("treatmentDate")
            customer_id = condition_to_customer.get(condition_id)
            if customer_id and treatment_date_str:
                try:
                    treatment_date = datetime.strptime(treatment_date_str, "%Y-%m-%d %H:%M:%S")
                    if treatment_date > customer_latest_treatment[customer_id]:
                        customer_latest_treatment[customer_id] = treatment_date
                except ValueError:
                    continue

    # Step 2: Perform text search
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)
        res = []
        if dbCol.ic in header and dbCol.name in header:
            customer_id_idx = header.index(dbCol.customerId)
            ic_index = header.index(dbCol.ic)
            name_index = header.index(dbCol.name)
            contact_index = header.index(dbCol.handPhoneNumber)
            oldCustomerId_index = header.index(dbCol.oldCustomerId)

            for line in csvFile:
                if (
                    userId.lower() in line[ic_index].lower() or
                    userId.lower() in line[customer_id_idx].lower() or
                    userId.lower() in line[name_index].lower() or
                    userId.lower() in line[contact_index].lower() or
                    userId.lower() in line[oldCustomerId_index].lower()
                ):
                    customer_id_raw = line[customer_id_idx]
                    normalized_id = _normalize_customer_id(customer_id_raw)
                    treatment_date = customer_latest_treatment.get(normalized_id, datetime.min)
                    res.append((
                        treatment_date,
                        [line[customer_id_idx], line[ic_index], line[name_index], line[contact_index], line[oldCustomerId_index]]
                    ))

            # Step 3: Sort by latest treatment date
            res.sort(key=lambda x: x[0], reverse=True)

            # Return just the row data (not the datetime)
            return [row for _, row in res] if res else errorCode.NO_USER_FOUND
        else:
            return errorCode.NO_USER_FOUND
        
                    
def addOldCustomerID(customerID, oldCustomerId):
    print(f'{customerID} --> {oldCustomerId}')
    updated = False

    # Read all rows
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    if not rows:
        print("Empty CSV")
        return

    header = rows[0]
    if dbCol.customerId in header and dbCol.oldCustomerId in header:
        customer_id_index = header.index(dbCol.customerId)
        old_customer_id_index = header.index(dbCol.oldCustomerId)

        for i in range(1, len(rows)):  # Skip header
            if rows[i][customer_id_index] == customerID:
                rows[i][old_customer_id_index] = oldCustomerId
                updated = True
                break

        if updated:
            # Write the updated rows back to the file
            with open(DB_PATH, mode='w', encoding='utf-8', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)
            print("Added old customer ID successfully.")
        else:
            print("Customer ID not found.")
            return errorCode.NO_USER_FOUND
    else:
        print("Required columns not found.")
        return errorCode.NO_USER_FOUND

def addCustomer(getFormDataFunc):
    header, row, customerId = getFormDataFunc()

    file_exists = os.path.exists(DB_PATH)
    try:
        with open(DB_PATH, mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)
        print(f"Customer added: {customerId}")
    except Exception as e:
        print(f"Error saving new customer: {e}")

def saveCustomerChanges(getFormDataFunc, customer_id_value):
    header, updated_row, customerId = getFormDataFunc(customer_id_value)
    temp_file_path = DB_PATH + ".tmp"
    updated = False

    try:
        with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
             open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            file_header = next(reader)
            writer.writerow(file_header)

            try:
                customer_id_idx = file_header.index(dbCol.customerId)
            except ValueError:
                raise Exception("Customer ID column not found in CSV header")

            for row in reader:
                if not row or all(cell.strip() == '' for cell in row):
                    continue
                if row[customer_id_idx] == customerId:
                    writer.writerow(updated_row)
                    updated = True
                else:
                    writer.writerow(row)

        if updated:
            os.replace(temp_file_path, DB_PATH)
            print(f"Customer updated: {customerId}")
        else:
            os.remove(temp_file_path)
            print("Customer ID not found, no update done.")

    except FileNotFoundError:
        with open(DB_PATH, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(updated_row)
        print(f"CSV file not found. Created new and saved customer: {customerId}")
    except Exception as e:
        print(f"Error updating customer: {e}")

def deleteCustomerById(customerId):
    temp_file_path = DB_PATH + ".tmp"
    deleted = False

    try:
        with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
             open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader)
            writer.writerow(header)

            try:
                customer_id_idx = header.index(dbCol.customerId)
            except ValueError:
                print("Customer ID column not found in header.")
                return

            for row in reader:
                if not row or all(cell.strip() == '' for cell in row):
                    continue
                if row[customer_id_idx].strip() == customerId:
                    print(f"Deleting customer: {customerId}")
                    deleted = True
                    continue
                writer.writerow(row)

        if deleted:
            os.replace(temp_file_path, DB_PATH)
            print("Customer deleted successfully.")
        else:
            os.remove(temp_file_path)
            print("Customer not found; nothing deleted.")

    except Exception as e:
        print(f"Error deleting customer: {e}")
        
        
def getCustomerListByLatestTreatmentDate(limit=20):
    # Step 1: Read conditionId -> customerId mapping
    condition_to_customer = {}
    with open(CONDITION_DB_PATH, mode='r', encoding='utf-8') as condition_file:
        reader = csv.DictReader(condition_file)
        for row in reader:
            condition_id = row.get("conditionId")
            customer_id = row.get("customerId")
            if condition_id and customer_id:
                condition_to_customer[condition_id] = customer_id

    # Step 2: Read treatment data and map customerId -> latest treatment date
    customer_latest_treatment = defaultdict(lambda: datetime.min)
    with open(TREATMENT_DB_PATH, mode='r', encoding='utf-8') as treatment_file:
        reader = csv.DictReader(treatment_file)
        for row in reader:
            condition_id = row.get("conditionId")
            treatment_date_str = row.get("treatmentDate")
            if not condition_id or not treatment_date_str:
                continue

            customer_id = condition_to_customer.get(condition_id)
            if not customer_id:
                continue

            try:
                treatment_date = datetime.strptime(treatment_date_str, "%Y-%m-%d %H:%M:%S")
                if treatment_date > customer_latest_treatment[customer_id]:
                    customer_latest_treatment[customer_id] = treatment_date
            except ValueError:
                continue

    # Step 3: Sort customers by latest treatment date
    sorted_customers = sorted(customer_latest_treatment.items(), key=lambda x: x[1], reverse=True)[:limit]
    sorted_customer_ids = [customer_id for customer_id, _ in sorted_customers]

    # Step 4: Fetch customer details
    results = []
    with open(DB_PATH, mode='r', encoding='utf-8') as db_file:
        reader = csv.DictReader(db_file)
        customer_dict = {
            _normalize_customer_id(row.get(dbCol.customerId)): row
            for row in reader
        }

    for customer_id in sorted_customer_ids:
        row = customer_dict.get(customer_id)
        if row:
            results.append([
                row.get(dbCol.customerId, ""),
                row.get(dbCol.ic, ""),
                row.get(dbCol.name, ""),
                row.get(dbCol.handPhoneNumber, ""),
                row.get(dbCol.oldCustomerId, ""),
            ])

    return results


def _normalize_customer_id(raw_id: str) -> str:
        """Normalize timestamp-style customer ID into compact numeric string."""
        return raw_id.replace('/', '').replace(':', '').replace(' ', '')


        