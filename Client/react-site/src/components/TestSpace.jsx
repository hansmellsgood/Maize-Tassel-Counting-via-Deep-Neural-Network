import React, { useEffect, useState } from "react";
import axios from 'axios';
import '../App.css';
import DropZone from './DropZone.jsx';
import Visualization from './Visualization.jsx';
import ReactDOM from 'react-dom';

const TodosContext = React.createContext({
    todos: [], fetchTodos: () => { }
})

export default function Todos() {
    const [todos, setTodos] = useState([])
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8000/predict")
        const todos = await response.json()
        setTodos(todos.data1)
        const data = todos.file
        const Example = ({ data }) => <img src={`data:image/jpeg;base64,${data}`} />
        ReactDOM.render(<Example data={data} />, document.getElementById('container'))
    }
    useEffect(() => {
        fetchTodos()
    }, [])

    return (
        <TodosContext.Provider value={{ todos, fetchTodos }}>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.1.0/react.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.1.0/react-dom.min.js"></script>
            <div className="test">
                <div className="container-fluid col">
                    <div className="align-items-center content p-3">
                        <h2 className="font-weight-light">Test Space</h2>
                        <hr />
                        <DropZone />
                    </div>
                    {todos.map((todo, index) => (
                        <b> {todo.id} {todo.file_name} {todo.count} <br /></b>                   
                    ))}
                    <div id="container"></div>
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
        fetch("http://localhost:8000/predict", {
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

