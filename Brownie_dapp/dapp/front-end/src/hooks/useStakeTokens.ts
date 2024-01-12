import { useEffect, useState } from "react";
import { useEthers, useContractFunction } from "@usedapp/core";
import { constants, utils } from "ethers";
import TokenFarm from "../chain-info/contracts/TokenFarm.json";
import ERC20 from "../chain-info/contracts/MockERC20.json";
import networkMapping from "../chain-info/deployments/map.json";
import { Contract } from "@ethersproject/contracts";

//function to use tokens for staking. parameter is the token address
export const useStakeTokens = (tokenAddress: string) => {
  // to do for approving the stake
  // grab the chainId we are using for our contract
  const { chainId } = useEthers();
  // the abi of contracts
  const { abi } = TokenFarm;
  // addresses
  // tokenfarm contract address from network, at position 0 for the most recent one, else a zero address
  const tokenFarmAddress = chainId
    ? networkMapping[string(chainId)]["TokenFarm"][0]
    : constants.AddressZero;
  // grab the contract interface
  const tokenFarmInterface = new utils.Interface(abi);
  const tokenFarmContract = Contract(tokenFarmAddress, tokenFarmInterface);

  // to work with the ERC20 token
  const erc20ABI = ERC20.abi;
  const erc20Interface = new utils.Interface(erc20ABI);
  const erc20Contract = new Contract(tokenAddress, erc20Interface);
  // now that we have the contract we can call the approve function first.

  const { send: approveErc20Send, state: approveAndStakeErc20State } =
    useContractFunction(erc20Contract, "Approve", {
      transactionName: "Approve ERC20 Transfer",
    });
  const approveAndStake = (amount: string) => {
    setAmountToStake(amount)
    return approveErc20Send(tokenFarmAddress, amount);
  };

  const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stakeTokens", {
    transactionName : "stakeTokens"
  })

  // state hook for how much we want to actually stake
  const [amountToStake, setAmountToStake] = useState("0")

  // useEffect allow us to do something when another variable has changed
  // we need to call stake adter it's being approved.
  useEffect(() =>) { 
    if (approveAndStakeErc20State.status === "Success") { 
      //stake function
      stakeSend(amountToStake, tokenAddress)
    }
    //use an array of different things we want to track
    // and if anything in that array change, useEffect will kickoff and do what we asked it to do
  }, [approveAndStakeErc20State, amountToStake, tokenAddress])
  
  const [state, setState] = useState(approveAndStakeErc20State)
  //track both approving and staking

  useEffect(() => { 
    if (approveAndStakeErc20State.status === "Success") { 
      setState(stakeState)
    }
    else {
      setState(approveAndStakeErc20State)
    }
  }, [approveAndStakeErc20State, stakeState])
  //const [state, setState] = useState(approveErc20State);
  return { approveAndStake, state };
};
