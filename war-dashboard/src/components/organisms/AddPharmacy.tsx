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
  storeId: string;
  name: string;
  address1: string;
  address2: string;
  address3: string;
  city: string;
  state: string;
  postalcode: string;
  telephone: string;
  enabled: boolean;
  active: boolean;
}

interface Props {
  onSubmit: (values: Values) => void;
}

export default function AddBusinessOrganization({
  onSubmit,
}: Props): ReactElement {
  const classes = useStyles();

  return (
    <Card className={classes.card}>
      <CardContent>
        <Formik
          initialValues={{
            storeId: "",
            name: "",
            address1: "",
            address2: "",
            address3: "",
            city: "",
            state: "",
            postalcode: "",
            telephone: "",
            enabled: false,
            active: false,
          }}
          onSubmit={(values, { resetForm }) => {
            onSubmit(values);
            resetForm();
          }}
        >
          <Form className={classes.root} noValidate autoComplete="off">
            <div>
              <Field
                name="storeId"
                label="Store ID"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="name"
                label="Name"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="address1"
                label="Address"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="address2"
                label=""
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="address3"
                label=""
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="city"
                label="City"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="state"
                label="State"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="postalcode"
                label="Postal Code"
                required={true}
                component={TextFieldComponent}
              />
              <Field
                name="telephone"
                label="Phone Number"
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
                name="active"
                color="primary"
                Label={{ label: "Active" }}
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
