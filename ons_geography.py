'''Using a DuckDB database to get ONS Geography data'''

import duckdb


def get_ons_from_postcode(postcode: str) -> str:
    '''Get the ONS Geography data from the given postcode'''

    conn = duckdb.connect("ons_postcodes.duckdb")

    # In the database load spatial
    conn.load_extension("spatial")

    postcode_data = conn.execute(
        "select * from postcodes where replace(postcode, ' ', '') = $1", [postcode.replace(' ', '')]).fetchall()

    conn.close()
    if len(postcode_data) == 0:
        return None
    return postcode_data[0]
