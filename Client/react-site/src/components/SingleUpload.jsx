import React from 'react'
import DropZone from './DropZone.jsx';
import Visualization from './Visualization.jsx';
import '../App.css';


function SingleUpload() {
    return (
        <div className='upload'>
            <div className="container-fluid">
                <div className="vertical-align-top content top p-3">
                    <h2 className="font-weight-light">Single Upload</h2>
                    <hr/>
                        <DropZone />
                </div>
                <div className="vertical-align-top content bottom p-3">
                    <h2 className="font-weight-light">Visualization</h2>
                    <hr/>
                        <Visualization />
                </div>
            </div>
        </div>
    )
}
export default SingleUpload
