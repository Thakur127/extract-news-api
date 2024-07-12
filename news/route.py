from typing import Annotated
from fastapi import APIRouter, Query, HTTPException
from .schema import NewsResponse
from fastapi.responses import StreamingResponse

from news.helper import (
    get_domain,
    get_page,
    get_content_from_page,
    generate_news_from_context,
)

router = APIRouter(prefix="/news", tags=["news"])


URL_PATTERN = "https?:\/\/(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:\/[\w\-.,@?^=%&:/~+#]*)?(?:\?[\w\-.,@?^=%&:/~+#]*)?(?:#[\w\-.,@?^=%&:/~+#]*)?"


AVAILABLE_DOMAIN = [
    "thehindu.com",
    "www.thehindu.com",
    "indianexpress.com",
    "www.indianexpress.com",
    "economictimes.indiatimes.com",
    "www.economictimes.indiatimes.com",
    "livemint.com",
    "www.livemint.com",
    "timesofindia.indiatimes.com",
    "www.timesofindia.indiatimes.com",
]


@router.get("/extract", status_code=200)
async def news_extract(url: Annotated[str, Query(pattern=URL_PATTERN)]) -> NewsResponse:
    domain = get_domain(url)
    if domain not in AVAILABLE_DOMAIN:
        raise HTTPException(
            status_code=400,
            detail=f"The domain/subdomain {domain} is not allowed. Allowed Domains/subdomains are {AVAILABLE_DOMAIN}",
        )
    page = get_page(url)
    content = get_content_from_page(page, domain)
    # generate_news_from_context(content)

    return StreamingResponse(generate_news_from_context(content))
