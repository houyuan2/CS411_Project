import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Button,
  Navbar,
  Form,
  Container,
  Row,
  Col,
  DropdownButton,
  Dropdown,
  Table,
  Modal,
  ModalFooter,
  Jumbotron,
  Alert
} from "react-bootstrap";
import Header from "../component/header.js";
import axios from "axios";
import StarRatings from "react-star-ratings";

class Index extends Component {
  state = {
    num_bedr: 0,
    num_restr: 0,
    parking: 0,
    lounge: 0,
    studyroom: 0,
    frontdesk: 0,
    coverIF: 0,
    coverEF: 0,
    coverWF: 0,
    privateWM: 0,
    hasKitchen: 0,
    HasRef: 0,
    HasTV: 0,
    flag: true,
    result: [],
    apart_key_id: "",
    show: false,
    rating: "",
    comment: "",
    nickname: "",
    dest: "",
    distanceinM: "",
    targeta: "",
    show_apart_name: "",
    showdest: false,
    all_room: "",
    all_apt: "",
    all_rating: "",
    overall_rating: "",
    all_around: "",
    showsimilar: false,
    resultsimilar: []
  };

  handleSubmit = event => {
    event.preventDefault();
    const Filter = {
      parking: this.state.parking,
      lounge: this.state.lounge,
      study_room: this.state.studyroom,
      front_desk: this.state.frontdesk,
      bedrooms: this.state.num_bedr,
      restrooms: this.state.num_restr,
      cover_internet_fee: this.state.coverIF,
      cover_electricity_fee: this.state.coverEF,
      cover_water_fee: this.state.coverWF,
      private_washing_machine: this.state.privateWM,
      has_kitchen: this.state.hasKitchen,
      has_refrigerator: this.state.HasRef,
      has_tv: this.state.HasTV
    };
    console.log(Filter)
    axios
      .post(`http://18.217.253.58:8000/advance_filter`, {
        Filter,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resFilter => {
        console.log(resFilter.data)
        this.setState({ result: resFilter.data });
      });
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

  handleFindAPT = event => {
    event.preventDefault();
    const search = {
      apart_key: this.state.targeta
    };
    axios
      .post(`http://18.217.253.58:8000/search`, {
        search,
        method: "POST",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(resultAPT => {
        this.setState({ result: resultAPT.data });
        this.setState({ targeta: "" });
      });
  };

  handleClose = () => {
    this.setState({ show: false });
  };

  handleShow = () => {
    this.setState({ show: true });
  };

  handleCloseDest = () => {
    this.setState({ showdest: false });
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

  OnChangerating = event => {
    this.setState({ rating: event.target.value });
  };
  OnChangecomment = event => {
    this.setState({ comment: event.target.value });
  };

  Onchangenickname = event => {
    this.setState({ nickname: event.target.value });
  };

  OnChangeDest = event => {
    this.setState({ dest: event.target.value });
  };

  OnChangetargeta = event => {
    this.setState({ targeta: event.target.value });
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

  componentDidMount() {
    const { input } = this.state;
    axios
      .get(`http://18.217.253.58:8000/show`, {
        method: "GET",
        headers: { "Access-Control-Allow-Origin": "*" }
      })
      .then(res => {
        this.setState({ result: res.data });
      });
  }

  dwB(value) {
    this.setState({ num_bedr: value });
  }

  dwR(value) {
    this.setState({ num_restr: value });
  }

  changeP = () => {
    if (document.getElementById("P").checked) {
      this.setState({ parking: 1 });
    } else {
      this.setState({ parking: 0 });
    }
  };
  changeL = () => {
    if (document.getElementById("L").checked) {
      this.setState({ lounge: 1 });
    } else {
      this.setState({ lounge: 0 });
    }
  };
  changeS = () => {
    if (document.getElementById("S").checked) {
      this.setState({ studyroom: 1 });
    } else {
      this.setState({ studyroom: 0 });
    }
  };
  changeF = () => {
    if (document.getElementById("F").checked) {
      this.setState({ frontdesk: 1 });
    } else {
      this.setState({ frontdesk: 0 });
    }
  };

  changeCIF = () => {
    if (document.getElementById("CIF").checked) {
      this.setState({ coverIF: 1 });
    } else {
      this.setState({ coverIF: 0 });
    }
  };
  changeCEF = () => {
    if (document.getElementById("CEF").checked) {
      this.setState({ coverEF: 1 });
    } else {
      this.setState({ coverEF: 0 });
    }
  };
  changeCWF = () => {
    if (document.getElementById("CWF").checked) {
      this.setState({ coverWF: 1 });
    } else {
      this.setState({ coverWF: 0 });
    }
  };
  changePWM = () => {
    if (document.getElementById("PWM").checked) {
      this.setState({ privateWM: 1 });
    } else {
      this.setState({ privateWM: 0 });
    }
  };
  changeHK = () => {
    if (document.getElementById("HK").checked) {
      this.setState({ hasKitchen: 1 });
    } else {
      this.setState({ hasKitchen: 0 });
    }
  };
  changeHR = () => {
    if (document.getElementById("HR").checked) {
      this.setState({ HasRef: 1 });
    } else {
      this.setState({ HasRef: 0 });
    }
  };
  changeHTV = () => {
    if (document.getElementById("HTV").checked) {
      this.setState({ HasTV: 1 });
    } else {
      this.setState({ HasTV: 0 });
    }
  };

  //insert

  changeWeb(value) {
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
        this.setState({ flag: false });
      });
  }

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
        this.setState({ flag: false });
        this.setState({ showsimilar: false });
      });
  }

  returnToH = () => {
    this.setState({ flag: true });
  };

  render() {
    // console.log("parking: ", this.state.parking);
    // console.log("num_rest: ", this.state.num_restr);
    if (this.state.flag) {
      return (
        <div>
          <Header></Header>
          <br />
          <br />
          <Container>
            <Row>
              <Col>
                <Form>
                  <Form.Group controlId="TA">
                    <Form.Label>Target Apartment:</Form.Label>
                    <Form.Control
                      type="TA"
                      value={this.state.targeta}
                      onChange={this.OnChangetargeta}
                    />
                  </Form.Group>
                  <Button
                    variant="outline-primary"
                    onClick={this.handleFindAPT}
                    block
                  >
                    Search
                  </Button>
                </Form>
                <br />
                <h3>Features Filter:</h3>
                <br />
                <Navbar bg="light">
                  <Navbar.Brand>Apartment Features:</Navbar.Brand>
                </Navbar>
                <Form>
                  <Form.Group controlId="checkP">
                    <Form.Check
                      type="checkbox"
                      id="P"
                      label="Parking"
                      onChange={this.changeP}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkL">
                    <Form.Check
                      type="checkbox"
                      id="L"
                      label="Lounge"
                      onChange={this.changeL}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkS">
                    <Form.Check
                      type="checkbox"
                      id="S"
                      label="Study Room"
                      onChange={this.changeS}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkF">
                    <Form.Check
                      type="checkbox"
                      id="F"
                      label="Front Desk"
                      onChange={this.changeF}
                    />
                  </Form.Group>

                  <Navbar bg="light">
                    <Navbar.Brand>Room Features:</Navbar.Brand>
                  </Navbar>

                  <Form.Group controlId="checkBR">
                    <DropdownButton id="dropdownB" title="Number of bedrooms">
                      <Dropdown.Item onSelect={() => this.dwB(1)}>
                        1
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwB(2)}>
                        2
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwB(3)}>
                        3
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwB(4)}>
                        4
                      </Dropdown.Item>
                    </DropdownButton>
                  </Form.Group>
                  <Form.Group controlId="checkRR">
                    <DropdownButton id="dropdownR" title="Number of restrooms">
                      <Dropdown.Item onSelect={() => this.dwR(0)}>
                        0
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwR(1)}>
                        1
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwR(2)}>
                        2
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwR(3)}>
                        3
                      </Dropdown.Item>
                      <Dropdown.Item onSelect={() => this.dwR(4)}>
                        4
                      </Dropdown.Item>
                    </DropdownButton>
                  </Form.Group>

                  <Form.Group controlId="checkCIF">
                    <Form.Check
                      type="checkbox"
                      id="CIF"
                      label="Cover Internet Fee"
                      onChange={this.changeCIF}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkCEF">
                    <Form.Check
                      type="checkbox"
                      id="CEF"
                      label="Cover Electricity Fee"
                      onChange={this.changeCEF}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkCWF">
                    <Form.Check
                      type="checkbox"
                      id="CWF"
                      label="Cover Water Fee"
                      onChange={this.changeCWF}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkPWM">
                    <Form.Check
                      type="checkbox"
                      id="PWM"
                      label="Private Washing Machine"
                      onChange={this.changePWM}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkHK">
                    <Form.Check
                      type="checkbox"
                      id="HK"
                      label="Kitchen"
                      onChange={this.changeHK}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkHR">
                    <Form.Check
                      type="checkbox"
                      id="HR"
                      label="Refigerator"
                      onChange={this.changeHR}
                    />
                  </Form.Group>
                  <Form.Group controlId="checkHTV">
                    <Form.Check
                      type="checkbox"
                      id="HTV"
                      label="TV"
                      onChange={this.changeHTV}
                    />
                  </Form.Group>
                  <Button
                    variant="outline-primary"
                    type="submit"
                    onClick={this.handleSubmit}
                    block
                  >
                    Submit
                  </Button>
                </Form>

                <br />
              </Col>
              <Col>
                <h3>Matched Apartments:</h3>
                <br />
                {this.state.result.map(each => {
                  return (
                    <div key={each["apart_key"]}>
                      <Button
                        variant="outline-primary"
                        onClick={() => this.changeWeb(each)}
                        size="lg"
                        block
                      >
                        {each.apart_key}
                      </Button>
                      <a>Location: {each["apart_addr"]}</a>
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

                <Button
                  variant="outline-primary"
                  onClick={this.handleFindAPT}
                  block
                >
                  Clear All Filter or Search
                </Button>
              </Col>
            </Row>
          </Container>
        </div>
      );
    }
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
                <Button variant="outline-primary" onClick={this.handleFindDest}>
                  Submit
                </Button>
              </Form>
              <br />
              <Modal show={this.state.showdest} onHide={this.handleCloseDest}>
                <Modal.Header>
                  <Modal.Title>
                    The distance between this apartment and your destination is:
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
                        <Col>
                          <a href={each["url"]} id="burl">
                            Checkout the Room's Website
                          </a>
                        </Col>
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

export default Index;
