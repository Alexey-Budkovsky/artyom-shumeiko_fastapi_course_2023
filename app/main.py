from fastapi import FastAPI
from typing import Optional


app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location,
        date_from,
        date_to,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = None,

):
    return location, date_from, date_to, stars, has_spa
