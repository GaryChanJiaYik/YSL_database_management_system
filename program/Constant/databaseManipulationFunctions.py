import csv
import Constant.errorCode as errorCode
import Constant.dbColumn as dbCol
from Model.customerObjectModel import CustomerModel
from Constant.converterFunctions import convertTimeStampToId

def searchForSingleUser( userId):
    print("from searching constant function")
    print(userId)
    with open('./data/db.csv', mode='r', encoding='utf-8') as file:
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
            print("From search single user")
          
            for lines in csvFile:
                if lines[customer_id] == userId:
                    print(lines[address_index])
                    customer = CustomerModel(
                        pCustomerId=lines[customer_id],
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