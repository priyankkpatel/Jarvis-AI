from json import load, dump  # Importing functions to read and write JSON files.
from groq import Groq  # Importing the Groq library to use its API.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.
import os  # Importing os module for directory and file operations.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

# Ensure the 'Data' directory exists.
if not os.path.exists("Data"):
    os.makedirs("Data")

# Initialize the ChatLog.json file if it doesn't exist.
if not os.path.exists(r"Data\ChatLog.json"):
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f, indent=4)

# Function to get real-time information.
def RealtimeInformation():
    # Get the current date and time.
    current_date_time = datetime.datetime.now()

    # Extract day of the week, day of the month, full month name, and year.
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # Format the information into a string.
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes {second} seconds.\n"

    return data

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    # Split the response into lines.
    lines = Answer.split('\n')

    # Remove empty lines.
    non_empty_lines = [line for line in lines if line.strip()]

    # Join the cleaned lines back together.
    modified_answer = '\n'.join(non_empty_lines)

    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    try:        
        # Load the existing chat log from the JSON file.
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)  # Use json.load to read the JSON data.

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": Query})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Specify the AI model to use.
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # Include system instructions, real-time info, and chat history.
            max_tokens=1024,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness (higher means more random).
            top_p=1,  # Use nucleus sampling to control diversity.
            stream=True,  # Enable streaming response.
            stop=None  # Allow the model to determine when to stop.
        )

        # Initialize an empty string to store the AI's response.
        Answer = ""

        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check if there's content in the current chunk.
                Answer += chunk.choices[0].delta.content

        # Clean up any unwanted tokens from the response.
        Answer = Answer.replace("</s>", "")

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": Answer})

        # Save the updated chat log to the JSON file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return AnswerModifier(Answer)

    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")

        # Reset the chat log.
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)

        # Retry the query after resetting the log.
        return ChatBot(Query)

# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # Prompt the user for a question.
        print(ChatBot(user_input))  # Call the chatbot function and print its response.
