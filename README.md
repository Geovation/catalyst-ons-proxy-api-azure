# Office for National Statistics postcode data proxy API

A proxy API for appending ONS lookup data to API calls to OS Places API. This is a wrapper around the OS Places API that adds ONS lookup data to the response. The ONS lookup data is stored in a DuckDB database and is queried using SQL.

## Setup

This is a Azure Function App written in Python. You can run it locally using the Azure Functions Core Tools and in VSCode with the Azure Functions extension.

### Database

The ONS lookup data is stored in a DuckDB database. The database is sources from the [Catalyst ONS Geographies](https://github.com/Geovation/catalyst-ons-geographies) repository. The database is stored in the `data` directory.

## Endpoints

The Azure function supports all the endpoints of the OS Places API. The documentation for the OS Places API can be found [on the technical specification page](https://osdatahub.os.uk/docs/places/technicalSpecification).

| Endpoint            | Description                              |
| ------------------- | ---------------------------------------- |
| /places/{operation} | A proxy for the various places endpoints |

## API key

In the places API a key can be included in the request by adding this as a query parameter. This wrapper will allow the same thing - pass your API key and it will be added to the request.

```
/places/find?maxresults=1&query=Ordnance%20Survey,%20Adanac%20Drive,%20SO16&key=yourapikey
```

## Data returned

The data returned by the proxy API is the same as the data returned by the OS Places API, with the addition of the ONS lookup data. The ONS lookup data is returned in the `ons_postcode_data` object key for each response item.

```json
{
  "DPA": {
    "UPRN": "200010019924",
    "UDPRN": "52126562",
    "ADDRESS": "ORDNANCE SURVEY, 4, ADANAC DRIVE, NURSLING, SOUTHAMPTON, SO16 0AS",
    "ORGANISATION_NAME": "ORDNANCE SURVEY",
    "BUILDING_NUMBER": "4",
    "THOROUGHFARE_NAME": "ADANAC DRIVE",
    "DEPENDENT_LOCALITY": "NURSLING",
    "POST_TOWN": "SOUTHAMPTON",
    "POSTCODE": "SO16 0AS",
    "RPC": "2",
    "X_COORDINATE": 437292.43,
    "Y_COORDINATE": 115541.95,
    "STATUS": "APPROVED",
    "LOGICAL_STATUS_CODE": "1",
    "CLASSIFICATION_CODE": "CO01GV",
    "CLASSIFICATION_CODE_DESCRIPTION": "Central Government Service",
    "LOCAL_CUSTODIAN_CODE": 1760,
    "LOCAL_CUSTODIAN_CODE_DESCRIPTION": "TEST VALLEY",
    "COUNTRY_CODE": "E",
    "COUNTRY_CODE_DESCRIPTION": "This record is within England",
    "POSTAL_ADDRESS_CODE": "D",
    "POSTAL_ADDRESS_CODE_DESCRIPTION": "A record which is linked to PAF",
    "BLPU_STATE_CODE": "2",
    "BLPU_STATE_CODE_DESCRIPTION": "In use",
    "TOPOGRAPHY_LAYER_TOID": "osgb1000002682081995",
    "WARD_CODE": "E05012936",
    "PARISH_CODE": "E04004629",
    "LAST_UPDATE_DATE": "31/03/2020",
    "ENTRY_DATE": "01/09/2010",
    "BLPU_STATE_DATE": "01/09/2010",
    "LANGUAGE": "EN",
    "MATCH": 0.6,
    "MATCH_DESCRIPTION": "NO MATCH",
    "DELIVERY_POINT_SUFFIX": "1A"
  },
  "ons_postcode_data": {
    "postcode": "SO160AS",
    "date_of_termination": null,
    "county_code": "E10000014",
    "county_name": "Hampshire",
    "county_electoral_division_code": "E58001784",
    "county_electoral_division_name": "Romsey Rural ED",
    "local_authority_district_code": "E07000093",
    "local_authority_district_name": "Test Valley",
    "ward_code": "E05012936",
    "ward_name": "Chilworth, Nursling & Rownhams",
    "easting": 437292,
    "northing": 115542,
    "country_code": "E92000001",
    "country_name": "England",
    "region_code": "E12000008",
    "region_name": "South East",
    "westminster_parliamentary_constituency_code": "E14001449",
    "westminster_parliamentary_constituency_name": "Romsey and Southampton North",
    "output_area_11_code": "E00117738",
    "lower_super_output_area_11_code": "E01023170",
    "middle_super_output_area_11_code": "E02004828",
    "built_up_area_24_code": "E63013470",
    "built_up_area_name": "Rownhams",
    "rural_urban_11_code": "C1",
    "rural_urban_11_name": "(England/Wales) Urban city and town",
    "index_multiple_deprivation_rank": 23969,
    "output_area_21_code": "E00190578",
    "lower_super_output_area_21_code": "E01023170",
    "middle_super_output_area_21_code": "E02004828"
  }
}
```

## Logging

The solution integrates logging to Azure App Insights, and configures a custom event to track calls to the Places API.

| Event name | Parameters | Description                                               |
| ---------- | ---------- | --------------------------------------------------------- |
| Places API | Operation  | Records every call the Places API, and the operation name |

## Environment setup

| Environment variable                  | Description                                                       |
| ------------------------------------- | ----------------------------------------------------------------- |
| APPLICATIONINSIGHTS_CONNECTION_STRING | Connection string for the application insights instance (if used) |
