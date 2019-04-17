import React from 'React';
import { shallow, mount, render } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

import Login from './Login';

configure({ adapter: new Adapter() });
const wrapper = shallow(<Login />);
it('Renders Google Login Button', () => {
  expect(wrapper.find(<GoogleLogin />));
});
