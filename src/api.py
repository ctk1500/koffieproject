import requests

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from src.db import VIN_Cache
from src.helper import convert_to_parquet, search, NotFound
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///vin_cache.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()


@app.get("/")
def index():
    return "VIN LOOKUP API RUNNING!!"


# VIN lookup route
@app.get("/lookup/{vin}")
def lookup_vin(vin: str):
    # Check if the result is in the cache
    result = session.query(VIN_Cache).filter(VIN_Cache.vin == vin).first()

    if result:
        # VIN found in cache, return the cached result
        return {
            "Input VIN Requested": vin,
            "Make": result.make,
            "Model": result.model,
            "Model Year": result.year,
            "Body Class": result.body_class,
            "Cached Result": True
        }
    else:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/{vin}?format=json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            try:
                if "Results" in data and data["Results"]:
                    make = search("Make", data["Results"])
                    model = search("Model", data["Results"])
                    year = search("Model Year", data["Results"])
                    body_class = search("Body Class", data["Results"])

                    # Insert the result into the cache
                    cache_entry = VIN_Cache(vin=vin, make=make, model=model, year=year, body_class=body_class)
                    session.add(cache_entry)
                    session.commit()

                    return {
                        "Input VIN Requested": vin,
                        "Make": make,
                        "Model": model,
                        "Model Year": year,
                        "Body Class": body_class,
                        "Cached Result?": False
                    }
            except NotFound as e:
                raise HTTPException(status_code=response.status_code, detail=str(e))

        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch VIN information from vPIC API")

    raise HTTPException(status_code=404, detail="VIN not found in the cache or vPIC API")


# VIN remove route
@app.get("/remove/{vin}")
def remove_vin(vin: str):
    # Delete the VIN from the cache
    result = session.query(VIN_Cache).filter(VIN_Cache.vin == vin).delete()
    if result:
        session.commit()
        return {
            "VIN": vin,
            "Cache Delete Success?": True
        }
    else:
        return {
            "VIN": vin,
            "Cache Delete Success?": False
        }


# VIN export route
@app.get("/export")
def export_cache():
    # Export the cache as a parquet file
    cache_data = session.query(VIN_Cache).all()
    output = convert_to_parquet(cache_data)

    return StreamingResponse(output, media_type="application/octet-stream", headers={'Content-Disposition': 'attachment; filename="cache.parquet"'})
