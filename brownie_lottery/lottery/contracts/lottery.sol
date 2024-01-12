// behaviour:

// function to enter the lottery:
// -- minimum payment
// -- keep track of wallets address entering
// -- payable function as a payment to enter is required else revert
// Function for conversion rate, need to get latest price feed (Aggregatorv3Interface)
// Function for only owner to start and ends lottery period -> only owner = contract sender
// Function for random winner
// Function for only winner to withdraw or get funds minus tx fees
// after winner get his price, reset players list for another round

// SPDX-License-Identifier: MIT;

pragma solidity ^0.6.6;

// Latest price
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
// Onlyowner
import "@openzeppelin/contracts/access/Ownable.sol";
// import VRF consumer base contract
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

// inherit VRF and ownable (onlyowner)
contract lottery is VRFConsumerBase, Ownable {
    //Keep track of registered players in a list
    address payable[] public players;

    //Winner address
    address payable public recentWinner;

    //Entrance fee in USD value
    uint256 public usdEntryFee;

    // recent random number
    uint256 public randomness;

    // Set AggregV3 as a variable, grab priceFeed address to interact with from config file
    AggregatorV3Interface internal priceFeed;

    // Create a lottery state End / Start
    // to avoid people to be able to enter if not started or already ended or when calculating a winner
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    // do a variable corresponding to the lottery_state "array"
    LOTTERY_STATE public lotteryStatus;
    // link token fee
    uint256 public fee;
    // add keyhash
    bytes32 public keyhash;
    // Event to fire the result or to request a randomnumber for security
    event requestedRandomness(bytes32 requestId);

    // constructor to define various settings at contract deployment
    // constructor input is an pricefeed address, which will be passed to priceFeed
    // add inherited VRF constructor (coordinator and link addresses as parameters)
    // add a VRF coordinator and link addresses variables as paramaeter to main constructor
    // add Fee
    constructor(
        address _priceFeed,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        //$50 fee times 10 raised to the 18th units in wei
        usdEntryFee = 50 * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeed);
        lotteryStatus = LOTTERY_STATE.CLOSED; // can be = to 1 but less readable
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // require lottery to be open
        require(
            lotteryStatus == LOTTERY_STATE.OPEN,
            "Lottery isn't not open, can't enter"
        );
        //Minimum required $50 else revert and return error
        require(msg.value >= getEntranceFee(), "Not enough ETH to enter");
        //push new addresses to the list
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (
            ,
            /*uint80 roundID*/
            int256 price, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = priceFeed.latestRoundData();

        //cast price to !uint256!
        //and as solidity doesnt works with decimals -> 10 ** 10 as our price feed is up to 18 decimals
        uint256 adjustedPrice = uint256(price) * 10**10;
        // adding 18 more decimals to usdEntrefee to be able to divide using a really big number
        //additional decimals will be cancelled out by our latest pricefeed
        uint256 costToEntry = (usdEntryFee * 10**18) / adjustedPrice;
        return uint256(costToEntry);
    }

    // conversion rate ETH to USD value
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethAmountInUSD = getEntranceFee();
        return ethAmountInUSD;
    }

    function fundLottery() public {}

    //lottery opening and ending is managed by an admin
    function startLottery() public onlyOwner {
        // to start a new lottery it requires to have been or to be closed first, like a door
        require(
            lotteryStatus == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery round yet !"
        );
        // open lottery
        lotteryStatus = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lotteryStatus == LOTTERY_STATE.CALCULATING_WINNER);

        // pseudo randomness to NOT USE!
        // concept of exploit of meebits for "randomness"
        // in that case miners can win any lottery they want using pseudo randomness as they got the key for difficulty
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce, // transaction number is predictable
        //             msg.sender, // predictable
        //             block.difficulty, // can be altered by miners
        //             block.timestamp // is predictable
        //         )
        //     )
        // ) % players.length;

        //At closing choose the winner
        lotteryStatus = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestID = requestRandomness(keyhash, fee);
        emit requestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestID, uint256 _randomness)
        internal
        override
    {
        // to fulfill the request verify lottery states, and randomness value as a number
        require(
            lotteryStatus == LOTTERY_STATE.CALCULATING_WINNER,
            "Wrong Lottery status!"
        );
        require(_randomness > 0, "Random number isn't valid.");

        // select winner by random number % players number
        // winner result equals to the corresponding players array index
        uint256 select_winner = _randomness % players.length;
        recentWinner = players[select_winner];
        // transfer the entire lottery funds to winner
        recentWinner.transfer(address(this).balance);
        // reset lottery players array to 0
        players = new address payable[](0);
        // reset lottery state
        lotteryStatus = LOTTERY_STATE.CLOSED;
        // recent random number
        randomness = _randomness;
    }
}
