from Constant.generatorFunctions import generateUUID
class TreatmentModel:
    def __init__(self, 
                pCustomerId="", 
                pTreatmentDescription="", 
                pTreatmentDate="",
                pPainLevel = 0,
                pTenseLevel = 0,
                pSoreLevel = 0,
                pNumbLevel = 0 
                 ):
          # Placeholder for treatment ID, if needed
        self.customerId = pCustomerId
        self.treatmentID = generateUUID()
        self.treatmentDescription = pTreatmentDescription
        self.painLevel = pPainLevel
        self.tenseLevel = pTenseLevel
        self.soreLevel = pSoreLevel
        self.numbLevel = pNumbLevel
        self.treatmentDate = pTreatmentDate
        self.version = 0
        self.amendmentDate = None
