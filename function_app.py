'''Azure Function App to append ONS Geography data to OS API calls'''

import json
import requests
import azure.functions as func

from ons_geography import get_ons_from_postcode

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="places/{operation}", methods=["GET"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    '''HTTP trigger function provides the route into the application'''

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

        # If the response is successful, append the ONS Geography data
        if response.status_code == 200:
            # Get the JSON response
            response_json = response.json()

            # For each result, append the ONS Geography data
            for result in response_json["results"]:
                # Get the postcode
                postcode = result.get("DPA", {}).get("POSTCODE")

                # Get the ONS Geography data
                ons_geography = get_ons_from_postcode(postcode)

                # Add the ONS Geography data to the result
                result["ons_geography"] = ons_geography

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
