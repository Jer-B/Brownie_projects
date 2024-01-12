/* eslint-disable spaced-comment*/
/// <reference types = "react-scripts"/>

//import token from main
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "@ethersproject/units";
import { Token } from "../Main";
import { BalanceMsg } from "../BalanceMsg";
//export walletbalanceprops interface
export interface WalletBalanceProps {
  token: Token;
}
//export the function to show the balance of the selected token
export const WalletBalance = ({ token }: WalletBalanceProps) => {
  //grab tokens infos
  const { image, address, name } = token;
  //grab wallet account
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(address, account);
  // format the number of tokenbalance, parsed in a float number otherwise it s gonna be 0
  const formattedTokenBalance: number = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;
  return (
    <BalanceMsg
      label={"Your unstake ${name} balance."}
      tokenImgSrc={image}
      amount={formattedTokenBalance}
    />
  );
};
