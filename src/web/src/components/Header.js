import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

export default class Header extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            links: [
                { link: '/', text: 'Home' },
                { link: '/help', text: 'Help' },
                { link: '/about', text: 'About' },
            ],
        };
    }
    render() {
        return (
            <Navbar className='justify-content-between bg-secondary'>
                <Navbar.Brand href='/' className='text-white'>
                    Descriptr
                </Navbar.Brand>
                <Nav variant='pills' defaultActiveKey='/'>
                    {this.state.links.map((item) => (
                        <Nav.Item key={item.text} className='px-2'>
                            <Nav.Link href={item.link} className='text-white'>
                                {item.text}
                            </Nav.Link>
                        </Nav.Item>
                    ))}
                </Nav>
            </Navbar>
        );
    }
}
