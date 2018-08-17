import React, { Component } from 'react';
import './BudgetCard.css';
import Compare from './Compare';
import { TextField, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import PieContainer from './Pie';



class BudgetCard extends Component {

    render() {
        return (
            <div className='BudgetCard'>
                <div className={this.props.category}>
                    <h1>{this.props.name}</h1>
                    <h2>${this.props.budgetted}</h2>
                    <h2>${this.props.remaining}</h2>
                    <EditDialog num={this.props.num} updateCards={this.props.updateCards} name={this.props.name} />
                    <CompareDialog name={this.props.name} />

                </div>
            </div>
        )
    }
}

class EditDialog extends React.Component {
    state = {
        value: this.props.value,
        open: false,
    };


    onChange = (e) => {
        this.setState({ value: e.target.value })
    }

    handleClickOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    handleSubmit = () => {
        this.props.updateCards(this.props.num, this.state.value);
        this.handleClose();
    };

    render() {
        return (
            <div>
                <Button onClick={this.handleClickOpen}>Edit</Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                >
                    <DialogTitle id="form-dialog-title">Edit</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            Edit the value for {this.props.name} to see changes reflected in your budget.
            </DialogContentText>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="name"
                            label="New value"
                            fullWidth
                            onChange={this.onChange.bind(this)}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose.bind(this)} color="primary">
                            Cancel
            </Button>
                        <Button onClick={this.handleSubmit.bind(this)} color="primary">
                            Submit
            </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

class CompareDialog extends React.Component {
    state = {
        data: {},
        open: false,
    };

    /*componentDidMount() {
        fetch('').then(data => {
            return data.json();
        }).then(results => {
            this.setState({ data: results })
        })
    }*/

    handleClickOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    render() {
        return (
            <div>
                <Button onClick={this.handleClickOpen}>What are others doing?</Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                >
                    <DialogTitle id="form-dialog-title">What are others spending on {this.props.name}?</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            See how people like you are spending.
                        </DialogContentText>

                        {/*<PieChart
                            size={400}
                            innerHoleSize={200}
                            labels
                            data={this.state.data}
                        />*/}


                        {/*<PieContainer />*/}

                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Close
            </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}


export default BudgetCard;