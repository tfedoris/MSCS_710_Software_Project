import Navigation from "components/organisms/Navigation";
import React from "react";
import { useStyles } from "themes/DynamicDrawerTheme";

const App = (): JSX.Element => {
  const [displayedView, setDisplayedView] = React.useState(<div />);
  const classes = useStyles();

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

  return (
    <div style={{ textAlign: "center" }}>
      <div className={classes.root}></div>
    </div>
  );
};

export default App;
