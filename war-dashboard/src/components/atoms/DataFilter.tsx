import { TextField, TextFieldProps } from "@material-ui/core";
import MenuItem from "@material-ui/core/MenuItem";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import React, { ReactElement } from "react";
import moment from "moment";

type Props = TextFieldProps;

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    textField: {
      // padding: theme.spacing(2),
    },
    input: {
      // padding: theme.spacing(2),
      color: "#a1a1a1",
    },
  })
);

export default function DataFilter({
  label = "Filter Data",
  fullWidth = true,
  InputLabelProps,
  disabled = false,
  onChange,
  ...props
}: Props): ReactElement {
  const classes = useStyles();

  const [selectedValue, setSelectedValue] = React.useState("");
  const [now, setNow] = React.useState(moment());
  const [lastMinute, setLastMinute] = React.useState(
    now.subtract(60, "seconds").toString()
  );
  const [lastHour, setLastHour] = React.useState(
    now.subtract(60, "minutes").toString()
  );
  const [lastDay, setLastDay] = React.useState(
    now.subtract(24, "hours").toString()
  );

  React.useEffect(() => {
    setNow(moment());
  }, []);

  React.useEffect(() => {
    setLastMinute(now.subtract(60, "seconds").toString());
    setLastHour(now.subtract(60, "minutes").toString());
    setLastDay(now.subtract(24, "hours").toString());
  }, [now]);

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedValue(event.target.value as string);
    console.log(event.target.value as string);
  };

  return (
    <TextField
      select
      value={selectedValue}
      onChange={handleChange}
      className={classes.textField}
      style={{ textAlign: "left" }}
      disabled={disabled}
      variant="outlined"
      label={label}
      required={false}
      fullWidth={true}
      InputLabelProps={{
        className: classes.input,
        ...InputLabelProps,
      }}
    >
      <MenuItem value={lastMinute}>Last 60 Seconds</MenuItem>
      <MenuItem value={lastHour}>Last 60 Minutes</MenuItem>
      <MenuItem value={lastDay}>Last 24 Hours</MenuItem>
    </TextField>
  );
}
