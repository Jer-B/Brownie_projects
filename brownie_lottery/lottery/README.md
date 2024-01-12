Lottery contract behaviour:
1. Users can enter lottery with ETH based on USD fee
ETH / USD conversion

2. An admin will choose when lottery ends (not decentralized since there is an admin, but  a DAO or a set time / block (chainlink keepers https://docs.chain.link/docs/chainlink-keepers/introduction/) can be put in place for full decentralization)

3. Winner is randomly selected
------------------------------------
Tests

1. 'mainnet_test_fork' brownie / alchemy
2. 'development' brownie / ganache
3. 'Testnet'
------------------------------------
Useful links:
Chainlink latest price -> https://docs.chain.link/docs/get-the-latest-price/
ETH / USD price feed addresses -> https://docs.chain.link/docs/ethereum-addresses/
Chainlink VRF for randomless -> https://docs.chain.link/docs/get-a-random-number/v1/

Alchemy, to support forked mainnet -> https://www.alchemy.com/

kovan faucets -> https://docs.chain.link/docs/link-token-contracts/#kovan


------------------------------------
Details:

Python / Solidity ^0.6.6/ Brownie

!!!! To debug Brownie or when running test on wsl at each session if multiple different version of nvm installed choose this one before running any brownie commands !!!!

to input in terminal->               nvm use 16.13.2

