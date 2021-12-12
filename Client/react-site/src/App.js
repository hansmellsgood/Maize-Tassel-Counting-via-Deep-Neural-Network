import React from "react";
import "./App.css";
import * as serviceWorker from "./serviceWorker";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {
  AboutUs,
  ContactUs,
  SideBarNav,
  SingleUpload
} from "./components";

function App() {
    return (
        <div className="App">
            <div className='wrapper'>
              <Router>
                <SideBarNav />
                <Routes>
                  <Route path="/" element={<AboutUs />} />
                  <Route path="/ContactUs" element={<ContactUs />} />
                  <Route path="/SingleUpload" element={<SingleUpload />} />
                </Routes>
              </Router>
            </div>   
        </div>
    )
}
serviceWorker.unregister();
export default App;