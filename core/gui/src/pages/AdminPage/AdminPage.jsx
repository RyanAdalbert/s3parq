import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import styled from 'styled-components';
import { Router, Route } from 'react-router-dom';

import Sidebar from '../../components/Sidebar/Sidebar';
import Header from '../../components/Header/Header';
import Footer from '../../components/Footer/Footer';
import PipelineIndex from '../../views/PipelineIndex/PipelineIndex';
import CreatePipeline from '../../views/CreatePipeline/CreatePipeline';
import { logOut } from '../../redux/actions/userAuthActions/userAuthActions';
import history from '../../utils/history';

// Styles
const AdminWrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const Main = styled.div`
  display: flex;
  flex: 5;
  width: 100%;
  height: 100vh;
  flex-direction: column;
`;

const routes = [
  // PipelineIndex
  {
    path: '/admin/pipelineindex',
    exact: true,
    main: () => <PipelineIndex />
  },
  // CreatePipeline
  {
    path: '/admin/createpipeline',
    main: () => <CreatePipeline />
  }
];

class AdminPage extends React.Component {
  render() {
    const { logOutHandler } = this.props;
    const { userName } = this.props;
    return (
      <Router history={history}>
        <AdminWrapper>
          <Sidebar />

          <Main>
            <Header logOutHandler={logOutHandler} userName={userName} />
            <Route
              path={routes[0].path}
              exact={routes[0].exact}
              component={routes[0].main}
              {...this.props}
            />
            <Route
              path={routes[1].path}
              exact={routes[1].exact}
              component={routes[1].main}
            />
            <Footer />
          </Main>
        </AdminWrapper>
      </Router>
    );
  }
}

const mapStateToProps = state => {
  return {
    oAuthToken: state.userReducer.oAuthToken,
    userName: state.userReducer.userName
  };
};

const mapDispatchToProps = dispatch => {
  return {
    logOutHandler: () => dispatch(logOut())
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AdminPage);

AdminPage.propTypes = {
  userName: PropTypes.string,
  logOutHandler: PropTypes.func
};
