import React from 'react'
import DropZoneM from './DropZoneM.jsx';
import Visualization from './Visualization.jsx';
import '../App.css';
import Scroll from 'react-scroll';


function MultipleUpload() {
    return (
        <div className='m-upload'>
            <Scroll.Element className="full-scroll-element" id="containerElement">
                <DropZoneM />
            </Scroll.Element>
        </div>
    )
}
export default MultipleUpload