from fastapi import FastAPI, HTTPException
from recipe_scrapers import scrape_me
from recipe_scrapers._exceptions import WebsiteNotImplementedError, NoSchemaFoundInWildMode

app = FastAPI()

@app.get("/scrape/")
def scrape_recipe(url: str):
    try:
        scraper = scrape_me(url)

        # Safely get title and ingredients
        def safe_get(method, default=None):
            try:
                return method()
            except NotImplementedError:
                return default
        
        return {
            "title": safe_get(scraper.title, "No title found"),
            "ingredients": safe_get(scraper.ingredients, [])
        }

    except WebsiteNotImplementedError:
        raise HTTPException(status_code=501, detail="Scraper for this website is not implemented.")
    except NoSchemaFoundInWildMode:
        raise HTTPException(status_code=502, detail="No schema found for this website in wild mode.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
