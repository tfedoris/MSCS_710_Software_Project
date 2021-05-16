import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  {
    name: "",
    utilization: 90,
    amt: 2400,
  },
  {
    name: "",
    utilization: 99,
    amt: 2210,
  },
  {
    name: "",
    utilization: 89,
    amt: 2290,
  },
  {
    name: "",
    utilization: 50,
    amt: 2000,
  },
  {
    name: "",
    utilization: 25,
    amt: 2181,
  },
  {
    name: "",
    utilization: 30,
    amt: 2500,
  },
  {
    name: "",
    utilization: 70,
    amt: 2100,
  },
];

export default function SimpleLineChart() {
  return (
    <LineChart
      width={500}
      height={300}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="utilization"
        stroke="#8884d8"
        activeDot={{ r: 8 }}
      />
    </LineChart>
  );
}
