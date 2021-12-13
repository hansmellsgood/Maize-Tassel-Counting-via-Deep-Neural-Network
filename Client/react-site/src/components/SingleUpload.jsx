import React from 'react'
import DropZone from './DropZone.jsx';
import '../App.css';


function SingleUpload() {
    return (
        <div className='upload'>
            <div className="container-fluid">
                <div className="vertical-align-top content top p-3">
                    <h2 className="font-weight-light">Single Upload</h2>
                        <DropZone />
                    </div>
                <div className="bottom">
                </div>
            </div>
        </div>
    )
}
export default SingleUpload
