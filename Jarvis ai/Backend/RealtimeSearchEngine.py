from googlesearch import search  # Importing the Google search library.
from groq import Groq  # Importing the Groq library to use its API.
from json import load, dump  # Importing functions to read and write JSON files.
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    # Perform a Google search and get up to 5 results.
    results = list(search(query,advanced=True, num_results=5))  # Removed 'advanced=True'.
    
    # Prepare the response string.
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"  # Use proper string formatting.
    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    # Split the response into lines.
    lines = Answer.split('\n')
    
    # Remove empty lines.
    non_empty_lines = [line for line in lines if line.strip()]
    
    # Join the cleaned lines back together.
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [  # Added missing commas here.
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "How can i help you"}
]

def Information():
    # Get the current date and time.
    current_date_time = datetime.datetime.now()
    
    # Extract relevant components of date and time.
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    # Format the information into a readable string.
    data = "Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Append the user's prompt to the message log.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    Answer = ""
    for chunks in completion:
        if chunks.choices[0].delta.content:
            Answer += chunks.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})  # Fixed the syntax error here.

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":  # Fixed indentation for this line.
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
