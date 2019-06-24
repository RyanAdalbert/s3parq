import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import * as actions from './pipleineActions';
import pipelineConstants from './pipelineActions';

const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

describe('pipeline actions', () => {
  afterEach(() => {
    fetchMock.restore();
  });

  it('creates FETCH_TODOS_SUCCESS when fetching todos has been done', () => {
    fetchMock.getOnce('', {
      body: { pipelines: ['do somthing'] },
      headers: { 'content-type': 'application/json' }
    });

    const text = 'Finish docs';

    const expectedAction = {
      type: types.ADD_TODO,
      text
    };
    expectedAction(store.getActions()).toEqual(expectedAction);
  });
});
