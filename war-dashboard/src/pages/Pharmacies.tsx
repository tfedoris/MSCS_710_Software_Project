import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";
import AddContact from "components/organisms/AddContact";
import React, { useState } from "react";
import MyTable from "scrap/MyTable";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import { Values } from "../components/organisms/AddPharmacy";
import AddPharmacy from "components/organisms/AddPharmacy";
import PharmaciesTable from "components/organisms/PharmaciesTable";

const API_ENDPOINT = "https://iapharmacyservice.azurewebsites.net/api/pharmacy";
const drawerWidth = 240;

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      display: "flex",
    },
    drawer: {
      width: drawerWidth,
      flexShrink: 0,
    },
    drawerPaper: {
      width: drawerWidth,
    },
    // necessary for content to be below app bar
    toolbar: theme.mixins.toolbar,
    content: {
      flexGrow: 1,
      backgroundColor: theme.palette.background.default,
      padding: theme.spacing(3),
    },
    spacer: {
      visibility: "hidden",
    },
  })
);

const contactsReducer = (state: any, action: any) => {
  switch (action.type) {
    case "CONTACTS_FETCH_INIT":
      return {
        ...state,
      };
    case "CONTACTS_FETCH_SUCCESS":
      return {
        ...state,
        data: action.payload,
      };
    case "CONTACTS_FETCH_FAILURE":
      return {
        ...state,
      };
    default:
      throw new Error();
  }
};

const IsEmpty = (data: Object) =>
  Object.values(data).every((x) => x === null || x === "");

export default function Pharmacies() {
  const classes = useStyles();

  const [contacts, dispatchContacts] = React.useReducer(contactsReducer, {
    data: [],
  });

  const handleFetchContacts = React.useCallback(() => {
    dispatchContacts({ type: "CONTACTS_FETCH_INIT" });

    axios
      .get(`${API_ENDPOINT}`)
      .then((result: any) => {
        console.log(result.data);
        dispatchContacts({
          type: "CONTACTS_FETCH_SUCCESS",
          payload: result.data,
        });
      })
      .catch(() => dispatchContacts({ type: "CONTACTS_FETCH_FAILURE" }));
  }, []);

  React.useEffect(() => {
    handleFetchContacts();
  }, [handleFetchContacts]);

  return (
    <>
      <div className={classes.toolbar} />
      <h1 style={{ textAlign: "left" }}>Pharmacies</h1>
      <AddPharmacy onSubmit={handleSubmit()} />
      <div className={classes.spacer}>.</div>
      <PharmaciesTable rows={contacts.data} />
    </>
  );

  function handleSubmit(): (values: Values) => void {
    return (data) => {
      if (IsEmpty(data)) return;
      axios
        .post(`${API_ENDPOINT}`, {
          id: uuidv4(),
          ...data,
        })
        .then((resp) => {
          console.log(resp.data);
          dispatchContacts({
            type: "CONTACTS_FETCH_SUCCESS",
            payload: [resp.data],
          });
          handleFetchContacts();
        })
        .catch((error) => {
          dispatchContacts({ type: "CONTACTS_FETCH_FAILURE" });
        });
    };
  }
}
