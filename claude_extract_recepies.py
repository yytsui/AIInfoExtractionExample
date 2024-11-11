import anthropic
import base64
import httpx
import os
from dotenv import load_dotenv

from extract_receipes import FILE_PATH

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
#FILE_PATH = "/home/yiy/projects/construction/example_files/CivilPermits/Civil Permit - 55 E 7th Ave - E 6th & Quebec.pdf"
FILE_PATH = "data/originalrecipeso00orde.pdf"

def run():
    # First fetch the file
   # pdf_url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
    #content = httpx.get(pdf_url).content
    with open(FILE_PATH, "rb") as f:
        content = f.read()
    pdf_data = base64.standard_b64encode(content).decode("utf-8")
    # Finally send the API request
    message = client.beta.messages.create(
        model="claude-3-5-sonnet-20241022",
        betas=["pdfs-2024-09-25"],
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extract all recipes"
                    }
                ]
            }
        ],
    )

    print(message.content)
    # lock(text="This appears to be a surveyor's or civil engineering document showing a property layout/site plan on Quebec Street.
    # It includes:\n\n
    # 1. A detailed property survey/site plan with measurements\n
    # 2. A small photograph showing what appears to be a street view of the property\n
    # 3. Various legends and symbols explaining the markings on the plan\n
    # 4. Company logos/information (appears to be Novus related)\n
    # 5. A key plan showing the location in the broader street context\n
    # 6. Various technical notations and measurements\n\n
    # The document seems to be related to property documentation, possibly for construction,
    # renovation, or property records purposes.
    # It includes professional survey markings, property lines, and various technical specifications
    # that would be used in civil engineering or architectural planning.\n\n
    # The layout shows both the property boundaries and its relationship to Quebec Street,
    # with precise measurements and notations typical of a professional land survey or site plan document.",
    # type='text')]
    #

    # [BetaTextBlock(text='Based on the survey/property plan shown,
    # this property is located on Quebec Street in Vancouver.
    # It appears to be situated between 7th Avenue and 6th Avenue (as shown by "6TH AVE" markings on the plan).',
    # type='text')]
    #
    # Process finished with exit code 0

if __name__ == "__main__":
    run()