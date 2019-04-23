import { createStore } from 'redux';
import transformGui from './reducer';

import { storeToken } from './actions';

const store = createStore(transformGui);

console.log(store.getState());

export default store;
