import csv
from csv import writer
import Constant.dbColumn as dbCol
from Model.treatmentModel import TreatmentModel
import os

DB_PATH = './data/treatmentDb.csv'

def getAllTreatmentByCustomerId(customerId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdTreatment)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = []

        for line in csvFile:
            if line != []:
                if line[customer_id_index] == customerId:
                    treatment = TreatmentModel(
                        pCustomerId=customerId,
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    result.append(treatment)
        
        return result




def createTreatment(treatmentModel):
    with open(DB_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  

        writer_object = writer(file)
        data = [value for key, value in vars(treatmentModel).items()]
        writer_object.writerow(data)



def getAllTreatmentByConditionID(conditionId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = []

        for line in csvFile:
            if line != []:
                if line[customer_id_index] == conditionId:
                    treatment = TreatmentModel(
                        pConditionId=conditionId,
                        pTreatmentId=line[treatment_id_index],
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    result.append(treatment)
        
        return result

def getTreatmentByID(treatmentID):
    #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        condition_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        result = None

        for line in csvFile:
            if line != []:
                if line[treatment_id_index] == treatmentID:
                    treatment = TreatmentModel(
                        pConditionId=line[condition_id_index],
                        pTreatmentId=treatmentID,
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    return treatment
        
        return result
   
def updateTreatmentByID(newTreatmentModel):
    print("UPDATING condition")
    print("condition id, ", newTreatmentModel.conditionID)
    print("treatment id: ", newTreatmentModel.treatmentID)
    treatmentId = newTreatmentModel.treatmentID
    temp_file_path = DB_PATH + ".tmp"
    updated = False
    print("received treatmentId: ", treatmentId)
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Skip completely empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[1].strip() == treatmentId:
                new_row = [value for _, value in vars(newTreatmentModel).items()]
                writer.writerow(new_row)
                updated = True
            else:
                writer.writerow(row)

    if updated:
        print("UPDATED DB")
        os.replace(temp_file_path, DB_PATH)
    else:
        print("DB NOT UPDATED")
        os.remove(temp_file_path)

    return updated
