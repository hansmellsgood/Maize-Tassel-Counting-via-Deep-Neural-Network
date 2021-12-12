import React from 'react'
import DropZone from './DropZone.jsx';
import '../App.css';


function SingleUpload() {
    return (
        <div className="container-fluid">
            <div className="row align-items-center content top p-3">
                <DropZone />
            </div>
            <div className="bottom">

            </div>
        </div>
    )
}
export default SingleUpload
