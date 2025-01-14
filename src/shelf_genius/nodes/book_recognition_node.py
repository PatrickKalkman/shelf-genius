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
Focus only on clearly visible book spines or covers.

Image (base64 encoded): {image_base64}

Return a strict JSON response with exactly these fields:
{{
    "books": [
        {{
            "title": "The exact book title",
            "author": "The book author"
        }}
    ]
}}

IMPORTANT FORMATTING RULES:
1. Never use nested quotes in strings
2. Only include books you can clearly identify
3. Both title and author must be present
4. Remove any special characters from titles and authors
5. If unsure about a book, exclude it entirely

Example with good formatting:
{{
    "books": [
        {{
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald"
        }},
        {{
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee"
        }}
    ]
}}"""


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
            # Convert dictionary results to BookInfo objects
            recognized_books = [
                BookInfo(title=book["title"], author=book["author"]) for book in result.get("books", [])
            ]

            logger.info(f"Successfully recognized {len(recognized_books)} books")
            state["recognized_books"] = recognized_books

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            state["recognized_books"] = []
            state["error"] = f"Failed to process image: {str(e)}"

        state["current_step"] = "book_recognition_node"
        return state

    except Exception as e:
        logger.error(f"Error in book recognition node: {str(e)}")
        state["error"] = f"Book recognition failed: {str(e)}"
        return state
