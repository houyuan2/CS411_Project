import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Button,
  Form,
  Container,
  Row,
  Col,
} from "react-bootstrap";
import Header from "../../component/header.js";
import Navs from "../../component/navs.js";
import axios from "axios";

class Index extends Component {
  handleLeave = () => {
    window.location.href = "../admin";
  };

  state = {
    room_keyi: "",
    room_keyd: "",
    cover_internet_fee: "",
    cover_electricity_fee: "",
    private_washing_machine: "",
    number_of_bedroom: "",
    number_of_bathroom: "",
    has_kitchen: "",
    has_refigerator: "",
    cover_water_fee: "",
    has_tv: "",
    size: ""
  };

  // insert apartment features table
  handleChangeRKI = event => {
    this.setState({ room_keyi: event.target.value });
  };

  handleChangeCIFI = event => {
    this.setState({ cover_internet_fee: event.target.value });
  };

  handleChangeCEFI = event => {
    this.setState({ cover_electricity_fee: event.target.value });
  };

  handleChangeCWFI = event => {
    this.setState({ cover_water_fee: event.target.value });
  };

  handleChangePWMI = event => {
    this.setState({ private_washing_machine: event.target.value });
  };

  handleChangeNBI = event => {
    this.setState({ number_of_bedroom: event.target.value });
  };

  handleChangeNRI = event => {
    this.setState({ number_of_bathroom: event.target.value });
  };

  handleChangeHKI = event => {
    this.setState({ has_kitchen: event.target.value });
  };

  handleChangeHRI = event => {
    this.setState({ has_refigerator: event.target.value });
  };

  handleChangeSI = event => {
    this.setState({ size: event.target.value });
  };

  handleChangeHTI = event => {
    this.setState({ has_refigerator: event.target.value });
  };

  handleSubmitInsertRF = event => {
    event.preventDefault();

    const newroomfeature = {
      room_key: this.state.room_keyi,
      cover_internet_fee: this.state.cover_internet_fee,
      cover_electricity_fee: this.state.cover_electricity_fee,
      private_washing_machine: this.state.private_washing_machine,
      number_of_bedroom: this.state.number_of_bedroom,
      number_of_bathroom: this.state.number_of_bathroom,
      has_kitchen: this.state.has_kitchen,
      has_refigerator: this.state.has_refigerator,
      cover_water_fee: this.state.cover_water_fee,
      has_tv: this.state.has_tv,
      size: this.state.size
    };

    axios
      .post(``, {
        newapartmentfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ room_keyi: "" });
        this.setState({ cover_internet_fee: "" });
        this.setState({ cover_electricity_fee: "" });
        this.setState({ cover_water_fee: "" });
        this.setState({ private_washing_machine: "" });
        this.setState({ number_of_bedroom: "" });
        this.setState({ number_of_bathroom: "" });
        this.setState({ has_kitchen: "" });
        this.setState({ has_refigerator: "" });
        this.setState({ has_tv: "" });
        this.setState({ size: "" });
      });
  };

  // delete apartment features table
  handleChangeRKD = event => {
    this.setState({ room_keyd: event.target.value });
  };

  handleSubmitDeleteRF = event => {
    event.preventDefault();

    const deleteroomfeature = {
      room_key: this.state.room_keyd
    };

    axios
      .post(``, {
        deleteroomfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ room_keyd: "" });
      });
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

                <Form.Group controlId="rki">
                  <Form.Label>Room Key</Form.Label>
                  <Form.Control
                    value={this.state.room_keyi}
                    onChange={this.handleChangeRKI}
                  />
                </Form.Group>

                <Form.Group controlId="cef">
                  <Form.Label>Cover Electricity Fee</Form.Label>
                  <Form.Control
                    value={this.state.cover_electricity_fee}
                    onChange={this.handleChangeCEFI}
                  />
                </Form.Group>

                <Form.Group controlId="cif">
                  <Form.Label>Cover Internet Fee</Form.Label>
                  <Form.Control
                    value={this.state.cover_internet_fee}
                    onChange={this.handleChangeCIFI}
                  />
                </Form.Group>

                <Form.Group controlId="cwf">
                  <Form.Label>Cover Water Fee</Form.Label>
                  <Form.Control
                    value={this.state.cover_water_fee}
                    onChange={this.handleChangeCWFI}
                  />
                </Form.Group>
                <Form.Group controlId="wm">
                  <Form.Label>Washing Machine</Form.Label>
                  <Form.Control
                    value={this.state.private_washing_machine}
                    onChange={this.handleChangePWMI}
                  />
                </Form.Group>
                <Form.Group controlId="nr">
                  <Form.Label>Number of Bathrrom</Form.Label>
                  <Form.Control
                    value={this.state.number_of_bathroom}
                    onChange={this.handleChangeNRI}
                  />
                </Form.Group>
                <Form.Group controlId="nb">
                  <Form.Label>Number of Bedroom</Form.Label>
                  <Form.Control
                    value={this.state.number_of_bedroom}
                    onChange={this.handleChangeNBI}
                  />
                </Form.Group>
                <Form.Group controlId="k">
                  <Form.Label>Kitchen</Form.Label>
                  <Form.Control
                    value={this.state.has_kitchen}
                    onChange={this.handleChangeHKI}
                  />
                </Form.Group>
                <Form.Group controlId="r">
                  <Form.Label>Refigerator</Form.Label>
                  <Form.Control
                    value={this.state.has_refigerator}
                    onChange={this.handleChangeHRI}
                  />
                </Form.Group>
                <Form.Group controlId="ht">
                  <Form.Label>TV</Form.Label>
                  <Form.Control
                    value={this.state.has_tv}
                    onChange={this.handleChangeHTI}
                  />
                </Form.Group>
                <Form.Group controlId="size">
                  <Form.Label>Size</Form.Label>
                  <Form.Control
                    value={this.state.size}
                    onChange={this.handleChangeSI}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitInsertRF}
                >
                  Insert
                </Button>
              </Form>
            </Col>
            <Col>
              <Form>
                <Form.Group controlId="rkd">
                  <Form.Label>Room Key</Form.Label>
                  <Form.Control
                    value={this.state.room_keyd}
                    onChange={this.handleChangeRKD}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitDeleteRF}
                >
                  Delete
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
