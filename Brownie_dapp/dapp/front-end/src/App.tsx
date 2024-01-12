import React from "react";
// import chains for networks
import { DAppProvider, ChainId } from "@usedapp/core";
// import header components for button
import { Header } from "./components/Header";
// import Main components for choosing the chain, balances, and wallets infos
import { Main } from "./components/Main";
// import container from material-ui . it act as the body formatter
import { Container } from "@material-ui/core";

function App() {
  return (
    <DAppProvider
      config={{
        supportedChains: [ChainId.Kovan, ChainId.Goerli],
        notifications: {
          //check in ms the blockchain for our transactions
          expirationPeriod: 1000,
          checkInterval: 1000,
        },
      }}
    >
      <Header />

      <Container maxWidth="md">
        <div>Hello Everybody!</div>
        <Main />
      </Container>
    </DAppProvider>
  );
}

export default App;
