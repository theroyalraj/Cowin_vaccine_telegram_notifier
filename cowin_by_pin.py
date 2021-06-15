import requests
from datetime import datetime
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
cowinapiurl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
cowinapiurlByPin = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

tgapiurl = "https://api.telegram.org/bot_botapi_/sendMessage?chat_id=@_groupid_&text="
botapi = "#"  # replace ############## with your tg bot http api.
groupid = "#"  # replace ###### with your group id(check readme if you don't know how to get).
curr_date = datetime.now()
date_formated = curr_date.strftime("%d-%m-%Y")  # the date format which passes correctly to the cowin api.
age = 18  # replace with 45 if you want to make notifier for 45 age group vaccination.


def ask_cowin(district_id):
    query = "?district_id={}&date={}".format(district_id, date_formated)
    cowin_url = cowinapiurl + query
    fetched_data = requests.get(cowin_url, headers=headers)
    struct_data(fetched_data)


def ask_cowin_by_pin(pincode):
    query = "?pincode={}&date={}".format(pincode, date_formated)
    cowin_url = cowinapiurlByPin + query
    # print(cowin_url)
    fetched_data = requests.get(cowin_url, headers=headers)
    # print(fetched_data)
    struct_data(fetched_data)


def struct_data(fetched_data):
    fetched_json = fetched_data.json()
    for center in fetched_json["centers"]:
        message = ""
        for session in center["sessions"]:
            if session["available_capacity"] > 0 and session["min_age_limit"] == age:
                message += "\nPincode: {} | Center Name: {} \nDate: {} | Dose 1: {} | Dose 2: {} \nVaccine: {} | Fees Type : {} \n*******************".format(
                    center["pincode"], center["name"], session["date"], session["available_capacity_dose1"],
                    session["available_capacity_dose2"], session["vaccine"], center["fee_type"])
                if center["fee_type"] == "Paid":
                    for vaccinefee in center["vaccine_fees"]:
                        message += "\nPrice : {} \n*******************".format(vaccinefee["fee"])

        if message.__eq__(""):
            print("no message")
        else:
            send_noti(message)
        print("Pincode: ",center["pincode"]," | Center Name: ",center["name"])
        print("Dose 1: ",session["available_capacity_dose1"]," | Age Limit: ", session["min_age_limit"])
        print()


def send_noti(message):
    tgurl = tgapiurl.replace("_botapi_", botapi)
    tgurl = tgurl.replace("_groupid_", groupid)
    tgurl = tgurl + message
    # print(tgurl)
    tgresponse = requests.get(tgurl)
    print(tgresponse)


if __name__ == "__main__":
    while True:
        ask_cowin_by_pin(826001)
        print("sleeping for 30 sec \n")
        time.sleep(30)
