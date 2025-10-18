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
              pAmendmentDate = None,
              pPainLevelAfter = 0,
              pTenseLevelAfter = 0,
              pSoreLevelAfter = 0,
              pNumbLevelAfter = 0,
              pAppointmentDate = "",
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
      # Allow float or JSON string for payment
      if isinstance(pTreatmentCost, (int, float)):
          self.treatmentCost = float(pTreatmentCost)
      elif isinstance(pTreatmentCost, str):
          pTreatmentCost = pTreatmentCost.strip()
          if pTreatmentCost.startswith("{") and pTreatmentCost.endswith("}"):
              # Likely a JSON string
              self.treatmentCost = pTreatmentCost
          else:
              # Try to parse as float
              try:
                  self.treatmentCost = float(pTreatmentCost)
              except ValueError:
                  self.treatmentCost = 0.0
      else:
          self.treatmentCost = 0.0
      self.version = 0
      self.amendmentDate = pAmendmentDate
      self.painLevelAfter = pPainLevelAfter
      self.tenseLevelAfter = pTenseLevelAfter
      self.soreLevelAfter = pSoreLevelAfter
      self.numbLevelAfter = pNumbLevelAfter
      self.appointmentDate = pAppointmentDate
