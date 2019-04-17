import React from 'react';
import styled from 'styled-components';

const FooterSec = styled.section`
  display: flex;
  justify-content: flex-end;
`;

const Footer = () => (
  <FooterSec>
    <p>
      &copy; {new Date().getFullYear()}{' '}
      <a href="https://www.integrichain.com/">IntegriChain</a> Incorporated. All
      Rights Reserved.
    </p>
  </FooterSec>
);

export default Footer;
