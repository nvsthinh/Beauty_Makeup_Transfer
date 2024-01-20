import Camera from "./Camera";
import ChooseStyle from "./ChooseStyle";
import styles from "./selectScreen.module.scss";

const SelectScreen = () => {
    return (
        <div className={styles.select}>
            <ChooseStyle />
            <Camera />
        </div>  
    )
}

export default SelectScreen;