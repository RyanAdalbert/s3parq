import storeToken from './actions';
import { STORE_TOKEN } from './actions';

const initialState = {
  authToken: 0
};

function transformGui(state = initialState, action) {
  switch (action.type) {
    case STORE_TOKEN:
      return Object.assign({}, state, {
        storeToken: action.text
      });
    default:
      return state;
  }
}

export default transformGui;
