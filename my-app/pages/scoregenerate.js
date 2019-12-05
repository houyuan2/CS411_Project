import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, Navbar, Form, Container, Col ,Row, Table, Modal,ModalFooter} from "react-bootstrap";
import Header from "../component/header.js";
import axios from "axios";
import StarRatings from "react-star-ratings";

class Index extends Component {
  state = {
    quest1: 0,
    quest2: 0,
    quest3: 0,
    quest4: 0,
    quest5: 0,
    quest6: 0,
    quest7: 0,
    quest8: 0,
    dest1: "",
    dest2: "",
    dest3: "",
    flag: "0",
    result: [],
    apart_key_id: "",
    all_room: [],
    all_apt: [],
    all_rating: [],
    overall_rating: [],
    all_around: [],
    dest: "",
    showdest: false,
    distanceinM: "",
    show: false,
    rating: "",
    comment: "",
    nickname: "",
    showsimilar: false,
    resultsimilar: []
  };

  changeWebnew(value) {
    //this.setState({ room_key: value["room_key"] });
    this.setState({ apart_key_id: value["apart_key"] });
    event.preventDefault();
    const showinfo = {
      apart_key: value["apart_key"]
    };
    axios
      .post(`http://18.217.253.58:8000/new_show`, {
        showinfo,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resultALLinfo => {
        this.setState({ all_room: resultALLinfo.data[1] });
        this.setState({ all_apt: resultALLinfo.data[2] });
        this.setState({ overall_rating: resultALLinfo.data[3] });
        this.setState({ all_rating: resultALLinfo.data[4] });
        this.setState({ all_around: resultALLinfo.data[0] });
        this.setState({ flag: "2" });
        this.setState({ showsimilar: false});
      });
  }

  returnToH = () => {
    this.setState({ flag: "1" });
  };

  handleClosesimilar = () => {
    this.setState({ showsimilar: false });
  };

  handleShowsimilar(value) {
    this.setState({ showsimilar: true });
    event.preventDefault();
    const similar_room = {
      room_key: value
    };
    console.log(similar_room);
    axios
      .post(`http://18.217.253.58:8000/similar_apart`, {
        similar_room,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resultsim => {
        console.log(resultsim.data);
        this.setState({ resultsimilar: resultsim.data });
        this.setState({ rating: "" });
      });
  }

  change1 = () => {
    if (document.getElementById("1").checked) {
      this.setState({ quest1: 1 });
    } else {
      this.setState({ quest1: 0 });
    }
  };

  change2 = () => {
    if (document.getElementById("2").checked) {
      this.setState({ quest2: 1 });
    } else {
      this.setState({ quest2: 0 });
    }
  };

  change3 = () => {
    if (document.getElementById("3").checked) {
      this.setState({ quest3: 1 });
    } else {
      this.setState({ quest3: 0 });
    }
  };

  change4 = () => {
    if (document.getElementById("4").checked) {
      this.setState({ quest4: 1 });
    } else {
      this.setState({ quest4: 0 });
    }
  };

  change5 = () => {
    if (document.getElementById("5").checked) {
      this.setState({ quest5: 1 });
    } else {
      this.setState({ quest5: 0 });
    }
  };

  change6 = () => {
    if (document.getElementById("6").checked) {
      this.setState({ quest6: 1 });
    } else {
      this.setState({ quest6: 0 });
    }
  };

  change8 = () => {
    if (document.getElementById("8").checked) {
      this.setState({ quest8: 1 });
    } else {
      this.setState({ quest8: 0 });
    }
  };

  change7 = () => {
    if (document.getElementById("7").checked) {
      this.setState({ quest7: 1 });
    } else {
      this.setState({ quest7: 0 });
    }
  };

  OnChangeDest1 = event => {
    this.setState({ dest1: event.target.value });
  };

  OnChangeDest2 = event => {
    this.setState({ dest2: event.target.value });
  };

  OnChangeDest3 = event => {
    this.setState({ dest3: event.target.value });
  };

  handleSubmit = event => {
    event.preventDefault();
    const Questions = {
      weights: {
        washing: this.state.quest1,
        nosharebath: this.state.quest2,
        kitchen: this.state.quest3,
        tv: this.state.quest4,
        car: this.state.quest5,
        study: this.state.quest6,
        lounge: this.state.quest7,
        shopping: this.state.quest8
      },
      dest1: this.state.dest1,
      dest2: this.state.dest2,
      dest3: this.state.dest3
    };
    axios
      .post(`http://18.217.253.58:8000/selectforyou`, {
        Questions,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(res => {
        this.setState({ result: res.data[0] });
        this.setState({ flag: "1" });
        this.setState({ quest1: 0 });
        this.setState({ quest2: 0 });
        this.setState({ quest3: 0 });
        this.setState({ quest4: 0 });
        this.setState({ quest5: 0 });
        this.setState({ quest6: 0 });
        this.setState({ quest7: 0 });
        this.setState({ quest8: 0 });
        this.setState({ dest1: "" });
        this.setState({ dest2: "" });
        this.setState({ dest3: "" });
      });
  };

  handleComment = () => {
    event.preventDefault();
    const newpeoplerating = {
      apart_key: this.state.apart_key_id,
      rating: this.state.rating,
      comment: this.state.comment,
      nick_name: this.state.nickname
    };
    axios
      .post(`http://18.217.253.58:8000/peoplerating_insert`, {
        newpeoplerating,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(() => {
        this.setState({ rating: "" });
        this.setState({ comment: "" });
        this.setState({ nickname: "" });
        this.setState({ show: false });
      });
  };

  OnChangecomment = event => {
    this.setState({ comment: event.target.value });
  };

  Onchangenickname = event => {
    this.setState({ nickname: event.target.value });
  };

  OnChangerating = event => {
    this.setState({ rating: event.target.value });
  };

  handleClose = () => {
    this.setState({ show: false });
  };

  handleShow = () => {
    this.setState({ show: true });
  };

  OnChangeDest = event => {
    this.setState({ dest: event.target.value });
  };

  handleFindDest = event => {
    event.preventDefault();
    const distance = {
      apart_key: this.state.apart_key_id,
      dest: this.state.dest
    };
    axios
      .post(`http://18.217.253.58:8000/AF1Distance`, {
        distance,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resultDest => {
        this.setState({ distanceinM: resultDest.data });
        this.setState({ dest: "" });
        this.setState({ showdest: true });
      });
  };

  handleCloseDest = () => {
    this.setState({ showdest: false });
  };

  changeWeb(value) {
    //this.setState({ room_key: value["room_key"] });
    this.setState({ apart_key_id: value["apart"] });
    event.preventDefault();
    const showinfo = {
      apart_key: value["apart"]
    };
    axios
      .post(`http://18.217.253.58:8000/new_show`, {
        showinfo,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resultALLinfo => {
        this.setState({ all_room: resultALLinfo.data[1] });
        this.setState({ all_apt: resultALLinfo.data[2] });
        this.setState({ overall_rating: resultALLinfo.data[3] });
        this.setState({ all_rating: resultALLinfo.data[4] });
        this.setState({ all_around: resultALLinfo.data[0] });
        this.setState({ flag: "2" });
      });
  }

  return = () => {
    this.setState({ flag: "0" });
  };

  render() {
    if (this.state.flag == "0") {
      return (
        <div>
          <Header></Header>
          <Container>
            <Col></Col>
            <Col></Col>
            <Col>
              <Navbar bg="light">
                <Navbar.Brand>
                  Questionary of Generating Apartments' Scores:
                </Navbar.Brand>
              </Navbar>
              <Form>
                <label>I need a private laundy</label>
                <Form.Group controlId="check1">
                  <Form.Check
                    type="checkbox"
                    id="1"
                    label="Check if apply"
                    onChange={this.change1}
                  />
                </Form.Group>
                <label>I do not want to share bathroom with others</label>
                <Form.Group controlId="check2">
                  <Form.Check
                    type="checkbox"
                    id="2"
                    label="Check if apply"
                    onChange={this.change2}
                  />
                </Form.Group>
                <label>I like cooking</label>
                <Form.Group controlId="check3">
                  <Form.Check
                    type="checkbox"
                    id="3"
                    label="Check if apply"
                    onChange={this.change3}
                  />
                </Form.Group>
                <label>I love TV</label>
                <Form.Group controlId="check4">
                  <Form.Check
                    type="checkbox"
                    id="4"
                    label="Check if apply"
                    onChange={this.change4}
                  />
                </Form.Group>
                <label>I own a car</label>
                <Form.Group controlId="check5">
                  <Form.Check
                    type="checkbox"
                    id="5"
                    label="Check if apply"
                    onChange={this.change5}
                  />
                </Form.Group>
                <label>I prefer to study in a studyroom</label>
                <Form.Group controlId="check6">
                  <Form.Check
                    type="checkbox"
                    id="6"
                    label="Check if apply"
                    onChange={this.change6}
                  />
                </Form.Group>
                <label>I am a party guy</label>
                <Form.Group controlId="check7">
                  <Form.Check
                    type="checkbox"
                    id="7"
                    label="Check if apply"
                    onChange={this.change7}
                  />
                </Form.Group>
                <label>I like shoping</label>
                <Form.Group controlId="check8">
                  <Form.Check
                    type="checkbox"
                    id="8"
                    label="Check if apply"
                    onChange={this.change8}
                  />
                </Form.Group>
                <Form.Text className="text-muted">
                  Please enter the first address of place you frequently go:
                </Form.Text>
                <Form.Control
                  type="DA"
                  value={this.state.dest1}
                  onChange={this.OnChangeDest1}
                />
                <Form.Text className="text-muted">
                  Please enter the second address of place you frequently go:
                </Form.Text>
                <Form.Control
                  type="DA"
                  value={this.state.dest2}
                  onChange={this.OnChangeDest2}
                />
                <Form.Text className="text-muted">
                  Please enter the third address of place you frequently go:
                </Form.Text>
                <Form.Control
                  type="DA"
                  value={this.state.dest3}
                  onChange={this.OnChangeDest3}
                />
                <br />
                <Button
                  variant="outline-primary"
                  type="submit"
                  onClick={this.handleSubmit}
                  block
                >
                  Submit
                </Button>
              </Form>
            </Col>
            <Col></Col>
            <Col></Col>
          </Container>
        </div>
      );
    } else if (this.state.flag == "1") {
      return (
        <div>
          <Header></Header>
          <Container>
            <Col></Col>
            <Col>
              <h3>Matched Apartments:</h3>
              <br />
              {this.state.result.map(each => {
                return (
                  <div key={each["apart"]}>
                    <Button
                      variant="outline-primary"
                      onClick={() => this.changeWeb(each)}
                      size="lg"
                      block
                    >
                    {each.apart}
                    </Button>
                    <br />
                    <Form.Label>Envitonment Rating: </Form.Label>
                    <br />
                    <StarRatings
                      rating={each["env"]}
                      starRatedColor="gold"
                      starDimension="25px"
                      starSpacing="15px"
                    />
                    <br />
                    <Form.Label>People Rating: </Form.Label>
                    <br />
                    <StarRatings
                      rating={each["ppl"]}
                      starRatedColor="gold"
                      starDimension="25px"
                      starSpacing="15px"
                    />
                    <br />
                    <Form.Label>Location Rating: </Form.Label>
                    <br />
                    <StarRatings
                      rating={each["loc"]}
                      starRatedColor="gold"
                      starDimension="25px"
                      starSpacing="15px"
                    />
                    <br />
                    <Form.Label>Smart Rating: </Form.Label>
                    <br />
                    <StarRatings
                      rating={each["smart"]}
                      starRatedColor="gold"
                      starDimension="25px"
                      starSpacing="15px"
                    />
                    <br />
                    <br />
                  </div>
                );
              })}
              <Button
                variant="outline-primary"
                type="submit"
                onClick={this.return}
                block
              >
                Return
              </Button>
            </Col>
            <Col></Col>
          </Container>
        </div>
      );
    } else if (this.state.flag == "2") {
      return (
        <div>
          <Header></Header>
          <Container>
            <Row>
              {this.state.all_apt.map(each => {
                return (
                  <div key={each["apart_addr"]}>
                    <Container>
                      <Row>
                        <Col></Col>
                        <h1>Apartment Name: {this.state.apart_key_id}</h1>
                        <Col></Col>
                      </Row>
                      <Table striped bordered hover>
                        <thead>
                          <tr>
                            <th>Apartment Address</th>
                            <th>Front Desk</th>
                            <th>Lounge</th>
                            <th>Parking</th>
                            <th>Study Room</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>{each["apart_addr"]}</td>
                            <td>{each["front_desk"]}</td>
                            <td>{each["lounge"]}</td>
                            <td>{each["parking"]}</td>
                            <td>{each["study_room"]}</td>
                          </tr>
                        </tbody>
                      </Table>
                    </Container>
                  </div>
                );
              })}
            </Row>
            <Row>
              <Container>
                {this.state.overall_rating.map(each => {
                  return (
                    <div key={each["env_rating"]}>
                      <Table striped bordered hover>
                        <thead>
                          <tr>
                            <th>Overall Rating</th>
                            <th>People Rating</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>{each["env_rating"]}</td>
                            <td>{each["ppl_rating"]}</td>
                          </tr>
                        </tbody>
                      </Table>
                    </div>
                  );
                })}
              </Container>
            </Row>
            <Row>
              <Col>
                <Form>
                  <Form.Group controlId="DA">
                    <Form.Label>Destination Address</Form.Label>
                    <Form.Control
                      type="DA"
                      value={this.state.dest}
                      onChange={this.OnChangeDest}
                    />
                    <Form.Text className="text-muted">
                      Please enter the address of place you frequently go!
                    </Form.Text>
                  </Form.Group>
                  <Button
                    variant="outline-primary"
                    onClick={this.handleFindDest}
                  >
                    Submit
                  </Button>
                </Form>
                <br />
                <Modal show={this.state.showdest} onHide={this.handleCloseDest}>
                  <Modal.Header>
                    <Modal.Title>
                      The distance between this apartment and your destination
                      is:
                    </Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <a>{this.state.distanceinM}</a>
                  </Modal.Body>
                  <ModalFooter>
                    <Button
                      variant="outline-primary"
                      onClick={this.handleCloseDest}
                    >
                      Close
                    </Button>
                  </ModalFooter>
                </Modal>
              </Col>
            </Row>
            <br />
            <Row>
              <Col></Col>
              {this.state.all_room.map(each => {
                return (
                  <Container>
                    <div key={each["roomkey"]}>
                    <Container>
                      <Row>
                        <Col>
                          <a>
                            Room Type: {each["number_of_bedroom"]}b
                            {each["number_of_bathroom"]}b
                          </a>
                        </Col>
                        <Col></Col>
                        <Col>
                          <Button
                            variant="outline-primary"
                            onClick={() =>
                              this.handleShowsimilar(each["roomkey"])
                            }
                          >
                            Find Similar Room!
                          </Button>
                          <Modal
                            show={this.state.showsimilar}
                            onHide={this.handleClosesimilar}
                          >
                            <Modal.Header closeButton>
                              <Modal.Title>
                                Here are the apartments that has similar room:
                              </Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                              {this.state.resultsimilar.map(each => {
                                return (
                                  <div key={each["apart_key"]}>
                                    <Button
                                      variant="outline-primary"
                                      onClick={() => this.changeWebnew(each)}
                                      size="lg"
                                      block
                                    >
                                      {each.apart_key}
                                    </Button>
                                    <a>Location: {each["apart_addr"]}</a>
                                    <br />
                                    <a>Similarity: {each["similarity"]}</a>
                                    <br />
                                    <StarRatings
                                      rating={each["overallrating"]}
                                      starRatedColor="gold"
                                      starDimension="25px"
                                      starSpacing="15px"
                                    />
                                    <br />
                                    <br />
                                  </div>
                                );
                              })}
                            </Modal.Body>
                            <ModalFooter>
                              <Button
                                variant="outline-primary"
                                onClick={this.handleClosesimilar}
                              >
                                Close
                              </Button>
                            </ModalFooter>
                          </Modal>
                        </Col>
                      </Row>
                    </Container>
                      <Table striped bordered hover size="sm">
                        <thead>
                          <tr>
                            <th>Attributes</th>
                            <th>Value</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>Cover Electricity Fee</td>
                            <td>{each["cover_electricity_fee"]}</td>
                          </tr>
                          <tr>
                            <td>Cover Internet Fee</td>
                            <td>{each["cover_internet_fee"]}</td>
                          </tr>
                          <tr>
                            <td>Cover Water Fee</td>
                            <td>{each["cover_water_fee"]}</td>
                          </tr>
                          <tr>
                            <td>Has Kitchen</td>
                            <td>{each["has_kitchen"]}</td>
                          </tr>
                          <tr>
                            <td>Has Refigerator</td>
                            <td>{each["has_refigerator"]}</td>
                          </tr>
                          <tr>
                            <td>Has TV</td>
                            <td>{each["has_tv"]}</td>
                          </tr>
                          <tr>
                            <td>Number of Bathroom</td>
                            <td>{each["number_of_bathroom"]}</td>
                          </tr>
                          <tr>
                            <td>Number of Bedroom</td>
                            <td>{each["number_of_bedroom"]}</td>
                          </tr>
                          <tr>
                            <td>Private Washing Machine</td>
                            <td>{each["private_washing_machine"]}</td>
                          </tr>
                          <tr>
                            <td>Room Size</td>
                            <td>{each["size"]}</td>
                          </tr>
                          <tr>
                            <td>Website Link</td>
                            <td>{each["url"]}</td>
                          </tr>
                        </tbody>
                      </Table>
                    </div>
                  </Container>
                );
              })}
              <br />
              <Col></Col>
            </Row>
            <Row>
              <Container>
                {this.state.all_rating.map(each => {
                  return (
                    <div key={each["nick_name"]}>
                      <Container>
                        <Table striped bordered hover>
                          <thead>
                            <tr>
                              <th>{each["nick_name"]}</th>
                              <th>{each["rating"]}</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td colSpan="2">{each["comment"]}</td>
                            </tr>
                          </tbody>
                        </Table>
                      </Container>
                      <br />
                    </div>
                  );
                })}
              </Container>
            </Row>
            <Container>
              {this.state.all_around.map(each => {
                return (
                  <div key={each["rest2"]}>
                    <Table striped bordered hover>
                      <thead>
                        <tr>
                          <th>Attributes</th>
                          <th>Number</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>Restaurant(within 0.5km)</td>
                          <td>{each["rest05"]}</td>
                        </tr>
                        <tr>
                          <td>Restaurant(within 1km)</td>
                          <td>{each["rest1"]}</td>
                        </tr>
                        <tr>
                          <td>Restaurant(within 2km)</td>
                          <td>{each["rest2"]}</td>
                        </tr>
                        <tr>
                          <td>Shop(within 0.5km)</td>
                          <td>{each["shop05"]}</td>
                        </tr>
                        <tr>
                          <td>Shop(within 1km)</td>
                          <td>{each["shop1"]}</td>
                        </tr>
                        <tr>
                          <td>Shop(within 2km)</td>
                          <td>{each["shop2"]}</td>
                        </tr>
                      </tbody>
                    </Table>
                  </div>
                );
              })}
            </Container>
            <Row>
              <Col></Col>
              <Col></Col>
              <Col></Col>
              <Button variant="outline-primary" onClick={this.handleShow}>
                Comment
              </Button>
              <Modal show={this.state.show} onHide={this.handleClose}>
                <Modal.Header closeButton>
                  <Modal.Title>We look forward to your comments!</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  <Form>
                    <Form.Group controlId="rating">
                      <Form.Label>Rating(0-5):</Form.Label>
                      <Form.Control
                        type="rating"
                        value={this.state.rating}
                        onChange={this.OnChangerating}
                      />
                    </Form.Group>
                    <Form.Group controlId="comment">
                      <Form.Label>Comment:</Form.Label>
                      <Form.Control
                        type="comment"
                        value={this.state.comment}
                        onChange={this.OnChangecomment}
                      />
                    </Form.Group>

                    <Form.Group controlId="nickname">
                      <Form.Label>Nick Name:</Form.Label>
                      <Form.Control
                        type="nickname"
                        value={this.state.nickname}
                        onChange={this.Onchangenickname}
                      />
                    </Form.Group>
                  </Form>
                </Modal.Body>
                <Modal.Footer>
                  <Button variant="primary" onClick={this.handleComment}>
                    Comment
                  </Button>
                </Modal.Footer>
              </Modal>
            </Row>
            <br />
            <Row>
              <Col></Col>
              <Col></Col>
              <Col></Col>
              <Button variant="outline-primary" onClick={this.returnToH}>
                Return To Features
              </Button>
            </Row>
          </Container>
        </div>
      );
    }
  }
}

export default Index;
