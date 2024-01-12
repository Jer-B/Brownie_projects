import React, { useState, useEffect } from "react";
import { Token } from "../Main";
import { useEthers, useTokenBalance, useNotifications } from "@usedapp/core";
import { formatUnits } from "@ethersproject/units";
import { Button, Input, CircularProgress, Snackbar } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert"
import { useStakeTokens } from "../../hooks/useStakeTokens";
import {utils} from "ethers"
export interface StakeFormProps {
  token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
  const { address: tokenAddress, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(tokenAddress, account);
  const formattedTokenBalance: number = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;
  const {notifications} = useNotifications()
  // make a state hook to track the inputted amount to interact with.
  // it can be a number or a string or an array of number or string
  // import it from react
  const [amount, setAmount] = useState<
    number | string | Array<number | string>
    >(0);
  // handle the change with an event when input is being filled
  const handleInputChange = { event: React.ChangeEvent<HTMLInputElement> } => { 
  // if value is nothing then nothing otherwise cast it as a number
  const newAmount = event.target.value === "" ? "" : Number(event.target.value)
  setAmount(newAmount)
  console.log(newAmount)
}
  //grab approvement from usestaketokens
const { approveAndStake, state: approveAndStakeErc20State } = useStakeTokens(tokenAddress)
// handleinputsubmit function
const handleStakeSubmit = () => {
  // cast amount string to wei
  const amountAsWei = utils.parseEther(amount.toString())
  return approveAndStake(amountAsWei.toString())
}

// waiting for if transaction are mined or not yet
const isMining = approveAndStakeErc20State.status === "mining"
const [showErc20ApprovalSuccess, setShowErc20ApprovalSuccess] = useState(false)
const [showStakeTokenSuccess, setShowStateTokenSuccess] = useState(false)

const handleCloseSnack = () => {
  setShowErc20ApprovalSuccess(false)
  setShowStateTokenSuccess(false)
}
// useEffect for notifications
useEffect(() => { 
  if (notifications.filter(notification) => notification.type === "transactionSucceed" && notification.transactionName === "Approve ERC20 Transfer").lentgh > 0 { 
  setShowErc20ApprovalSuccess(true)
  setShowStateTokenSuccess(false)
}
if (notifications.filter((notification) => notification.type === "transactionSuccedd" && notification.transactionName === "stakeTokens").length > 0 { 
  setShowErc20ApprovalSuccess(false)
  setShowStateTokenSuccess(true)
})
}, [notifications,showErc20ApprovalSuccess, showStakeTokenSuccess])
  return (
    <>
      <div>
      <Input onChange={handleInputChange} />
      <Button onClick={handleStakeSubmit} color="primary" size="large" disabled={ isMining}>
        {isMining ? <CircularProgress size={ 26} /> : "Stake!"} 
        </Button></div>
      <SnackBar open={showErc20ApprovalSuccess} autoHideDuration={5000} onClose={handleCloseSnack}>
        <Alert onClose={handleCloseSnack} severity="success">
          ERC-20 use approved! Waiting confirmation for staking.
        </Alert>
      </SnackBar>
            <SnackBar open={showStakeTokenSuccess} autoHideDuration={5000} onClose={ handleCloseSnack}>
            <Alert onClose={handleCloseSnack} severity="success">
              Token stake success.
            </Alert>
          </SnackBar>
    </>
  );
};
