from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    # Box retrieve()
    print(box.retrieve())

    # Box increment() || return an error as deployed contract doesnt have increment
    # print(box.increment())

    # Add Proxy Admin
    # Set the Admin to be this contract
    # This is the initializer function for UpgradeAndCall function in the proxyAdmin contract
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # Add Transparent Proxy
    # set the initializer
    initializer = box.store, 1
    # run it blank
    box_encoded_initializer_function = encode_function_data()

    # proxy = transparent proxy's Implementation Address, Admin, and initializer data, signed from which account with a gas limit
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy} . Can Upgrade to V2")

    # call a function on the proxy
    # we are assigning to proxy.address the box abi
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    # and delegate the call to the box
    print(proxy_box.retrieve())

    # deploy BoxV2
    box_v2 = BoxV2.deploy({"from": account})
    # call the upgrade function
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(box.retrieve())
