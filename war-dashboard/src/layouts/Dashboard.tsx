import { Grid, Paper } from "@material-ui/core";
import axios from "axios";
import React, { ReactElement, PureComponent } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import Typography from "@material-ui/core/Typography";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import SimpleLineChart from "components/organisms/SimpleLineChart";
import SimpleLineChart2 from "components/organisms/SimpleLineChart2";

interface Props {}

export default function Dashboard({}: Props): ReactElement {
  const [machineName, setMachineName] = React.useState("");

  React.useEffect(() => {
    async function fetchClientMachineInfo() {
      await axios
        .post(
          "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-data",
          { registration_id: "dCxPn_X3m", table_name: "client_machine" }
        )
        .then((response) => {
          const json_data = JSON.parse(response.data.data);
          if (response.data.success) {
            setMachineName(json_data[0].machine_name);
          }
        });
    }

    fetchClientMachineInfo();
  });

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Grid container spacing={4} alignItems="center" justify="center">
        <Grid item xs={12}>
          <Paper
            style={{ padding: 10, width: "50%", display: "center" }}
            elevation={5}
          >
            <Typography variant="h5" noWrap>
              {machineName}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper
            style={{
              padding: 10,
              display: "inline-block",
            }}
            elevation={5}
          >
            <Typography>Memory Utilization</Typography>
            <SimpleLineChart />
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper
            style={{
              padding: 10,
              display: "inline-block",
            }}
            elevation={5}
          >
            <Typography>CPU Utilization</Typography>
            <SimpleLineChart2 />
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}
