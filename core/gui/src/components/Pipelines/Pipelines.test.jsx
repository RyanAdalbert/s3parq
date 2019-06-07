import Pipelines from './Pipelines';

describe('<Pipelines /> rendering', () => {
  const wrapper = shallow(<Pipelines />);
  it('should render a <Should render a pipeline component /> to display the pipelines', () => {
    expect(wrapper.exists()).toBe(true);
  });
});
