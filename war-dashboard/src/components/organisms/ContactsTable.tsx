import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import CheckIcon from "@material-ui/icons/Check";
import React from "react";

interface Props {
  rows: Array<{
    id: string;
    firstname: string;
    lastname: string;
    telephone: string;
    mobile: string;
    emailaddress: string;
    enabled: boolean;
    admin: boolean;
    primarycontact: boolean;
  }>;
}

export default function ContactsTable({ rows }: Props) {
  return (
    <TableContainer component={Paper}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>First Name</TableCell>
            <TableCell>Last Name</TableCell>
            <TableCell>Phone Number</TableCell>
            <TableCell>Mobile Number</TableCell>
            <TableCell>Email Address</TableCell>
            <TableCell>Enabled</TableCell>
            <TableCell>Admin</TableCell>
            <TableCell>Primary</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.firstname}</TableCell>
              <TableCell>{row.lastname}</TableCell>
              <TableCell>{row.telephone}</TableCell>
              <TableCell>{row.mobile}</TableCell>
              <TableCell>{row.emailaddress}</TableCell>
              <TableCell>{row.enabled ? <CheckIcon /> : ""}</TableCell>
              <TableCell>{row.admin ? <CheckIcon /> : ""}</TableCell>
              <TableCell>{row.primarycontact ? <CheckIcon /> : ""}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
