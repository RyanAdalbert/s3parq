import React from 'React';
import App from './App';
import { shallow } from 'enzyme';

const wrapper = shallow(<App />);

it('renders', () => {
  expect(wrapper.exists()).toBe(true);
});
