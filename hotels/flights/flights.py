import requests
import streamlit as st
st.image('./logo/flights.png', width=700)


def search_flight_destinations(query):
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {"query": query}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def search_flights(from_id, to_id, depart_date, page_no, adults, children):
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {
        "fromId": from_id,
        "toId": to_id,
        "departDate": depart_date,
        "pageNo": page_no,
        "adults": adults,
        "children": children,
        "currency_code": "AED"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def main():
    st.title("Flight Search")

    # Search Flight Destinations
    query = st.text_input("Search Flight Destinations (e.g., New York)")
    if st.button("Search Destinations"):
        if query:
            result = search_flight_destinations(query)
            st.write(result)
        else:
            st.error("Please enter a destination query.")

    

    # Search Flights
    st.header("Search Flights")

    from_id = st.text_input("Departure Airport Code (e.g., BOM.AIRPORT)")
    to_id = st.text_input("Arrival Airport Code (e.g., DEL.AIRPORT)")
    depart_date = st.date_input("Departure Date")
    page_no = st.number_input("Page Number", value=1)
    adults = st.number_input("Number of Adults", min_value=1, value=1)
    children = st.text_input("Children Ages (comma-separated)")

    if st.button("Search Flights"):
        if from_id and to_id and depart_date:
            depart_date_str = depart_date.strftime("%Y-%m-%d")
            result = search_flights(from_id, to_id, depart_date_str, page_no, adults, children)
            st.write(result)
        else:
            st.error("Please fill in all the required fields.")
    st.markdown(
        """
        <style>
        body {
            background-color: White; /* Set your desired background color code */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
