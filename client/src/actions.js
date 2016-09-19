/**
 * @flow
 */
import { server } from './config';

export const REQUEST_ALL = 'REQUEST_ALL';
export const RECEIVE_ALL = 'RECEIVE_ALL'

"use strict"

export function requestAllUpdates(): Object {
  return {
    type: REQUEST_ALL,
  };
}

export const receiveAllPosts = (json: Object) => ({
  type: RECEIVE_ALL,
  items: json,
});

export const fetchAllUpdates = () => (dispatch: Function) => {
  dispatch(requestAllUpdates());
  return fetch(server + '/api')
    .then(response => response.json())
    .then(json => dispatch(receiveAllPosts(json)));
};
