'''Azure Function App to append ONS Geography data to OS API calls'''

import json
from logging import getLogger

import requests

import azure.functions as func

from azure.functions import HttpRequest, HttpResponse
from azure.monitor.opentelemetry import configure_azure_monitor

from ons_geography import get_ons_from_postcodes

configure_azure_monitor(
    logger_name=__name__,
)

logger = getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name('places')
@app.route(route="places/{operation}")
def http_trigger(req: HttpRequest) -> HttpResponse:
    '''HTTP trigger function provides the route into the application.'''

    # The operation is one of "find", "postcode", "uprn", "nearest", "bbox", "radius", "polygon"
    operation = req.route_params.get("operation")

    query_params = req.params

    # Call the OS Places API
    api_url = "https://api.os.uk/search/places/v1/" + operation + "?"

    # Add all the query parameters to the URL
    for key, value in query_params.items():
        api_url += f"&{key}={value}"

    try:
        # Call the OS Places API
        response = requests.get(api_url, timeout=10)

        # Log the request
        # We simply record the call to Places and the operation name
        logger.info("Places API", extra={
                "microsoft.custom_event.name": "Places API", "operation": operation})

        # If the response is successful, append the ONS Geography data
        if response.status_code == 200:
            # Get the JSON response
            response_json = response.json()

            # The return data is a list of results with a "DPA" key and/or an "LPI" key
            # The DPA object is the delivery point address - use the POSTCODE key
            # The LPI object is the land and property identifier - use the POSTAL_ADDRESS_CODE key

            # Create an array of postcodes by trying first from the LPI object or the DPA object
            postcodes = []
            for result in response_json["results"]:
                postcode = result.get("LPI", {}).get(
                    "POSTAL_ADDRESS_CODE") or result.get("DPA", {}).get("POSTCODE")
                if postcode and postcode.replace(' ', '') not in postcodes:
                    postcodes.append(postcode.replace(' ', ''))

            ons_data_array = get_ons_from_postcodes(postcodes)

            # For each result, append the ONS Geography data
            for result in response_json["results"]:
                # Get the postcode
                postcode = result.get("LPI", {}).get(
                    "POSTAL_ADDRESS_CODE") or result.get("DPA", {}).get("POSTCODE")

                # Find the ONS Geography data for the postcode
                ons_postcode_data = None
                for ons_data in ons_data_array:
                    if ons_data.get("postcode").replace(' ', '') == postcode.replace(' ', ''):
                        ons_postcode_data = ons_data
                        break

                # Add the ONS Geography data to the result
                result["ons_postcode_data"] = ons_postcode_data

            return func.HttpResponse(json.dumps(response_json), status_code=200, mimetype="application/json")

        else:
            # If the response is not successful, return the error message
            return func.HttpResponse(
                "Error calling OS Places API: " + response.text,
                status_code=response.status_code
            )

    except Exception as e:
        # If there is an exception, return the error message
        return func.HttpResponse(
            "Error calling OS Places API: " + str(e),
            status_code=500
        )
