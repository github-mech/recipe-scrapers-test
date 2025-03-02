import requests
from fastapi import FastAPI, HTTPException
from recipe_scrapers import scrape_html
from recipe_scrapers._exceptions import WebsiteNotImplementedError, NoSchemaFoundInWildMode

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

@app.get("/scrape/")
def scrape_recipe(url: str):
    try:
        # Fetch HTML content manually with headers to avoid 403 errors
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an HTTPError for failed requests (403, 404, etc.)

        # Use scrape_html() instead of scrape_me()
        scraper = scrape_html(response.text, url=url)

        return {
            "title": scraper.title(),
            "ingredients": scraper.ingredients(),
            "instructions": scraper.instructions(),
        }

    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {http_err}")
    except WebsiteNotImplementedError:
        raise HTTPException(status_code=501, detail="Scraper for this website is not implemented.")
    except NoSchemaFoundInWildMode:
        raise HTTPException(status_code=502, detail="No schema found for this website.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
