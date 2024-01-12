// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// Stake token (deposit)
// unstake (withdrawals)
// issue dapptokens as rewards
// add allowed tokens for staking
// get eth value

// Onlyowner
import "@openzeppelin/contracts/access/Ownable.sol";
// IERC20 (TransferFrom)
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
// AggregatorV3Interface
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    //Address array for allowed token
    address[] public allowedTokens;

    // address array of stackers
    address[] public stakers;

    //IERC20
    IERC20 public dappToken;

    // map token address to the staking address pointing to their deposited amount
    mapping(address => mapping(address => uint256)) public stakingBalance;

    // map token staked per adress
    mapping(address => uint256) public uniqueTokenStaked;

    // map token address to its own pricefeed address
    mapping(address => address) public tokenPriceFeedMapping;

    // constructor of the DappToken
    constructor(address _dappTokenAddress) public {
        // store dapptoken as global variable using ierc20 library
        dappToken = IERC20(_dappTokenAddress);
    }

    // set the price of an associated token to its pricefeed
    function setPriceFeedContract(address _token, address _priceFeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    // function issuing rewards to stakers
    function issueTokens() public onlyOwner {
        //loop through stakers list
        for (
            uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
            stakersIndex++
        ) {
            //one at the time grab recipient
            address recipient = stakers[stakersIndex];
            // send reward based on their total value locked
            uint256 userTotalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    // get the user's total value locked
    // instead of having a claiming option which is very gas efficient we are gonna loop through users and send them the tokens
    function getUserTotalValue(address _user) public view returns (uint256) {
        // initialize a total value locked to 0
        uint256 totalValue = 0;
        // require users to have at least 1 token from uniques tokens list to be able to receive their reward
        require(
            uniqueTokenStaked[_user] > 0,
            "You aren't staking in da house !"
        );

        // loop through allowed token to know the amount token staked.
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            // total value += actual total value + each single token value
            // after convertion into a same asset as the asset used to calculate the reward ratio
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _user,
                    allowedTokens[allowedTokensIndex]
                );
        }
        return totalValue;
    }

    // calculate single tokens value for the reward ratio
    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        // if 1 eth staked and price is 2000$ return 2000$
        // if 200$ of dai return 200$

        // if user stakedtoken is 0 do not block it, they might have a different token staked which isnt 0.
        if (uniqueTokenStaked[_user] <= 0) {
            return 0;
        }

        // get the price of a token then multiply by users staking balance of that token
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return ((stakingBalance[_token][_user] * price) / (10**decimals));
    }

    // get the value of a token using chainlink pricefeed
    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        // priceFeedAddress of the _token paramaeter
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        //decimals
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    //function for staking tokens
    // amount + address of the token
    function stakeTokens(uint256 _amount, address _token) public {
        // require an amount superior than 0
        require(_amount > 0, "Amount should be more than 0!");
        // require a list of tokens to be authorized and match with whats been trying to be deposited
        require(
            tokenIsAllowed(_token),
            "This token isn't allowed for deposit."
        );
        // transfer from sender to this token farm contract, the defined amount.
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        //update users list tokens
        updateUniqueTokenStaked(msg.sender, _token);

        // staking balance from msg.sender of this token is now equal previous amount deposit + new _amount.
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        if (uniqueTokenStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    // update the deposited list of tokens for each users. Using an ID for each different tokens, internal function, only this contract can call it
    function updateUniqueTokenStaked(address _user, address _token) internal {
        // if the token stacked balance of the user is less or equal to 0, update the number of different token by one
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokenStaked[_user] = uniqueTokenStaked[_user] + 1;
        }
    }

    // function adding allowed token to the allowedToken list
    //onlyOwner can add tokens
    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    // function checking allowed token
    function tokenIsAllowed(address _token) public returns (bool) {
        // make a loop iterating through the list checking if the token address is authorized or not
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
            return false;
        }
    }

    // function to unstake staked deposit
    function unstakeToken(address _token) public {
        // fatch user balance. staking balance of the token from msg.sender
        uint256 balance = stakingBalance[_token][msg.sender];
        // only users with more than 0 staked can unstake
        require(
            balance > 0,
            "Staking balance is 0 man ! Nuthing to withdraw for you here."
        );
        // transfert the staked balance to the user
        IERC20(_token).transfer(msg.sender, balance);
        // reset staked balance of the user to 0
        stakingBalance[_token][msg.sender] = 0;
        // avoid the reentrancy attack
        uniqueTokenStaked[msg.sender] = uniqueTokenStaked[msg.sender] - 1;

        // when user staked balance is 0 remove the user from the staker array
        if (uniqueTokenStaked[msg.sender] == 0) {
            for (
                uint256 stakersIndex = 0;
                stakersIndex < stakers.length;
                stakersIndex++
            ) {
                if (stakers[stakersIndex] == msg.sender) {
                    stakers[stakersIndex] = stakers[stakers.length - 1];
                    stakers.pop();
                }
            }
        }
    }
}
