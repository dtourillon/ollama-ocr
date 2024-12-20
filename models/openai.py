import base64
import os
from dotenv import load_dotenv

from openai import OpenAI
from streamlit.runtime.uploaded_file_manager import UploadedFile

load_dotenv(".env")


def extract_text(
    uploaded_file: UploadedFile,
    openai_model_name: str = "gpt-4o-mini",
) -> str:
    """
    Args:
        uploaded_file: Uploaded file
        openai_model_name: OpenAI model name

    Returns:
        text extracted from uploaded file
    """
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    response = client.chat.completions.create(
        model=openai_model_name,
        store=True,
        messages=[
            {
                "role": "system",
                "content": "You are a tool to parse images.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Recreate the image's content as a machine-readable txt format. BE SURE TO VALIDATE THE DATA. No Intro or Outro words. Return ONLY the content of the document.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64.standard_b64encode(uploaded_file.getvalue()).decode()}",
                        },
                    },
                ],
            }
        ]
    )

    return response.choices[0].message.content
