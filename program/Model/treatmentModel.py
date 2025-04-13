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
        self.customerId = pCustomerId
        self.treatmentDescription = pTreatmentDescription
        self.painLevel = pPainLevel
        self.tenseLevel = pTenseLevel
        self.soreLevel = pSoreLevel
        self.numbLevel = pNumbLevel
        self.treatmentDate = pTreatmentDate
