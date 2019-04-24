# Configuration DB API 0.2

This API works as an interface between the React frontend and the configuration database. It, along with the React frontend, will offer a user-friendly way of adding and/or modifying DAG pipelines. It is written using [Flask](http://flask.pocoo.org/) and is meant to be deployed on any external server running Unix. By default, the Flask server will run on port 5000.

### New Features

* Index page which returns all pipelines and basic specifications for each pipeline.
 - Pipelines are returned as nested JSON in the form [key: obj] where _key_ is the pipeline's primary key (id) and _obj_ is the data associated with that pipeline (as another JSON object)

### Supported Endpoints
* /config_api/login
	- Precondition: POST request containing an OAuth token as a form argument in the form {token:"foo"}. foo should be an access token granted by Google (the React frontend handles this). For internal purposes, this access token can be generated using [Google's OAuth Playground.](https://developers.google.com/oauthplayground/)
	- Function: Gets the email address associated with a valid OAuth token. Authorizes a user based on a lookup in the Configuration database.
	- Postcondition: Returns a 200 OK Response if the token corresponds to a valid db user. Returns a 403 Forbidden if the access token provided is invalid. Returns a 400 Bad Request if the login token is not properly specified.

* /config_api/validate
	- Precondition: Successfully login using a valid access token. Pass that access token in this request in the same format as in /login
	- Function: Validates the passed session token against Flask's session variable (containing the token after successful login)
	- Postcondition: Returns a 200 OK Response if the token matches Flask's session token. Returns a 403 Forbidden if the token does not match Flask's session token. Returns a 400 Bad Request if the login token is not properly specified.

* config_api/index
 	- Precondition: Successfully login using a valid access token. Pass that access token in a POST request as form data
 	- Function: Queries all pipelines in the Configuration DB. Constructs a nested dict to be returned as a nested JSON object of various attributes of each pipeline in the query.
 	- Postcondition: Response code 405 if method is invalid. Response code 400 if no token is found in request. Response code 403 if passed token does not match the token stored in the server session. With a valid request, returns a 200 OK Response along with a JSON-formatted string object. This is a nested JSON object with each key matching the primary key of the Pipeline table. Each value in this string is another JSON object with key/value pairs containing various data about the pipeline. The key/value pairs of this inner JSON object are as follows:
 		- `name`: name of the pipeline
 		- `brand`: name of the brand a pipeline belongs to
 		- `pharma_company`: name of the pharmaceutical company a pipeline belongs to
 		- `type`: name of the PipelineType of a pipeline, e.g. regression, profitability
 		- `status`: is "Active" or "Inactive" whether the pipeline is_active
 		- `description`: text description of a pipeline
 		- `run_freq`: frequency the pipeline is run
 		- `states`: list of all states a pipeline uses. Right now, this is limited to the name of a PipelineState
 		- `transformations`: list of all transformations a pipelines uses. Right now, this is limited to the name of a TransformationTemplate
