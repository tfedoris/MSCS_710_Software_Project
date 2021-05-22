import {
  createStyles,
  makeStyles,
  TextField,
  TextFieldProps,
  Theme,
} from "@material-ui/core";
import { FieldProps } from "formik";
import React from "react";

type Props = FieldProps & TextFieldProps;

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    textField: {
      // padding: theme.spacing(0),
    },
    input: {
      // padding: theme.spacing(2),
      color: "#a1a1a1",
    },
  })
);

const TextFieldComponent = ({
  label,
  required = false,
  error = false,
  helperText = "",
  fullWidth = true,
  field,
  InputLabelProps,
  inputProps,
  className,
  disabled,
}: Props) => {
  const classes = useStyles();

  return (
    <TextField
      disabled={disabled}
      className={className}
      fullWidth={fullWidth}
      label={label}
      required={false}
      error={error}
      helperText={helperText}
      variant="outlined"
      InputLabelProps={{
        className: classes.input,
        shrink: true,
        ...InputLabelProps,
      }}
      inputProps={inputProps}
      {...field}
    />
  );
};

export default TextFieldComponent;
