// import usethers
import {useEthers} from '@usedapp/core'
// import material ui package to use its styling
import {Button, makeStyles} from '@material-ui/core'

// make a global constant for the style
const usestyles = makeStyles((theme) => ({
    // do a container style which will be affected to the the button
    container: {
        //style. separated by comas
        padding: theme.spacing(4),
        display: "flex",
        justifyContent: "flex-end",
        gap: theme.spacing(1)
    }
}))

// export a constant variable called header, which is a function doing whats in brackets
export const Header = () => {
    //affect the container to the export
    const classes = usestyles()
    const{account, activateBrowserWallet, deactivate}=useEthers()

    // constant variable checking if connected or not
    const isConnected = account !== undefined
    // a way to use id statement , if account is not undefined then account is connected.

    // if connected return a button to connect to
    return(
        // ? -> question mark is a tertiary operator meaning if it is True we do one thing, 
        //if it is False we do something else at the colon mark ->  : 
        // if connected there is a button for disconnection
        // if not show a connect button
                //wrap the whole into the styled container from above
    <div className={classes.container}>
        <div>
            {isConnected ? 
            (
            <Button variant="contained" color="secondary" onClick = {deactivate}>
                Disconnect
            </Button>
            ) 
            : 
            (
                <Button variant="contained" color="secondary" onClick={activateBrowserWallet}>
                    Connect
                </Button>
            )
            }
        </div>
    </div>
    )
}