import React from 'react';
import { useState } from 'react';

function DisplayTest() {
    const [display, setDisplay] = useState({
        count: 999,
        Mcount: 999,
        mhe: "mhe value",
        mse: "mse value",
        r2: "r2 value",
        rmse: "rmse value",
        //date : new Date()
      });
      
    const updateCount = () => {
        setDisplay(previousState => {
            return { ...previousState, count: 0}
    })};

    const updateMCount =() => {
        setDisplay(previousState=> {
            return{ ...previousState, Mcount: 0}
    })};

    const downloadFile =() => {
        
    }


    return (

        <div className='resultsDisplay'>
            <p>Count: {display.count.toString()}</p> 
            <button type="button"onClick={updateCount}>Update Count</button>
            <button type="button"onClick={updateMCount}>Update MCount</button>

            
            
        </div>
    )
}

export default DisplayTest;
