import Pipelines from './Pipelines';

describe('<Pipelines /> rendering', () => {
  const wrapper = shallow(<Pipelines />);
  it('should render a <TableContainer /> to display the pipelines', () => {
    expect(wrapper.find(TableContainer)).toHaveLength(1);
  });
});
