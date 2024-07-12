from bs4 import BeautifulSoup


class NewsCompany:
    def __init__(self, page: str):
        self.page = page
        self.soup = BeautifulSoup(page.content, "lxml")
        for script in self.soup.find_all("script"):
            script.decompose()
        for style in self.soup.find_all("style"):
            style.decompose()

    def thehindu(self):
        content = self.soup.find(class_="storyline")
        for script in content.find_all("script"):
            script.decompose()
        return content

    def indianexpress(self):
        content = self.soup.findAll(True, {"class": ["heading-part", "story-details"]})
        return content

    def economictimes(self):
        header = self.soup.find("h1", {"class": "artTitle"})
        byline = self.soup.find("div", {"class": "artByline"})
        synopsis = self.soup.find("div", {"class": "artSyn"})
        artBody = self.soup.find("article", {"class": "artData"})
        content = header, byline, synopsis, artBody
        return content

    def mint(self):
        headline = self.soup.find("h1", {"class": "headline"})
        articleInfo = self.soup.find_all("span", {"class": "articleInfo"})
        mainArea = self.soup.find("div", {"id": "mainArea"})
        return headline, articleInfo, mainArea

    def timesofindia(self):
        headline = self.soup.find("h1", {"class": "HNMDR"})
        byline = self.soup.find("div", {"class": "byline_action"})
        synopsis = self.soup.find("div", {"class": "art_synopsis"})
        body = self.soup.find("div", {"class": "_s30J"})
        return headline, byline, synopsis, body
