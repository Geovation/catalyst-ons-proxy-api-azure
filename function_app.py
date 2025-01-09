'''Azure Function App to append ONS Geography data to OS API calls'''

import logging
import azure.functions as func

from ons_geography import get_ons_from_long_lat


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="places", methods=["GET"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    '''HTTP trigger function provides the route into the application'''

    # Get the complete request Headers
    headers = req.headers

    # Get the request query parameters
    query_params = req.params

    # Call the OS Places API
    # The API URL is https://api.ordnancesurvey.co.uk/places/v1/addresses/postcode?postcode=AB12DE

    name = req.params.get('name')

    response = get_ons_from_long_lat(-1.5, 2.5)

    return func.HttpResponse(str(response))
