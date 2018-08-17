import React, { Component } from 'react';
import './BasicForm.css';
import { TextField, Button } from '@material-ui/core';


class BasicForm extends Component {
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
            <div className="BasicForm">
                <form>
                    <p>I live in
                    <TextField
                            name="location"
                            placeholder="22181"
                            onChange={this.handleChange}
                            margin="normal"
                        />
                        and I make $
                    <TextField
                            name="salary"
                            placeholder={30000}
                            onChange={this.handleChange}
                            margin="normal"
                        />
                        a month.
                         <Button variant="contained" color="primary" className='Submit' onClick={this.handleSubmit} onSubmit={this.handleSubmit}>Go</Button>
                    </p>


                </form>
            </div>
        );
    }
}

export default BasicForm;
