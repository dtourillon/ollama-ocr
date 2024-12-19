import ollama
from streamlit.runtime.uploaded_file_manager import UploadedFile


def extract_text(uploaded_file: UploadedFile) -> str:
    """
    Args:
        uploaded_file: Uploaded file

    Returns:
        text extracted from uploaded file
    """
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': """Analyze the text in the provided image. Extract all readable content
                        and present it in a structured Markdown format that is clear, concise,
                        and well-organized. Ensure proper formatting (e.g., headings, lists, or
                        code blocks) as necessary to represent the content effectively.""",
            'images': [uploaded_file.getvalue()]
        }]
    )
    return response.message.content
