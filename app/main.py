from fastapi import FastAPI

app = FastAPI()

@app.get("/hotels/{hotel_id}")
def get_hotels(hotel_id: int):
    return hotel_id