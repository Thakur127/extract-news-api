from pydantic import BaseModel


class NewsResponse(BaseModel):
    url: str
    news: str
