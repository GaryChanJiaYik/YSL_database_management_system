import csv
import Model.conditionModel as CM

DB_PATH = './data/conditionDb.csv'


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
        
        return result

def insertConditionToDb( conditionModel):
    with open(DB_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  

        writer_object = csv.writer(file)
        data = [value for key, value in vars(conditionModel).items()]
        writer_object.writerow(data)