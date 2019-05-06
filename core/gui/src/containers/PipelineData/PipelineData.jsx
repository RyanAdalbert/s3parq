import React, { Component } from 'react';

export default function PipelineData(WrappedComponent) {
  return class extends Component {
    render() {
      return <WrappedComponent />;
    }
  };
}
