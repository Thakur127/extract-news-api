import requests, os, time
import google.generativeai as genai
from news.news_company import NewsCompany
from urllib.parse import urlparse
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def get_domain(url: str) -> str:
    return urlparse(url).netloc


def get_page(url: str) -> str:
    time.sleep(2)
    try:
        return requests.get(url)
    except:
        raise HTTPException(status_code=400, detail="BAD URL")


def get_content_from_page(page: str, domain: str) -> str:
    content = NewsCompany(page)
    print(domain)
    match domain:
        case "thehindu.com" | "www.thehindu.com":
            return content.thehindu()
        case "indianexpress.com" | "www.indianexpress.com":
            return content.indianexpress()
        case "economictimes.indiatimes.com" | "www.economictimes.indiatimes.com":
            return content.economictimes()
        case "www.livemint.com" | "livemint.com":
            return content.mint()
        case "timesofindia.indiatimes.com" | "www.timesofindia.indiatimes.com":
            return content.timesofindia()
        case "_":
            raise ValueError("Please specify domain")


async def generate_news_from_context(context: str) -> str:
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    prompt = f"""Given the provided context for the news, extract the exact/same information in Markdown syntax with all links referenced in the article:
    
    CONTEXT:{context}'    
    """
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text
