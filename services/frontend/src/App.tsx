import { useState, useEffect } from 'react'

// import api from './api'
import axios from 'axios'


export default function App() {
    const [ count, setCount ] = useState(0)

    const fetchCount = async (): Promise<number> => {
        // let response = await api.get("/requests")
        let response = await axios.get("/api/requests")
        // console.log("API", response.data)
        const data = response.data
        return data.count
    }

    useEffect(() => {
        const loadCount = async () => {
            const count = await fetchCount()
            setCount(count)
        }
        loadCount()
    }, [])

    return (
        <div>
            <h1>Request count: {count}</h1>
            <p>Anton</p>
            <p>Anton</p>
            {/* <p>{process.env.REACT_PUBLIC_ANTON}</p> */}
        </div>
    )
}
