import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";

interface Props {}

export default function Dashboard({}: Props): ReactElement {
  return (
    <div>
      <h1>Dashboard Header</h1>
    </div>
  );
}
