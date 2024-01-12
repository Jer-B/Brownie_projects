from importlib.abc import Loader
from scripts.helpful_scripts import get_account, get_contract
from brownie import DappToken, TokenFarm, network, config
from web3 import Web3
import yaml
import json
import os
import shutil

# keep 100 dapp token (ratio 1:1) for tests
KEPT_BALANCE = Web3.toWei(100, "ether")

# add the front-end update as False in the parameter
def deploy_token_farm_and_dapp_token(front_end_update=False):
    # get account
    account = get_account()
    # deploy dappToken
    dapp_token = DappToken.deploy({"from": account})
    # deploy token farm
    # token farm takes one parameter, the dapptoken which it needs for being able to give it as a reward
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # at deployment send dapptoken to the contract minus a sum for test purpose signed from account
    # the kept balance as global variable
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    # 1 block confirmation
    tx.wait(1)
    # 3 tokens allowed WETH DAI/FAU DAPPTOKEN (pretend that FAU (faucet token ) is DAI)
    # weth_token: '0xd0a1e359811322d97991e03f863a0c30c2cf029c'
    # fau_token: '0xFab46E002BbF0b4509813474841E0716E6730136'
    # dai_usd_price_feed: '0x777A68032a88E5A84678A77Af2CD65A7b3c0775a'
    # eth_usd_price_feed: '0x9326BFA02ADD2366b30bacB125260Af641031331'
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")

    # dictionary key: Token, Value: pricefeed of the token
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    # run the front end update, if parameter is True
    if front_end_update:
        update_front_end()
    return token_farm, dapp_token


# function for adding token and loop through for adding


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from", account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from", account}
        )
        set_tx.wait(1)
    return token_farm


# function to update our front end with all deployed addresses of our contracts and tokens
# convert yaml to json and send it to the front in a json format for typescript to use it
def update_front_end():
    # send the build folder to chain-info
    copy_folders_to_front_end("./build", "./front-end/src/chain-info")
    # conver yaml to json and send it over to front-end
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        # write the dictionary into a brownie-config.json file to the src folder of the front-end
        with open("./front-end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("front-end updated!")


# send the build folder to the front end
def copy_folders_to_front_end(src, dest):
    # import OS and Shutil
    # if the build folder exist in destination , delete it
    if os.path.exists(dest):
        shutil.rmtree(dest)
    # then copy to the a new build folder
    # so it will work as an update
    shutil.copytree(src, dest)


def main():
    deploy_token_farm_and_dapp_token(front_end_update=True)
    # so at each deployment to rinkeby or kovan front-end will be automatically updated
