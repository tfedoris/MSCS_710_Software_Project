import "date-fns";
import React from "react";
import Grid from "@material-ui/core/Grid";
import DateFnsUtils from "@date-io/date-fns";
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
} from "@material-ui/pickers";
import { textFieldStyles } from "themes/Styles";

interface Props {
  label: string;
  onDateChange: (date: Date) => void;
}

export default function DatePicker(props: Props) {
  const classes = textFieldStyles();

  const [selectedDate, setSelectedDate] = React.useState<Date>(new Date());

  const handleDateChange = (date: Date | null) => {
    if (!date) return;
    date.setHours(0, 0, 0, 0);
    setSelectedDate(date);
    props.onDateChange(date);
  };

  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <KeyboardDatePicker
        id={props.label}
        className={classes.root}
        defaultValue={new Date()}
        label={props.label}
        format="MM/dd/yyyy"
        inputVariant="outlined"
        value={selectedDate}
        onChange={handleDateChange}
        KeyboardButtonProps={{
          "aria-label": "change date",
          style: { color: "white" },
        }}
      />
    </MuiPickersUtilsProvider>
  );
}
