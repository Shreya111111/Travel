import streamlit as st
import folium
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import os
from apikey import apikey 
from geopy.geocoders import Nominatim

# Set OpenAI API key
os.environ["OPEN_API_KEY"]= apikey
st.image('./logo/logo.png', width=700)
# Function to parse the itinerary string and extract locations
def parse_itinerary(itinerary_str):
    locations = []
    lines = itinerary_str.split("\n\n")
    for line in lines:
        parts = line.strip().split(". ")
        if len(parts) > 1:
            name = parts[0]
            description = parts[1]
            locations.append({"name": name, "description": description})
    return locations

# Function to generate itinerary based on user inputs
def generate_itinerary(destination):
    # Initialize OpenAI language model
    llm = OpenAI(openai_api_key=os.environ["OPEN_API_KEY"], model="gpt-3.5-turbo-instruct", temperature=0.6)

    # Prompt template for generating itinerary
    destination_template = PromptTemplate(input_variables=['destination'], template="Please tell me your preferred {destination}")
    destination_chain = LLMChain(llm=llm, prompt=destination_template)

    places_template = PromptTemplate(input_variables=['destination'], template="Tell me the some amazing places within {destination}")
    places_chain = LLMChain(llm=llm, prompt=places_template, output_key="itinerary")

    shopping_template = PromptTemplate(input_variables=['destination'], template="Suggest me some good places to shop and what to shop in {destination}")
    shopping_chain = LLMChain(llm=llm, prompt=shopping_template, output_key="shops")

    chain = SequentialChain(chains=[destination_chain, places_chain, shopping_chain],
                            input_variables=['destination'],
                            output_variables=["itinerary", 'shops'])

    # Generate itinerary
    itinerary = chain.invoke({'destination': destination})

    return itinerary

# Function to generate a map using Folium
def generate_map(locations):
    # Initialize map
    map = folium.Map(location=[0, 0], zoom_start=10)
    geolocator = Nominatim(user_agent="my_geocoder")

    # Add markers for each location in the itinerary
    for location in locations:
        try:
            location_info = geolocator.geocode(location['name'])
            if location_info:
                folium.Marker(
                    location=(location_info.latitude, location_info.longitude),
                    popup=location['name'],
                    icon=folium.Icon(color='blue')
                ).add_to(map)
        except Exception as e:
            print(f"Error geocoding location {location['name']}: {e}")

    return map

# Streamlit app
def main():
    # Set page title
    st.title("Travel Assistant")

    # Get user inputs
    destination = st.text_input("What is your destination?")

    # Button to generate itinerary
    if st.button("Generate Itinerary"):
        # Generate itinerary based on user inputs
        itinerary = generate_itinerary(destination)

        # Display itinerary
        st.write("Day-wise Itinerary:")
        st.write(itinerary)

        # Parse itinerary string and extract locations
        locations = parse_itinerary(itinerary["itinerary"])

        # Generate and display map
        if locations:
            map = generate_map(locations)
            st.write(map._repr_html_(), unsafe_allow_html=True)
        else:
            st.write("Itinerary not found or incomplete.")

if __name__ == "__main__":
    main()
