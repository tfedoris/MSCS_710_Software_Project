import { CardActions, CardContent } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import PrimaryButton from "components/atoms/PrimaryButton";
import { Field, Form, Formik } from "formik";
import React, { ReactElement } from "react";
import TextFieldComponent from "../atoms/TextField";
import { CheckboxWithLabel } from "formik-material-ui";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      "& .MuiTextField-root": {
        margin: theme.spacing(1),
      },
    },
    card: {
      width: "50%",
    },
  })
);

export interface Values {
  firstname: string;
  lastname: string;
  telephone: string;
  mobile: string;
  emailaddress: string;
  enabled: boolean;
  admin: boolean;
  primarycontact: boolean;
}

interface Props {
  onSubmit: (values: Values) => void;
}

export default function AddContact({ onSubmit }: Props): ReactElement {
  const classes = useStyles();

  return (
    <Card className={classes.card}>
      <CardContent>
        <Formik
          initialValues={{
            firstname: "",
            lastname: "",
            telephone: "",
            mobile: "",
            emailaddress: "",
            enabled: false,
            admin: false,
            primarycontact: false,
          }}
          onSubmit={(values, { resetForm }) => {
            onSubmit(values);
            resetForm();
          }}
        >
          <Form className={classes.root} noValidate autoComplete="off">
            <div>
              <Field
                name="firstname"
                label="First"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="lastname"
                label="Last"
                required={true}
                component={TextFieldComponent}
              />
            </div>
            <div>
              <Field
                name="telephone"
                label="Phone Number"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="mobile"
                label="Mobile Number"
                required={true}
                component={TextFieldComponent}
              />
            </div>
            <div>
              <Field
                name="emailaddress"
                label="Email Address"
                required={true}
                component={TextFieldComponent}
              />
            </div>
            <div>
              <Field
                component={CheckboxWithLabel}
                type="checkbox"
                name="enabled"
                color="primary"
                Label={{ label: "Enabled" }}
              />
              <Field
                component={CheckboxWithLabel}
                type="checkbox"
                name="admin"
                color="primary"
                Label={{ label: "Admin" }}
              />
              <Field
                component={CheckboxWithLabel}
                type="checkbox"
                name="primarycontact"
                color="primary"
                Label={{ label: "Primary" }}
              />
            </div>
            <div>
              <CardActions
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <PrimaryButton type="submit" title="Submit"></PrimaryButton>
              </CardActions>
            </div>
          </Form>
        </Formik>
      </CardContent>
    </Card>
  );
}
