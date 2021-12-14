import React, { useEffect, useState } from "react";
import '../App.css';



const TodosContext = React.createContext({
    todos: [], fetchTodos: () => { }
})

export default function Todos() {
    const [todos, setTodos] = useState([])
    const fetchTodos = async () => {
        const response = await fetch("http://localhost:8000/test")
        const todos = await response.json()
        setTodos(todos.data)
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
                    </div>
                {todos.map((todo) => (
                    <b>{todo.item}</b>
                ))}
                </div>
            </div>
        </TodosContext.Provider>
    )
}

function AddTest() {
    const [item, setItem] = React.useState("")
    const { todos, fetchTodos } = React.useContext(TodosContext)
}


