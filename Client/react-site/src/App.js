import React from "react";
import "./App.css";
import * as serviceWorker from "./serviceWorker";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {
  AboutUs,
  UserManual,
  ContactUs,
  SideBarNav,
  SingleUpload,
  TestSpace
} from "./components";

function App() {
    return (
        <div className="App">
            <div className='wrapper'>
              <Router>
                <SideBarNav />
                <Routes>
                  <Route path="/" element={<AboutUs />} />
                  <Route path="/UserManual" element={<UserManual />} />
                  <Route path="/ContactUs" element={<ContactUs />} />
                  <Route path="/SingleUpload" element={<SingleUpload />} />
                  <Route path="/TestSpace" element={<TestSpace />} />
                </Routes>
              </Router>
            </div>
            
        </div>
    )
}
serviceWorker.unregister();
export default App;