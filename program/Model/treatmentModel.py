from Constant.generatorFunctions import generateUUID

class TreatmentModel:
  def __init__(self, 
                pTreatmentId="",
              pConditionId="", 
              pTreatmentDescription="", 
              pTreatmentCost="",
              pTreatmentDate="",
              pPainLevel = 0,
              pTenseLevel = 0,
              pSoreLevel = 0,
              pNumbLevel = 0,
              pAmendmentDate = None
                ):
        # Placeholder for treatment ID, if needed
      self.conditionID = pConditionId
      self.treatmentID = pTreatmentId if pTreatmentId else generateUUID()
      self.treatmentDescription = pTreatmentDescription
      self.painLevel = pPainLevel
      self.tenseLevel = pTenseLevel
      self.soreLevel = pSoreLevel
      self.numbLevel = pNumbLevel
      self.treatmentDate = pTreatmentDate
      self.treatmentCost = pTreatmentCost
      self.version = 0
      self.amendmentDate = pAmendmentDate
