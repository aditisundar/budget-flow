import React, { Component } from 'react';
import BudgetCard from '../components/BudgetCard';
import './Flowchart.css';

const url = 'http://localhost:5000/';

const CARDS1 = [
    {
        category: "Expenses",
        name: "Restaurants",
        amount: 100,
    },
    {
        category: "Expenses",
        name: "Groceries",
        amount: 300,
    },
    {
        category: "Debt",
        name: "Movies",
        amount: 50,
    },
]

class Flowchart extends Component {
    constructor() {
        super();
        this.state = {
            cards: []
        }
        this.updateCards = this.updateCards.bind(this);
    }

    componentDidMount() {
        fetch(url + this.props.salary + '/' + this.props.location).then(data => {
            return data.json();
        }).then(results => {
            this.setState({ cards: results });
        })
    }

    componentWillReceiveProps(nextProps, prevProps) {
        if (nextProps !== prevProps) {
            fetch(url + this.props.salary + '/' + this.props.location).then(data => {
                return data.json();
            }).then(results => {
                this.setState({ cards: results });
            })
        }
    }

    updateCards(val, key) {
        fetch(url + 'update/' + this.props.salary + '/' + this.props.location + val + '/' + key).then(data => {
            return data.json();
        }).then(results => {
            console.log(results)
            this.setState({ cards: results });
        })
    }


    render() {
        var count = 0;
        return (
            <div className='Flowchart'>
                {this.state.cards.map(card => {
                    count++;
                    return <BudgetCard
                        className='BudgetCard'
                        category={card.category}
                        key={count}
                        num={count}
                        name={card.name}
                        amount={card.amount}
                        budgetted={card.budgetted}
                        remaining={card.remaining}
                        updateCards={this.updateCards}
                    />
                })
                }
            </div>
        )
    }
}

export default Flowchart;