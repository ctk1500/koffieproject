API for caching and retrieving vehicle VINs

**before running please run init/create_db.py in init folder**

/lookup

-lookup vin in database cache, if not found use vpic.nhtsa.dot.gov api

/remove

-remove vin from the cache if exists

/export

-download database cache as a parquet file

Running fastapi:

uvicorn main:app --reload