import React, { Component } from 'react';
import './BasicForm.css';
import { TextField, Button } from '@material-ui/core';


class BasicForm extends Component {

    render() {
        return (
            <div className="BasicForm">
                <form>
                    <p>I live in
                    <TextField
                            name="location"
                            placeholder="22181"
                            onChange={this.props.handleChange}
                            margin="normal"
                        />
                        and I make $
                    <TextField
                            name="salary"
                            placeholder={30000}
                            onChange={this.props.handleChange}
                            margin="normal"
                        />
                        a month.
                         <Button variant="contained" color="primary" className='Submit' onClick={this.props.handleSubmit} onSubmit={this.props.handleSubmit}>Go</Button>
                    </p>


                </form>
            </div>
        );
    }
}

export default BasicForm;
