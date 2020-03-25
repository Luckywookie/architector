import '@babel/polyfill';

import React from 'react';
import {
  Route,
  BrowserRouter as Router,
  Switch,
} from 'react-router-dom';

import { BaseView } from './views/base/BaseView';

export const App = () => (
  <Router basename="/main">
    <div>
      <Switch>
        <Route exact path="/" component={BaseView} />
      </Switch>
    </div>
  </Router>
);
