# Configuration DB API 0.2

This API works as an interface between the React frontend and the configuration database. It, along with the React frontend, will offer a user-friendly way of adding and/or modifying DAG pipelines. It is written using [Flask](http://flask.pocoo.org/) and is meant to be deployed on any external server running Unix. By default, the Flask server will run on port 5000.

### New Features

* Index page which returns all pipelines and basic specifications for each pipeline.
 - Pipelines are returned as nested JSON in the form [key: obj] where _key_ is the pipeline's primary key (id) and _obj_ is the data associated with that pipeline (as another JSON object)
 - Moved authorization token from POST request data to all methods' request header "Authorization" (the greatest advantage of this is that we don't need to use POST requests over GET requests when the only data being sent by the client is the access token)

### Supported Endpoints
* /config_api/login
	- Precondition: GET request containing an OAuth token as a header in the form {Authorization:"foo"}. foo should be an access token granted by Google (the React frontend handles this). For internal purposes, this access token can be generated using [Google's OAuth Playground.](https://developers.google.com/oauthplayground/)
	- Function: Gets the email address associated with a valid OAuth token. Authorizes a user based on a lookup in the Configuration database.
	- Postcondition: Returns a 200 OK Response if the token corresponds to a valid db user. Returns an error code/message if not.

* /config_api/validate
	- Precondition: Successfully login using a valid access token. Pass that access token in this request in the same format as in /login
	- Function: Validates the passed session token against Flask's session variable (containing the token after successful login)
	- Postcondition: Returns a 200 OK Response if the token matches Flask's session token. Returns an error code/message if not.

* /config_api/index
 	- Precondition: Successfully login using a valid access token. Pass that access token in the Authorization header of a GET request
 	- Function: Queries all pipelines in the Configuration DB. Constructs a nested dict to be returned as a nested JSON object of various attributes of each pipeline in the query.
 	- Postcondition: Returns an error code/message if the request is invalid. With a valid request, returns a 200 OK Response along with a JSON-formatted string object. This is a JSON object containing an array of individual JSON objects. Each of these objects has a key matching the primary key of the Pipeline table, and a value which is another JSON object with `key`/value pairs containing various data about the pipeline. The `key`/value pairs of this inner JSON object are as follows:
 		- `name`: name of the pipeline
 		- `brand`: name of the brand a pipeline belongs to
 		- `pharma_company`: name of the pharmaceutical company a pipeline belongs to
 		- `type`: name of the PipelineType of a pipeline, e.g. regression, profitability
 		- `status`: is "Active" or "Inactive" whether the pipeline is_active
 		- `description`: text description of a pipeline
 		- `run_freq`: frequency the pipeline is run
 		- `states`: list of all states a pipeline uses. Right now, this is limited to the name of a PipelineState
 		- `transformations`: list of all transformations a pipelines uses. Right now, this is limited to the name of a TransformationTemplate

Here's what the /index return object looks like:
```
{
  "data": [
    {
      "1": {
        "name": "bluth_banana_regression",
        "brand": "Cornballer",
        "pharma_company": "Sitwell",
        "type": "regression",
        "status": "Active",
        "description": null,
        "run_freq": "daily",
        "states": [
          "raw",
          "ingest",
          "master"
        ],
        "transformations": [
          "extract_from_ftp",
          "initial_ingest"
        ]
      }
    },
    {
      "2": {
        "name": "bluth_profitability",
        "brand": "Cornballer",
        "pharma_company": "Sitwell",
        "type": "profitability",
        "status": "Active",
        "description": null,
        "run_freq": "hourly",
        "states": [
          "raw"
        ],
        "transformations": [
          "extract_from_ftp",
          "extract_from_ftp"
        ]
      }
    }
  ]
}
```
