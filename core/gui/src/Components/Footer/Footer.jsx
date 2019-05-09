import React from 'react';
import styled from 'styled-components';

const FooterSec = styled.section`
  display: flex;
  justify-content: flex-end;
  background: #00a131;
  padding: 2px 5%;

  p {
    margin: 10px;
    color: #fff;
  }

  a {
    color: #fff;
    font-weight: 600;
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
