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
            <p>
              We are a group of undergraduate Bachelor of Computer Science students at the University of Wollongong doing our Final Year Project.<br />
              The group members are:<br />
              Lim Gyu Hyun<br />
              Lim Wei Han<br />
              Guok Mee Han<br />
              Chu Ki Min Clement<br />
              Phua Zhon
            </p>
        </div>
      </div>    
      </Scroll.Element>
    </div>
  );
}

export default AboutUs;