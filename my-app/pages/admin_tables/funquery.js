import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, Form, Container, Row, Col } from "react-bootstrap";
import Header from "../../component/header.js";
import Navs from "../../component/navs.js";
import axios from "axios";

class Index extends Component {
  handleLeave = () => {
    window.location.href = "../admin";
  };

  state = {
    apart_key: "",
    count: "",
    getApts: []
  };

  handleSubmitGetRoomCount = event => {
    event.preventDefault();

    const roomscount = {
      apart_key: this.state.apart_key
    };

    axios
      .post(`http://18.217.253.58:8000/get_rooms_count`, {
        roomscount,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(responserm => {
        this.setState({ apart_key: "" });
        this.setState({ count: responserm.data[0].num });
      });
  };

  handleOnClickgetAWPS = () => {
    const { input } = this.state;
    axios
      .get(`http://18.217.253.58:8000/get_apart_with_parking_and_study_room`, {
        method: "GET",
        headers: {
          "Access-Control-Allow-Origin": "*"
        }
      })
      .then(response => {
        this.setState({ getApts: response.data[0].apartments });
      });
  };

  handleChangeAK = event => {
    this.setState({ apart_key: event.target.value });
  };

  render() {
    return (
      <div>
        <Header></Header>
        <br />
        <Navs></Navs>
        <Container>
          <Row>
            <Col>
              <Form>
                <Form.Group controlId="aptk">
                  <Form.Label>Apartment Key:</Form.Label>
                  <Form.Control
                    type="email"
                    value={this.state.apart_key}
                    onChange={this.handleChangeAK}
                  />
                </Form.Group>
                <Button
                  variant="primary"
                  type="submit"
                  onClick={this.handleSubmitGetRoomCount}
                >
                  Get Room Count
                </Button>
              </Form>
              <br />
              <a>{this.state.count}</a>
              <br />
              <br />
            </Col>
            <Col>
              <Button
                variant="primary"
                onClick={this.handleOnClickgetAWPS}
              >
                Get Apartment with Parking and Study Room
              </Button>
              <br />
              {this.state.getApts.map(each => {
                return (
                  <div key={each}>
                    <a>{each}</a>
                    <br />
                  </div>
                );
              })}
            </Col>
          </Row>
          <Row>

            <Button variant="primary" onClick={this.handleLeave}>
              Back to Admin Main Page!
            </Button>
          </Row>
        </Container>
      </div>
    );
  }
}

export default Index;
