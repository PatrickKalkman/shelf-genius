from langchain_core.output_parsers import JsonOutputParser
from loguru import logger
from openai import OpenAI

from shelf_genius.models.shelf_genius_state import ShelfGeniusState

RECOMMENDATION_TEMPLATE = """You are a book recommendation system analyzing a user's bookshelf.
Based on the books they own and the detailed metadata about these books, recommend ONE NEW book they might enjoy.
IMPORTANT:
- Do NOT recommend any books that are already on their shelf
- Do NOT recommend books that are too similar to what they already have (e.g., if they have a unit testing book, don't recommend other testing books)
- Look for interesting connections between their diverse interests to recommend something unique
- Consider recommending books that bridge multiple interests shown in their collection

Try to expand their horizons by finding interesting connections between topics like:
- If they have technical books and business books, consider books about tech entrepreneurship
- If they have programming and design books, consider books about creative coding or generative art
- Look for emerging topics that relate to their interests but aren't directly represented

Current books on shelf:
{book_list}

Detailed metadata about these books:
{book_metadata}

RESPONSE FORMAT REQUIREMENTS:
1. Return ONLY valid JSON
2. Include title, author, and reasoning fields
3. Use simple double quotes for strings, never nested quotes
4. Remove special characters from strings
5. MUST recommend a book that is NOT already listed above
6. MUST recommend a book that explores different topics than what's already on the shelf

REQUIRED JSON STRUCTURE:
{{
    "recommendation": {{
        "title": "string",
        "author": "string",
        "reasoning": "string"
    }}
}}

RESPOND ONLY WITH VALID JSON - NO OTHER TEXT OR EXPLANATION"""


def format_book_list(state: ShelfGeniusState) -> str:
    """Format recognized books into a readable string."""
    books = state.get("recognized_books", [])
    return "\n".join([f"- {book.title} by {book.author}" for book in books if book.title and book.author])


def format_metadata(state: ShelfGeniusState) -> str:
    """Format book metadata into a readable string."""
    metadata = state.get("book_metadata", [])
    formatted = []

    for book in metadata:
        info = []
        if "title" in book:
            info.append(f"Title: {book['title']}")
        if "authors" in book:
            info.append(f"Authors: {', '.join(book['authors'])}")
        if "categories" in book:
            info.append(f"Categories: {', '.join(book['categories'])}")
        if "description" in book:
            # Truncate description to keep prompt length manageable
            desc = book["description"][:200] + "..." if len(book.get("description", "")) > 200 else book["description"]
            info.append(f"Description: {desc}")

        formatted.append(" | ".join(info))

    return "\n".join(formatted)


def book_recommendation_node(state: ShelfGeniusState) -> ShelfGeniusState:
    """Generate a book recommendation based on the user's current books."""
    try:
        logger.info("Starting book recommendation node...")

        # Check if we have the necessary data
        if not state.get("recognized_books"):
            raise ValueError("No recognized books found in state")

        # Format the books and metadata for the prompt
        book_list = format_book_list(state)
        metadata = format_metadata(state)

        # Prepare the prompt with the formatted data
        prompt = RECOMMENDATION_TEMPLATE.format(book_list=book_list, book_metadata=metadata)

        # Initialize OpenAI client
        client = OpenAI()

        # Create the chat completion request
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,  # Slightly higher temperature for more creative recommendations
        )

        # Get the raw response content
        response_content = response.choices[0].message.content
        logger.debug(f"Raw LLM response: {response_content}")

        try:
            # First try direct JSON parsing
            import json

            result = json.loads(response_content)
        except json.JSONDecodeError:
            # If that fails, try the langchain parser
            result = JsonOutputParser().parse(response_content)

        logger.debug(f"Parsed result: {result}")

        if not isinstance(result, dict):
            raise ValueError("Response is not a dictionary")

        if "recommendation" not in result:
            # If we don't have the recommendation key, try to restructure the response
            if all(key in result for key in ["title", "author", "reasoning"]):
                result = {"recommendation": result}
            else:
                raise ValueError("Missing required fields in response")

        # Update state with the recommendation
        state["book_recommendation"] = result["recommendation"]
        state["current_step"] = "book_recommendation_node"

        logger.info(
            f"Successfully generated book recommendation: {result['recommendation']['title']} by {result['recommendation']['author']}"
        )

        return state

    except Exception as e:
        logger.error(f"Error while generating book recommendation: {str(e)}")
        state["error"] = f"Book recommendation failed: {str(e)}"
        return state
