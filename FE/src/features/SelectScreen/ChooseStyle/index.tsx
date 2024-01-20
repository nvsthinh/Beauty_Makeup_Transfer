import ChangeImageButton from "./ChangeImageButton";
import Image from "./Image";
import styles from "../selectScreen.module.scss";
import ChooseStyleButton from "./ChooseStyleButton";
import { faCaretLeft, faCaretRight, faLeftLong } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const ChooseStyle = () => {
    return (
        <div className={styles.chooseStyle}>
            <div className={styles.chooseStyleButtonWrapper}>
                <ChooseStyleButton title="Choose style"/>
                <ChooseStyleButton title="Choose style"/>
            </div>
            <div className={styles.imageWrapper}>
                <div className={styles.cibWrapper}>
                    <ChangeImageButton icon={<FontAwesomeIcon icon={faCaretLeft} />}/>
                </div>
                <div className={styles.image}>
                    <Image src=""/>
                </div>
                <div className={styles.cibWrapper}>
                    <ChangeImageButton icon={<FontAwesomeIcon icon={faCaretRight} />}/>
                </div>
            </div>
        </div>
    )
}

export default ChooseStyle;