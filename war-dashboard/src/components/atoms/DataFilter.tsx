import { TextField, TextFieldProps } from "@material-ui/core";
import MenuItem from "@material-ui/core/MenuItem";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import React, { ReactElement } from "react";
import moment from "moment";

interface Props {
  onChange: (timeframe: Object) => void;
  refresh: boolean;
}

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

export default function DataFilter({ onChange, refresh }: Props): ReactElement {
  const classes = useStyles();

  const [selectedValue, setSelectedValue] = React.useState("");
  const [now, setNow] = React.useState(moment().format());
  const [lastMinute, setLastMinute] = React.useState(
    moment().subtract(60, "seconds").format()
  );
  const [lastHour, setLastHour] = React.useState(
    moment().subtract(60, "minutes").format()
  );
  const [lastDay, setLastDay] = React.useState(
    moment().subtract(24, "hours").format()
  );
  const [lastWeek, setLastWeek] = React.useState(
    moment().subtract(7, "days").format()
  );

  React.useEffect(() => {
    setNow(moment().format());
    setLastMinute(moment().subtract(60, "seconds").format());
    setLastHour(moment().subtract(60, "minutes").format());
    setLastDay(moment().subtract(24, "hours").format());
    setLastWeek(moment().subtract(7, "days").format());
  }, [refresh]);

  React.useEffect(() => {
    switch (selectedValue) {
      case "minute":
        onChange({ start: lastMinute, end: now });
        break;
      case "hour":
        onChange({ start: lastHour, end: now });
        break;
      case "day":
        onChange({ start: lastDay, end: now });
        break;
      default:
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lastMinute, lastHour, lastDay]);

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedValue(event.target.value as string);
    switch (event.target.value) {
      case "minute":
        onChange({ start: lastMinute, end: now });
        break;
      case "hour":
        onChange({ start: lastHour, end: now });
        break;
      case "day":
        onChange({ start: lastDay, end: now });
        break;
      case "week":
        onChange({ start: lastWeek, end: now });
        break;
      default:
    }
  };

  return (
    <TextField
      select
      value={selectedValue}
      onChange={handleChange}
      className={classes.textField}
      style={{ textAlign: "left" }}
      variant="outlined"
      label="Timeframe"
      required={false}
      fullWidth={true}
      InputLabelProps={{
        className: classes.input,
      }}
    >
      <MenuItem value={"minute"}>Last 60 Seconds</MenuItem>
      <MenuItem value={"hour"}>Last 60 Minutes</MenuItem>
      <MenuItem value={"day"}>Last 24 Hours</MenuItem>
      <MenuItem value={"week"}>Last 7 Days</MenuItem>
    </TextField>
  );
}
