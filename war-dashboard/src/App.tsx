import Navigation from "components/organisms/Navigation";
import React from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import "./App.css";
import Amplify from "aws-amplify";
import { AmplifyAuthenticator, AmplifySignOut } from "@aws-amplify/ui-react";
import { AuthState, onAuthUIStateChange } from "@aws-amplify/ui-components";
import awsconfig from "./aws-exports";

Amplify.configure(awsconfig);

const AuthStateApp: React.FunctionComponent = () => {
  const [displayedView, setDisplayedView] = React.useState(<div />);
  const classes = useStyles();

  const [authState, setAuthState] = React.useState<AuthState>();
  const [user, setUser] = React.useState<any | undefined>();

  React.useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData) => {
      setAuthState(nextAuthState);
      setUser(authData);
    });
  }, []);

  const handleSidebarSelect = (pageName: string): void => {
    switch (pageName) {
      case "Dashboard":
        setDisplayedView(<h1>Dashboard</h1>);
        break;
      case "Account":
        setDisplayedView(<h1>Account</h1>);
        break;
      default:
        setDisplayedView(<div />);
    }
  };

  return authState === AuthState.SignedIn && user ? (
    <div style={{ textAlign: "center" }}>
      <div className={classes.root}>
        <Navigation onSelect={handleSidebarSelect}>
          <div className="App">
            <div>Hello, {user.username}</div>
            <AmplifySignOut />
          </div>
        </Navigation>
      </div>
    </div>
  ) : (
    <AmplifyAuthenticator />
  );
};

export default AuthStateApp;
