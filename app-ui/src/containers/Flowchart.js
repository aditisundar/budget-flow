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

const CARDS = fetch(url + '3000/22181')

class Flowchart extends Component {
    constructor() {
        super();
        this.updateCards = this.updateCards.bind(this);
    }

    updateCards(value) {
    }


    render() {
        return (
            <div className='Flowchart'>
                {CARDS.map(card => {
                    return <BudgetCard className='BudgetCard' category={card.category} key={card.name} name={card.name} amount={card.amount} />
                })}
            </div>
        )
    }
}

export default Flowchart;