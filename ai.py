import json
import os
from string import Template

from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger
from pdf_text import read_pdf

load_dotenv()
# Set your OpenAI API Key
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def ask_ai(prompt, system_content, temperature=0):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
        messages=[
            {"role": "system",
             "content": system_content},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content
