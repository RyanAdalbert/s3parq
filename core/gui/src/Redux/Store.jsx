import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

import rootReducer from './Reducers/RootReducer';

export default function Store(initialState = {}) {
  return createStore(rootReducer, initialState, applyMiddleware(thunk));
}
