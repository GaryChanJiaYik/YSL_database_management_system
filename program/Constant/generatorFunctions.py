import uuid

def generateUUID():
    uniqueUUID = uuid.uuid4()
    formattedUUID = str(uniqueUUID).split('-')[-1]
    return formattedUUID