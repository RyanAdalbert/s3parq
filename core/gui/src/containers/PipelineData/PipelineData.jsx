import React, { Component } from 'react';
import PropTypes, { func } from 'prop-types';
import { connect } from 'react-redux';
import { compose } from 'redux';

import { fetchPipelines } from '../../redux/actions/pipelineActions/pipelineActions';
import { fetchFilters } from '../../redux/actions/filtersActions/filtersActions';

// Data container for the pipelines component, handles data for the pipelines component
const PipelineData = WrappedComponent => {
  return class extends Component {
    componentDidMount() {
      const { dispatch, oAuthToken } = this.props;
      dispatch(fetchFilters(oAuthToken));
      dispatch(fetchPipelines(oAuthToken));
    }

    render() {
      return <WrappedComponent {...this.props} />;
    }
  };
};

const mapStateToProps = state => {
  return {
    oAuthToken: state.userReducer.oAuthToken,
    isLoggedIn: state.pipelineReducer.isLoggedIn,
    pipelines: state.pipelineReducer.pipelines,
    expanded: state.pipelineReducer.expanded,
    filters: state.filtersReducer.filters,
    filtersFetched: state.filtersReducer.fetched,
    pipelinesFetched: state.pipelineReducer
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
