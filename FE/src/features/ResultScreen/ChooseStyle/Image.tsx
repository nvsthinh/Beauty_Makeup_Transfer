import { FC } from "react";

type ImageProps = {
    src: string
}

const Image:FC<ImageProps> = ({
    src
}) => {
    return (
        src ? <img src={src}/> : <></>
    )
}

export default Image