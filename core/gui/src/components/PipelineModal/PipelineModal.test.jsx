import PipelineModal from './PipelineModal';

function createTestProps(props) {
  return {
    Onhide: null,
    show: true,
    pipelineInfo: {
      name: 'bluth_profitability',
      brand: 'Cornballer',
      pharma_company: 'Sitwell',
      type: 'profitability',
      status: 'Active',
      description: 'This is a test description',
      run_freq: 'hourly',
      states: ['raw', 'not raw'],
      transformations: [
        'test',
        'extract_from_ftp',
        'extract_from_ftp',
        'extract_from_ftp',
        'extract_from_ftp',
        'extract_from_ftp'
      ]
    }
  };
}
const setUp = () => {
  const props = createTestProps();
  const wrapper = shallow(<PipelineModal {...props} />);
  return wrapper;
};

describe('<PipelineModal /> rendering', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = setUp();
  });

  it('should render without errors', () => {
    //console.log(wrapper.debug());
    expect(wrapper.exists()).toBe(true);
    //Possible way to test rendering more comepletely but would require more documentation to explain
    //expect(wrapper).toMatchSnapshot();
  });

  it('should render two lists: one for states and one for transforms', () => {
    //Example of further testing of the rendering
    expect(wrapper.find('ul').length).toBe(2);
  });
});

describe('<PipelineModal /> interactions', () => {
  //Replacing the passed in function with a mock that can be tracked
  const fnClick = jest.fn();
  const props = createTestProps();
  const wrapper = shallow(<PipelineModal {...props} onHide={fnClick} />);
  it('should register one click event upon exit', () => {
    wrapper.find('Button').simulate('click');
    expect(fnClick).toHaveBeenCalledTimes(1);
  });
});
