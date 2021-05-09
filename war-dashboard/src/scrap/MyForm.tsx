import { Button } from "@material-ui/core";
import { Field, Form, Formik } from "formik";
import React, { ReactElement } from "react";
import TextFieldComponent from "../components/atoms/TextField";

interface Values {
  firstName: string;
  lastName: string;
  email: string;
}

interface Props {
  onSubmit: (values: Values) => void;
}

export default function MyForm({ onSubmit }: Props): ReactElement {
  return (
    <Formik
      initialValues={{ firstName: "", lastName: "", email: "" }}
      onSubmit={(values, { resetForm }) => {
        onSubmit(values);
        resetForm();
      }}
    >
      {({ values }) => (
        <Form>
          <div>
            <Field
              name="firstName"
              placeholder="First Name"
              component={TextFieldComponent}
            />
          </div>
          <div>
            <Field
              name="lastName"
              placeholder="Last Name"
              component={TextFieldComponent}
            />
          </div>
          <div>
            <Field
              name="email"
              placeholder="Email"
              component={TextFieldComponent}
            />
          </div>
          <Button type="submit">Submit</Button>
          <pre>{JSON.stringify(values, null, 2)}</pre>
        </Form>
      )}
    </Formik>
  );
}
