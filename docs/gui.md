# Core Gui Docs

## Set up

### Docker
As of right now you will need your local core repo to be inside a Repos directory in your root user directory. 

`Users/user/Repos/Core`

To start GUI container fun `script/dev_env --gui` from root core directory. This will start the docker container for the GUI and and start up an instace of the api, in a separate terminal window. 

### Dependancies
To install all necessary dependancies run `NPM install`, or `Yarn` if you are using Yarn.

___
## Redux and State Managment

We are using [Redux](https://github.com/reduxjs/redux) for our state managment along with [Redux-Thunk](https://github.com/reduxjs/redux-thunk) for async actions, and [Redux-Api-Middleware](https://github.com/agraboso/redux-api-middleware) for API calls.

You can use the [Redux DevTools](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en) google chrome extension to inspect the Redux Store.
___

## Other things of note

### Styling
We are handling styling with [Styled-Components](https://www.styled-components.com/).

### API
For questions about the API see API Documentation [here](https://github.com/IntegriChain1/core/blob/master/docs/flask_api.md).

### Create-React-App
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
