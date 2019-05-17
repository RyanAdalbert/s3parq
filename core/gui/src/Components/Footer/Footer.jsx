import React from 'react';
import styled from 'styled-components';

const FooterSec = styled.section`
  display: flex;
  justify-content: flex-end;
  width: 100%;
  background: #00a131;
  grid-area: ft;

  p {
    margin: 10px 50px;
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
