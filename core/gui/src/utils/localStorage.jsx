export const loadState = () => {
  try {
    const serializedState = localStorage.getItem('token');
    if (serializedState === null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch (err) {
    return undefined;
  }
};

export const saveState = state => {
  try {
    const serializedState = state;
    localStorage.setItem('token', serializedState);
  } catch (err) {
    //Ignore write errors.
  }
};
