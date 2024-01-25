import { FC } from "react";
import styles from "../selectScreen.module.scss";

type ChangeImageButtonProps = {
    icon: any,
}

const ChangeImageButton: FC<ChangeImageButtonProps> = ({
    icon
}) => {
    return (
        <button className={styles.cib}>{icon}</button>
    )
}

export default ChangeImageButton;