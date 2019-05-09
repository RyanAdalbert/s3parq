import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import { loadState, saveState } from './utils/localStorage';

import './index.css';
import App from './app/App';
import rootReducer from './redux/reducers';
import userReducer from './redux/reducers/userReducer';

const presistedState = loadState();
const composeEnhancer = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  rootReducer,
  presistedState,
  composeEnhancer(applyMiddleware(thunk))
);

//Store Token
store.subscribe(() => {
  saveState({
    token: store.getState().userReducer.state.oAuthToken
  });
});

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
