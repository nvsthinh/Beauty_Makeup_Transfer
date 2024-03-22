import React, { useEffect, useState } from "react";
import { StatusBar } from "expo-status-bar";
import {
  View,
  Image,
  Text,
  FlatList,
  ScrollView,
  StyleSheet,
} from "react-native";
import {
  useFonts,
  Exo2_400Regular,
  Exo2_700Bold,
} from "@expo-google-fonts/exo-2";
import axios from "axios"; // Import Axios
import * as NavigationBar from "expo-navigation-bar";
import { NavigationContainer, useNavigation } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Dashboard from "./src/screens/DashboardScreen";
import Result from "./src/screens/ResultScreen";
// enableScreens();

const Stack = createNativeStackNavigator();
const App = () => {
  // const visibility = NavigationBar.useVisibility();
  // React.useEffect(() => {
  //   if (visibility === "visible") {
  //     const interval = setTimeout(() => {
  //       NavigationBar.setVisibilityAsync("hidden");
  //     }, /* 3 Seconds */ 0);

  //     return () => {
  //       clearTimeout(interval);
  //     };
  //   }
  // }, [visibility]);
  let [fontsLoaded] = useFonts({
    Exo2_400Regular,
    Exo2_700Bold,
  });
  if (!fontsLoaded) {
    return null;
  }
  return (
    <>
      <NavigationContainer>
        <Stack.Navigator
          screenOptions={{
            gestureEnabled: true,
            gestureDirection: "horizontal",
            animation: "slide_from_right",
            headerTitleStyle: {
              fontFamily: "Exo2_700Bold",
              color: "#434343",
              fontSize: 18,
            },
          }}
        >
          <Stack.Screen
            name="Dashboard"
            options={{
              headerShown: false,
              gestureEnabled: false,
            }}
            component={Dashboard}
          />
          <Stack.Screen
            name="Result"
            options={{
              headerShown: true,
              gestureEnabled: false,
            }}
            component={Result}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "red",
    alignItems: "center",
    justifyContent: "center",
  },
});
export default App;
