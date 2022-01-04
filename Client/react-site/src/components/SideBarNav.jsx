import React from 'react'
import { ProSidebar, Menu, MenuItem, SubMenu, SidebarHeader, SidebarContent, SidebarFooter } from 'react-pro-sidebar';
import { NavLink } from 'react-router-dom';
import '../App.css';
import 'react-pro-sidebar/dist/css/styles.css';

function SideBarNav() {
    return (
        <ProSidebar>
            <SidebarHeader>
                <div className="sidebar-header">
                    <h3>Maize Tassel<br />Counting<br />Application</h3>
                </div>
            </SidebarHeader>
            <SidebarContent>
                <Menu>
                    <MenuItem>
                        <NavLink className="nav-link" to="/">
                            About Us
                        </NavLink>
                    </MenuItem>
                    <MenuItem>
                        <NavLink className="nav-link" to="/UserManual">
                            User Manual
                        </NavLink>
                    </MenuItem>
                    <MenuItem>
                        <NavLink className="nav-link" to="/SingleUpload">
                            Single Upload
                        </NavLink>
                    </MenuItem>
                    <MenuItem>
                        <NavLink className="nav-link" to="/MultipleUpload">
                            Multiple Upload
                        </NavLink>
                    </MenuItem>
                    <MenuItem>
                        <NavLink className="nav-link" to="/ContactUs">
                            Contact Us
                        </NavLink>
                    </MenuItem>         
                </Menu>
            </SidebarContent>
            <SidebarFooter>
                <p className='footerP'>Developed by the students from the project group FYP-21-S4-23<br/></p>
            </SidebarFooter>
        </ProSidebar>
    );
}

export default SideBarNav
