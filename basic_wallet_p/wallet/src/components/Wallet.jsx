import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Wallet() {
    const [blocks, setBlocks] = useState([]);

    const fetchBlocks = () => {
        axios.get('http://localhost:5000/chain')
        .then(res => {
            setBlocks(res.data.chain)
        })
        .catch(err => {
            return err
        })
    }

    useEffect(() => fetchBlocks(), [])

    return (
        <div>

        </div>
    )
}