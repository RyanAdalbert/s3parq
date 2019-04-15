import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';

import Routes from 'Routes/Routes.jsx';

class Sidebar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      width: window.innerWidth
    };
  }

  componentDidMount() {
    this.updateDimensions();
    window.addEventListener('resize', this.updateDimensions.bind(this));
  }

  updateDimensions() {
    this.setState({ width: window.innerWidth });
  }

  activeRoute(routeName) {
    return this.props.location.pathname.indexOf(routeName) > -1 ? 'active' : '';
  }

  render() {
    return (
      <div>
        <div>
          <a
            href="https://www.creative-tim.com"
            className="simple-text logo-mini"
          >
            <div>
              <img src={logo} alt="logo_image" />
            </div>
          </a>
        </div>
        <div>
          <ul>
            {this.state.width <= 991 ? <HeaderLinks /> : null}
            {Routes.map((prop, key) => {
              if (!prop.redirect)
                return (
                  <li key={key}>
                    <NavLink to={prop.path}>
                      <p>{prop.name}</p>
                    </NavLink>
                  </li>
                );
              return null;
            })}
          </ul>
        </div>
      </div>
    );
  }
}

export default Sidebar;
