'''Using a DuckDB database to get ONS Geography data'''

import os

import duckdb

def get_ons_from_postcodes(postcodes):
    '''Get the ONS Geography data from the postcodes'''

    # The path is either data/ or /data/ depending on the environment
    db = '/data/ons_postcodes.duckdb'
    if not os.path.exists(db):
        db = 'data/ons_postcodes.duckdb'

    conn = duckdb.connect(db)

    # For all postcodes in the postcode array, remove any whitespace
    postcodes = [postcode.replace(' ', '') for postcode in postcodes]

    postcode_list = ','.join(f'\'{p}\'' for p in postcodes)

    query = conn.execute(  # Not parameterised - fix this
        "select * from vw_postcodes where replace(postcode, ' ', '') IN (" + postcode_list + ")")

    descriptions = query.description

    postcode_data = query.fetchall()

    conn.close()
    if len(postcode_data) == 0:
        return None

    # Convert the data to a dictionary using the column names
    ons_data = []
    # Loop through each row returned
    for row in postcode_data:
        ons_data_object = {}
        # Loop through each column in the row
        for i in range(len(row)):
            if descriptions[i][0] not in ['longitude', 'latitude', 'geometry']:
                ons_data_object[descriptions[i][0]] = row[i]
        ons_data.append(ons_data_object)

    return ons_data
