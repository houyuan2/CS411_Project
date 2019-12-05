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
    apart_keyi: "",
    env_rating: "",
    ppl_rating: "",
    rest_05_count: "",
    rest_1_count: "",
    rest_2_count: "",
    shop_05_count: "",
    shop_1_count: "",
    shop_2_count: "",
    apart_keyd: ""
  };
  //insert key table
  handleChangeAKI = event => {
    this.setState({ apart_keyi: event.target.value });
  };

  handleChangeER = event => {
    this.setState({ env_rating: event.target.value });
  };

  handleChangePR = event => {
    this.setState({ ppl_rating: event.target.value });
  };

  handleChangeR5C = event => {
    this.setState({ rest_05_count: event.target.value });
  };

  handleChangeR1C = event => {
    this.setState({ rest_1_count: event.target.value });
  };

  handleChangeR2C = event => {
    this.setState({ rest_2_count: event.target.value });
  };

  handleChangeS5C = event => {
    this.setState({ shop_05_count: event.target.value });
  };

  handleChangeS1C = event => {
    this.setState({ shop_1_count: event.target.value });
  };

  handleChangeS2C = event => {
    this.setState({ shop_2_count: event.target.value });
  };

  handleSubmitInsert = event => {
    event.preventDefault();

    const newratingtable = {
      apart_key: this.state.apart_keyi,
      env_rating: this.state.env_rating,
      ppl_rating: this.state.ppl_rating,
      rest_05_count: this.state.rest_05_count,
      rest_1_count: this.state.rest_1_count,
      rest_2_count: this.state.rest_2_count,
      shop_05_count: this.state.shop_05_count,
      shop_1_count: this.state.shop_1_count,
      shop_2_count: this.state.shop_2_count
    };

    axios
      .post(``, {
        newratingtable,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apart_keyi: "" });
        this.setState({ env_rating: "" });
        this.setState({ ppl_rating: "" });
        this.setState({ rest_05_count: "" });
        this.setState({ rest_1_count: "" });
        this.setState({ rest_2_count: "" });
        this.setState({ shop_05_count: "" });
        this.setState({ shop_1_count: "" });
        this.setState({ shop_2_count: "" });
      });
  };

  //delete key table
  handleChangeAKD = event => {
    this.setState({ apart_keyd: event.target.value });
  };

  handleSubmitDelete = event => {
    event.preventDefault();

    const deleteratingtable = {
      apart_key: this.state.apart_keyd
    };

    axios
      .post(``, {
        deleteratingtable,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apart_keyd: "" });
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
                <Form.Group controlId="aki">
                  <Form.Label>Appartment Key</Form.Label>
                  <Form.Control
                    value={this.state.apart_keyi}
                    onChange={this.handleChangeAKI}
                  />
                </Form.Group>

                <Form.Group controlId="er">
                  <Form.Label>Environment Rating</Form.Label>
                  <Form.Control
                    value={this.state.env_rating}
                    onChange={this.handleChangeER}
                  />
                </Form.Group>

                <Form.Group controlId="rp">
                  <Form.Label>PPL Rating</Form.Label>
                  <Form.Control
                    value={this.state.ppl_rating}
                    onChange={this.handleChangePR}
                  />
                </Form.Group>

                <Form.Group controlId="r5c">
                  <Form.Label>Restaurant Count (0.5)</Form.Label>
                  <Form.Control
                    value={this.state.rest_05_count}
                    onChange={this.handleChangeR5C}
                  />
                </Form.Group>

                <Form.Group controlId="r1c">
                  <Form.Label>Restaurant Count (1)</Form.Label>
                  <Form.Control
                    value={this.state.rest_1_count}
                    onChange={this.handleChangeR1C}
                  />
                </Form.Group>

                <Form.Group controlId="r2c">
                  <Form.Label>Restaurant Count (2)</Form.Label>
                  <Form.Control
                    value={this.state.rest_2_count}
                    onChange={this.handleChangeR2C}
                  />
                </Form.Group>

                <Form.Group controlId="s5c">
                  <Form.Label>Shop Count (0.5)</Form.Label>
                  <Form.Control
                    value={this.state.shop_05_count}
                    onChange={this.handleChangeS5C}
                  />
                </Form.Group>

                <Form.Group controlId="s1c">
                  <Form.Label>Shop Count (1)</Form.Label>
                  <Form.Control
                    value={this.state.shop_1_count}
                    onChange={this.handleChangeS1C}
                  />
                </Form.Group>

                <Form.Group controlId="s2c">
                  <Form.Label>Shop Count (2)</Form.Label>
                  <Form.Control
                    value={this.state.shop_2_count}
                    onChange={this.handleChangeS2C}
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
                <Form.Group controlId="akd">
                  <Form.Label>Appartment Key</Form.Label>
                  <Form.Control
                    value={this.state.apart_keyd}
                    onChange={this.handleChangeAKD}
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
