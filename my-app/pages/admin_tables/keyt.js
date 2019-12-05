import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Button,
  Navbar,
  Nav,
  Form,
  FormControl,
  InputGroup,
  Container,
  Row,
  Col,
  Image,
  Badge,
  ListGroup
} from "react-bootstrap";
import Header from "../../component/header.js";
import Navs from "../../component/navs.js";
import axios from "axios";

class Index extends Component {
  handleLeave = () => {
    window.location.href = "../admin";
  };

  state = {
    apt_addi: "",
    apt_namei: "",
    room_keyd: "",
    apt_nameu: "",
    room_keyu: ""
  };
  //insert key table
  handleChangeANI = event => {
    this.setState({ apt_namei: event.target.value });
  };


  handleSubmitInsert = event => {
    event.preventDefault();

    const newapartment = {
      aptname: this.state.apt_namei,
    };
    console.log(newapartment)
    axios
      .post(`http://18.217.253.58:8000/keytable_insert`, {
        newapartment,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apt_namei: "" });
        this.setState({ apt_addi: "" });
      });
  };

  //delete key table
  handleChangeRKD = event => {
    this.setState({ room_keyd: event.target.value });
  };

  handleSubmitDelete = event => {
    event.preventDefault();

    const deleteroom = {
      roomkey: this.state.room_keyd
    };

    axios
      .post(`http://18.217.253.58:8000/keytable_delete`, {
        deleteroom,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ room_keyd: "" });
      });
  };

  //update key table
  handleChangeANU = event => {
    this.setState({ apt_nameu: event.target.value });
  };

  handleChangeRKU = event => {
    this.setState({ room_keyu: event.target.value });
  };

  handleSubmitUpdate = event => {
    event.preventDefault();

    const changeapartment = {
      aptname: this.state.apt_nameu,
      roomkey: this.state.room_keyu
    };

    axios
      .post(`http://18.217.253.58:8000/keytable_update`, {
        changeapartment,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apt_nameu: "" });
        this.setState({ room_keyu: "" });
      });
  };

  render() {
    //console.log("count: ", this.state.count);
    return (
      <div>
        <Header></Header>
        <br />
        <Navs></Navs>
        <Container>
          <Row>
            <Col>
              <Form>
                <Form.Group controlId="aptnamei">
                  <Form.Label>Appartment Name</Form.Label>
                  <Form.Control
                    value={this.state.apt_namei}
                    onChange={this.handleChangeANI}
                  />
                </Form.Group>

                {/* <Form.Group controlId="aptaddi">
                  <Form.Label>Apartment Address</Form.Label>
                  <Form.Control
                    value={this.state.apt_addi}
                    onChange={this.handleChangeAAI}
                  />
                </Form.Group> */}

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitInsert}
                >
                  Insert
                </Button>
              </Form>
            </Col>
            <Col>
              <Form>
                <Form.Group controlId="roomkeyd">
                  <Form.Label>Room Key</Form.Label>
                  <Form.Control
                    value={this.state.room_keyd}
                    onChange={this.handleChangeRKD}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitDelete}
                >
                  Delete
                </Button>
              </Form>
            </Col>

            <Col>
              <Form>
                <Form.Group controlId="aptnameu">
                  <Form.Label>Appartment Name</Form.Label>
                  <Form.Control
                    value={this.state.apt_nameu}
                    onChange={this.handleChangeANU}
                  />
                </Form.Group>

                <Form.Group controlId="roomkeyu">
                  <Form.Label>Room Key</Form.Label>
                  <Form.Control
                    value={this.state.room_keyu}
                    onChange={this.handleChangeRKU}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitUpdate}
                >
                  Update
                </Button>
              </Form>
            </Col>
          </Row>
          <br />
          <br />
          <Row>
            <Col></Col>
            <Col>
            <Button variant="primary" onClick={this.handleLeave}>
              Back to Admin Main Page!
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
