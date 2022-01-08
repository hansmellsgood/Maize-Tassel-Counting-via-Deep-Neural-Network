import React from "react";
import '../App.css';
import Accordion from "react-bootstrap/Accordion";
import Scroll from 'react-scroll';

function UserManual() {
  return (
    <div className="manual w-100 h-100">
        <Scroll.Element className="full-scroll-element" id="containerElement">
        <div className="container-fluid">
            <div className="align-items-center content p-3">
                <h2 className="font-weight-light">User Manual</h2>
                <hr/>
                <div className="accordion-dimensions">
                    <Accordion>
                    <Accordion.Item eventKey="0">
                        <Accordion.Header><h6>Instructions for Single Image</h6></Accordion.Header>
                        <Accordion.Body>
                            <h6>Step 1 - Selection and Upload</h6>
                            <p>
                                Under Single Upload, click within the border box to select the intended file or drag and drop the file for uploading. Please only select one JPEG format file.<br /> 
                                The information of the selected image will be displayed on the right side of the border box, you may click on the file name in blue to preview or click on the X button in red to remove the file from selection.<br />
                                After selection please click on the upload button at the bottom of the border box.
                            </p>
                            <h6>Step 2 - Visualization and Results</h6>
                            <p>
                                After the upload button has been clicked, a message will appear with the progress bar and an X button on the top right side of the screen. Click on the X button to return back to the page.<br /> 
                                After a few short moments the uploaded image will appear under the Visualization display area with the file name and predicted count displayed under Results.
                            </p>
                            <h6>Step 3 - Enlarge or Toggle Image</h6>
                            <p>
                                After the image has been displayed under the Visualization display area, clicking on the image will cause it to appear in an enlarged size with the X button on the top right to return back to the page once clicked.<br />
                                Clicking on the Toggle Visualization button will switch the display between the original uploaded image and the processed visualization image (Density Map for Regression Model). 
                            </p>    
                        </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="1">
                        <Accordion.Header><h6>Instructions for Multiple Images</h6></Accordion.Header>
                        <Accordion.Body>
                        <h6>Step 1 - Selection and Upload</h6>
                            <p>
                                Under Multiple Upload, click within the border box to select the intended files or drag and drop the files for uploading. The application will accept multiple JPEG format files.<br /> 
                                The information of the selected images will be displayed on the right side of the border box, you may click on the file names in blue to preview or click on the X button in red to remove the file from selection.<br />
                                After selection please click on the upload button at the bottom of the border box.
                            </p>
                            <h6>Step 2 - Visualization and Results</h6>
                            <p>
                                After clicking on the upload button, a message will appear with the progress bar and an X button on the top right side of the screen. Click on the X button to return back to the page.<br /> 
                                After a few moments the uploaded images will appear under the Visualization display area and organised according to each uploaded image with the file name and predicted count displayed.
                            </p>
                            <h6>Step 3 - Enlarge or Toggle Images</h6>
                            <p>
                                After the images has been displayed under the Visualization display area, clicking on the image will cause it to appear in an enlarged size with the X button on the top right to return back to the page once clicked.<br />
                                Clicking on the Toggle Visualization button will switch the displays between the original uploaded images and the processed visualization images (Density Map for Regression Model). 
                            </p>    
                        </Accordion.Body>
                    </Accordion.Item>
                    </Accordion>
                </div>
            </div>
        </div> 
        </Scroll.Element>
    </div>
    
  );
}

export default UserManual;