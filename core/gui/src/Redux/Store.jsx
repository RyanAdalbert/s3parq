import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

import reducer from './Reducers/index';

export default function Store(initialState = {}) {
  return createStore(reducer, initialState, applyMiddleware(thunk));
}
