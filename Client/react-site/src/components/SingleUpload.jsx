import React from 'react'
import DropZone from './DropZone.jsx';
import Visualization from './Visualization.jsx';
import '../App.css';
import Scroll from 'react-scroll';


function SingleUpload() {
    return (
        <div className='upload'>
            <Scroll.Element className="full-scroll-element" id="containerElement">
                <DropZone />
            </Scroll.Element>
        </div>
    )
}
export default SingleUpload
