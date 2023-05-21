
import pandas

from io import BytesIO
from src.db import VIN_Cache


class NotFound(Exception):
    ...


def search(value: str, results: list):

    for el in results:
        if el["Variable"] == value:
            return el["Value"]

    raise NotFound(f"Value not found {value}")


def convert_to_parquet(cache_data: list[VIN_Cache]):
    df = pandas.DataFrame(
        [(entry.vin, entry.make, entry.model, entry.year, entry.body_class) for entry in cache_data],
        columns=["vin", "make", "model", "year", "body_class"]
    )
    output = BytesIO()
    df.to_parquet(output, index=False)
    output.seek(0)
    return output
