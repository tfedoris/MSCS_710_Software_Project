import { TextField, TextFieldProps } from "@material-ui/core";
import { FieldProps } from "formik";
import React, { ReactElement } from "react";

type Props = FieldProps & TextFieldProps;

function MyField({ label, placeholder, field }: Props): ReactElement {
  return <TextField label={label} placeholder={placeholder} {...field} />;
}

export default MyField;
