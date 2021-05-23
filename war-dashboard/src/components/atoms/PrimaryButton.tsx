import React from "react";

import Button from "@material-ui/core/Button";

interface Props {
  title: string;
  disabled?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset" | undefined;
  style?: React.CSSProperties | undefined;
  preventRender?: boolean;
  color?: "primary" | "inherit" | "secondary" | "default" | undefined;
}

const PrimaryButton = ({
  title,
  disabled = false,
  onClick,
  type,
  style,
  preventRender = false,
  color = "primary",
}: Props) =>
  preventRender ? null : (
    <Button
      variant="contained"
      color={color}
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
