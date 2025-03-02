import requests
from fastapi import FastAPI, HTTPException
from recipe_scrapers import scrape_me, scrape_html
from recipe_scrapers._exceptions import WebsiteNotImplementedError, NoSchemaFoundInWildMode

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

@app.get("/scrape/")
def scrape_recipe(url: str):
    try:
        # Try the standard method first
        scraper = scrape_me(url)

    except Exception as e:
        # If 403 Forbidden, manually fetch HTML and use scrape_html()
        if "403" in str(e):
            try:
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()  # Raise error for HTTP failures
                
                # Pass both the HTML and the original URL to scrape_html()
                scraper = scrape_html(response.text, org_url=url)

            except requests.exceptions.HTTPError as http_err:
                raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {http_err}")
            except Exception as err:
                raise HTTPException(status_code=500, detail=f"Failed to fetch site HTML: {err}")
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    # Safely get title and ingredients
    def safe_get(method, default=None):
        try:
            return method()
        except NotImplementedError:
            return default
    
    return {
        "title": safe_get(scraper.title, "No title found"),
        "total_time": safe_get(scraper.total_time, 0),
        "yields": safe_get(scraper.yields, "Unknown"),
        "image": safe_get(scraper.image, ""),
        "ingredients": safe_get(scraper.ingredients, []),
        "instructions": safe_get(scraper.instructions, "No instructions found"),
        "author": safe_get(scraper.author, "Unknown")
    } 
