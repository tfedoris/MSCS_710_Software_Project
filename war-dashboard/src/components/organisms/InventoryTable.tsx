import FormControlLabel from "@material-ui/core/FormControlLabel";
import IconButton from "@material-ui/core/IconButton";
import Paper from "@material-ui/core/Paper";
import {
  createStyles,
  lighten,
  makeStyles,
  Theme,
} from "@material-ui/core/styles";
import Switch from "@material-ui/core/Switch";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TablePagination from "@material-ui/core/TablePagination";
import TableRow from "@material-ui/core/TableRow";
import TableSortLabel from "@material-ui/core/TableSortLabel";
import Toolbar from "@material-ui/core/Toolbar";
import Tooltip from "@material-ui/core/Tooltip";
import Typography from "@material-ui/core/Typography";
import FilterListIcon from "@material-ui/icons/FilterList";
import React from "react";

interface Props {
  rows: Array<{
    pid: number;
    name: string;
    process_status: string;
    cpu_percent: number;
    memory_physical_used_byte: number;
    memory_virtual_bsed_byte: number;
    io_read_count: number;
    io_read_bytes: number;
    io_write_count: number;
    io_write_bytes: number;
    thread_num: number;
  }>;
}

interface Data {
  pid: number;
  name: string;
  process_status: string;
  cpu_percent: number;
  memory_physical_used_byte: number;
  memory_virtual_bsed_byte: number;
  io_read_count: number;
  io_read_bytes: number;
  io_write_count: number;
  io_write_bytes: number;
  thread_num: number;
}

function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

type Order = "asc" | "desc";

function getComparator<Key extends keyof any>(
  order: Order,
  orderBy: Key
): (
  a: { [key in Key]: string | number },
  b: { [key in Key]: string | number }
) => number {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort<T>(array: T[], comparator: (a: T, b: T) => number) {
  const stabilizedThis = array.map((el, index) => [el, index] as [T, number]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

interface HeadCell {
  disablePadding: boolean;
  id: keyof Data;
  label: string;
  alignRight: boolean;
}

const headCells: HeadCell[] = [
  {
    id: "pid",
    alignRight: true,
    disablePadding: false,
    label: "PID",
  },
  {
    id: "name",
    alignRight: true,
    disablePadding: false,
    label: "Name",
  },
  {
    id: "process_status",
    alignRight: true,
    disablePadding: false,
    label: "Status",
  },
  {
    id: "cpu_percent",
    alignRight: true,
    disablePadding: false,
    label: "CPU % (avg across all cores)",
  },
  {
    id: "memory_physical_used_byte",
    alignRight: true,
    disablePadding: false,
    label: "Memory Used (MB)",
  },
  {
    id: "memory_virtual_bsed_byte",
    alignRight: true,
    disablePadding: false,
    label: "Virtual Memory Used (MB)",
  },
  {
    id: "io_read_count",
    alignRight: true,
    disablePadding: false,
    label: "I/O Read Count",
  },
  {
    id: "io_read_bytes",
    alignRight: true,
    disablePadding: false,
    label: "I/O Read (KB)",
  },
  {
    id: "io_write_count",
    alignRight: true,
    disablePadding: false,
    label: "I/O Write Count",
  },
  {
    id: "io_write_bytes",
    alignRight: true,
    disablePadding: false,
    label: "I/O Write (KB)",
  },
  {
    id: "thread_num",
    alignRight: true,
    disablePadding: false,
    label: "Threads",
  },
];

interface EnhancedTableProps {
  classes: ReturnType<typeof useStyles>;
  onRequestSort: (
    event: React.MouseEvent<unknown>,
    property: keyof Data
  ) => void;
  order: Order;
  orderBy: string;
  rowCount: number;
}

function EnhancedTableHead(props: EnhancedTableProps) {
  const { classes, order, orderBy, onRequestSort } = props;
  const createSortHandler =
    (property: keyof Data) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, property);
    };

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.alignRight ? "right" : "left"}
            padding={headCell.disablePadding ? "none" : "default"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <span className={classes.visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </span>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

const useToolbarStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      paddingLeft: theme.spacing(2),
      paddingRight: theme.spacing(1),
    },
    highlight:
      theme.palette.type === "light"
        ? {
            color: theme.palette.secondary.main,
            backgroundColor: lighten(theme.palette.secondary.light, 0.85),
          }
        : {
            color: theme.palette.text.primary,
            backgroundColor: theme.palette.secondary.dark,
          },
    title: {
      flex: "1 1 100%",
    },
  })
);

interface EnhancedTableToolbarProps {
  title: string;
}

const EnhancedTableToolbar = ({ title }: EnhancedTableToolbarProps) => {
  const classes = useToolbarStyles();

  const handleClick = () => {};

  return (
    <Toolbar>
      <Typography
        className={classes.title}
        variant="h5"
        id="tableTitle"
        component="div"
        align="left"
      >
        {title}
      </Typography>
      <Tooltip title="Filter Inventory">
        <IconButton aria-label="filter-inventory" onClick={handleClick}>
          <FilterListIcon />
        </IconButton>
      </Tooltip>
    </Toolbar>
  );
};

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      width: "100%",
    },
    paper: {
      width: "100%",
      marginBottom: theme.spacing(2),
    },
    table: {
      minWidth: 750,
    },
    visuallyHidden: {
      border: 0,
      clip: "rect(0 0 0 0)",
      height: 1,
      margin: -1,
      overflow: "hidden",
      padding: 0,
      position: "absolute",
      top: 20,
      width: 1,
    },
  })
);

interface Props {
  rows: Array<{
    pid: number;
    name: string;
    process_status: string;
    cpu_percent: number;
    memory_physical_used_byte: number;
    memory_virtual_bsed_byte: number;
    io_read_count: number;
    io_read_bytes: number;
    io_write_count: number;
    io_write_bytes: number;
    thread_num: number;
  }>;
  title?: string;
}

export default function InventoryTable({
  rows,
  title = `Processes Metrics`,
  ...props
}: Props) {
  const classes = useStyles();
  const [order, setOrder] = React.useState<Order>("asc");
  const [orderBy, setOrderBy] = React.useState<keyof Data>("name");
  const [page, setPage] = React.useState(0);
  const [dense, setDense] = React.useState(false);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);

  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: keyof Data
  ) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChangeDense = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDense(event.target.checked);
  };

  const emptyRows =
    rowsPerPage - Math.min(rowsPerPage, rows.length - page * rowsPerPage);

  return (
    <div className={classes.root}>
      <Paper className={classes.paper}>
        <EnhancedTableToolbar title={title} />
        <TableContainer>
          <Table
            className={classes.table}
            aria-labelledby="tableTitle"
            size={dense ? "small" : "medium"}
            aria-label="enhanced table"
          >
            <EnhancedTableHead
              classes={classes}
              order={order}
              orderBy={orderBy}
              onRequestSort={handleRequestSort}
              rowCount={rows.length}
            />
            <TableBody>
              {stableSort(rows, getComparator(order, orderBy))
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row, index) => {
                  return (
                    <TableRow hover tabIndex={-1} key={row.pid}>
                      <TableCell align="left">{row.name}</TableCell>
                      <TableCell align="right">{row.process_status}</TableCell>
                      <TableCell align="right">{row.cpu_percent}</TableCell>
                      <TableCell align="right">
                        {row.memory_physical_used_byte}
                      </TableCell>
                      <TableCell align="right">
                        {row.memory_virtual_bsed_byte}
                      </TableCell>
                      <TableCell align="right">{row.io_read_count}</TableCell>
                      <TableCell align="right">{row.io_read_bytes}</TableCell>
                      <TableCell align="right">{row.io_write_count}</TableCell>
                      <TableCell align="right">{row.io_write_bytes}</TableCell>
                      <TableCell align="right">{row.thread_num}</TableCell>
                    </TableRow>
                  );
                })}
              {emptyRows > 0 && (
                <TableRow style={{ height: (dense ? 33 : 53) * emptyRows }}>
                  <TableCell colSpan={6} />
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onChangePage={handleChangePage}
          onChangeRowsPerPage={handleChangeRowsPerPage}
        />
      </Paper>
      <div style={{ textAlign: "left" }}>
        <FormControlLabel
          control={<Switch checked={dense} onChange={handleChangeDense} />}
          label="Dense padding"
        />
      </div>
    </div>
  );
}
