from fastapi import FastAPI


app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location,
        date_from,
        date_to,
        stars,
        has_spa,
):
    return date_from, date_to
