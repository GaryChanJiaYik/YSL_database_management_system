import csv
import json
from csv import writer
import Constant.dbColumn as dbCol
from Model.treatmentModel import TreatmentModel
from Constant.converterFunctions import getFormattedDateTime
from Constant.generatorFunctions import generateUUID
import os
from datetime import datetime
from Constant.appConstant import DB_PATH


def getAllTreatmentByCustomerId(customerId):
   
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8') as file:
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
    with open(DB_PATH["TREATMENT"], mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  

        writer_object = writer(file)
        data = [value for key, value in vars(treatmentModel).items()]
        writer_object.writerow(data)



def getAllTreatmentByConditionID(conditionId):
   #!!!!!!!!!!!! customerId --> converted format
   with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as file:
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

def getAllTreatmentByConditionID(conditionId):
    # Read TREATMENT2 and store in a dictionary for quick lookup
    treatment2_data = {}
    with open(DB_PATH["TREATMENT2"], mode='r', encoding='utf-8', newline='') as file2:
        csvFile2 = csv.reader(file2)
        header2 = next(csvFile2)

        condition_id_index2 = header2.index(dbCol.conditionId)
        treatment_id_index2 = header2.index(dbCol.treatmentId)
        pain_after_index = header2.index(dbCol.treatmentPainLevelAfter)
        tense_after_index = header2.index(dbCol.treatmentTenseLevelAfter)
        sore_after_index = header2.index(dbCol.treatmentSoreLevelAfter)
        numb_after_index = header2.index(dbCol.treatmentNumbLevelAfter)
        appointment_date_index = header2.index(dbCol.appointmentDate)

        for line in csvFile2:
            if line != []:
                key = (line[condition_id_index2], line[treatment_id_index2])
                treatment2_data[key] = {
                    "painAfter": line[pain_after_index],
                    "tenseAfter": line[tense_after_index],
                    "soreAfter": line[sore_after_index],
                    "numbAfter": line[numb_after_index],
                    "appointmentDate": line[appointment_date_index],
                }
    
    # Read TREATMENT and match with TREATMENT2
    result = []
    with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as file1:
        csvFile1 = csv.reader(file1)
        header1 = next(csvFile1)

        condition_id_index = header1.index(dbCol.conditionId)
        treatment_id_index = header1.index(dbCol.treatmentId)
        treatment_description = header1.index(dbCol.treatmentDescription)
        treatment_cost = header1.index(dbCol.treatmentCost)
        treatment_date = header1.index(dbCol.treatmentDate)    
        pain_lvl = header1.index(dbCol.treatmentPainLevel)
        tense_lvl = header1.index(dbCol.treatmentTenseLevel)
        sore_lvl = header1.index(dbCol.treatmentSoreLevel)
        numb_lvl = header1.index(dbCol.treatmentNumbLevel)

        for line in csvFile1:
            if line != [] and line[condition_id_index] == conditionId:
                tid = line[treatment_id_index]
                key = (conditionId, tid)
                after_data = treatment2_data.get(key, {})

                treatment = TreatmentModel(
                    pConditionId=conditionId,
                    pTreatmentId=tid,
                    pTreatmentDescription=line[treatment_description],
                    pTreatmentCost=line[treatment_cost],
                    pTreatmentDate=line[treatment_date],
                    pNumbLevel=line[numb_lvl],
                    pPainLevel=line[pain_lvl],
                    pSoreLevel=line[sore_lvl],
                    pTenseLevel=line[tense_lvl],

                    # Optional: Add "after" data if exists
                    pNumbLevelAfter=after_data.get("numbAfter"),
                    pPainLevelAfter=after_data.get("painAfter"),
                    pSoreLevelAfter=after_data.get("soreAfter"),
                    pTenseLevelAfter=after_data.get("tenseAfter"),
                    pAppointmentDate=after_data.get("appointmentDate"),
                )

                result.append(treatment)

    # Sort by treatmentDate
    result.sort(key=lambda x: datetime.strptime(x.treatmentDate, "%Y-%m-%d %H:%M:%S"), reverse=True)
    return result            
        

def getTreatmentByID(treatmentID):
    # Read TREATMENT2 into a dictionary keyed by (conditionId, treatmentId)
    treatment2_data = {}
    with open(DB_PATH["TREATMENT2"], mode='r', encoding='utf-8', newline='') as file2:
        csvFile2 = csv.reader(file2)
        header2 = next(csvFile2)

        condition_id_index2 = header2.index(dbCol.conditionId)
        treatment_id_index2 = header2.index(dbCol.treatmentId)
        pain_after_index = header2.index(dbCol.treatmentPainLevelAfter)
        tense_after_index = header2.index(dbCol.treatmentTenseLevelAfter)
        sore_after_index = header2.index(dbCol.treatmentSoreLevelAfter)
        numb_after_index = header2.index(dbCol.treatmentNumbLevelAfter)
        appointment_date_index = header2.index(dbCol.appointmentDate)

        for line in csvFile2:
            if line:
                key = (line[condition_id_index2], line[treatment_id_index2])
                treatment2_data[key] = {
                    "painAfter": line[pain_after_index],
                    "tenseAfter": line[tense_after_index],
                    "soreAfter": line[sore_after_index],
                    "numbAfter": line[numb_after_index],
                    "appointmentDate": line[appointment_date_index],
                }

    # Now read TREATMENT and find the matching treatmentID
    with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as file1:
        csvFile1 = csv.reader(file1)
        header1 = next(csvFile1)

        condition_id_index = header1.index(dbCol.conditionId)
        treatment_id_index = header1.index(dbCol.treatmentId)
        treatment_description_index = header1.index(dbCol.treatmentDescription)
        treatment_cost_index = header1.index(dbCol.treatmentCost)
        treatment_date_index = header1.index(dbCol.treatmentDate)
        pain_lvl_index = header1.index(dbCol.treatmentPainLevel)
        tense_lvl_index = header1.index(dbCol.treatmentTenseLevel)
        sore_lvl_index = header1.index(dbCol.treatmentSoreLevel)
        numb_lvl_index = header1.index(dbCol.treatmentNumbLevel)

        for line in csvFile1:
            if line and line[treatment_id_index] == treatmentID:
                condition_id = line[condition_id_index]
                key = (condition_id, treatmentID)
                after_data = treatment2_data.get(key, {})

                treatment = TreatmentModel(
                    pConditionId=condition_id,
                    pTreatmentId=treatmentID,
                    pTreatmentDescription=line[treatment_description_index],
                    pTreatmentCost=line[treatment_cost_index],
                    pTreatmentDate=line[treatment_date_index],
                    pNumbLevel=line[numb_lvl_index],
                    pPainLevel=line[pain_lvl_index],
                    pSoreLevel=line[sore_lvl_index],
                    pTenseLevel=line[tense_lvl_index],

                    # Add after data if exists
                    pNumbLevelAfter=after_data.get("numbAfter"),
                    pPainLevelAfter=after_data.get("painAfter"),
                    pSoreLevelAfter=after_data.get("soreAfter"),
                    pTenseLevelAfter=after_data.get("tenseAfter"),
                    pAppointmentDate=after_data.get("appointmentDate"),
                )
                return treatment

    # If not found
    return None


def updateTreatmentByID(newTreatmentModel):
    print("UPDATING treatment")
    print("condition id: ", newTreatmentModel.conditionID)
    print("treatment id: ", newTreatmentModel.treatmentID)

    treatmentId = newTreatmentModel.treatmentID
    updated = False

    # ───────────────────────────────────────────────
    # Part 1: Update TREATMENT file
    # ───────────────────────────────────────────────
    treatment_temp_path = DB_PATH["TREATMENT"].with_suffix('.tmp')

    with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as infile, \
         open(treatment_temp_path, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        condition_id_idx = header.index('conditionId')
        treatment_id_idx = header.index('treatmentId')
        amendment_idx = header.index('amendmentDate')

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if row[treatment_id_idx].strip() == treatmentId:
                # Backup old data to TREATMENT_REV
                if row[amendment_idx].strip() == '0':
                    row[amendment_idx] = getFormattedDateTime(dateOnly=True)

                row[condition_id_idx] = generateUUID()
                addToTreatmentRevisionTable(row)

                # Write updated treatment data
                new_row = [value for _, value in vars(newTreatmentModel).items()]
                writer.writerow(new_row)
                updated = True
            else:
                writer.writerow(row)

    if updated:
        os.replace(treatment_temp_path, DB_PATH["TREATMENT"])
        print("→ Updated TREATMENT file")
    else:
        os.remove(treatment_temp_path)
        print("→ No match found in TREATMENT")

    # ───────────────────────────────────────────────
    # Part 2: Update or Insert into TREATMENT2
    # ───────────────────────────────────────────────
    treatment2_temp_path = DB_PATH["TREATMENT2"].with_suffix('.tmp')
    updated2 = False

    with open(DB_PATH["TREATMENT2"], mode='r', encoding='utf-8', newline='') as infile2, \
         open(treatment2_temp_path, mode='w', encoding='utf-8', newline='') as outfile2:

        reader2 = csv.reader(infile2)
        writer2 = csv.writer(outfile2)

        header2 = next(reader2)
        writer2.writerow(header2)

        condition_id_idx2 = header2.index('conditionId')
        treatment_id_idx2 = header2.index('treatmentId')
        version_idx = header2.index('version') if 'version' in header2 else -1
        amend_idx2 = header2.index('amendmentDate') if 'amendmentDate' in header2 else -1

        matched = False

        for row in reader2:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            if (
                row[treatment_id_idx2].strip() == newTreatmentModel.treatmentID and
                row[condition_id_idx2].strip() == newTreatmentModel.conditionID
            ):
                matched = True

                # Backup old row
                if amend_idx2 != -1:
                    row[amend_idx2] = getFormattedDateTime(dateOnly=True)

                if version_idx != -1:
                    try:
                        row[version_idx] = str(int(row[version_idx]) + 1)
                    except:
                        row[version_idx] = "1"
                
                new_row = [
                    newTreatmentModel.conditionID,
                    newTreatmentModel.treatmentID,
                    newTreatmentModel.painLevelAfter,
                    newTreatmentModel.tenseLevelAfter,
                    newTreatmentModel.soreLevelAfter,
                    newTreatmentModel.numbLevelAfter,
                    newTreatmentModel.appointmentDate,
                    row[version_idx],  # Incremented version
                    getFormattedDateTime(dateOnly=True)  # Updated amendmentDate
                ]

                # Optional: backup old row
                # addToTreatment2RevisionTable(row)

                writer2.writerow(new_row)
                updated2 = True
            else:
                writer2.writerow(row)

        if not matched:
            # Add new row from newTreatmentModel (you must extract relevant values)
            new_row = [
                newTreatmentModel.conditionID,
                newTreatmentModel.treatmentID,
                newTreatmentModel.painLevelAfter,
                newTreatmentModel.tenseLevelAfter,
                newTreatmentModel.soreLevelAfter,
                newTreatmentModel.numbLevelAfter,
                newTreatmentModel.appointmentDate,
                "1",  # version
                getFormattedDateTime(dateOnly=True)  # amendmentDate
            ]

            writer2.writerow(new_row)
            # addToTreatment2RevisionTable(new_row)
            print("→ Inserted new row into TREATMENT2")
            updated2 = True

    if updated2:
        os.replace(treatment2_temp_path, DB_PATH["TREATMENT2"])
        print("→ Updated TREATMENT2 file")
    else:
        os.remove(treatment2_temp_path)
        print("→ No match found in TREATMENT2")

    return updated or updated2


def addToTreatmentRevisionTable(data):
    with open(DB_PATH["TREATMENT_REV"], mode='a', encoding='utf-8', newline='\n') as file:
        # Ensure there's a newline before writing if needed
        file.write("\n")  
        writer_object = writer(file)
        writer_object.writerow(data)

def getAllTreatmentRevisionByID(treatmentID):
    with open(DB_PATH["TREATMENT_REV"], mode='r', encoding='utf-8') as file:
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
    print("treatment id:", treatmentID)

    temp_file_path = DB_PATH["TREATMENT"].with_suffix('.tmp')
    deleted = False

    # Step 1: Delete from main treatment CSV
    with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as infile, \
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
                deleted = True  # Skip this row
            else:
                writer.writerow(row)

    if deleted:
        os.replace(temp_file_path, DB_PATH["TREATMENT"])
        print("TREATMENT DELETED FROM MAIN FILE")

        # Step 2: Delete from TREATMENT2
        __deleteTreatment2ByID(treatmentID)

        # Step 3: Delete from revisions
        __deleteTreatmentRevisionsByID(treatmentID)
    else:
        os.remove(temp_file_path)
        print("TREATMENT NOT FOUND")

    return deleted


def __deleteTreatment2ByID(treatmentID):
    temp_file_path = DB_PATH["TREATMENT2"].with_suffix('.tmp')
    deleted = False

    with open(DB_PATH["TREATMENT2"], mode='r', encoding='utf-8', newline='') as infile, \
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
                deleted = True  # Skip this row
            else:
                writer.writerow(row)

    if deleted:
        os.replace(temp_file_path, DB_PATH["TREATMENT2"])
        print("TREATMENT2 entry deleted.")
    else:
        os.remove(temp_file_path)
        print("No matching entry found in TREATMENT2.")


def __deleteTreatmentRevisionsByID(treatmentID):
    print("DELETING RELATED TREATMENT REVISIONS")
    
    revision_temp_path = DB_PATH["TREATMENT_REV"].with_suffix('.tmp')
    deleted_any = False

    with open(DB_PATH["TREATMENT_REV"], mode='r', encoding='utf-8', newline='') as infile, \
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
        os.replace(revision_temp_path, DB_PATH["TREATMENT_REV"])
        print("RELATED REVISIONS DELETED")
    else:
        os.remove(revision_temp_path)
        print("NO RELATED REVISIONS FOUND")
        
        

def getConditionTotalCost(conditionId):
    total_cost = 0.0

    with open(DB_PATH["TREATMENT"], mode='r', encoding='utf-8', newline='') as file:
        csvFile = csv.reader(file)
        header = next(csvFile)
        
        condition_id_index = header.index(dbCol.conditionId)
        treatment_cost_index = header.index(dbCol.treatmentCost)

        for line in csvFile:
            if line and line[condition_id_index] == conditionId:
                cost_str = line[treatment_cost_index]
                try:
                    # Try parsing cost_str as JSON dict with multiple payment methods
                    cost_data = json.loads(cost_str)
                    if isinstance(cost_data, dict):
                        # Sum all payment amounts in this dict
                        total_cost += sum(float(amount) for amount in cost_data.values())
                    else:
                        # If not dict, just try to convert directly to float (fallback)
                        total_cost += float(cost_str)
                except (ValueError, json.JSONDecodeError):
                    print(f"Invalid cost value: {cost_str}")
    
    return total_cost