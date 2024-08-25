from fastapi import FastAPI


app = FastAPI()


@app.get("/hotels/{hotel_id}")
def get_hotels(hotel_id: int, date_from, date_to):
    return hotel_id, date_from, date_to
