import React, {useState} from 'react';
import '../App.css';
import Button from 'react-bootstrap/Button';
import DisplayTest from './DisplayTest';

function Visualization() {
    const [display, setDisplay] = useState({
        count: 0,
        //date : new Date()
    });
    const countBtn = () => {
        setDisplay(previousState => {
            return { ...previousState, count: 999}
    })};
    const downloadBtn = () => {
        
    };
    const densityMap = () => {

    };

    return (
        <div className='visualization contain-box row'>
            <div className='col img-right'>
                <img 
                    class="img-fluid mb-lg-10"
                    src="http://placehold.it/1024x768"
                    alt=""
                />
            </div>
            <div className='col'>
                <div className='btn group p-0'>
                    <Button variant="secondary" size="sm" className="visualization-btn" onClick={countBtn}>Count Maize Tassels</Button>
                    <Button variant="secondary" size="sm" className="visualization-btn" onClick={densityMap}>Density Map</Button>
                    <Button variant="secondary" size="sm" className="visualization-btn" onClick={downloadBtn}>Download Image</Button>
                </div>
                <div className='single-results pt-3'>
                    <h5>Results</h5>
                    <div className='resultsDisplay'>
                        <p>Count: {display.count.toString()}</p>    
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Visualization;
