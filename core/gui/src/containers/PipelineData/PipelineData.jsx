import React, { Component } from 'react';
import PropTypes, { func } from 'prop-types';
import { connect } from 'react-redux';
import { compose } from 'redux';

import { fetchPipelines } from '../../redux/actions/pipelineActions/pipelineActions';
import { fetchFilters } from '../../redux/actions/filterActions/filterActions';

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
    pipelines: Object.values(state.pipelineReducer.pipelines),
    expanded: state.pipelineReducer.expanded,
    filters: state.filterReducer.fetchFilters.filters,
    setFilters: state.filterReducer.setFilters,
    brand: state.filterReducer.brand,
    company: state.filterReducer.company,
    type: state.filterReducer.type,
    status: state.filterReducer.status,
    filtersFetched: state.filterReducer.fetched,
    pipelinesFetched: state.pipelineReducer,
    modalShow: state.pipelineReducer.modalShow
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
