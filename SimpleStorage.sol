// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SampleStorage {
    uint256 public storedNum;

    function showNum(uint _storedNum) public virtual {
        storedNum = _storedNum;
        readData();
    }

    function readData() public view returns (uint256) {
        return storedNum;
    }

    struct People {
        uint age;
        string name;
    }
    People public person = People({name: "Adam", age: 549});
    People[] public persons;

    // calldata, memory, storage
    mapping(string => uint) public nameToAge;

    function addPeople(uint age, string memory _name) public {
        persons.push(People(age, _name));
        nameToAge[_name] = age;
    }

    function viewPerson(uint personsIndex) public returns (uint) {
        person = persons[personsIndex];
        return person.age;
    }
}
