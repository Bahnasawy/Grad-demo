import React, { useState } from "react";
import axios from "axios";

const index = () => {
  const [res, setRes]: [any, Function] = useState({});
  const [kilgarif, setKilgarif]: [any, Function] = useState({});
  const [burrows, setburrows]: [any, Function] = useState({});

  const req = async (path: string) => {
    const res = await axios({
      url: `http://127.0.0.1:3000/${path}`,
      method: "GET",
    });
    path === "kilgariff" ? setKilgarif(res.data) : setburrows(res.data);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex flex-row mb-4">
        <div className="flex flex-col mx-6">
          <button
            className="px-2 py-1 text-gray-100 bg-teal-600 rounded"
            onClick={() => req("kilgariff")}
          >
            Kilgariff
          </button>1
          {Object.keys(kilgarif).map((key) => (
            <p key={key}>
              {key}: {kilgarif[key]}
            </p>
          ))}
        </div>
        <div className="flex flex-col mx-6">
          <button
            className="px-2 py-1 text-gray-100 bg-teal-600 rounded"
            onClick={() => req("burrows")}
          >
            Burrow's
          </button>
          {Object.keys(burrows).map((key) => (
            <p key={key}>
              {key}: {burrows[key]}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default index;
