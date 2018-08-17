import React, { Component } from 'react';
import './App.css';
import Flowchart from './Flowchart';
import BasicForm from '../components/BasicForm'


class App extends Component {
  constructor() {
    super();
    this.state = {
      salary: 0,
      location: '',
      budgetEntered: 0
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit(e) {
    this.setState({ budgetEntered: 1 });
    console.log(this.state);

  }

  render() {
    return (
      <div className="App">
        <div className="header">
          <h1 className='part1'>cache</h1><h1 className='part2'>Flow</h1> <h2>Easy, quick budgets in a matter of seconds</h2>
        </div>
        <BasicForm
          salary={this.state.salary}
          location={this.state.location}
          budgetEntered={this.state.budgetEntered}
          handleChange={this.handleChange}
          handleSubmit={this.handleSubmit}
          updateCards={this.updateCards} />
        {this.state.budgetEntered && <Flowchart
          salary={this.state.salary}
          location={this.state.location}
          budgetEntered={this.state.budgetEntered}
          handleChange={this.handleChange}
          handleSubmit={this.handleSubmit}
          updateCards={this.updateCards} />}
      </div>
    );
  }
}

export default App;
