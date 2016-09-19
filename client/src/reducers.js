  /**
 * @flow
 */

import { List } from 'immutable';
import {
  REQUEST_ALL,
  RECEIVE_ALL
} from './actions.js';

"use strict"

export function webhooksUpdates(
  state: Object = {
    isFetching: false,
    items: List(),
  },
  action: Object,
): Object {
  switch (action.type) {
    case REQUEST_ALL:
      return {
        ...state,
        isFetching: true,
      };
    case RECEIVE_ALL:
      return {
        ...state,
        items: List(action.items),
        isFetching: false,
      }

    default:
      return state;
  }
}

export default webhooksUpdates;
