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
        fetch(url + '3000/22181').then(data => {
            return data.json();
        }).then(results => {
            this.setState({ cards: results });
            console.log(this.state.cards)
        })
    }

    updateCards(value) {

    }


    render() {
        return (
            <div className='Flowchart'>
                {this.state.cards.map(card => {
                    return <BudgetCard
                        className='BudgetCard'
                        category={card.category}
                        key={card.name}
                        name={card.name}
                        amount={card.amount}
                        budgetted={card.budgetted}
                        remaining={card.remaining}
                    />
                })}
            </div>
        )
    }
}

export default Flowchart;