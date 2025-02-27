from fastapi import FastAPI, HTTPException
from recipe_scrapers import scrape_me
from recipe_scrapers._exceptions import WebsiteNotImplementedError, NoSchemaFoundInWildMode

app = FastAPI()

@app.get("/scrape/")
def scrape_recipe(url: str):
    try:
        scraper = scrape_me(url)

        # Helper function to handle missing fields
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
            "ratings": safe_get(scraper.ratings, 0),
            "reviews": safe_get(scraper.reviews, 0),  # Handles the error here!
            "host": safe_get(scraper.host, "Unknown"),
            "author": safe_get(scraper.author, "Unknown"),
            "category": safe_get(scraper.category, "Unknown"),
            "cuisine": safe_get(scraper.cuisine, "Unknown"),
            "nutrients": safe_get(scraper.nutrients, {}),
            "description": safe_get(scraper.description, "No description available"),
            "language": safe_get(scraper.language, "Unknown"),
            "canonical_url": safe_get(scraper.canonical_url, url)  # Default to the input URL
        }

    except WebsiteNotImplementedError:
        raise HTTPException(status_code=501, detail="Scraper for this website is not implemented.")
    except NoSchemaFoundInWildMode:
        raise HTTPException(status_code=502, detail="No schema found for this website in wild mode.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
