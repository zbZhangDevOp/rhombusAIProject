import React from "react";
import "./App.css";
import FileUpload from "./components/FileUpload";

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <div className="font-bold text-3xl flex justify-center mb-10">
          CSV Inspector
        </div>
        <FileUpload />
      </header>
    </div>
  );
};

export default App;
