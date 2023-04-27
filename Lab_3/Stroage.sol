// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract Storage {

    struct User {
        uint lastUpdate; // last counter update time
        string name;  // user name
        string surname; // user surname
        string location;   // user address
        uint data; // counter value
    }

    User[] private users;

    constructor() {
        users.push(User({
            lastUpdate: 0,
            name: "Admin",
            surname: "Admin",
            location: "Admin",
            data: 0
        }));
    }

    function createUser(string memory name, string memory surname, string memory location, uint data) public {
        users.push(User({
            lastUpdate: block.timestamp,
            name: name,
            surname: surname,
            location: location,
            data: data
        }));
    }

    function getLastUserId() public view returns(uint) {
        return users.length - 1;
    }

    function getName(uint id) public view returns (string memory){
        return users[id].name;
    }

    function setName(uint id, string memory userName) public {
        users[id].name = userName;
    }

    function getSurName(uint id) public view returns (string memory){
        return users[id].surname;
    }

    function setSurName(uint id, string memory userSurName) public {
        users[id].surname = userSurName;
    }

    function getLocation(uint id) public view returns (string memory){
        return users[id].location;
    }

    function setLocation(uint id, string memory location) public {
        users[id].location = location;
    }

    function send(uint id, uint counterData) public {
        if (block.timestamp >= (users[id].lastUpdate + 4 weeks)) {
            users[id].data = counterData;
        }
    }

    function get(uint id) public view returns (uint){
        return users[id].data;
    }
}