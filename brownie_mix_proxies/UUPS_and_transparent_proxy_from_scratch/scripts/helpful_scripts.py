from brownie import network, config, accounts
import eth_utils

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

# Added Mainnet blockchain list
FORKED_LOCAL_ENVIRONMENTS = ["mainnet_test_fork"]

# Added dev blockcahins list
LOCAL_BLOCKCHAINS_ENVIRONMENTS = ["development", "eth_local"]


def get_account():
    # change this : if network.show_active() == "development"
    # to below line
    if (
        network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENTS
        or FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Default chain, Default account 0")
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


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


# initializer Transparent proxy

# Start from none and next parameter can be any number
# initializer = box.store, 1


def encode_function_data(initializer=None, *args):
    # if args is zero it will be an issue
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


# depending on if with use an ProxyAdmin contract or using an initializer function there is couple way to upgrade contracts.
# the way that will be use here, is to wrap everything together in its own function
def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args,
):
    # if there is a proxy admin contract check if there is an initializer
    if proxy_admin_contract:
        if initializer:
            # if there is an initializer encode data
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            # if no initializer, we dont need to encode data
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    # if there is no ProxyAdmin contract
    else:
        # check if there is an initializer
        if initializer:
            # if there is an initializer encode data
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            # if there is no initializer
            transaction = proxy_admin_contract.upgradeTo(
                new_implementation_address, {"from": account}
            )
    return transaction
