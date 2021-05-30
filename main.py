# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from datetime import datetime


base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
current = datetime.now()
tele_url = "https://api.telegram.org/bot1768293622:AAGxdJ-oGAvcOywNyNuYs02_wOxTfS9iLe0/sendMessage?chat_id=@grpid&text="
grp_id = "pune_under18_45Slotsfinder"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

today_date = current.strftime("%d-%m-%y")   #get todays date
#print(today_date)

pune_district_id = 363 # from "https://cdn-api.co-vin.in/api/v2/admin/location/districts/21" where 21 is stateid of Maharashtra

def fetch_data_from_url(pune_district_id):
    extension = "?district_id={}&date={}".format(pune_district_id, today_date)
    main_url = base_url + extension
    response = requests.get(main_url, headers=headers)
    #print(response.text)
    #print(type(response))
    get_required_data(response)

def get_required_data(response):
    response_json = response.json()
    print(response_json['centers'])
    #print()
    for center in response_json['centers']:
        for sessions in center["sessions"]:

            if sessions["available_capacity_dose1"] > 0 and sessions["min_age_limit"] == 18 and center['fee_type'] == "Paid":
                #fee = sessions['vaccine_fees'][0]['fee']
                message = "Pincode : {} \nName : {}\nVaccine = {}, Doses Available = {}\nPaid and for age {}+".format(center["pincode"],center["name"],sessions["vaccine"],sessions["available_capacity_dose1"],sessions["min_age_limit"])
                send_msg_telegram(message)
            if sessions["available_capacity_dose1"] > 0 and sessions["min_age_limit"] == 18 and center['fee_type'] == "Free":
                message = "Pincode : {} \nName : {}\nVaccine = {}, Doses Available = {}\nNo Fees and for age {}+".format(center["pincode"],center["name"],sessions["vaccine"],sessions["available_capacity_dose1"],sessions["min_age_limit"])
                print()
                send_msg_telegram(message)
            if sessions["available_capacity_dose1"] > 0 and sessions["min_age_limit"] == 45 and center['fee_type'] == "Free":
                message = "Pincode : {} \nName : {}\nVaccine = {}, Doses Available = {}\nNo Fees and for age 45+".format(
                    center["pincode"], center["name"], sessions["vaccine"], sessions["available_capacity_dose1"])
                print()
                send_msg_telegram(message)
            if sessions["available_capacity_dose1"] > 0 and sessions["min_age_limit"] == 45 and center['fee_type'] == "Paid":
                message = "Pincode : {} \nName : {}\nVaccine = {}, Doses Available = {}\nPaid and for age 45+".format(
                    center["pincode"], center["name"], sessions["vaccine"], sessions["available_capacity_dose1"])
                print()
                send_msg_telegram(message)


def send_msg_telegram(message):
    final_tel_url = tele_url.replace("grpid", grp_id)
    final_tel_url = final_tel_url + message
    response = requests.get(final_tel_url)
    print(response)


if __name__ == '__main__':
    fetch_data_from_url(pune_district_id)


