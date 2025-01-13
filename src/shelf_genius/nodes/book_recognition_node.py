from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from loguru import logger

from shelf_genius.models.shelf_genius_state import ShelfGeniusState

load_dotenv()


def book_recognition_node(state: ShelfGeniusState) -> ShelfGeniusState:
    try:
        logger.info("Starting book recognition node...")

        # Initialize the LLM
        llm = OpenAI()

        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=["image_base64"],
            template="Analyze the following base64 encoded image and recognize the books in it. "
            "Report the title and author of each book in JSON format. "
            "If a book cannot be recognized, discard it. "
            "Image: {image_base64}",
        )

        # Create the chain and invoke it
        chain = prompt_template | llm
        result = chain.invoke(state["image_base64"])

        # Parse the result and update the state
        recognized_books = []
        for book in result:
            if "title" in book and "author" in book and book["title"] and book["author"]:
                recognized_books.append(book)

        state["recognized_books"] = recognized_books
        state["current_step"] = "book_recognition_node"

        return state

    except Exception as e:
        logger.error(f"Error while recognizing books in image: {str(e)}")
        state["error"] = f"Book recognizing failed: {str(e)}"
        return state
