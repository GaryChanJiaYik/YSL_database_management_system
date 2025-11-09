class CustomerModel():
    def __init__(self, 
                pCustomerId="-",
                pOldCustomerId="", 
                pEmail="-", 
                pIc="-",
                pCustomerName="-",
                pGender="-",
                pRace="-",
                pAddress="-",
                pHandphoneNum="-",
                pInstagram="-",
                pHowDidYouFindUs= "-",
                pConsent="-"
                ):
        self.customerId = pCustomerId
        self.oldCustomerId = pOldCustomerId
        self.email = pEmail
        self.ic = pIc
        self.customerName = pCustomerName
        self.gender = pGender
        self.race = pRace
        self.address = pAddress
        self.handphone = pHandphoneNum
        self.instagram = pInstagram
        self.howDidYouFindUs = pHowDidYouFindUs
        self.consent = pConsent