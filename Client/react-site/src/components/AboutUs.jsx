import React from "react";
import '../App.css';


function AboutUs() {
  return (
    <div className="about">
      <div className="container-fluid col">
        <div className="row align-items-center content p-3">
          <h2 className="font-weight-light">About Us</h2>
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
    </div>
  );
}

export default AboutUs;