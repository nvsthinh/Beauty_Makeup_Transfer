import { useState } from "react";
import Webcam from "react-webcam";
import styles from "../selectScreen.module.scss";

const WebCam = () => {

    const [openWebcam, setOpenWebcam] = useState(false);

    return (
        <div>
            <div className={!openWebcam ? styles.webcam : ""}>
                {
                    openWebcam && 
                    <Webcam 
                        width={500}
                        height={600}/>
                }
            </div>
            <div style={{
                textAlign: "center",
                marginTop: 10
            }}>
                <button className={styles.owcBtn} onClick={() => setOpenWebcam(true)}>Take your photo</button>
            </div>
        </div>
    )
}

export default WebCam;