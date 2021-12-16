import React from 'react';
import '../App.css';
import Button from 'react-bootstrap/Button';

const result = () =>{
    var eCount = 'Count: 99';
    var eManualCount = 'Manual Count: 100';
    var eAccuracy = 'MHE: xxx MSE: xxx R2: xxx RMSE: xxx';

    
}

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
                <Button variant="secondary" size="sm" className="visualization-btn">Count Maize Tassels</Button>
                <Button variant="secondary" size="sm" className="visualization-btn">Density Map</Button>
                <Button variant="secondary" size="sm" className="visualization-btn">Dot Annotations</Button>
                <Button variant="secondary" size="sm" className="visualization-btn">Download Image</Button>

                <div className='single-results'>
                    <h5>Results</h5>
                    this.result.eCount
                </div>
            </div>
            
        </div>
    )
}

export default Visualization
