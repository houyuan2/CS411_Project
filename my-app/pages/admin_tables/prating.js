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
    apart_key: "",
    rating: "",
    comment: "",
    nick_name: "",
    comment_id: ""
  };
  //insert key table
  handleChangeAK = event => {
    this.setState({ apart_key: event.target.value });
  };

  handleChangeR = event => {
    this.setState({ rating: event.target.value });
  };

  handleChangeC = event => {
    this.setState({ comment: event.target.value });
  };

  handleChangeNN = event => {
    this.setState({ nick_name: event.target.value });
  };

  handleSubmitInsert = event => {
    event.preventDefault();

    const newpeoplerating = {
      apart_key: this.state.apart_key,
      rating: this.state.rating,
      comment: this.state.comment,
      nick_name: this.state.nick_name
    };

    axios
      .post(``, {
        newpeoplerating,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ apart_key: "" });
        this.setState({ rating: "" });
        this.setState({ comment: "" });
        this.setState({ nick_name: "" });
      });
  };

  //delete key table
  handleChangeCI = event => {
    this.setState({ comment_id: event.target.value });
  };

  handleSubmitDelete = event => {
    event.preventDefault();

    const deletepeoplerating = {
      comment_id: this.state.comment_id
    };

    axios
      .post(``, {
        deletepeoplerating,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ comment_id: "" });
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
                <Form.Group controlId="ak">
                  <Form.Label>Appartment Ket</Form.Label>
                  <Form.Control
                    value={this.state.apart_key}
                    onChange={this.handleChangeAK}
                  />
                </Form.Group>

                <Form.Group controlId="r">
                  <Form.Label>Rating</Form.Label>
                  <Form.Control
                    value={this.state.rating}
                    onChange={this.handleChangeR}
                  />
                </Form.Group>

                <Form.Group controlId="c">
                  <Form.Label>Comment</Form.Label>
                  <Form.Control
                    value={this.state.comment}
                    onChange={this.handleChangeC}
                  />
                </Form.Group>

                <Form.Group controlId="nn">
                  <Form.Label>Nick Name</Form.Label>
                  <Form.Control
                    value={this.state.nick_name}
                    onChange={this.handleChangeNN}
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
                <Form.Group controlId="ci">
                  <Form.Label>Comment ID</Form.Label>
                  <Form.Control
                    value={this.state.comment_id}
                    onChange={this.handleChangeCI}
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
