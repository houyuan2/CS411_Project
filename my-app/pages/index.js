import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Container,
  Row,
  Col,
  Image,
  Badge,
  ListGroup
} from "react-bootstrap";
import Header from "../component/header.js";
import myImg from "../component/Logo.png";
import img from "../component/background.jpg";

class Index extends Component {
  styling = {
    backgroundImage: `url('${img}')`,
    backgroundRepeat: "no-repeat",
    backgroundSize: "1450px 710px"
  };
  render() {
    //console.log("count: ", this.state.count);
    return (
      <div style={this.styling}>
        <Header></Header>
        <Container>
          <Row>
            <br />
          </Row>
          <Row>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <Col>
              <Image src={myImg} rounded width={100} />
            </Col>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <Col></Col>
          </Row>
          <Row>
            <Badge variant="secondary">Intro:</Badge>
          </Row>
          <Row>
            <br />
            <ListGroup as="ul">
              <ListGroup.Item as="li">
                Here at Matcha, we are driven by a single goal; to do our part
                in making the world a better place for all. Our decision-making
                process is informed by comprehensive empirical studies and
                high-quality data evaluation. We strive to build productive
                relationships and make a positive impact on all of our pursuits.
              </ListGroup.Item>
            </ListGroup>
          </Row>
          <Row>
            <br />
          </Row>
          <Row>
            <Badge variant="secondary">About Us:</Badge>
          </Row>
          <Row>
            <br />
          </Row>
          <Row>
            <ListGroup as="ul">
              <ListGroup.Item as="li">KuiHua Liu</ListGroup.Item>
              <ListGroup.Item as="li">Shuncheng Liu</ListGroup.Item>
              <ListGroup.Item as="li">Houyuan Sha</ListGroup.Item>
              <ListGroup.Item as="li">Hao Yuan</ListGroup.Item>
            </ListGroup>
          </Row>
          <Row>
            <br />
          </Row>
          <Row>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <a href="/features" className="btn btn-info" role="button">
              Start your journey with Matcha
            </a>
            <Col></Col>
            <Col></Col>
            <Col></Col>
            <Col></Col>
          </Row>
        </Container>
        <br />
        <br />
        <br />
      </div>
    );
  }
}

export default Index;
