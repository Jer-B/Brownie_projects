/* eslint-disable spaced-comment*/
/// <reference types = "react-scripts"/>

// as token and supportedTokens is gonna come from main, we need to import main
import { supportedTokens } from "../Main"
import { Box, Tab, makeStyles } from "@material-ui/core"
import { TabContext, TabList, TabPanel } from "@material-ui/lab"
import React, { useState } from "react"
import {WalletBalance} from "./WalletBalance"
import { StakeForm } from "./StakeForm"
// define what yourWalletProps is gonna look like
interface yourWalletProps {
    supportedTokens: Array<Token>
    //supportedTokens is gonna be an array of Tokens
}

const useStyles = makeStyles((them) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)

    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px"
    },
    header: {
        color: "white"
    }

}))


// export YoutWallet.tsx, make it a function,

// pass as parameter supportedTokens of type yourWalletProps
export const YourWallet = ({ supportedTokens }: yourWalletProps) => {
    //StateHook for selectedtokenindex
    // default state number 0
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)
    //define the change value and function.
    // a react change event
    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        // set the state hook. parse the newvalue integer.
        setSelectedTokenIndex(parseInt(newValue))
    }
    const classes= useStyles()
    return (
        <Box>
            <h1 className={classes.header}>Your Wallet</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="stake Tab">
                        {supportedTokens.map((token, index) => {
                            return (
                                <Tab
                                    label={token.name}
                                    value={index.toString()}
                                    key={index}
                                />
                            )
                        })}
                    </TabList>
                    {supportedTokens.map((token, index)) => {
                    return(
                    <TabPanel value={index.toString()} key={index}>
                        <div className={classes.tabContent}>
                            <WalletBalance token ={supportedTokens[selectedTokenIndex]}></WalletBalance>
                            <StakeForm token ={supportedTokens[selectedTokenIndex]} />
                        </div>

                    </TabPanel>
                    )
                })}
                </TabContext>
            </Box>



        </Box>
    )
}