import { USER_OBJ } from '../Actions';

export default function UserAuth(state = 0, action) {
  switch (action.type) {
    case USER_OBJ:
      return [
        {
          name: 'Alec',
          token: '12345'
        }
      ];
    default:
      return state;
  }
}
