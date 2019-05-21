import React, { Component } from 'react';
import PropTypes, { func } from 'prop-types';
import { connect } from 'react-redux';
import { compose } from 'redux';

import { fetchPipelines } from '../../redux/actions/pipelineActions/pipelineActions';

// Data container for the pipelines component, handles data for the pipelines component
const PipelineData = WrappedComponent => {
  return class extends Component {
    componentDidMount() {
      const { dispatch, oAuthToken } = this.props;
      console.log(oAuthToken);
      dispatch(fetchPipelines(oAuthToken));
    }

    render() {
      return <WrappedComponent {...this.props} />;
    }
  };
};

const mapStateToProps = state => {
  return {
    oAuthToken: state.pipelineReducer.oAuthToken,
    isLoggedIn: state.pipelineReducer.isLoggedIn,
    pipelines: state.pipelineReducer.pipelines,
    expanded: state.pipelineReducer.expanded
  };
};

const composedPipelineData = compose(
  connect(mapStateToProps),
  PipelineData
);

export default composedPipelineData;

PipelineData.propTypes = {
  dispatch: func,
  oAuthToken: PropTypes.string
};
