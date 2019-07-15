import Header from './Header';

const setUp = (props = {}) => {
  const wrapper = shallow(<Header {...props} />);
  return wrapper;
};

describe('<Header /> rendering', () => {
  let wrapper;
  beforeEach(() => {
    wrapper = setUp();
  });

  it('should render without errors', () => {
    // console.log(wrapper.debug());

    expect(wrapper.exists()).toBe(true);
  });
});

describe('<Header/> interaction', () => {
  const mockOnClicked = jest.fn();
  beforeEach(() => {
    wrapper = setUp((onclick = { mockOnClicked }));
  });
});