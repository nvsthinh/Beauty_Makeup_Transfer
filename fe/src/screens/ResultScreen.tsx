// ResultScreen.js

import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  Image,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  Linking,
  ScrollView,
} from "react-native";

const ResultScreen = ({ route }: { route: any }) => {
  const { base64DataOrigin, base64DataStyle, style_id } = route.params;

  const handleNavigation = (link: any) => {
    Linking.openURL(link)
      .then((data) => {
        // console.log("Link opened:", data);
      })
      .catch(() => {
        // console.error("Error opening link");
      });
  };

  const [data, setData]: any = useState([]); // State to hold the combined data

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch(
          `http://192.168.0.100:5000/get_metadata?style_id=${style_id}`
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const responseData = await response.json();
        // console.log(responseData);
        // Combine studyData and playData into one array
        const combinedData = [
          ...responseData.result.map((item: any) => ({
            Item: item.Item,
            Item_Description: item.Item_Description,
            Link: item.Link, // You can replace this with the actual link if needed
            image: { uri: `data:image/png;base64,${item.Img}` },
            Product_Description: `${item.Product_Description}`,
          })),
        ];
        // console.log("combineData: ", combinedData);
        setData(combinedData);
        // console.log("Load image path success");
      } catch (error: any) {
        // console.error("There was an error!", error.message);
      }
    })();
  }, []);

  const [mainImageHeight, setMainImageHeight] = useState(280); // State to control the main image height
  const toggleMainImageHeight = () => {
    // Toggle between 150 and 280 for main image height
    setMainImageHeight(mainImageHeight === 280 ? 150 : 280);
  };
  return (
    <View style={styles.container}>
      {/* Button to toggle main image height */}
      <TouchableOpacity onPress={toggleMainImageHeight} style={styles.button}>
        <Text style={styles.buttonText}>
          {mainImageHeight === 280 ? "View Sample" : "Only Image Result"}
        </Text>
      </TouchableOpacity>
      {/* Display the main image */}
      <View style={{ flexDirection: "row" }}>
        <View style={styles.imageContainer}>
          <Image
            source={{ uri: base64DataOrigin }}
            style={[styles.mainImage, { height: mainImageHeight }]}
          />
          {/* Ảnh 1*/}
        </View>
        <View
          style={[
            styles.imageContainer,
            mainImageHeight === 280 && { display: "none" },
          ]}
        >
          <Image
            source={{ uri: base64DataStyle }}
            style={[
              styles.mainImage,
              {
                height: mainImageHeight,
              },
            ]}
          />
          {/* Ảnh 2*/}
        </View>
      </View>
      {/* Display the horizontal list of small images */}
      <View
        style={{
          alignItems: "flex-start",
          alignSelf: "flex-start",
          marginLeft: 10,
        }}
      >
        <Text
          style={{
            fontSize: 16,
            fontWeight: "700",
            color: "black",
          }}
        >
          Product Information
        </Text>
      </View>
      {data && (
        <FlatList
          data={data}
          keyExtractor={(item) => item.Img}
          horizontal
          showsHorizontalScrollIndicator={false}
          renderItem={({ item }: { item: any }) => (
            <ScrollView scrollEnabled>
              <View style={styles.smallImageContainer}>
                {/* Display small image */}
                <Image
                  source={{ uri: item.image?.uri }}
                  style={styles.smallImage}
                />
                {/* Display title and link on the right */}
                <View style={styles.smallImageInfo}>
                  <Text style={styles.smallImageTitle}>{item.title}</Text>
                  <Text numberOfLines={12} style={[styles.smallImageTitle, {textAlign: 'left'}]}>
                    {item.Product_Description}
                  </Text>

                  <TouchableOpacity onPress={() => handleNavigation(item.Link)}>
                    <Text style={styles.smallImageLink}>Find Product</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </ScrollView>
          )}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#F9F9E0",
  },
  // mainImage: {
  //   width: 320, // Adjust the size as needed
  //   height: 280, // Adjust the size as needed
  //   marginVertical: 20,
  // },
  smallImageContainer: {
    marginRight: 10,
    marginTop: 20,
    marginLeft: 10,
  },
  smallImage: {
    width: "100%", // Adjust the size as needed
    height: 80, // Adjust the size as needed
    resizeMode: "cover", // Đảm bảo ảnh sẽ đầy đủ chiều rộng và chiều cao trong view
    padding: 10,
    borderRadius: 5,
  },
  smallImageInfo: {
    marginTop: 5,
    alignItems: "center",
    flexDirection: "column",
  },
  smallImageTitle: {
    fontSize: 10,
    fontWeight: "bold",
    textAlign: "center",
    width: 160,
  },
  smallImageLink: {
    color: "blue",
    fontSize: 10,
    width: 160,
    textAlign: "center",
  },
  containerImage: {
    flex: 1,
    flexDirection: "row", // Chia màn hình theo chiều ngang
  },
  imageContainer: {
    flex: 1, // Sử dụng 50% chiều rộng của màn hình
    marginVertical: 20, // Khoảng cách giữa ảnh
    alignItems: "center", // Canh chỉnh ảnh theo trục dọc
  },
  mainImage: {
    width: "90%", // Độ rộng của ảnh
    height: 100, // Độ cao của ảnh
    resizeMode: "cover", // Đảm bảo ảnh sẽ đầy đủ chiều rộng và chiều cao trong view
  },
  button: {
    borderRadius: 5, //
    backgroundColor: "#D63484",
    padding: 10,
    marginTop: 20,
  },
  buttonText: {
    color: "white",
    fontWeight: "bold",
  },
});

export default ResultScreen;
