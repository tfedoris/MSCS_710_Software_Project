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
  name: string;
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
            name: "",
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
                name="name"
                label="Name"
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
