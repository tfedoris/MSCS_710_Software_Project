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
  }>;
}

export default function PharmaciesTable({ rows }: Props) {
  return (
    <TableContainer component={Paper}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Store ID</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Address 1</TableCell>
            <TableCell>Address 2</TableCell>
            <TableCell>Address 3</TableCell>
            <TableCell>City</TableCell>
            <TableCell>State</TableCell>
            <TableCell>Postal Code</TableCell>
            <TableCell>Phone Number</TableCell>
            <TableCell>Enabled</TableCell>
            <TableCell>Active</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.storeId}</TableCell>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.address1}</TableCell>
              <TableCell>{row.address2}</TableCell>
              <TableCell>{row.address3}</TableCell>
              <TableCell>{row.city}</TableCell>
              <TableCell>{row.state}</TableCell>
              <TableCell>{row.postalcode}</TableCell>
              <TableCell>{row.telephone}</TableCell>
              <TableCell>{row.enabled ? <CheckIcon /> : ""}</TableCell>
              <TableCell>{row.active ? <CheckIcon /> : ""}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
