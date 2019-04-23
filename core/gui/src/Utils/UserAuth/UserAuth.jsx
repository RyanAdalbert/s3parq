// Function that Authorizes Google Response
import { storeToken } from '../../Redux/Actions/index';

export default function userAuth(responseGoogle, dispatch) {
  dispatch(storeToken(responseGoogle.accessToken));
}
