customerId = "Timestamp"
ic = "IC身份证"
name = "Name名"
email = "Email电邮"
gender = "Gender性别"
race = "Race种族"
address ="Address地址"
handPhoneNumber = "HP No.手机号"
instagram = "Instagram"
knowUsMethod = "How did get know our centre?你是怎么来到我们这里？"
oldCustomerId = "Old Customer ID"
consent = '''CONSENT FOR TREATMENT 
I understand that I can ask any questions pertaining to the therapy before filling this form. I could, if the need arises, withdraw my consent to stop the therapy at any time throughout the procedure. The procedure, its risks and benefits have been explained to me, and I understand the explanation given.
I hereby agree for the therapy to be carried out on me. I also understand that a record of the therapy given shall be kept. This record is confidential and will not be disclosed to an outside party, unless it has been authorised by me, or my representative, or as ordered by the court of law to do so.
治疗同意书
我明白在填写本表格之前，我可以提出任何疑问相关治疗的问题。如果有需要，我可以在治疗过程中随时撤回我的同意并终止治疗。治疗的程序、风险和益处已向我解释，我已理解所提供的说明。
因此，我同意接受治疗。我也明白，治疗记录将被保存，该记录是保密的，除非得到我的授权、我的代表的授权，或根据法院的命令，否则不会透露给外部人士。'''


customerModelAttributeToField = {
  'customerId': "Customer ID",
  'ic': "IC",
  'customerName': "Name",
  'email': "Email",
  'gender': "Gender",
  'race': "Race",
  'address': "Address",
  'handphone': "Contact",
  'instagram': "Instagram",
  'howDidYouFindUs': "How did get know our centre?",
  "oldCustomerId": "Old Customer ID",
  "consent": "Consent"
}


TreatmentModelAttributeToField = {
    'treatmentDescription': "Treatment Description",
    'treatmentPainLevel': "Pain Level",
    'treatmentTenseLevel': "Tense Level",
    'treatmentSoreLevel': "Sore Level",
    'treatmentNumbLevel': "Numb Level",
    'treatmentDate': "Treatment Date",
    'treatmentPainLevelAfter': "Pain Level",
    'treatmentTenseLevelAfter': "Tense Level",
    'treatmentSoreLevelAfter': "Sore Level",
    'treatmentNumbLevelAfter': "Numb Level",
    'appointmentDate': "Appointment Date",
    'treatmentCost': "Treatment Cost",
}

ConditionModelAttributeToField = {
  'conditionDescription': "Condition Description"
}


# FOR TREATMENT DB
customerIdTreatment = "CustomerId"
treatmentDescription = "treatmentDescription"
treatmentPainLevel = "treatmentPainLevel"
treatmentTenseLevel = "treatmentTenseLevel"
treatmentSoreLevel = "treatmentSoreLevel"
treatmentNumbLevel = "treatmentNumbLevel"
treatmentDate = "treatmentDate"
treatmentId = "treatmentId"
amendmentDate = "amendmentDate"
treatmentCost = "treatmentCost"
# FOR TREATMENT2 DB
treatmentPainLevelAfter = "treatmentPainLevelAfter"
treatmentTenseLevelAfter = "treatmentTenseLevelAfter"
treatmentSoreLevelAfter = "treatmentSoreLevelAfter"
treatmentNumbLevelAfter = "treatmentNumbLevelAfter"
appointmentDate = "appointmentDate"

# For condition db
customerIdConditionDb = "customerId"
conditionId = "conditionId"
conditionDescription = "conditionDescription"
undergoingTreatment = "undergoingTreatment"
conditionDate = "conditionDate"

