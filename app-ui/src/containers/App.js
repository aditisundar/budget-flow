import React, { Component } from 'react';
import './App.css';
import Flowchart from './Flowchart';
import BasicForm from '../components/BasicForm'


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="header">
          <h1>BudgetFlow</h1> <h2>Easy, quick budgets in a matter of seconds</h2>
        </div>
        <BasicForm />
        <Flowchart />
      </div>
    );
  }
}

export default App;
