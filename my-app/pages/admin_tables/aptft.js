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
    af_aptnamei: "",
    af_aptnameu: "",
    af_aptnamed: "",
    af_parking: "",
    af_studyroom: "",
    af_lounge: "",
    af_frontdesk: "",
    af_parkingu: "",
    af_studyroomu: "",
    af_loungeu: "",
    af_frontdesku: "",
    apart_addr:""
  };

  // insert apartment features table
  handleChangeAFANI = event => {
    this.setState({ af_aptnamei: event.target.value });
  };

  handleChangeAFPI = event => {
    this.setState({ af_parking: event.target.value });
  };

  handleChangeAFLI = event => {
    this.setState({ af_lounge: event.target.value });
  };

  handleChangeAFSI = event => {
    this.setState({ af_studyroom: event.target.value });
  };

  handleChangeAFFI = event => {
    this.setState({ af_frontdesk: event.target.value });
  };

  handleChangeAFLLI = event => {
    this.setState({ apart_addr: event.target.value });
  };

  handleSubmitInsertAF = event => {
    event.preventDefault();

    const newapartmentfeature = {
      apt_name: this.state.af_aptnamei,
      parking: this.state.af_parking,
      study_room: this.state.af_studyroom,
      lounge: this.state.af_lounge,
      front_desk: this.state.af_frontdesk,
      apart_addr: this.state.apart_addr
    };

    axios
      .post(`http://18.217.253.58:8000/apartfeature_insert`, {
        newapartmentfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ af_aptnamei: "" });
        this.setState({ af_parking: "" });
        this.setState({ af_studyroom: "" });
        this.setState({ af_lounge: "" });
        this.setState({ af_frontdesk: "" });
        this.setState({ apart_addr: "" });
      });
  };

  // delete apartment features table
  handleChangeAFAND = event => {
    this.setState({ af_aptnamed: event.target.value });
  };

  handleSubmitDeleteAF = event => {
    event.preventDefault();

    const deleteapartmentfeature = {
      apt_name: this.state.af_aptnamed
    };
    axios
      .post(`http://18.217.253.58:8000/apartfeature_delete`, {
        deleteapartmentfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ af_aptnamed: "" });
      });
  };

  //update
  handleChangeAFANU = event => {
    this.setState({ af_aptnameu: event.target.value });
  };

  handleChangeAFPU = event => {
    this.setState({ af_parkingu: event.target.value });
  };

  handleChangeAFLU = event => {
    this.setState({ af_loungeu: event.target.value });
  };

  handleChangeAFSU = event => {
    this.setState({ af_studyroomu: event.target.value });
  };

  handleChangeAFFU = event => {
    this.setState({ af_frontdesku: event.target.value });
  };

  handleSubmitUpdateAF = event => {
    event.preventDefault();

    const newapartmentfeature = {
      apt_name: this.state.af_aptnameu,
      parking: this.state.af_parkingu,
      study_room: this.state.af_studyroomu,
      lounge: this.state.af_loungeu,
      front_desk: this.state.af_frontdesku,
    };
    axios
      .post(`http://18.217.253.58:8000/apartfeature_update`, {
        newapartmentfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ af_aptnameu: "" });
        this.setState({ af_parkingu: "" });
        this.setState({ af_studyroomu: "" });
        this.setState({ af_loungeu: "" });
        this.setState({ af_frontdesku: "" });
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
                <Form.Group controlId="af_aptnamei">
                  <Form.Label>Appartment Name</Form.Label>
                  <Form.Control
                    value={this.state.af_aptnamei}
                    onChange={this.handleChangeAFANI}
                  />
                </Form.Group>

                <Form.Group controlId="aptpi">
                  <Form.Label>Parking</Form.Label>
                  <Form.Control
                    value={this.state.af_parking}
                    onChange={this.handleChangeAFPI}
                  />
                </Form.Group>

                <Form.Group controlId="aptli">
                  <Form.Label>Lounge</Form.Label>
                  <Form.Control
                    value={this.state.af_lounge}
                    onChange={this.handleChangeAFLI}
                  />
                </Form.Group>

                <Form.Group controlId="aptsi">
                  <Form.Label>Study Room</Form.Label>
                  <Form.Control
                    value={this.state.af_studyroom}
                    onChange={this.handleChangeAFSI}
                  />
                </Form.Group>

                <Form.Group controlId="aptfi">
                  <Form.Label>Front Desk</Form.Label>
                  <Form.Control
                    value={this.state.af_frontdesk}
                    onChange={this.handleChangeAFFI}
                  />
                </Form.Group>
                <Form.Group controlId="af_aptaddr">
                  <Form.Label>Appartment Address</Form.Label>
                  <Form.Control
                    value={this.state.apart_addr}
                    onChange={this.handleChangeAFLLI}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitInsertAF}
                >
                  Insert
                </Button>
              </Form>
            </Col>
            <Col>
              <Form>
                <Form.Group controlId="aptnd">
                  <Form.Label>Apartment Name</Form.Label>
                  <Form.Control
                    value={this.state.af_aptnamed}
                    onChange={this.handleChangeAFAND}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitDeleteAF}
                >
                  Delete
                </Button>
              </Form>
            </Col>
            <Col>
              <Form>
                <Form.Group controlId="af_aptnameu">
                  <Form.Label>Appartment Name</Form.Label>
                  <Form.Control
                    value={this.state.af_aptnameu}
                    onChange={this.handleChangeAFANU}
                  />
                </Form.Group>

                <Form.Group controlId="aptpu">
                  <Form.Label>Parking</Form.Label>
                  <Form.Control
                    value={this.state.af_parkingu}
                    onChange={this.handleChangeAFPU}
                  />
                </Form.Group>

                <Form.Group controlId="aptlu">
                  <Form.Label>Lounge</Form.Label>
                  <Form.Control
                    value={this.state.af_loungeu}
                    onChange={this.handleChangeAFLU}
                  />
                </Form.Group>

                <Form.Group controlId="aptsu">
                  <Form.Label>Study Room</Form.Label>
                  <Form.Control
                    value={this.state.af_studyroomu}
                    onChange={this.handleChangeAFSU}
                  />
                </Form.Group>

                <Form.Group controlId="aptfu">
                  <Form.Label>Front Desk</Form.Label>
                  <Form.Control
                    value={this.state.af_frontdesku}
                    onChange={this.handleChangeAFFU}
                  />
                </Form.Group>

                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmitUpdateAF}
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
