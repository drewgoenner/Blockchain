import React from 'react';


export default function Display({chain, coins}) {


    if(chain.length) {

      return (
        <div className="list">
          
          {coins && <h3>Coins: {coins}</h3>}
          {chain.map(block => {
            if (block.transactions[0]) {
                return (
                <div className="blockWrapper" key={block.previous_hash}>
                  <p><b>Sender:</b> {block.transactions[0].sender}</p>
                  <p><b>Recipient:</b> {block.transactions[0].recipient}</p>
                  <p><b>Amount:</b> {block.transactions[0].amount}</p>
                </div>
              )
            }
          })}
        </div>
      )
    } else {
      return (
      <div>
        <p>Loading...</p>
        </div>
      )
    }
}