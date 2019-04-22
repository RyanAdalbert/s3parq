import React from 'react';
import { Switch, Route } from 'react-router-dom';
import styled from 'styled-components';

import AdminPage from '../Containers/AdminPage/AdminPage';
import LoginPage from '../Containers/LoginPage/LoginPage';

// Styles
const AppContainer = styled.section`
  display: block;
`;

const App = () => (
  <AppContainer>
    <Switch>
      <Route exact path="/" component={LoginPage} />
      <Route path="/admin" component={AdminPage} />
    </Switch>
  </AppContainer>
);

export default App;
