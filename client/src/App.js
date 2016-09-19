/**
 * @flow
 */

import React, { Component, PropTypes } from 'react';
import dateformat from 'dateformat';
import { connect } from 'react-redux';
import { List } from 'immutable';
import { fetchAllUpdates } from './actions';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  static propTypes = {
    isFetching: PropTypes.bool.isRequired,
    items: PropTypes.objectOf(List),
    dispatch: PropTypes.func.isRequired
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(fetchAllUpdates());
  }

  render() {
    const { isFetching, items } = this.props;

    if (isFetching) {
      return <div className="loader" />;
    }

    const updates = items.map((item, key) => {
      const time = item.entry && item.entry[0].time;
      const date = new Date(time * 1000);
      return (
        <div key={key}>
          <div>
            {dateformat(date, 'dddd mmmm dS, h:MM:ss TT')}
          </div>
          <pre>
            {JSON.stringify(item, null, '  ')}
          </pre>
        </div>
      );
    }).toArray();
    console.log(updates);
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Webhooks</h2>
        </div>

        <div className="App-main">
          {updates}
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => {
  const {
    isFetching,
    items,
  } = state;
  return {
    isFetching,
    items,
  };
}

export default connect(mapStateToProps)(App);
