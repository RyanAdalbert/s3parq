import { createStore } from 'redux';
import transformGui from './reducers';

const store = createStore(transformGui);

export default store;
