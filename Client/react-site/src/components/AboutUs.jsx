import React from "react";
import '../App.css';
import Scroll from 'react-scroll';

function AboutUs() {
  return (
    <div className="about">
      <Scroll.Element className="full-scroll-element" id="containerElement">
      <div className="container-fluid col">
        <div className="align-items-center content p-3">
          <h2 className="font-weight-light">About Us</h2>
          <hr/>
              <h6>Welcome to the Maize Tassel Counting Application website (MaxiMaize), We are a group of  final year students from the Bachelor in Computer Science program <br />specializing in Big Data at Singapore Institute of Management (SIM GE) - University of Wollongong, NSW AU.<br />
              </h6>
              <br />
              <h6>The team members of FYP-21-S4-23</h6>
              <p>Lim Gyu Hyun<br />
                Lim Wei Han<br />
                Guok Mee Han<br />
                Chu Ki Min Clement<br />
                Phua Zhon</p>
              <h6>Project</h6>
              <p>Accurate counting of maize tassels is important for monitoring the growth status of maize plants. In this project, the group is expected to develop a robust deep neural network model<br />
              to accurately count maize tassels in order to free humans (farmers) from intensive manual work of counting maize tassels.</p>
              <h6>Goal</h6>
              <p>For the end-product we aim to create a web-based application, with the primary use to automate the counting of maize tassels based on the models we are developing.<br />
              We plan to provide a solution for farmers in automating the counting of maize tassels in the field. The farmers are also able to access the application from anywhere as long<br /> 
              as they have access to the internet and also be able to upload the images of the field.</p>
        </div>
      </div>    
      </Scroll.Element>
    </div>
  );
}

export default AboutUs;