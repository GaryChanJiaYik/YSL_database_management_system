import datetime
import Components.popupModal as popupModal
def convertTimeStampToId(timestamp):
    exclude = [" ", "/", ":"]
    result = ""
    for char in timestamp:
        if char not in exclude:
            result += char
    return result
    
def formatDateTime(root, hour, minute, am_pm):
    now = datetime.datetime.now()

    try:
        hour = int(hour)
        minute = int(minute)
        am_pm = am_pm

        if hour < 1 or hour > 12 or minute < 0 or minute > 59:
            raise ValueError("Invalid time")

        # Convert to 24-hour format
        if am_pm == "PM" and hour != 12:
            hour += 12
        elif am_pm == "AM" and hour == 12:
            hour = 0

        # Combine with today's date
        date = now.date()
        combined_datetime = datetime.datetime.combine(date, datetime.time(hour, minute))
        return combined_datetime
    except Exception as e:
        print(f"Error in formatDateTime: {e}")
        popupModal.renderPopUpModal(root, "Invalid time format", "Error", "Error")
        return
    
def getFormattedDateTime(dateOnly =False):

    if dateOnly:
        return datetime.datetime.now().strftime("%Y-%m-%d") 
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M") 


def getDatefromTimeStamp(timestamp):
    return timestamp[:10] 
