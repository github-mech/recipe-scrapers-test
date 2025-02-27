from fastapi import FastAPI
from recipe_scrapers import scrape_me

app = FastAPI()

@app.get("/scrape/")
def scrape_recipe(url: str):
    scraper = scrape_me(url)

    return {
        "title": scraper.title(),
        "total_time": scraper.total_time(),
        "yields": scraper.yields(),
        "image": scraper.image(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "ratings": scraper.ratings(),
        "reviews": scraper.reviews(),
        "host": scraper.host(),
        "author": scraper.author(),
        "category": scraper.category(),
        "cuisine": scraper.cuisine(),
        "nutrients": scraper.nutrients(),
        "description": scraper.description(),
        "language": scraper.language(),
        "canonical_url": scraper.canonical_url()
    }
