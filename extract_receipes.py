import json
import os
import time

import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
import openai

load_dotenv()
# Set your OpenAI API Key
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
FILE_PATH = "data/originalrecipeso00orde.pdf"
INSTRUCTION =  f"""
    Extract all recipes from the following text starting from ---Page 11---. Each recipe should include:
    - Recipe name
    - Ingredients (with item, quantity, and unit)
    - Instructions (use the original text as much as possible)
    - Author
    - Page number

    Format each recipe in JSON format like this:

    {{
        "recipe": "Recipe Name",
        "page": 12,
        "author": "Author Name",
        "ingredients": [
            {{"item": "ingredient 1", "quantity": 2, "unit": "cups"}},
            {{"item": "ingredient 2", "quantity": 1, "unit": "tablespoon"}}
        ],
        "instructions": [
            "Step 1",
            "Step 2",
            "Step 3"
        ]
    }}.
    Not every page will have a recipe, so you may need to skip some pages.
    """ 

def upload_pdf(file_path):
    """
    Upload a PDF file to OpenAI's API.
    """
    print(f"Uploading file: {file_path}")
    with open(file_path, 'rb') as f:
        response = openai_client.files.create(
            file=f,
            purpose='assistants'
        )
    print(f"File uploaded successfully with ID: {response}")
    return response

def extract_text_from_pdf(file_id):
    """
    Extract text from the uploaded PDF using OpenAI's GPT-4 model.
    """
    print("Extracting text using GPT-4...")
    prompt = f"""
    Extract all recipes from the uploaded PDF file. Each recipe should include:
    - Recipe name
    - Ingredients (with item, quantity, and unit)
    - Instructions (use the original text as much as possible)
    - Author
    - Page number

    Format each recipe in JSON format like this:

    {{
        "recipe": "Recipe Name",
        "page": 12,
        "author": "Author Name",
        "ingredients": [
            {{"item": "ingredient 1", "quantity": 2, "unit": "cups"}},
            {{"item": "ingredient 2", "quantity": 1, "unit": "tablespoon"}}
        ],
        "instructions": [
            "Step 1",
            "Step 2",
            "Step 3"
        ]
    }}
    """

    # Use GPT-4 model to extract structured data
    try:
        assistant = openai_client.beta.assistants.create(
            model="gpt-4o",
            #messages=[
            #    {"role": "system", "content": "You are a helpful assistant for extracting recipes."},
            #    {"role": "user", "content": prompt}
            #],
            temperature=0.0
        )
        response = assistant.append_message(prompt).create_message().result

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def save_recipes_to_json(recipes_text, output_file):
    """
    Save extracted recipes to a JSON file.
    """
    try:
        recipes = json.loads(recipes_text)
        with open(output_file, 'w') as f:
            json.dump(recipes, f, indent=4)
        print(f"Recipes have been saved to {output_file}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def main():
    file_path = 'data/originalrecipeso00orde.pdf'  # Update with your file path

    # Step 1: Upload the PDF file
    file_id = upload_pdf(file_path)

    # Step 2: Give some time for the file to be processed
    time.sleep(5)

    # Step 3: Extract recipes using GPT-4
    recipes_text = extract_text_from_pdf(None)

    if recipes_text:
        # Step 4: Save extracted recipes to a JSON file
        output_file = 'recipes.json'
        save_recipes_to_json(recipes_text, output_file)

def run():
    client = openai_client
    prompt = f"""
       Extract all recipes from the uploaded PDF file. Each recipe should include:
       - Recipe name
       - Ingredients (with item, quantity, and unit)
       - Instructions (use the original text as much as possible)
       - Author
       - Page number

       Format each recipe in JSON format like this:

       {{
           "recipe": "Recipe Name",
           "page": 12,
           "author": "Author Name",
           "ingredients": [
               {{"item": "ingredient 1", "quantity": 2, "unit": "cups"}},
               {{"item": "ingredient 2", "quantity": 1, "unit": "tablespoon"}}
           ],
           "instructions": [
               "Step 1",
               "Step 2",
               "Step 3"
           ]
       }}
       """
    assistant = client.beta.assistants.create(
        name="Analyst Assistant",
        instructions="You are an helpful assistant for extracting cooking recipes from a book.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )

    message_file = client.files.create(file=open("data/originalrecipeso00orde.pdf", "rb"), purpose="assistants")
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
                "attachments": [{"file_id": message_file.id, "tools": [{"type": "file_search"}]}],
            }
        ]
    )

    #run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    #messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    #print(messages[0].content[0].text.value)

def ask_ai(prompt):

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful information extraction assistant. You will extract recipes from a book."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content

def read_pdf(pdf_path: str, start_page: int, end_page: int) -> str:
    """Extract text from PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages):
                n = i + 1
                if n < start_page or n > end_page:
                    continue
                page_message = f"---Page {n}---\n"
                text += page_message
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def run2():
    content = read_pdf(FILE_PATH, 11,175)
    #print(content)
    #print(len(content))
    prompt = f"""{INSTRUCTION}\n\n{content}"""
    print(prompt)
    response = ask_ai(prompt)
    print(response)
    with open("recipes.json", "w") as f:
        f.write(response)
if __name__ == "__main__":
    run2()
