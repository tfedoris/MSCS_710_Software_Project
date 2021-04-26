import React from "react";

import Button from "@material-ui/core/Button";

interface IProps_PrimaryButton {
  title: string;
  disabled?: boolean;
  onClick?: React.MouseEventHandler<HTMLButtonElement> | undefined;
  type?: "button" | "submit" | "reset" | undefined;
  style?: React.CSSProperties | undefined;
}

const PrimaryButton = ({
  title,
  disabled = false,
  onClick,
  type,
  style,
}: IProps_PrimaryButton) => (
  <Button
    variant="contained"
    color="primary"
    disabled={disabled}
    onClick={onClick}
    size="medium"
    type={type}
    style={style}
  >
    {title}
  </Button>
);

export default PrimaryButton;
