import React from "react";

import Typography from "@material-ui/core/Typography";

interface IProps_Typography {
  children: string;
  variant?: "header" | "title" | "subtitle" | "body";
}

const getMappedVariant = (variant: string) => {
  switch (variant) {
    case "header":
      return "h4";
    case "title":
      return "subtitle1";
    case "subtitle":
      return "subtitle2";
    default:
      return "body1";
  }
};

const TypographyComponent = ({
  children,
  variant = "body",
}: IProps_Typography) => (
  <Typography variant={getMappedVariant(variant)}>{children}</Typography>
);

export default TypographyComponent;
