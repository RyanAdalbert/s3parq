import PipelineRow from './PipelineRow';

// const setUp = (props={}) => {
//     const wrapper = shallow(<PipelineRow {...props}/> );
//     return wrapper;
// };

describe('<PipelineRow/> Rendering', () => {
  const wrapper = shallow(<PipelineRow pipelines={[]} />);
  it('should render PipelineRow', () => {
    console.log(wrapper.debug());
    expect(wrapper.length).toBe(1);
  });
});
