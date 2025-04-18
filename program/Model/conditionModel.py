class ConditionModel:
    def __init__(self, customerId, condition_id, conditionDescription, undergoingTreatment, conditionDate):
        self.customerId = customerId
        self.conditionId = condition_id
        self.conditionDescription = conditionDescription    
        self.undergoingTreatment = undergoingTreatment
        self.conditionDate = conditionDate
