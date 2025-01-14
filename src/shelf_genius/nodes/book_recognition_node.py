from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from loguru import logger

from shelf_genius.models.shelf_genius_state import ShelfGeniusState

load_dotenv()


@dataclass
class BookInfo:
    """Represents a recognized book from the image."""

    title: str
    author: str


BOOK_RECOGNITION_TEMPLATE = """You are a book recognition system analyzing bookshelf images.
Your task is to identify books from the image and return ONLY a valid JSON response.

Image (base64 encoded): {image_base64}

RESPONSE FORMAT REQUIREMENTS:
1. You must return ONLY valid JSON
2. The JSON must contain a "books" array
3. Each book in the array MUST have both "title" and "author" fields
4. Use simple quotes for strings, never nested quotes
5. Remove special characters from titles and authors
6. Return empty books array if no books are clearly visible

REQUIRED JSON STRUCTURE:
{{
    "books": [
        {{
            "title": "string",
            "author": "string"
        }}
    ]
}}

If you cannot identify both title AND author for a book, do not include it.
Return this if no books are clearly identifiable:
{{
    "books": []
}}

Example of valid response:
{{
    "books": [
        {{
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald"
        }}
    ]
}}

RESPOND ONLY WITH VALID JSON - NO OTHER TEXT OR EXPLANATION"""


def book_recognition_node(state: ShelfGeniusState) -> ShelfGeniusState:
    try:
        logger.info("Starting book recognition node with local LLaVA...")

        # Initialize local LLaVA through OpenAI interface
        llm = ChatOpenAI(
            base_url="http://localhost:8080/v1",  # Local llama.cpp server
            api_key="dummy",  # Not checked by local server
            model="local-model",  # Model name doesn't matter for local server
            temperature=0.1,
            max_tokens=4096,
        )

        # Create the chain with JsonOutputParser
        parser = JsonOutputParser()

        recognition_chain = (
            PromptTemplate(template=BOOK_RECOGNITION_TEMPLATE, input_variables=["image_base64"]) | llm | parser
        )

        # Process the image
        try:
            result = recognition_chain.invoke({"image_base64": state["image_base64"]})

            logger.info(result)
            if not isinstance(result, dict) or "books" not in result:
                raise ValueError("Invalid response format from LLM")

            # Convert dictionary results to BookInfo objects
            recognized_books = [
                BookInfo(title=book["title"], author=book["author"]) for book in result["books"]
            ]

            logger.info(f"Successfully recognized {len(recognized_books)} books")
            # Ensure we're creating a new state dict with the recognized books
            return {
                **state,
                "recognized_books": recognized_books,
                "current_step": "book_recognition_node"
            }

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            state["recognized_books"] = []
            state["error"] = f"Failed to process image: {str(e)}"

    except Exception as e:
        logger.error(f"Error in book recognition node: {str(e)}")
        state["error"] = f"Book recognition failed: {str(e)}"
        return state
