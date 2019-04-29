export const INITIAL_STATE = {
  token: ''
};
const authReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case 'GOOGLE_LOGIN_RESPONSE':
      return {
        state,
        token: action.token
      };
    default:
      return state;
  }
};

export default authReducer;
