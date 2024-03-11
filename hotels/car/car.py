import streamlit as st
import requests

st.image('./logo/car.png', width=600)
def search_car_locations(query):
    url = "https://booking-com15.p.rapidapi.com/api/v1/cars/searchDestination"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {"query": query}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def search_car_rentals(pick_up_latitude, pick_up_longitude, drop_off_latitude, drop_off_longitude, pick_up_date, drop_off_date, pick_up_time, drop_off_time, driver_age, currency_code):
    url = "https://booking-com15.p.rapidapi.com/api/v1/cars/searchCarRentals"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {
        "pick_up_latitude": pick_up_latitude,
        "pick_up_longitude": pick_up_longitude,
        "drop_off_latitude": drop_off_latitude,
        "drop_off_longitude": drop_off_longitude,
        "pick_up_date": pick_up_date,
        "drop_off_date": drop_off_date,
        "pick_up_time": pick_up_time,
        "drop_off_time": drop_off_time,
        "driver_age": driver_age,
        "currency_code": currency_code
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def main():
    st.title("Car Rentals")

    # Search Car Locations
    query = st.text_input("Search Car Locations (e.g., New York)")
    if st.button("Search Locations"):
        if query:
            result = search_car_locations(query)
            st.write(result)
        else:
            st.error("Please enter a location query.")

    # Search Car Rentals
    st.header("Search Car Rentals")
    pick_up_latitude = st.text_input("Pick-up Latitude")
    pick_up_longitude = st.text_input("Pick-up Longitude")
    drop_off_latitude = st.text_input("Drop-off Latitude")
    drop_off_longitude = st.text_input("Drop-off Longitude")
    pick_up_date = st.date_input("Pick-up Date")
    drop_off_date = st.date_input("Drop-off Date")
    pick_up_time = st.text_input("Pick-up Time")
    drop_off_time = st.text_input("Drop-off Time")
    driver_age = st.text_input("Driver Age")
    currency_code = st.text_input("Currency Code", value="USD")

    if st.button("Search Car Rentals"):
        if pick_up_latitude and pick_up_longitude and drop_off_latitude and drop_off_longitude and pick_up_date and drop_off_date and pick_up_time and drop_off_time and driver_age and currency_code:
            result = search_car_rentals(pick_up_latitude, pick_up_longitude, drop_off_latitude, drop_off_longitude, str(pick_up_date), str(drop_off_date), pick_up_time, drop_off_time, driver_age, currency_code)
            st.write(result)
        else:
            st.error("Please fill in all the required fields.")

if __name__ == "__main__":
    main()
