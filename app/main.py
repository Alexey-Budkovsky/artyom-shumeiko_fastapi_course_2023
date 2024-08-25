from fastapi import FastAPI
from typing import Optional
from datetime import date


app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = None,

):
    return location, date_from, date_to, stars, has_spa
