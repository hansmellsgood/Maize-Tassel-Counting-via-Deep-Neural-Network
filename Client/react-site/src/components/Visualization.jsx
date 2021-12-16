import React from 'react';
import '../App.css';
import Button from 'react-bootstrap/Button';
import DisplayTest from './DisplayTest';

function Visualization() {
    
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
                    <Button variant="secondary" size="sm" className="visualization-btn">Count Maize Tassels</Button>
                    <Button variant="secondary" size="sm" className="visualization-btn">Density Map</Button>
                    <Button variant="secondary" size="sm" className="visualization-btn">Dot Annotations</Button>
                    <Button variant="secondary" size="sm" className="visualization-btn">Download Image</Button>
                </div>
                <div className='single-results pt-3'>
                    <h5>Results</h5>
                    <DisplayTest />
                </div>
            </div>
            
        </div>
    )
}

export default Visualization;
