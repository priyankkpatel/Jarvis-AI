import asyncio
from random import randint
from PIL import Image
import httpx
from dotenv import load_dotenv
import os
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = os.path.join("Data")  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]  # Generate filenames

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

load_dotenv()
api_key = os.getenv("HuggingFaceAPIKey")

if not api_key:
    raise ValueError("HuggingFaceAPIKey is not set in the environment variables.")
headers = {"Authorization": f"Bearer {api_key}"}

async def query(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"API error: {response.status_code}, {response.text}")
            return None

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []  # List to hold image generation tasks
    
    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}"
        }
        task = asyncio.create_task(query(payload))  # Create a task
        tasks.append(task)

    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    # Ensure the Data folder exists
    os.makedirs("Data", exist_ok=True)

    # Save the generated images
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:  # Only save valid images
            with open(os.path.join("Data", f"{prompt.replace(' ', '_')}{i+1}.jpg"), "wb") as f:
                f.write(image_bytes)
        else:
            print(f"Failed to generate image {i+1}.")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main function to generate images based on the status file
def main():
    while True:
        try:
            # Read the status and prompt from the data file
            with open(os.path.join("Frontend", "Files", "ImageGenration.data"), "r") as f:
                data: str = f.read()
            
            # Split the data into Prompt and Status
            prompt, status = data.split(",")

            if status.strip() == "True":
                print(f"Generating images for prompt: {prompt}")
                GenerateImages(prompt=prompt)

                # Reset the file status after generating images
                with open(os.path.join("Frontend", "Files", "ImageGenration.data"), "w") as f:
                    f.write("False,False")
                break
            else:
                sleep(1)
        except Exception as e:
            # Handle any exception that occurs during file reading or processing
            print(f"An error occurred: {e}")
            sleep(1)  # Prevent tight loop in case of repeated errors

if __name__ == "__main__":
    main()
