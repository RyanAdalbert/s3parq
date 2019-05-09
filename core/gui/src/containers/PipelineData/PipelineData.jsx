import React, { Component } from 'react';
import { connect } from 'react-redux';
import { compose } from 'redux';

import { fetchPipelines } from '../../redux/actions/pipelineActions/pipelineActions';

// Data container for the pipelines component, handles data for other pipeline

const PipelineData = WrappedComponent => {
  return class extends Component {
    componentDidMount() {
      const { dispatch, oAuthToken } = this.props;
      return dispatch(fetchPipelines(oAuthToken));
    }

    render() {
      return <WrappedComponent />;
    }
  };
};

const mapStateToProps = state => {
  return {
    oAuthToken: state.pipelineReducer.oAuthToken,
    isLoggedIn: state.pipelineReducer.isLoggedIn
  };
};

const composedPipelineData = compose(
  connect(mapStateToProps),
  PipelineData
);

export default composedPipelineData;
