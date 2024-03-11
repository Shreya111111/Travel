import streamlit as st
import requests
st.image('./logo/hotels.png', width=700)
# Function to fetch destination information
def fetch_destination(query):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {"query": query}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Function to search hotels based on destination ID
def search_hotels(dest_id, arrival_date, departure_date, adults, children_age, room_qty, page_number):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    headers = {
        "X-RapidAPI-Key": "0c63117868msh5a2f12f252b5985p1ff156jsn28a528f984ba",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    querystring = {
        "dest_id": dest_id,
        "search_type": "CITY",
        "arrival_date": arrival_date,
        "departure_date": departure_date,
        "adults": adults,
        "children_age": children_age,
        "room_qty": room_qty,
        "page_number": page_number,
        "languagecode": "en-us",
        "currency_code": "AED"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Streamlit app
def main():
    st.title("Booking.com Hotel Search")

    # Fetch destination ID
    query = st.text_input("Enter your destination query:")
    if st.button("Search Destination"):
        if query:
            result = fetch_destination(query)
            if "data" in result:
                destinations = result["data"]
                if len(destinations) > 0:
                    dest_name = destinations[0]['name']
                    dest_id = destinations[0]['dest_id']
                    st.write(f"Destination found: {dest_name}, ID: {dest_id}")
                    st.session_state["dest_id"] = dest_id  # Save destination ID in session state
                else:
                    st.error("No destinations found.")
            else:
                st.error("Failed to fetch destinations.")

    # Search hotels
    dest_id = st.session_state.get("dest_id")
    if dest_id:
        arrival_date = st.date_input("Arrival Date", value=None)
        st.session_state["arrival_date"] = arrival_date  # Save arrival date in session state

        # Retrieve departure date from session state
        departure_date = st.session_state.get("departure_date")
        if departure_date is None:
            departure_date = st.date_input("Departure Date", value=None)
            st.session_state["departure_date"] = departure_date  # Save departure date in session state

        adults = st.number_input("Number of Adults", min_value=1, value=1)
        children_age = st.text_input("Children Ages (comma-separated)")
        room_qty = st.number_input("Number of Rooms", min_value=1, value=1)
        page_number = st.number_input("Page Number", min_value=1, value=1)

        if st.button("Search Hotels"):
            result = search_hotels(dest_id, str(arrival_date), str(departure_date), adults, children_age, room_qty, page_number)
            st.write(result)
    else:
        st.error("Please search for a destination first.")

if __name__ == "__main__":
    main()