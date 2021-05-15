import Navigation from "components/organisms/Navigation";
import React from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import "./App.css";
import Amplify from "aws-amplify";
import { AmplifyAuthenticator, AmplifySignOut } from "@aws-amplify/ui-react";
import { AuthState, onAuthUIStateChange } from "@aws-amplify/ui-components";
import awsconfig from "./aws-exports";
import axios from "axios";
import shortid from "shortid";
import { LocalConvenienceStoreOutlined } from "@material-ui/icons";
import Dashboard from "layouts/Dashboard";

Amplify.configure(awsconfig);

const AuthStateApp: React.FunctionComponent = () => {
  const [displayedView, setDisplayedView] = React.useState("Account");
  const classes = useStyles();

  const [authState, setAuthState] = React.useState<AuthState>();
  const [user, setUser] = React.useState<any | undefined>();
  const [registrationId, setRegistrationId] = React.useState("[LOADING...]");

  React.useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData: any) => {
      setAuthState(nextAuthState);
      setUser(authData);
    });
  });

  React.useEffect(() => {
    async function fetchRegistrationId() {
      await axios
        .post(
          "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-registration-id",
          { user_id: user.username }
        )
        .then(async (response) => {
          if (response.data.success) {
            setRegistrationId(response.data.data.registration_id);
          } else if (response.data.success === false) {
            await axios
              .post(
                "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/insert-registration-info",
                { user_id: user.username, registration_id: shortid.generate() }
              )
              .then((insertResponse) => {
                console.log(insertResponse);
              });
          }
        });
    }

    if (
      user &&
      (authState === AuthState.SignedIn || registrationId === "[LOADING...]")
    ) {
      fetchRegistrationId();
    }
  }, [user, authState, registrationId]);

  const handleSidebarSelect = (pageName: string): void => {
    setDisplayedView(pageName);
  };

  return authState === AuthState.SignedIn && user ? (
    <div style={{ textAlign: "center" }}>
      <div className={classes.root}>
        <Navigation onSelect={handleSidebarSelect}>
          {
            {
              Dashboard: <Dashboard />,
              Account: (
                <React.Fragment>
                  <h1>Hello, {user.username}</h1>
                  <h2>Registration ID: {registrationId}</h2>
                  <AmplifySignOut />
                </React.Fragment>
              ),
            }[displayedView]
          }
        </Navigation>
      </div>
    </div>
  ) : (
    <AmplifyAuthenticator />
  );
};

export default AuthStateApp;
