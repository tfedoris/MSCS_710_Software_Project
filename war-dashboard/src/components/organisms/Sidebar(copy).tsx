import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";

import AccountTreeIcon from "@material-ui/icons/AccountTree";
import ListAltIcon from "@material-ui/icons/ListAlt";
import LocalPharmacyIcon from "@material-ui/icons/LocalPharmacy";
import BusinessIcon from "@material-ui/icons/Business";
import DashboardIcon from "@material-ui/icons/Dashboard";
import ContactsIcon from "@material-ui/icons/Contacts";

import { createStyles, Theme, makeStyles } from "@material-ui/core/styles";
import React from "react";

const drawerWidth = 240;

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    drawer: {
      width: drawerWidth,
      flexShrink: 0,
    },
    drawerPaper: {
      width: drawerWidth,
    },
    // necessary for content to be below app bar
    toolbar: theme.mixins.toolbar,
  })
);

interface Props {
  onSelect?: (pageName: string) => void;
}

export default function Sidebar({ onSelect }: Props): JSX.Element {
  const classes = useStyles();
  const [selectedIndex, setSelectedIndex] = React.useState(0);

  const handleListItemClick = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>,
    index: number,
    name: string
  ) => {
    setSelectedIndex(index);

    if (onSelect) {
      onSelect(name);
    }
  };

  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
      anchor="left"
    >
      <div className={classes.toolbar} />
      <Divider />
      <List component="nav">
        {["Dashboard", "Inventory"].map((text, index) => (
          <ListItem
            button
            key={text}
            selected={selectedIndex === index}
            onClick={(event) => handleListItemClick(event, index, text)}
          >
            <ListItemIcon>
              {
                {
                  Dashboard: <DashboardIcon />,
                  Inventory: <ListAltIcon />,
                }[text]
              }
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List component="nav">
        {[
          "Organizations",
          "Fullfillment Groups",
          "Fullfillment Centers",
          "Pharmacies",
          "Contacts",
        ].map((text, index) => (
          <ListItem
            button
            key={text}
            selected={selectedIndex === index + 2}
            onClick={(event) => handleListItemClick(event, index + 2, text)}
          >
            <ListItemIcon>
              {
                {
                  Organizations: <AccountTreeIcon />,
                  "Fullfillment Groups": <AccountTreeIcon />,
                  "Fullfillment Centers": <BusinessIcon />,
                  Pharmacies: <LocalPharmacyIcon />,
                  Contacts: <ContactsIcon />,
                }[text]
              }
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}
