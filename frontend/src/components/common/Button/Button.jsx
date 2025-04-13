import React from "react";
import "./Button.css";

const Button = ({
    children,
    onClick,
    variant = "primary",
    size = "medium",
    disabled = false,
    fullWidth = false,
    type = "button",
}) => {
    const classNames = [
        "custom-button",
        `custom-button--${variant}`,
        `custom-button--${size}`,
        fullWidth ? "custom-button--full-width" : "",
    ].join(" ");

    return (
        <button
            className={classNames}
            onClick={onClick}
            disabled={disabled}
            type={type}
        >
            {children}
        </button>
    );
};

export default Button;
