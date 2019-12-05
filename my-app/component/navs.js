import React, { Component, useState } from "react";
import {
  Nav,
} from "react-bootstrap";

class Navs extends Component {
  render() {
    return (
      <div>
        <Nav fill variant="tabs" defaultActiveKey="/admin">
          <Nav.Item>
            <Nav.Link href="/admin_tables/keyt">Key Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/aptft">Apartment Features Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/roomft">Room Features Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/distance"> Distance Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/rating"> Rating Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/prating"> People Rating Table</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href="/admin_tables/funquery"> Fun Query Demo</Nav.Link>
          </Nav.Item>
        </Nav>
      </div>
    );
  }
}

export default Navs;
