# Office for National Statistics data proxy API

A proxy API for appending ONS lookup data to API calls for OS data.

## Setup

This is a Azure Function App written in Python. You can run it locally using the Azure Functions Core Tools and in VSCode with the Azure Functions extension.

## Endpoints

The Azure function supports all the endpoints of the OS Places API. The documentation for the OS Places API can be found [on the technical specification page](https://osdatahub.os.uk/docs/places/technicalSpecification).

| Endpoint | Description |
| --- | --- |
| /places/{operation} | A proxy for the various places endpoints |


## Data returned

The data returned by the proxy API is the same as the data returned by the OS Places API, with the addition of the ONS lookup data. The ONS lookup data is returned in the `ons` key for each response item.


```json


```
