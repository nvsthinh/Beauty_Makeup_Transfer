import styles from "../selectScreen.module.scss"
import WebCam from "./Webcam"

const Camera = () => {
    return (
        <div className={styles.camera}>
            <div className={styles.webcamWrapper}>
                <WebCam />
            </div>
            <div className="">
                <button className={styles.done}>Done</button>
            </div>
        </div>
    )
}

export default Camera