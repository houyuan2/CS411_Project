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
    apart_key: "",
    dest_addr: "",
    distance: "",
    search_idi: "",
    search_id: ""
  };
  //insert key table
  handleChangeAK = event => {
    this.setState({ apart_key: event.target.value });
  };

  handleChangeDA = event => {
    this.setState({ dest_addr: event.target.value });
  };

  handleChangeD = event => {
    this.setState({ distance: event.target.value });
  };

  handleChangeSII = event => {
    this.setState({ search_idi: event.target.value });
  };

  handleSubmitInsert = event => {
    event.preventDefault();

    const newdistancetable = {
      apart_key: this.state.apart_key,
      dest_addr: this.state.dest_addr,
      distance: this.state.distance,
      search_id: this.state.search_idi
    };

    axios
      .post(`http://18.217.253.58:8000/distancetable_insert`, {
        newdistancetable,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apart_key: "" });
        this.setState({ dest_addr: "" });
        this.setState({ distance: "" });
        this.setState({ search_idi: "" });
      });
  };

  //delete key table
  handleChangeSI = event => {
    this.setState({ search_id: event.target.value });
  };

  handleSubmitDelete = event => {
    event.preventDefault();

    const deleteroomfeature = {
      search_id: this.state.search_id
    };

    axios
      .post(`http://18.217.253.58:8000/distancetable_delete`, {
        deleteroomfeature,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ search_id: "" });
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
                <Form.Group controlId="sii">
                  <Form.Label>Search Id</Form.Label>
                  <Form.Control
                    value={this.state.search_idi}
                    onChange={this.handleChangeSII}
                  />
                </Form.Group>
                <Form.Group controlId="ak">
                  <Form.Label>Appartment Key</Form.Label>
                  <Form.Control
                    value={this.state.apart_key}
                    onChange={this.handleChangeAK}
                  />
                </Form.Group>

                <Form.Group controlId="ds">
                  <Form.Label>destination Address</Form.Label>
                  <Form.Control
                    value={this.state.dest_addr}
                    onChange={this.handleChangeDA}
                  />
                </Form.Group>

                <Form.Group controlId="d">
                  <Form.Label>Distance</Form.Label>
                  <Form.Control
                    value={this.state.distance}
                    onChange={this.handleChangeD}
                  />
                </Form.Group>

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
                <Form.Group controlId="si">
                  <Form.Label>Search Id</Form.Label>
                  <Form.Control
                    value={this.state.search_id}
                    onChange={this.handleChangeSI}
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
