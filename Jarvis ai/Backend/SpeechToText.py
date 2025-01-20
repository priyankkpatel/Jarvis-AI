from selenium import webdriver
from selenium.webdriver.common.by import By  # Correct import for By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file
os.makedirs("Data", exist_ok=True)  # Ensure the directory exists
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Generate the file path for the HTML file
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Launch the browser with the specified options
Service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)

TempdirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant status and write it to a file
def SetAssistantStatus(Status, TempDirPath):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()  # Convert to lowercase and remove leading/trailing spaces
    query_words = new_query.split()  # Split the query into words
    
    # Define a list of question words
    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose", "whom",
        "can you", "what's", "where's", "how's", "can you"
    ]
    
    # Check if the query contains a question word
    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:  # If it ends with punctuation
            new_query = new_query[:-1] + "?"  # Replace the punctuation with a question mark
        else:
            new_query += "?"  # If no punctuation, add a question mark at the end
    else:
        # Add a period if the query is not a question and doesn't have punctuation
        if query_words[-1][-1] not in ['.', '?', '!']:
            new_query += "."
    
    return new_query.capitalize()  # Capitalize the first letter of the modified query

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognization():
    driver.get("file://" + Link)
    driver.find_element(By.ID, value="start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, value="output").text

            if Text:
                driver.find_element(By.ID, value="end").click()

            if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                return QueryModifier(Text)
            else:
                SetAssistantStatus("Translating..", TempdirPath)
                return QueryModifier(UniversalTranslator(Text))    
        except Exception as e:
            pass

if __name__ == "__main__":
    while True:
        Text = SpeechRecognization()
        print(Text)
