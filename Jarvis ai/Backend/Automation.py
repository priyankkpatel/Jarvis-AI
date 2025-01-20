# Import required libraries
from AppOpener import close, open as appopen  # Functions to open and close apps
from webbrowser import open as webopen  # Import web browser functionality
from pywhatkit import search, playonyt  # For Google search and YouTube playback
from dotenv import dotenv_values  # To manage environment variables
from bs4 import BeautifulSoup  # For parsing HTML content
from rich import print  # For styled console output
from groq import Groq  # For AI chat functionalities
import webbrowser  # For opening URLs
import subprocess  # For interacting with the system
import requests  # For making HTTP requests
import keyboard  # For keyboard-related actions
import asyncio  # For asynchronous programming
import os  # For operating system functionalities

# Load environment variables from the .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key

# Check if the API key is present
if not GroqAPIKey:
    raise ValueError("GroqAPIKey is not found in the environment variables.")

# Define CSS classes for parsing specific elements in HTML content
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLCW", 
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
    "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table",
    "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# Define a user-agent for making web requests
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

# List to store chatbot messages
messages = []

# System message to provide context to the chatbot
username = os.environ.get('Username', 'User')  # Default to 'User' if 'Username' is not defined
SystemChatBot = [{"role": "system", "content": f"Hello, I am {username}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."}]

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search
    return True  # Indicate success



# Initialize the Groq client with your API key (replace with your own API key)


messages = [{"role": "system", "content": "You are a content writer. Write professional content based on the prompt."}]

def Content(Topic: str):
    def OpenNotepad(File):
        """Open the text file in Notepad."""
        default_text_editor = 'notepad.exe'  # Default text editor (Notepad)
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.

    def ContentWriterAI(prompt):
        """Generate content using the Groq API."""
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = client.chat.create(
                            model="llama-3.3-70b-versatil",  # Ensure the correct model is available
                            messages=messages,
                            max_tokens=2048,
                            temperature=0.7,
                            top_p=1,
                            stream=False,  # Set to False for full response
                        )
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Error generating content."

        Answer = completion["choices"][0]["message"]["content"].strip()  # Extract the response
        messages.append({"role": "assistant", "content": Answer})  # Save the response to history
        return Answer

    # Clean the topic by removing "Content" keyword and any other necessary adjustments
    Topic = Topic.replace("Content", "").strip()

    # Generate content for the provided topic
    ContentByAI = ContentWriterAI(Topic)
    
    if not ContentByAI:
        return False  # If no content generated, return failure

    # Save the generated content to a text file in a safe directory path
    file_path = os.path.join("Data", f"{Topic.lower().replace(' ', '_')}.txt")  # Use _ for safe file names
    os.makedirs("Data", exist_ok=True)  # Ensure the "Data" folder exists

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(ContentByAI)  # Write the content to the file
    except Exception as e:
        print(f"Error saving the file: {e}")
        return False  # Return failure if there’s an issue saving the file
    
    # Open the file in Notepad
    OpenNotepad(file_path)

    return True  # Return success
    

def PlayYoutube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video. 
    return True  # Indicate success.





def YoutubeSearch(Topic):
    Url4search = f"https://www.youtube.com/results?search_query={Topic}"  # Corrected to use Topic
    webbrowser.open(Url4search)
    return True



# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.Session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app
        return True  # Indicate success.
    except Exception as e:
        print(f"Error: {e}")
        return False  # Indicate failure if there was an error.

    # Nested function to extract links from HTML content.
    def extract_links(html):
        if html is None:
            return []
        soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
        links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
        return [link.get('href') for link in links]  # Return the links.

    # Nested function to perform a Google search and retrieve HTML.
    def search_google(query):
        url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
        headers = {"User-Agent": "Mozilla/5.0"}  # Use a predefined user-agent.
        response = sess.get(url, headers=headers)  # Perform the GET request.
        
        if response.status_code == 200:
            return response.text  # Return the HTML content.
        else:
            print("Failed to retrieve search results.")  # Print an error message.
            return None
        
        

    # Perform the Google search.
    html = search_google(app)
    if html:
        link = extract_links(html)[0]  # Extract the first link from the search results.
        webbrowser.open(link)  # Open the link in a web browser.
        return True  # Indicate success.
    return False  # Indicate failure if no HTML is retrieved or link extraction fails.


def CloseApp(app):
    if "chrome" in app :
        pass 

    else : 
        try :
            close(app, match_closest=True ,output=True , throw_error = True)
            return True
        except : 
         return False
        

       
        
# Function to execute system-level commands.
def System(command):
    
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True  # Indicate success.


# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks.
    
    for command in commands:
        if command.startswith("open "):  # Handle "open" commands.
            if "open it" in command or "open file" in command:  # Ignore specific commands.
                pass
            else:
                # Schedule app opening for other "open" commands.
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):  # Placeholder for general commands.
            pass
        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass
        elif command.startswith("close"):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))
            funcs.append(fun)
        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content"):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No function found for: {command}")  # Print an error for unrecognized commands.
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*funcs)
    
    # Process the results
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):  # Translate and execute commands.
        pass
    return True  # Indicate success.


