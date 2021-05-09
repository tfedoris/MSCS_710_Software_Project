import { TextField, TextFieldProps } from "@material-ui/core";
import { FieldProps } from "formik";
import React from "react";

type Props = FieldProps & TextFieldProps;

// interface IProps_TextField {
//   label: string;
//   value?: string;
//   required?: boolean;
//   onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
//   error?: boolean;
//   errorMessage?: string;
//   fullWidth?: boolean;
// }

const TextFieldComponent = ({
  label,
  required = false,
  error = false,
  helperText = "",
  fullWidth = true,
  field,
}: Props) => (
  <TextField
    fullWidth={fullWidth}
    label={label}
    required={required}
    error={error}
    helperText={helperText}
    variant="outlined"
    InputLabelProps={{
      shrink: true,
    }}
    {...field}
  />
);

export default TextFieldComponent;
