import React from 'react';
import { Container, Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

import DownloadButton from './DownloadButton';

export default class Header extends React.Component {
    constructor(props) {
        super(props);

        // Check if executable or prod web server
        const isProd = /^file/.test(window.location)
            || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location);
        this.state = {
            links: [
                { link: '/', text: 'Home' },
                { link: '/help', text: 'Help' },
                { link: '/about', text: 'About' },
            ],
            downloadVisible: isProd,
        };
    }
    render() {
        return (
            <Navbar className='justify-content-between bg-secondary'>
                <Navbar.Brand href='/' className='text-white'>
                    Descriptr
                </Navbar.Brand>
                <Container fluid>
                    <Nav variant='pills' defaultActiveKey='/'>
                        {this.state.links.map((item) => (
                            <Nav.Item key={item.text} className='px-2'>
                                <Nav.Link
                                    to={item.link}
                                    eventKey={item.link}
                                    className='text-white'
                                    as={Link}>
                                    {item.text}
                                </Nav.Link>
                            </Nav.Item>
                        ))}
                    </Nav>
                    {!this.state.downloadVisible && <DownloadButton />}
                </Container>
            </Navbar>
        );
    }
}
