import React from "react";
import { View, ActivityIndicator, Dimensions } from "react-native";

export default function LoadProgress({ divide }: { divide?: any | undefined }) {
  return (
    <View
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
        alignItems: "center",
        justifyContent: "center",
        height: divide
          ? Dimensions.get("window").height / divide
          : Dimensions.get("window").height / 1.3,
      }}
    >
      <ActivityIndicator size="large" />
    </View>
  );
}
