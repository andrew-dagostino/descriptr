import React from 'react';
import { Button, Dropdown, DropdownButton } from 'react-bootstrap';


function DownloadButton(props) {

    function getPackage(key, e) {
        let url = new URL('/api/pkg')
        url.search = new URLSearchParams({ type: key }).toString()

        // Fetch the file at GET /api/pkg?type=win|nix|mac and download
        // TODO, I actually had a hard time finding a definitive way to download a file with the
        // Fetch API, this should work. Once we have the backend /api/pkg endpoint working this
        // will need to be tested.
        fetch(url)
            .then(res => res.blob())
            .then(blob => {
                let file = window.URL.createObjectURL(blob);
                window.location.assign(file);
            });
    }

    return (
        <DropdownButton
            as={Button}
            id="dl-dropdown"
            onSelect={getPackage}
            size="sm"
            title="Download Desktop App"
        >
            <Dropdown.Item eventKey="win">Windows</Dropdown.Item>
            <Dropdown.Item eventKey="nix">Linux</Dropdown.Item>
            <Dropdown.Item eventKey="mac">MacOS</Dropdown.Item>
        </DropdownButton>
    );
}

export default DownloadButton;
