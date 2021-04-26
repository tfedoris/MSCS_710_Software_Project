import IconButton from "@material-ui/core/IconButton";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import MenuIcon from "@material-ui/icons/Menu";
import clsx from "clsx";
import AppBar from "@material-ui/core/AppBar";
import React from "react";
import { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";

interface Props {
  onClick: () => void;
  open: boolean;
}

export default function TopAppBar({ onClick, open }: Props): ReactElement {
  const classes = useStyles();

  return (
    <AppBar
      position="fixed"
      className={clsx(classes.appBar, {
        [classes.appBarShift]: open,
      })}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          onClick={onClick}
          edge="start"
          className={clsx(classes.menuButton, { open } && classes.hide)}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap>
          Persistent drawer
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
