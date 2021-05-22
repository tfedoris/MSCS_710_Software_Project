import { Select, Theme, TextFieldProps, TextField } from "@material-ui/core";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import { createStyles, makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Field, FieldProps } from "formik";
import React, { ReactElement } from "react";
import { Endpoint } from "services/API";

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

type Props = TextFieldProps;

export default function FulfillmentCenterSelector({
  label,
  fullWidth = true,
  InputLabelProps,
  disabled = false,
  onChange,
  ...props
}: Props): ReactElement {
  const [items, setItems] = React.useState([]);
  const [mappedRows, setMappedRows] = React.useState([
    <MenuItem
      key={"DefaultFulfillmentCenterMenuItem"}
      value={"Default"}
      disabled
    >
      Select a Fulfillment Center
    </MenuItem>,
  ] as any);

  React.useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      axios.get(Endpoint.FullfillmentCenter).then(
        (response) => {
          if (!isCancelled) setItems(response.data);
        },
        (error) => {
          console.log(error.response.status);
        }
      );
    };

    fetchData();
    const elements = items.map((item: any) => {
      return (
        <MenuItem key={item.id} value={item.id}>
          {item.name}
        </MenuItem>
      );
    });
    setMappedRows([
      <MenuItem
        key={"DefaultFulfillmentCenterMenuItem"}
        value={"Default"}
        disabled
      >
        Select an Fulfillment Center
      </MenuItem>,
      ...elements,
    ]);

    return () => {
      isCancelled = true;
      return;
    };
  }, [items]);

  const classes = useStyles();
  return (
    <TextField
      select
      value={props.value}
      onChange={onChange}
      className={classes.textField}
      style={{ textAlign: "left" }}
      disabled={disabled}
      variant="outlined"
      label={label}
      required={false}
      fullWidth={fullWidth}
      InputLabelProps={{
        className: classes.input,
        shrink: true,
        ...InputLabelProps,
      }}
    >
      {mappedRows}
    </TextField>
  );
}
