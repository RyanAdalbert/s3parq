import React from 'react';
import { connect } from 'react-redux';
import { Route, Redirect, withRouter } from 'react-router-dom';

const PrivateRoute = ({ component, auth, ...rest }) => {
  let ComponentToRender = component;

  return (
    <Route
      {...rest}
      render={props =>
        auth === true ? (
          <ComponentToRender {...props} />
        ) : (
          <Redirect to={{ pathname: '/', state: { from: props.location } }} />
        )
      }
    />
  );
};

const mapStateToProps = (state, ownProps) => ({
  auth: state.userReducer.isLoggedIn
});
export default withRouter(connect(mapStateToProps)(PrivateRoute));
