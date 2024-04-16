import React, { useState } from "react";
import axios from "axios";
import { format } from "date-fns";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

interface ProcessedData {
  [key: string]: unknown;
}

// Following is a mapping of data types from the backend to the frontend.
const dataTypeMappings: { [key: string]: string } = {
  object: "Text",
  int64: "Integer",
  int32: "Integer",
  int16: "Integer",
  int8: "Integer",
  float64: "Float",
  float32: "Float",
  bool: "Boolean",
  "datetime64[ns]": "Date/Time",
  "timedelta[ns]": "Date/Time",
  category: "Category",
  complex: "Complex Number",
};

// Following is a list of available data types that the user can choose from.
const availableDataTypes = [
  "Text",
  "Integer",
  "Float",
  "Boolean",
  "Date/Time",
  "Category",
];

interface DataTypes {
  [key: string]: string;
}

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // This state is used to store the processed data.
  const [processedData, setProcessedData] = useState<ProcessedData[]>([]);

  // This state is used to store the data types of the processed data.
  const [dataTypes, setDataTypes] = useState<DataTypes>({});

  // This state is used to store the user's data type overrides.
  const [userDataTypeOverrides, setUserDataTypeOverrides] = useState<{
    [key: string]: string;
  }>({});

  // This function is called when the user selects a file.
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  // This function is called when the user clicks the "Upload" button.
  // It sends the file to the backend for processing.
  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/playground/upload/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        const responseData = JSON.parse(response.data.data);
        setProcessedData(responseData);
        setDataTypes(response.data.dataTypes);
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  // This function converts the value to a display value based on the data type.
  const convertToDisplayValue = (value: unknown, dataType: string): string => {
    if (value === null || value === undefined) {
      return "";
    } else if (
      dataTypeMappings[dataType] === "Date/Time" &&
      typeof value === "number"
    ) {
      return format(new Date(value), "MM/dd/yyyy");
    } else {
      return String(value);
    }
  };

  return (
    <div>
      <div className="flex justify-between gap-10 mb-20">
        <Input type="file" onChange={handleFileChange} />
        <Button onClick={handleUpload}>Upload</Button>
      </div>

      {processedData.length > 0 && (
        <div>
          <div className="font-bold text-3xl flex justify-center mb-10">
            Processed Data:
          </div>
          <Table>
            <TableCaption>A list of processed data.</TableCaption>
            <TableHeader>
              <TableRow>
                {Object.keys(processedData[0]).map((key) => (
                  <TableHead key={key}>
                    <div className="mb-2">{key}</div>
                    <select
                      value={userDataTypeOverrides[key] || dataTypes[key]}
                      onChange={(e) => {
                        setUserDataTypeOverrides({
                          ...userDataTypeOverrides,
                          [key]: e.target.value,
                        });
                      }}
                    >
                      {availableDataTypes.map((type) => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {processedData.map((row, index) => (
                <TableRow key={index}>
                  {Object.keys(row).map((key) => (
                    <TableCell key={key} className="font-medium">
                      {convertToDisplayValue(
                        row[key],
                        userDataTypeOverrides[key] || dataTypes[key]
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
