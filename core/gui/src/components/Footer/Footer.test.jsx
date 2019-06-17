import Footer from './Footer';

describe('<Footer /> rendering', () => {
  const wrapper = shallow(<Footer />);
  it('should render one <FooterSec/>', () => {
    expect(wrapper.find('p').length).toEqual(1);
  });
});
