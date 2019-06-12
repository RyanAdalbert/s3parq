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
    console.log(wrapper.debug());

    expect(wrapper.exists()).toBe(true);
  });
});

describe('<Header/> interaction', () => {
  let wrapper;
  const mockOnClicked = jest.fn();
  beforeEach(() => {
    wrapper = setUp((onclick = { mockOnClicked }));
  });

  it('should call the onClick function when [Log out] is clicked', () => {
    const component = wrapper.find('log-out');
    console.log(component.debug());
    expect(wrapper.find('log-out').simulate('clicked')).toHaveBeenCalledTimes(
      1
    );
  });
});
