'''Using a DuckDB database to get ONS Geography data'''

import duckdb


def get_ons_from_postcode(postcode: str) -> str:
    '''Get the ONS Geography data from the given postcode'''

    conn = duckdb.connect("ons_postcodes.duckdb")

    # In the database load spatial
    conn.load_extension("spatial")

    query = conn.execute(
        "select * from postcodes where replace(postcode, ' ', '') = $1", [postcode.replace(' ', '')])

    descriptions = query.description

    postcode_data = query.fetchall()

    conn.close()
    if len(postcode_data) == 0:
        return None

    # Convert the data to a dictionary using the column names
    ons_data = {}
    for i in range(len(postcode_data[0])):
        # Don't include longitude/latitude/geometry
        if descriptions[i][0] not in ['longitude', 'latitude', 'geometry']:
            ons_data[descriptions[i][0]] = postcode_data[0][i]

    return ons_data
