import React from 'react';
import { connect } from 'react-redux';
import styled from 'styled-components';

import Sidebar from '../../components/Sidebar/Sidebar';
import Header from '../../components/Header/Header';
import Footer from '../../components/Footer/Footer';
import PipelineDash from '../../views/PipelineDash/PipelineDash';
import { logOut } from '../../redux/actions/userAuthActions/userAuthActions';

// Styles
const AdminWrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const Main = styled.div`
  flex: 5;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

class AdminPage extends React.Component {
  render() {
    const { logOutHandler } = this.props;
    const { userName } = this.props;
    return (
      <AdminWrapper>
        <Sidebar />
        <Main>
          <Header logOutHandler={logOutHandler} userName={userName} />
          <PipelineDash {...this.props} />
          <Footer />
        </Main>
      </AdminWrapper>
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
