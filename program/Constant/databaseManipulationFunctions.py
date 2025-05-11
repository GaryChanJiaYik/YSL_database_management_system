import csv
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
from Model.customerObjectModel import CustomerModel
from Constant.converterFunctions import convertTimeStampToId

DB_PATH = './data/db.csv'

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
                        pRace=lines[race_index]
                    )
                    return customer          
        else:
            return errorCode.NO_USER_FOUND

def searchForUserBasedOn_ID_IC_Name_Email(userId):
    with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        res = []
        if dbCol.ic in header and dbCol.name in header:
            customer_id, ic_index, name_index, email_index = header.index(dbCol.customerId), header.index(dbCol.ic), header.index(dbCol.name), header.index(dbCol.email)
            for lines in csvFile:
                if (
                    userId.lower() in lines[ic_index].lower() or
                    userId.lower() in lines[customer_id].lower() or
                    userId.lower() in lines[name_index].lower() or
                    userId.lower() in lines[email_index].lower()
                ):
                    res.append([lines[customer_id], lines[ic_index], lines[name_index], lines[email_index]])
            return res
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
            with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)
            print("Added old customer ID successfully.")
        else:
            print("Customer ID not found.")
            return errorCode.NO_USER_FOUND
    else:
        print("Required columns not found.")
        return errorCode.NO_USER_FOUND
        