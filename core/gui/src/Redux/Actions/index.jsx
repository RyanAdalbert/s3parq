//Store access token from google
export const storeToken = token => ({
  type: 'STORE_TOKEN',
  token
});

export const storeName = name => ({
  type: 'STORE_NAME',
  name
});
