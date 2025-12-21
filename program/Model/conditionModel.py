class ConditionModel:
    def __init__(self, customerId, condition_id, conditionDescription, undergoingTreatment, conditionDate, 
                 highBloodPressure=False, bloodSugar=False, cholesterol=False, uricAcid=False,
                 bloating=False, heartDisease=False, stroke=False, cancer=False):
        self.customerId = customerId
        self.conditionId = condition_id
        self.conditionDescription = conditionDescription    
        self.undergoingTreatment = undergoingTreatment
        self.conditionDate = conditionDate
        self.highBloodPressure = highBloodPressure
        self.bloodSugar = bloodSugar
        self.cholesterol = cholesterol
        self.uricAcid = uricAcid
        self.bloating = bloating
        self.heartDisease = heartDisease
        self.stroke = stroke
        self.cancer = cancer