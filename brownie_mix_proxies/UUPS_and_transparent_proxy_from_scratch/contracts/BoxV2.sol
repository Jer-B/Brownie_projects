// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract BoxV2 {
    // store and retrieve some type of value
    // same contract as Box but with an additional function of increment
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function store(uint256 newValue) public {
        value = newValue;

        emit ValueChanged(newValue);
    }

    function retrieve() public view returns (uint256) {
        return value;
    }

    // additional function increment
    function increment() public {
        value = value + 1;
        emit ValueChanged(value);
    }
}
