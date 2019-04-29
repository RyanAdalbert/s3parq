import React from 'react';
import styled from 'styled-components';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import AdminPage from '../containers/AdminPage/AdminPage';
import LoginPage from '../containers/LoginPage/LoginPage';

// Styles
const AppContainer = styled.section`
  display: block;
`;

const App = () => (
  <AppContainer>
    <Router>
      <Route exact path="/" component={LoginPage} />
      <Route path="/admin" component={AdminPage} />
    </Router>
  </AppContainer>
);

export default App;
