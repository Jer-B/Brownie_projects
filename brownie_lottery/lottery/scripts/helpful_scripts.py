from brownie import (
    network,
    config,
    accounts,
    VRFCoordinatorMock,
    MockV3Aggregator,
    LinkToken,
    Contract,
)

# --------------
# Modification following refactoring
# --------------
# add mockv3aggregator to brownie import and web3
# decimals and initial_answer in constant / static variables
from web3 import Web3

# --------------
# Modification after refactoring when making scripts to interact with fund and withdraw function
# --------------
# Actually the price feed for the pair ETH - USD is 8 decimals
# value before change Decimals -> 18 and starting price -> 2000
# so put value to 8 decimals and starting price to 2000 following by 8 zeros
DECIMALS = 8
STARTING_PRICE = 200000000000

# Add Mainnet Forked blockchain list
FORKED_LOCAL_ENVIRONMENTS = ["mainnet_test_fork", "lottery-fork"]

# Add dev blockcahins list
LOCAL_BLOCKCHAINS_ENVIRONMENTS = ["development", "eth_local"]

# --------------
# New get_account() function made for lottery
# --------------

# use index of accounts variables for it to be more robust
# accounts[0]
# accounts.add("env")
# accounrts.load("id")
def get_account(index=None, id=None):
    print("get sender account...")
    # if we pass an index return accounts[index number]
    if index:
        return accounts[index]
        # otherwise if we pass an ID return accounts.load("ID")
    elif id:
        return accounts.load(id)
    # otherwise depending on the blockchain return accounts[0]
    elif (
        network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Default chain, Default account 0")
        return accounts[0]
    # else default account if no other account specified
    return accounts.add(config["wallets"]["from_key"])


# -------------
# Previously used get_account() function
# -------------

# def get_account():
#     # change this : if network.show_active() == "development"
#     # to below line
#     if (
#         network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENTS
#         or FORKED_LOCAL_ENVIRONMENTS
#     ):
#         print("Default chain, Default account 0")
#         return accounts[0]
#     else:
#         return accounts.add(config["wallets"]["from_key"])


# -----------
#  Contracts
# -----------
# remapping contracts for contract_type
contract_to_mock = {
    # contract : of type
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """Grab contract addresses from brownie-config if defined
    else deploy a mock and return the mock
        Use:
             Args:
                 contract_name(string)

             Returns:
                 The most recent deployed project contract => [-1].
                 brownie.network.contract.ProjectContract
    """
    # defining type of contract related to the mappings
    contract_type = contract_to_mock(contract_name)
    # if local chain, check if already deployed contract exist
    print("checking chain...")
    if network.show_active in LOCAL_BLOCKCHAINS_ENVIRONMENTS:
        if len(contract_type) <= 0:  # equivalent of-> if MockV3Aggregator.length <= 0
            print("Development chain detected...")
            print("no mock detected, create deployment for it...")

            mock_v3_deploy()
        # else

        print("Found an existing mock contract, grabbing the last one deployed...")
        contract = contract_type[-1]
    # else (if not local chains) get contract ABI and address using Contract.from_abi package and function of brownie
    # to grab contract addresses from config file
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # Address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # from the name of the contract_type, it's address, and abi
        # any contracts has an .abi and ._name attribute corresponding to getting their ABI or Name
    return contract

    print("checking chain...")
    # deploy the contract lottery from our wallets as sender
    # -----------------------
    if network.show_active() not in LOCAL_BLOCKCHAINS_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print(network.show_active(), " network detected, grabbing price feed...")
    else:
        print("Development chain detected...")
        if len(MockV3Aggregator) <= 0:
            print("no mock detected, create deployment for it...")

            mock_v3_deploy()
        print("Found a mock, grabbing the last one deployed...")
        price_feed_address = MockV3Aggregator[-1].address
        print(f"Price feed result:{price_feed_address}")

    lottery_deploying = lottery.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract Deployed")
    return lottery_deploying


# skip or not contract verification depending of the chain in use
def verify_contracts():
    # first modification change this : if network.show_active() == "development"
    # second modification change this : if network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENTS:
    # to below line
    if (
        network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENTS
        or FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Default chain, skip contract verification")
        return False
    else:
        return True


# flexible rpc connection
# def flexible_price_feed():
#    if network.show_active() == "development":
#        print("No price on development chain to match")
#        return 0
#    else:
#        return "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"


# --------------
# Modification following refactoring
# --------------
# add mockv3aggregator function
# instead of {"from": account} use {"from": get_account()}

# --------------
# Modification after refactoring when making scripts to interact with fund and withdraw function
# --------------
# Hard code decimals and starting price values instead of using web3 conversion with toWei
# line that changed ->DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}


def mock_v3_deploy():
    if len(MockV3Aggregator) <= 0:
        print(
            f"{network.show_active()} network detected. Access MockV3Aggregator for price feed."
        )  # mock_deploy =
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mock deployment done. Get price_feed from it...")


# fund lottery with link token
def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
