import React, { Component } from "react";
import {
  Button,
  Navbar,
  Nav,
  Form,
  Modal,
} from "react-bootstrap";

class Header extends Component {
  state = {
    show: false,
    username: "",
    password: ""
  };

  handleClose = () => {
    this.setState({ show: false });
  };
  handleShow = () => {
    this.setState({ show: true });
  };

  username = event => {
    this.setState({ username: event.target.value });
  };
  password = event => {
    this.setState({ password: event.target.value });
  };

  handleLogIn = () => {
    if (
      this.state.username == "Admin" &&
      this.state.password == "Matcha123456"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User1" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User2" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "Use3" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User4" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User5" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User6" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User7" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User8" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User9" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else if (
      this.state.username == "User10" &&
      this.state.password == "123"
    ) {
      window.location.href = "/admin";
    }
    else {
      alert("Username or Password Wrong!!!");
      this.setState({ username: "" });
      this.setState({ password: "" });
    }
  };

  render() {
    return (
      <div>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="/index">Matcha Apartment</Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link href="/features">Apartment Features</Nav.Link>
            <Nav.Link href="/scoregenerate">Select For You</Nav.Link>
          </Nav>
          <Form inline>
            <Button variant="outline-light" onClick={this.handleShow}>
              Admin LogIn
            </Button>
          </Form>
        </Navbar>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Enter Username and Password:</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group controlId="Username">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  type="username"
                  value={this.state.username}
                  onChange={this.username}
                />
              </Form.Group>

              <Form.Group controlId="Password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  value={this.state.password}
                  onChange={this.password}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="primary" onClick={this.handleLogIn}>
              Log In
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

export default Header;
