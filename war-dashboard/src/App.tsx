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
import DarkIcon from "@material-ui/icons/Brightness4";
import LightIcon from "@material-ui/icons/Brightness7";
import Dashboard from "layouts/Dashboard";
import Typography from "@material-ui/core/Typography";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import { IconButton, Tooltip } from "@material-ui/core";
import RefreshButton from "components/atoms/RefreshButton";

Amplify.configure(awsconfig);

const AuthStateApp: React.FunctionComponent = () => {
  const [displayedView, setDisplayedView] = React.useState("Account");
  const classes = useStyles();

  const [authState, setAuthState] = React.useState<AuthState>();
  const [user, setUser] = React.useState<any | undefined>();
  const [registrationId, setRegistrationId] = React.useState("[LOADING...]");
  const [darkMode, setDarkMode] = React.useState(
    localStorage.getItem("dark-mode") === "true"
  );
  const [refresh, toggleRefresh] = React.useState(false);

  const theme = React.useMemo(
    () =>
      createMuiTheme({
        palette: {
          type: darkMode ? "dark" : "light",
        },
      }),
    [darkMode]
  );

  React.useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData: any) => {
      setAuthState(nextAuthState);
      setUser(authData);
    });
  });

  React.useEffect(() => {
    localStorage.setItem("dark-mode", darkMode.toString());
  }, [darkMode]);

  React.useEffect(() => {
    async function fetchRegistrationId() {
      await axios
        .post(
          "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-registration-id",
          { user_id: user.username }
        )
        .then(async (response) => {
          if (response.data.success) {
            console.log(response.data.data);
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

    if (user) {
      fetchRegistrationId();
    }
  }, [registrationId, user, refresh]);

  const handleSidebarSelect = (pageName: string): void => {
    setDisplayedView(pageName);
  };

  return authState === AuthState.SignedIn && user ? (
    <ThemeProvider theme={theme}>
      <div style={{ textAlign: "center" }}>
        <div className={classes.root}>
          <Navigation
            onSelect={handleSidebarSelect}
            themeButton={
              <Tooltip title="Toggle Theme">
                <IconButton onClick={() => setDarkMode(!darkMode)}>
                  {darkMode ? (
                    <LightIcon style={{ color: "white" }} />
                  ) : (
                    <DarkIcon style={{ color: "white" }} />
                  )}
                </IconButton>
              </Tooltip>
            }
            username={user.username}
            signoutButton={<AmplifySignOut />}
          >
            {
              {
                Dashboard: <Dashboard registrationId={registrationId} />,
                Account: (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                      height: "80vh",
                    }}
                  >
                    <Typography variant="h1">Hello, {user.username}</Typography>
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "center",
                        alignItems: "center",
                      }}
                    >
                      <Typography
                        variant="h2"
                        style={{
                          textDecorationLine: "underline",
                        }}
                      >{`Registration ID: `}</Typography>
                      <Typography
                        variant="h2"
                        style={{
                          whiteSpace: "break-spaces",
                          fontWeight: "bold",
                          color: "#FF9900",
                        }}
                      >
                        {` ${registrationId}`}
                      </Typography>
                      <RefreshButton
                        onToggleRefresh={() => toggleRefresh(!refresh)}
                      />
                    </div>
                  </div>
                ),
              }[displayedView]
            }
          </Navigation>
        </div>
      </div>
    </ThemeProvider>
  ) : (
    <AmplifyAuthenticator />
  );
};

export default AuthStateApp;
