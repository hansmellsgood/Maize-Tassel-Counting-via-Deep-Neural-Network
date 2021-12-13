import React from "react";
import '../App.css';

function ContactUs() {
  return (
    <div className="contact">
      <div className="container-fluid col">
        <div className="align-items-center content p-3">
          <h2 className="font-weight-light">Contact Us</h2>
          <hr/>
          <h5>Facebook</h5>
          <div className="body-text">
            <a href="/" target="_blank">Facebook Page (opens new empty page)</a>
          </div>
          <h5>YouTube</h5>
          <div className="body-text">
            <a href="/" target="_blank">YouTube Page (opens new empty page)</a>
          </div>
          <h5>E-mail</h5>
            <div className="body-text">
              <h6>Lim Gyu Hyun</h6><p>limgyuhyun@email.com</p>
              <h6>Lim Wei Han</h6><p>limweihan@email.com</p>
              <h6>Guok Mee Han</h6><p>guokmeehan@email.com</p>
              <h6>Chu Ki Min Clement</h6><p>chukiminclement@email.com</p>
              <h6>Phua Zhon</h6><p>phuazhon@email.com</p>
          </div>
        </div>
      </div>    
    </div>
  );
}

export default ContactUs;