import { TextField, TextFieldProps, Theme } from "@material-ui/core";
import MenuItem from "@material-ui/core/MenuItem";
import { createStyles, makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import React, { ReactElement } from "react";
import { Endpoint } from "utilities/API";

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

interface Props {
  userId: string;
  onChange: (value: string) => void;
}

export default function FulfillmentCenterSelector({
  userId,
  onChange,
}: Props): ReactElement {
  const [items, setItems] = React.useState([] as any);
  const [mappedRows, setMappedRows] = React.useState([] as any);
  const [selectedValue, setSelectedValue] = React.useState("");

  const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    setSelectedValue(event.target.value as string);
    onChange(event.target.value as string);
    console.log(event.target.value as string);
  };

  React.useEffect(() => {
    let isCancelled = false;

    const fetchData = async () => {
      axios.post(Endpoint.ClientMachines, { user_id: userId }).then(
        (response) => {
          if (!isCancelled && response.data.success)
            setItems(response.data.data);
        },
        (error) => {
          console.log(error.response.status);
        }
      );
    };

    fetchData();
    if (items.length > 0) {
      const elements = items.map((item: any) => {
        return (
          <MenuItem key={item.machine_id} value={item.machine_id}>
            {item.machine_name}
          </MenuItem>
        );
      });
      setMappedRows(elements);
    }

    return () => {
      isCancelled = true;
      return;
    };
  }, [items, userId]);

  const classes = useStyles();
  return (
    <TextField
      select
      value={selectedValue}
      onChange={handleChange}
      className={classes.textField}
      style={{ textAlign: "left" }}
      disabled={false}
      variant="outlined"
      label="User Machine"
      required={false}
      fullWidth={true}
      InputLabelProps={{
        className: classes.input,
      }}
    >
      {mappedRows}
    </TextField>
  );
}
