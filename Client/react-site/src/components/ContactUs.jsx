import React from "react";
import '../App.css';
import Scroll from 'react-scroll';

function ContactUs() {
  return (
    <div className="contact">
      <Scroll.Element className="full-scroll-element" id="containerElement">
      <div className="container-fluid col">
        <div className="align-items-center content p-3">
          <h2 className="font-weight-light">Contact Us</h2>
          <hr/>
          <h5>E-mail</h5>
            <div className="body-text">
              <h6>Lim Gyu Hyun</h6><p>lim069@mymail.sim.edu.sg</p>
              <h6>Lim Wei Han</h6><p>whlim018@mymail.sim.edu.sg</p>
              <h6>Guok Mee Han</h6><p>mhguok001@mymail.sim.edu.sg</p>
              <h6>Chu Ki Min Clement</h6><p>kmcchua001@mymail.sim.edu.sg</p>
              <h6>Phua Zhon</h6><p>zphua001@mymail.sim.edu.sg</p>
          </div>
        </div>
      </div>
      </Scroll.Element>    
    </div>
  );
}

export default ContactUs;