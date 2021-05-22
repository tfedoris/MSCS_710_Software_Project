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
  return <div></div>;
}
