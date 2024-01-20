import { Route, Routes } from "react-router-dom";
import SelectScreen from "./features/SelectScreen";
import ResultScreen from "./features/ResultScreen";
import "./App.scss";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route 
          path="/"
          element={<SelectScreen />}
        />
        <Route
          path="/result"
          element={<ResultScreen />}
        />
      </Routes>
    </div>
  );
}

export default App;
