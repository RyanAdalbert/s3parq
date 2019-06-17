import PipelineModal from './PipelineModal';

const setUp = (props = {}) => {
  const wrapper = shallow(<PipelineModal {...props} />);
  return wrapper;
};
function createTestProps(props) {
  return {
    show: true
  };
}

describe('<PipelineModal /> rendering', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = setUp();
  });

  it('should render without errors', () => {
    console.log(wrapper.debug());

    expect(wrapper.exists()).toBe(true);
  });
});
