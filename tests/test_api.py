import json
import pyarrow.parquet as pq

import pytest

from src.db import VIN_Cache
from src.helper import convert_to_parquet, search, NotFound


# test search method of helper
def test_search():
    with open('tests/response.json', 'r') as file:
        response = json.loads(file.read())
    result = search("Make", response["Results"])
    assert result == "PETERBILT"
    result = search("Model", response["Results"])
    assert result == "388"


# test search with empty list
def test_empty_search():
    with pytest.raises(NotFound):
        search("Make", [])


def test_convert_to_parquet():
    entry = VIN_Cache(vin="x", make="x", model="x", year="x", body_class="x")
    result = convert_to_parquet([entry])
    # convert result back to table
    table = pq.read_table(result)
    # convert the table to a pandas DataFrame
    df = table.to_pandas()
    # assert data of file is equal to entry
    assert str(df.head()) == '  vin make model year body_class\n0   x    x     x    x          x'
