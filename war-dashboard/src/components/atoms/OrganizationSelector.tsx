import {
  Select,
  Theme,
  TextFieldProps,
  TextField,
  InputAdornment,
} from "@material-ui/core";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import { createStyles, makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Field, FieldProps } from "formik";
import React, { ReactElement } from "react";
import { Endpoint } from "services/Endpoint";
import { textFieldStyles } from "../../themes/Styles";

type Props = TextFieldProps;

export default function OrganizationSelector({
  label = "Organization",
  fullWidth = true,
  InputLabelProps,
  disabled = false,
  onChange,
  ...props
}: Props): ReactElement {
  const [items, setItems] = React.useState([]);
  const [mappedRows, setMappedRows] = React.useState([
    <MenuItem key={"DefaultOrganizationMenuItem"} value={"Default"}>
      All Organizations
    </MenuItem>,
  ] as any);

  React.useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      axios.get(Endpoint.Organization).then(
        (response) => {
          if (!isCancelled) setItems(response.data);
        },
        (error) => {
          console.log(error?.response.status);
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
      <MenuItem key={"DefaultOrganizationMenuItem"} value={"Default"}>
        All Organizations
      </MenuItem>,
      ...elements,
    ]);

    return () => {
      isCancelled = true;
      return;
    };
  }, [items]);

  const classes = textFieldStyles();
  return (
    <TextField
      select
      value={props.value}
      onChange={onChange}
      className={classes.root}
      style={{ textAlign: "left" }}
      disabled={disabled}
      variant="outlined"
      label={label}
      required={false}
      fullWidth={true}
      InputLabelProps={{
        shrink: true,
        ...InputLabelProps,
      }}
      InputProps={{
        style: {
          zIndex: "auto",
        },
      }}
      SelectProps={{ className: classes.icon }}
    >
      {mappedRows}
    </TextField>
  );
}
