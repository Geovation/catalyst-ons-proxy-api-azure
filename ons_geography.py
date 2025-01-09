'''Using a DuckDB database to get ONS Geography data'''

import duckdb


def get_ons_from_long_lat(longitude: float, latitude: float) -> str:
    '''Get the ONS Geography data from the given longitude and latitude'''
    conn = duckdb.connect("ons_postcodes.duckdb")

    # In the database load spatial
    conn.load_extension("spatial")

    postcode_data = conn.sql(
        "select * from postcodes where postcode = 'BA1 1RG'").fetchall()

    conn.close()
    return postcode_data
