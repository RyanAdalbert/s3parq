const initialState = {
  authToken: 0
};

function userObj(state = initialState, action) {
  switch (action.type) {
    case 'STORE_TOKEN':
      return Object.assign({}, state, {
        storeToken: action.text
      });
    default:
      return state;
  }
}

export default userObj;
