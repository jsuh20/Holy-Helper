import Webcam from "react-webcam";
import { useRef, useState } from "react";
import ResultPopUp from "./ResultPopUp";

export default function CameraComponent() {
  const webcamRef = useRef<Webcam>(null);
  const [data, setData] = useState(null);

  const capture = async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) {
        console.error("No image source available");
        return;
    }

    const formData = new FormData();
    const blob = await fetch(imageSrc).then(res => res.blob());
    formData.append("image", blob, "photo.jpg");

    const response = await fetch("http://localhost:5001/predict", {
        method: "POST",
        body: formData,
    });
    const responseData = await response.json();
    setData(responseData);
    console.log(responseData);
  };

  return (
    <div>
      <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" />
      <button onClick={capture}>Analyze Emotion</button>
      {data && <ResultPopUp data={data} onClose={() => setData(null)}/>}
    </div>
  );
}
