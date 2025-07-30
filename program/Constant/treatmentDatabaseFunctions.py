import csv
from csv import writer
import Constant.dbColumn as dbCol
from Model.treatmentModel import TreatmentModel
from Constant.converterFunctions import getFormattedDateTime
from Constant.generatorFunctions import generateUUID
import os
from datetime import datetime
from utils import resource_path

DB_PATH = resource_path('./data/treatmentDb.csv')
TREATMENT_REVISION_PATH = resource_path('./data/treatmentRevisionHistory.csv')

def getAllTreatmentByCustomerId(customerId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.customerIdTreatment)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_cost = header.index(dbCol.treatmentCost)
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
                        pTreatmentCost=line[treatment_cost],
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
   with open(DB_PATH, mode='r', encoding='utf-8', newline='') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        customer_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_cost = header.index(dbCol.treatmentCost)
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
                        pTreatmentCost=line[treatment_cost],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl]
                    )
                    result.append(treatment)
        
        # Sort by treatmentDate
        result.sort(key=lambda x: datetime.strptime(x.treatmentDate, "%Y-%m-%d %H:%M:%S"), reverse=True)
        return result

def getTreatmentByID(treatmentID):
    #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)           
        condition_id_index = header.index(dbCol.conditionId)
        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_cost = header.index(dbCol.treatmentCost)
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
                        pTreatmentCost=line[treatment_cost],
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
    print("condition id: ", newTreatmentModel.conditionID)
    print("treatment id: ", newTreatmentModel.treatmentID)

    treatmentId = newTreatmentModel.treatmentID
    temp_file_path = DB_PATH + ".tmp"
    updated = False

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        header = next(reader)
        writer = csv.writer(outfile)
        writer.writerow(header)

        # Get column indexes using header names
        condition_id_idx = header.index('conditionId')
        treatment_id_idx = header.index('treatmentId')
        amendment_idx = header.index('amendmentDate')

        for row in reader:
            # Skip completely empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[treatment_id_idx].strip() == treatmentId:
                # Update condition ID to new UUID
                row[condition_id_idx] = generateUUID()

                # If amendmentDate is '0', replace it with a timestamp
                if row[amendment_idx].strip() == '0':
                    row[amendment_idx] = getFormattedDateTime(dateOnly=True)

                # Save old version to revisions table
                addToTreatmentRevisionTable(row)

                # Write updated treatment from model
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

def addToTreatmentRevisionTable(data):
    with open(TREATMENT_REVISION_PATH, mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  
        writer_object = writer(file)
        writer_object.writerow(data)

def getAllTreatmentRevisionByID(treatmentID):
    with open(TREATMENT_REVISION_PATH, mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)    

        treatment_id_index = header.index(dbCol.treatmentId)
        treatment_description = header.index(dbCol.treatmentDescription)
        treatment_cost = header.index(dbCol.treatmentCost)
        treatment_date = header.index(dbCol.treatmentDate)    
        pain_lvl = header.index(dbCol.treatmentPainLevel)
        tense_lvl = header.index(dbCol.treatmentTenseLevel)
        sore_lvl = header.index(dbCol.treatmentSoreLevel)
        numb_lvl = header.index(dbCol.treatmentNumbLevel)
        ammendDate = header.index(dbCol.amendmentDate)
        result = []

        for line in csvFile:
            if line != []:
                if line[treatment_id_index] == treatmentID:
                    treatment = TreatmentModel(
                        pConditionId=line[0],
                        pTreatmentId=line[treatment_id_index],
                        pTreatmentDescription= line[treatment_description],
                        pTreatmentCost=line[treatment_cost],
                        pTreatmentDate=line[treatment_date],
                        pNumbLevel=line[numb_lvl],
                        pPainLevel=line[pain_lvl],
                        pSoreLevel=line[sore_lvl],
                        pTenseLevel=line[tense_lvl],
                        pAmendmentDate= line[ammendDate]
                    )
                    result.append(treatment)
        
        return result

def deleteTreatmentByID(treatmentID):
    print("DELETING treatment")
    print("treatment id: ", treatmentID)

    temp_file_path = DB_PATH + ".tmp"
    deleted = False

    # Step 1: Delete from main treatment CSV
    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(temp_file_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        header = next(reader)
        writer = csv.writer(outfile)
        writer.writerow(header)

        treatment_id_idx = header.index('treatmentId')

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[treatment_id_idx].strip() == treatmentID:
                deleted = True  # Skip writing this row
            else:
                writer.writerow(row)

    if deleted:
        os.replace(temp_file_path, DB_PATH)
        print("TREATMENT DELETED FROM MAIN FILE")
        # Now also delete from revisions
        __deleteTreatmentRevisionsByID(treatmentID)
    else:
        os.remove(temp_file_path)
        print("TREATMENT NOT FOUND")

    return deleted


def __deleteTreatmentRevisionsByID(treatmentID):
    print("DELETING RELATED TREATMENT REVISIONS")
    
    revision_temp_path = TREATMENT_REVISION_PATH + ".tmp"
    deleted_any = False

    with open(TREATMENT_REVISION_PATH, mode='r', encoding='utf-8', newline='') as infile, \
         open(revision_temp_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        header = next(reader)
        writer = csv.writer(outfile)
        writer.writerow(header)

        treatment_id_idx = header.index('treatmentId')

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[treatment_id_idx].strip() == treatmentID:
                deleted_any = True  # Skip this revision
            else:
                writer.writerow(row)

    if deleted_any:
        os.replace(revision_temp_path, TREATMENT_REVISION_PATH)
        print("RELATED REVISIONS DELETED")
    else:
        os.remove(revision_temp_path)
        print("NO RELATED REVISIONS FOUND")
        
        
def getConditionTotalCost(conditionId):
    total_cost = 0.0

    with open(DB_PATH, mode='r', encoding='utf-8', newline='') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)
        
        # Get the index of relevant columns
        condition_id_index = header.index(dbCol.conditionId)
        treatment_cost_index = header.index(dbCol.treatmentCost)

        # Loop through the CSV lines
        for line in csvFile:
            if line and line[condition_id_index] == conditionId:
                try:
                    total_cost += float(line[treatment_cost_index])
                except ValueError:
                    print(f"Invalid cost value: {line[treatment_cost_index]}")
    
    return total_cost