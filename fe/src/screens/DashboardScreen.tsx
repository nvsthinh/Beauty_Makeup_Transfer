import React, { useState, useRef, useEffect } from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";

import Icon from "react-native-vector-icons/FontAwesome";
import * as MediaLibrary from "expo-media-library";
import { Camera, CameraType } from "expo-camera";
import LoadProgress from "../components/LoadProgress";

const DashboardScreen = ({ navigation }: { navigation: any }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0); // set và get , ES  useState constant, function
  const [cameraOpen, setCameraOpen] = useState(false);
  const [hasCameraPermission, setHasCameraPermission]: any = ({} =
    useState(null));
  const [type, setType] = useState(Camera.Constants.Type.front);
  const [flash, setFlash] = useState(Camera.Constants.FlashMode.off);
  const [isStudyPressed, setIsStudyPressed] = useState(true);
  const [isCaptureDisabled, setIsCaptureDisabled] = useState(false);
  const [loadProgress, setLoadProgress] = useState(false);
  const cameraRef = useRef(null);
  // Cập nhật để sử dụng state
  const [studyImagePaths, setStudyImagePaths] = useState([]);
  const [playImagePaths, setPlayImagePaths] = useState([]);
  // const playImagePaths = [
  //   require("../../assets/img5.png"),
  //   require("../../assets/img6.png"),
  //   require("../../assets/img7.png"),
  //   require("../../assets/img8.png"),
  //   require("../../assets/img9.png"),
  // ];
  const currentImagePaths: any = isStudyPressed
    ? studyImagePaths
    : playImagePaths;

  useEffect(() => {
    (async () => {
      try {
        // console.log("Load function groupStyle");
        // Sử dụng fetch thay cho axios
        const response = await fetch("http://192.168.0.100:5000/group_style");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json(); // Phân tích cú pháp JSON từ response
        // console.log("Next 1", data);

        // Giả sử API trả về dữ liệu hợp lệ cho cả hai mảng
        const studyData = data.result[0].data.map((item: any) => ({
          id: item.StyleID,
          uri: `data:image/png;base64,${item.base64}`,
        }));
        // console.log("Next 2");

        // console.log("studyData: " + JSON.stringify(studyData));
        const playData = data.result[1].data.map((item: any) => ({
          id: item.StyleID,
          uri: `data:image/png;base64,${item.base64}`,
        }));
        // console.log("Next 3");

        setStudyImagePaths(studyData);
        setPlayImagePaths(playData);
        // console.log("Load image path success");
      } catch (error: any) {
        // console.error("There was an error!", error.message);
      }
      setCurrentImageIndex(0);
      setIsStudyPressed(true);
      setCameraOpen(false);
      MediaLibrary.requestPermissionsAsync();
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === "granted");
    })();
  }, []);

  // useEffect(() => {
  //   console.log("currentImagePaths: ", currentImagePaths);
  //   console.log("uri is ", currentImagePaths[currentImageIndex]?.uri);
  // }, [isStudyPressed]);

  const handleNextImage = () => {
    if (currentImageIndex < currentImagePaths.length - 1) {
      setCurrentImageIndex(currentImageIndex + 1);
    }
  };

  const handlePrevImage = () => {
    if (currentImageIndex > 0) {
      setCurrentImageIndex(currentImageIndex - 1);
    }
  };

  const handleOpenCamera = () => {
    setCameraOpen(true);
  };

  const handleCloseCamera = () => {
    setCameraOpen(false);
  };

  const handleTakePicture = async () => {
    if (cameraRef.current) {
      try {
        setIsCaptureDisabled(true); // Disable the button
        const options = { quality: 0.5, base64: true };
        const data = await (cameraRef.current as Camera).takePictureAsync(
          options
        );
        // console.log("Picture taken successfully");
        const startTime = performance.now(); // Bắt đầu tính thời gian

        // Convert base64 of the current image to standard base64
        // const currentImagePath = currentImagePaths[currentImageIndex];
        // const asset = Asset.fromModule(currentImagePath);
        // await asset.downloadAsync();

        // const localUri: any = asset.localUri;
        // const base64Data = await FileSystem.readAsStringAsync(localUri, {
        //   encoding: FileSystem.EncodingType.Base64,
        // });
        // navigation.navigate("Result", {
        //   base64Data: base64Data,
        // });
        // console.log("Base64 Data is ", base64Data);

        //     const currentImageBase64 = await FileSystem.readAsStringAsync(
        //       currentImagePath.toString(),
        //       {
        //         encoding: FileSystem.EncodingType.Base64,
        //       }
        //     );
        // console.log("Current Image Base64:", currentImageBase64);

        const takenImageBase64 = data.base64;
        // console.log("Taken Image Base64:", takenImageBase64);

        // Prepare the request payload
        const payload = {
          origin_img_base64: takenImageBase64,
          style_img_base64: currentImagePaths[currentImageIndex]?.uri,
        };

        setLoadProgress(true);
        // Make a POST request to your Flask API
        const response = await fetch("http://192.168.0.100:5000/image", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        // console.log("Response from Flask API:", response);
        const endTime = performance.now();
        const elapsedTime = endTime - startTime; // Thời gian đã trôi qua từ khi bắt đầu gọi API đến khi kết thúc (milliseconds)
        if (response.ok) {
          const result = await response.json();
          // console.log("Result from Flask API:", result.result_data);
          setLoadProgress(false);
          setCameraOpen(false);
          // Kết thúc tính thời gian

          console.log("Thời gian gọi API:", elapsedTime.toFixed(2), "ms");
          navigation.navigate("Result", {
            base64DataOrigin: `data:image/png;base64,${result.result_data}`,
            base64DataStyle: currentImagePaths[currentImageIndex]?.uri,
            style_id: currentImagePaths[currentImageIndex]?.id,
          });
        } else {
          setLoadProgress(false);

          setCameraOpen(false);

          console.error("Error sending images to Flask API:", response.status);
        }
      } catch (error: any) {
        setLoadProgress(false);

        setCameraOpen(false);

        console.error("Error taking picture:", error);
      } finally {
        setLoadProgress(false);

        setCameraOpen(false);

        setIsCaptureDisabled(false); // Enable the button after execution
      }
    }
  };

  const handleStudy = () => {
    setCurrentImageIndex(0);
    setIsStudyPressed(true);
  };

  const handlePlay = () => {
    setCurrentImageIndex(0);
    setIsStudyPressed(false);
  };
  if (loadProgress) {
    return <LoadProgress divide={1} />;
  } else {
    return (
      <View style={styles.container}>
        {/* Phase 1: Header */}
        <View style={styles.header}>
          <Text style={styles.headerText}>Welcome To Beauty MakeUp Style</Text>
        </View>
        <View style={styles.optionsContainer}>
          <TouchableOpacity
            onPress={handleStudy}
            style={[
              styles.optionButton,
              {
                backgroundColor: isStudyPressed ? "#D63484" : "#FF9BD2",
                flex: 1,
              },
            ]}
          >
            <Text style={styles.optionButtonText}>Study</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={handlePlay}
            style={[
              styles.optionButton,
              {
                backgroundColor: isStudyPressed ? "#FF9BD2" : "#D63484",
                flex: 1,
              },
            ]}
          >
            <Text style={styles.optionButtonText}>Play</Text>
          </TouchableOpacity>
        </View>

        <View>
          <Image
            source={{ uri: currentImagePaths[currentImageIndex]?.uri }}
            style={styles.image}
          />

          <View style={styles.navigationButtons}>
            <TouchableOpacity
              onPress={handlePrevImage}
              style={{ flex: 2, alignItems: "center" }}
            >
              <Icon name="arrow-left" size={30} color="black" />
            </TouchableOpacity>

            <Text style={styles.navigationText}>
              {currentImageIndex + 1} / {currentImagePaths.length}
            </Text>

            <TouchableOpacity
              onPress={handleNextImage}
              style={{ flex: 2, alignItems: "center" }}
            >
              <Icon name="arrow-right" size={30} color="black" />
            </TouchableOpacity>
          </View>
        </View>
        <View>
          {cameraOpen && (
            <Camera
              ref={cameraRef}
              style={styles.camera}
              type={type as CameraType}
              flashMode={flash}
            />
          )}
          {!cameraOpen && (
            <TouchableOpacity
              onPress={cameraOpen ? handleCloseCamera : handleOpenCamera}
              style={styles.openCameraButton}
            >
              <Text style={styles.openCameraButtonText}>
                {cameraOpen ? "Close Camera" : "Open Camera"}
              </Text>
            </TouchableOpacity>
          )}
          {cameraOpen && (
            <TouchableOpacity
              onPress={handleTakePicture}
              style={styles.cameraButton}
              disabled={isCaptureDisabled}
            >
              <Text style={styles.cameraButtonText}>Capture && Done</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    );
  }
};
// CSS : casading stylesheet
const styles = StyleSheet.create({
  container: {
    flex: 1,
    position: "relative",
    alignItems: "center",
    backgroundColor: "#F9F9E0",
    marginTop: 20,
  },
  header: {
    marginTop: 25,
    marginBottom: 5,
    padding: 20,
    backgroundColor: "#402B3A",
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
  },
  headerText: {
    color: "white",
    fontSize: 20,
  },

  image: {
    width: 220,
    height: 220,
    margin: 5,
    borderRadius: 10,
  },
  navigationButtons: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    margin: 10,
  },
  navigationText: {
    fontSize: 18,
    alignItems: "center",
  },
  openCameraButton: {
    backgroundColor: "#402B3A",
    padding: 10,
    borderRadius: 5,
    marginTop: 20,
  },
  openCameraButtonText: {
    color: "white",
    fontSize: 16,
  },
  camera: {
    width: 250,
    height: 250,
  },
  cameraButton: {
    backgroundColor: "#402B3A",
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
  },
  cameraButtonText: {
    fontSize: 16,
    color: "white",
    textAlign: "center",
  },
  optionsContainer: {
    flexDirection: "row",
  },
  optionButton: {
    backgroundColor: "#434343",
    padding: 10,
    marginLeft: 20,
    marginRight: 20,
    borderRadius: 5,
  },
  optionButtonText: {
    color: "white",
    fontSize: 16,
    textAlign: "center",
  },
});

export default DashboardScreen;
