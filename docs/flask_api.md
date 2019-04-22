#Configuration DB API 0.1

This API works as an interface between the React frontend and the configuration database. It, along with the React frontend, will offer a user-friendly way of adding and/or modifying DAG pipelines. It is written using [Flask](http://flask.pocoo.org/) and is meant to be deployed on any external server running Unix. By default, the Flask server will run on port 5000.

###New Features

* OAuth 2.0 token validation against configuration db
* Session cookie stores token value and is required with each subsequent API request

###Supported Endpoints
* /config_api/login
	- Precondition: POST request containing an OAuth token as a form argument in the form {token:"foo"}. foo should be an access token granted by Google (the React frontend handles this). For internal purposes, this access token can be generated using [Google's OAuth Playground.](https://developers.google.com/oauthplayground/)
	- Function: Gets the email address associated with a valid OAuth token. Authorizes a user based on a lookup in the Configuration database.
	- Postcondition: Returns a 200 OK Response if the token corresponds to a valid db user. Returns a 403 Forbidden if the access token provided is invalid. Returns a 400 Bad Request if the login token is not properly specified.

* /config_api/validate
	- Precondition: Successfully login using a valid access token. Pass that access token in this request in the same format as in /login
	- Function: Validates the passed session token against Flask's session variable (containing the token after successful login)
	- Postcondition: Returns a 200 OK Response if the token matches Flask's session token. Returns a 403 Forbidden if the token does not match Flask's session token. Returns a 400 Bad Request if the login token is not properly specified.