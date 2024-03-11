import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
import os

# Set OpenAI API key
os.environ["OPEN_API_KEY"] = "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"

# Initialize OpenAI language model
llm = OpenAI(openai_api_key=os.environ["OPEN_API_KEY"],model="gpt-3.5-turbo-instruct" ,temperature=0.6)

# Prompt template for destination input
destination_template = PromptTemplate(input_variables=['destination'],template="Hello! I am your travel assistant. What is your {destination}?")
destination_chain= LLMChain(llm=llm,prompt=destination_template)

# Prompt template for duration input
days_template = PromptTemplate(input_variables=['days'],template="For how many {days} do you want to visit? Please specify the dates if possible.")
days_chain= LLMChain(llm=llm,prompt=days_template)
# Prompt template for generating itinerary
itinerary_template = PromptTemplate(input_variables=['destination', 'days'],template="Generate a detailed day-wise itinerary for visiting {destination} for {days} days.")
itinerary_chain= SimpleSequentialChain(chains=[destination_chain,days_chain])

# Function to generate itinerary based on user inputs

def generate_itinerary(destination, days):
    # Generate itinerary prompt
    prompt = itinerary_template.format(destination=destination, days=days)
    
    # Create input dictionary with the required key 'input'
    inputs = {'input': prompt, 'destination': destination, 'days': days}
    
    # Generate itinerary
    itinerary = itinerary_chain.run(inputs)
    return itinerary

# Streamlit app
def main():
    # Set page title
    st.title("Travel Assistant")

    # Get user inputs
    destination_template = st.text_input("What is your destination?")
    days_template = st.number_input("For how many days do you want to visit?", min_value=1, step=1)
    preferred_dates = st.text_input("Preferred dates (if known)")

    # Button to generate itinerary
    if st.button("Generate Itinerary"):
        # Generate itinerary based on user inputs
        itinerary = generate_itinerary(destination_template, days_template)
        # Display itinerary
        st.write("Day-wise Itinerary:")
        st.write(itinerary)

if _name_ == "_main_":
    main()