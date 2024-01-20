import { FC } from "react";
import styles from "../selectScreen.module.scss";

type ChooseStyleButtonProps = {
    title: string,
}

const ChooseStyleButton: FC<ChooseStyleButtonProps> = ({
    title
}) => {
    return (
        <button className={styles.csb}>{title}</button>
    )
}

export default ChooseStyleButton;