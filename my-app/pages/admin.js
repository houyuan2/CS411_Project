import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Button,
  Container,
  Row,
  Col,
} from "react-bootstrap";
import Header from "../component/header.js";
import Navs from "../component/navs.js";
import axios from "axios";

class Index extends Component {
  handleLeave = () => {
    window.location.href = "/index";
  };

  render() {
    return (
      <div>
        <Header></Header>
        <br />
        <Navs></Navs>
        <Container>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <Row>
            <Col></Col>
            <Col>
              <h2> Welcome Admin! </h2>
            </Col>
            <Col></Col>
          </Row>
          <br />
          <br />
          <br />
          <Row>
            <Col></Col>
            <Col>If you done, hit the buttom to leave!</Col>
            <Col></Col>
          </Row>
          <br />
          <Row>
            <Col></Col>
            <Col>
            <Button variant="primary" onClick={this.handleLeave}>
              Bye-Bye and see You Next Time!
            </Button>
              </Col>
            <Col></Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default Index;
