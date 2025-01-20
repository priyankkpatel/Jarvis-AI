import pygame  # Import pygame library for handling audio playback
import random  # Import random for generating random choices
import asyncio  # Import asyncio for asynchronous operations
import edge_tts  # Import edge_tts for text-to-speech functionality
import os  # Import os for file path handling
from dotenv import dotenv_values  # Import dotenv for reading environment variables from a .env file

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Get the Assistant Voice from the environment variables


# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text: str) -> None:
    """
    Converts text to an audio file using Edge TTS and saves it as an MP3 file.

    :param text: The text to convert into speech.
    """
    file_path = r"Data/speech.mp3"  # Define the path where the speech file will be saved

    # Check if the file already exists
    if os.path.exists(file_path):
        os.remove(file_path)  # If it exists, remove it to avoid overwriting errors

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
 
 
    await communicate.save(file_path)  # Save the generated speech as an MP3 file

pygame.init()  # Initialize pygame
pygame.mixer.init()

def TTS(Text, func=lambda r=None: True):
    """
    Handles text-to-speech playback using pygame.

    :param Text: The text to be converted into speech.
    :param func: A callable that returns a boolean. If it returns False, playback stops.
    """
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data/speech.mp3")
            pygame.mixer.music.play()  # Play the audio

            # Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if not func():  # Check if the external function returns False
                    break
                pygame.time.Clock().tick(10)  # Limit the loop to 10 ticks per second

            return True  # Return True if the audio played successfully

        except Exception as e:  # Handle any exceptions during the process
            print(f"Error in TTS: {e}")

        finally:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")


def TextToSpeech(Text, func=lambda r=None: True):
    """
    Converts text into speech and plays it. If the text is too long, it plays a truncated version
    along with a predefined response.

    :param Text: The text to be converted into speech.
    :param func: A callable that returns a boolean. If it returns False, playback stops.
    """
    # Split the text by periods into a list of sentences
    Data = str(Text).split(".")

    # List of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
    ]

    # If the text is very long (more than 4 sentences and 250 characters)
    if len(Data) > 4 and len(Text) >= 250:
        # Play the first two sentences along with a random response
        TTS(" ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        # Otherwise, just play the whole text
        TTS(Text, func)


# Main execution loop
if __name__ == "__main__":
    while True:
        try:
            # Prompt user for input and pass it to the TextToSpeech function
            TextToSpeech(input("Enter text: "))
        except KeyboardInterrupt:
            print("Exiting program.")
            break
