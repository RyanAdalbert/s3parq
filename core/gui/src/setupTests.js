import React from 'react';
import Enzyme, { shallow, render, mount } from 'enzyme';
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { createSerializer } from 'enzyme-to-json';
import 'jest-enzyme';

//Changing the serializer from Jest to be from enzyme-to-json to provide
//better readability.
expect.addSnapshotSerializer(createSerializer({ mode: 'deep' }));
//
configure({ adapter: new Adapter() });

// Used to make Enzyme functions available throughout all test files
global.React = React;
global.shallow = shallow;
global.render = render;
global.mount = mount;
