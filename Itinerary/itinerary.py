import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import requests
import json
import streamlit as st

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

import requests
import json
import time
import streamlit as st
st.image('./logo/logo.png', width=700)
class AssistantManager:
    thread_id = "thread_dLVUxAboknZy46QjKPIBQ0W9"
    assistant_id = "asst_uI9Iq6NdKivEUMbl7eaKnTiq"

    def __init__(self, client):
        self.client = client
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name, instructions=instructions, tools=tools
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"AssisID:::: {self.assistant.id}")

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"ThreadID::: {self.thread.id}")

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id, role=role, content=content
            )

    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                instructions=instructions,
            )

    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)

            self.summary = "\n".join(summary)
            print(f"SUMMARY-----> {role.capitalize()}: ==> {response}")

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            # Here you can add more functions if needed
            raise ValueError(f"Unknown function: {func_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id, run_id=self.run.id, tool_outputs=tool_outputs
        )

    def get_summary(self):
        return self.summary

    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id, run_id=self.run.id
                )
                print(f"RUN STATUS:: {run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW...")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )

    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id, run_id=self.run.id
        )
        print(f"Run-Steps::: {run_steps}")
        return run_steps.data

def main():
    openai_client = openai.Client(api_key=os.environ.get("OPENAI_API_KEY"))

    manager = AssistantManager(client=openai_client)

    st.title("ITINERARY GENERATOR")
    #st.image('bg.jpg')
    location_name = st.text_input("Enter location name:")
    submit_button = st.button(label="Run Assistant")

    if submit_button:
        manager.create_assistant(
            name="Assistant Application",
            instructions="You are a personal travel Assistant.Your job is to generate itineraries based on user destination. Generate the itinerary day wise for each of the input",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_tripadvisor_data",  # You can remove this line if not needed
                        "description": "Fetch data for a given location.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location_name": {
                                    "type": "string",
                                    "description": "The name of the location.",
                                }
                            },
                            "required": ["location_name"],
                        },
                    },
                }
            ],
        )
        manager.create_thread()

        manager.add_message_to_thread(
            role="user", content=f"fetch data for location with name: {location_name}"
        )
        manager.run_assistant(instructions="Fetch data")

        manager.wait_for_completion()

        summary = manager.get_summary()

        st.write(summary)

        st.text("Run Steps:")
        st.code(manager.run_steps(), language="json")

        # Add download button
        st.download_button('Download Itinerary', summary, file_name='itinerary.txt')

if __name__ == "__main__":
    main()