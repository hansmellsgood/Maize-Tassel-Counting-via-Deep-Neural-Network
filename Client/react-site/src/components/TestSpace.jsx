import React, { useEffect, useState } from "react";
import axios from 'axios';
import '../App.css';
import DropZone from './DropZone.jsx';
import Visualization from './Visualization.jsx';

const TodosContext = React.createContext({
    todos: [], fetchTodos: () => { }
})

export default function Todos() {
    const [todos, setTodos] = useState([])
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8000/ping", {method:'GET'})
        const todos = await response.json()
        setTodos(todos.data1)
    }
    useEffect(() => {
        fetchTodos()
    }, [])

    return (
        <TodosContext.Provider value={{ todos, fetchTodos }}>       
            <div className="test">
                <div className="container-fluid col">
                    <div className="align-items-center content p-3">
                        <h2 className="font-weight-light">Test Space</h2>
                        <hr />
                        <DropZone />
                    </div>
                    <AddTodo />
                    {todos.map((todo) => (
                        <b> {todo.id} {todo.citem}<br /></b>
                    ))}
                    <Visualization />
                </div>
            </div>
        </TodosContext.Provider>
    )
}

function AddTodo() {
    const [item, setItem] = React.useState("")
    const { todos, fetchTodos } = React.useContext(TodosContext)

    const handleInput = event => {
        setItem(event.target.value)
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const newTodo = {
            "id": todos.length+1,
            "citem": item
        }
        fetch("http://localhost:8000/ping", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newTodo)
        }).then(fetchTodos)
    }
    return (
        <div>
        <form onSubmit={handleSubmit}>
            <input
                    pr="4.5rem"
                    type="text"
                    placeholder="Add a todo item"
                    aria-label="Add a todo item"
                    onChange={handleInput}        
            />
            <input type="submit" value="Submit"/>
        </form>
        </div>
    )
}

