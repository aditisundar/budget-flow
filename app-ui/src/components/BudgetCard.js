import React, { Component } from 'react';
import './BudgetCard.css';
import { TextField, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';



class BudgetCard extends Component {

    render() {
        return (
            <div className='BudgetCard'>
                <div className={this.props.category}>
                    <h1>{this.props.name}</h1>
                    <h2>${this.props.amount}</h2>
                    <Edit updateCards={this.props.updateCards} name={this.props.name} />
                    <Button >What others are doing</Button>

                </div>
            </div>
        )
    }
}

class Edit extends React.Component {
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
        this.props.updateCards(this.state.value);
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
                        <Button onClick={this.handleClose} color="primary">
                            Cancel
            </Button>
                        <Button onClick={this.handleClose} color="primary">
                            Subscribe
            </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}


export default BudgetCard;