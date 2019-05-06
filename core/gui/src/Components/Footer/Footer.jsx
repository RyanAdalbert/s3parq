import React from 'react';
import styled from 'styled-components';

const FooterSec = styled.section`
  display: flex;
  justify-content: flex-end;
  background: #ccc;
  padding: 2px 5%;

  p {
    margin: 10px;
  }

  a {
    color: #fff;
  }
`;

const Footer = () => (
  <FooterSec>
    <p>
      &copy; {new Date().getFullYear()}{' '}
      <a href="https://www.integrichain.com/">IntegriChain</a> Inc. All Rights
      Reserved.
    </p>
  </FooterSec>
);

export default Footer;
