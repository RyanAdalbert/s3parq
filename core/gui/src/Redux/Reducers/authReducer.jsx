const authReducer = (state = {}, action) => {
  switch (action.type) {
    case 'STORE_TOKEN':
      return [
        state,
        {
          token: action.token
        }
      ];
    default:
      return state;
  }
};

export default authReducer;
