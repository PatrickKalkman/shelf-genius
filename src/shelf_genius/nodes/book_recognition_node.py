from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from loguru import logger
from openai import OpenAI

from shelf_genius.models.shelf_genius_state import BookInfo, ShelfGeniusState

load_dotenv()

BOOK_RECOGNITION_TEMPLATE = """You are a book recognition system analyzing bookshelf images.
Your task is to identify books from the image and return ONLY a valid JSON response.

RESPONSE FORMAT REQUIREMENTS:
1. You must return ONLY valid JSON
2. The JSON must contain a "books" array
3. Each book in the array MUST have both "title" and "author" fields
4. Use simple double quotes for strings, never nested quotes
5. Remove special characters from titles and authors
6. Return empty books array if no books are clearly visible

REQUIRED JSON STRUCTURE:
{
    "books": [
        {
            "title": "string",
            "author": "string"
        }
    ]
}

If you cannot identify both title OR author for a book, just leave the string empty.
Return this if no books are clearly identifiable:
{
    "books": []
}

RESPOND ONLY WITH VALID JSON - NO OTHER TEXT OR EXPLANATION"""


def book_recognition_node(state: ShelfGeniusState) -> ShelfGeniusState:
    try:
        logger.info("Starting book recognition node with GPT-4-o-mini...")

        client = OpenAI()

        client = OpenAI()

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{state['image_base64']}"}},
                    {"type": "text", "text": BOOK_RECOGNITION_TEMPLATE},
                ],
            }
        ]

        # Use the OpenAI client directly
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, max_tokens=4096, temperature=0.1
        )

        # Parse the JSON response
        result = JsonOutputParser().parse(response.choices[0].message.content)

        if not isinstance(result, dict) or "books" not in result:
            raise ValueError("Invalid response format from LLM")

        recognized_books = [BookInfo(title=book["title"], author=book["author"]) for book in result["books"]]

        logger.info(f"Successfully recognized {len(recognized_books)} books")

        return {**state, "recognized_books": recognized_books, "current_step": "book_recognition_node"}

    except Exception as e:
        logger.error(f"Error in book recognition node: {str(e)}")
        state["error"] = f"Book recognition failed: {str(e)}"
        return state
