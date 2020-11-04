import React, { useState } from "react";
import axios from "axios";
import papers from "../json/papers.json";
import Select from "react-select";
import {
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Bar,
  Label,
} from "recharts";

const index = () => {
  const [burrows, setburrows]: [any, Function] = useState(null);
  const [author, setAuthor]: [string, Function] = useState("Madison");
  const [selected, setSelected]: [any, Function] = useState("");
  const [res, setRes]: [any, Function] = useState("");

  const options = papers[author].map((paper: any) => ({
    value: paper,
    label: paper,
  }));

  const req = async (path: string) => {
    const res = await axios({
      url: `http://127.0.0.1:3000/${path}`,
      method: "POST",
      data: selected,
    });
    console.log(res.data);

    const data = res.data.mostCommon;
    const chart = data.map((token: any) => ({
      name: token[0],
      freq: token[1],
    }));
    let min = 9999;
    let minAuth = "";
    Object.keys(res.data.results).map((auth) => {
      if (res.data.results[auth] < min) {
        min = res.data.results[auth];
        minAuth = auth;
      }
    });
    setRes(minAuth);
    setburrows(chart);
  };

  return (
    <div className="flex justify-start h-screen">
      <div className="z-10 flex flex-col items-end ">
        <button className="author" onClick={() => setAuthor("Madison")}>
          Madison
        </button>
        <button className="author" onClick={() => setAuthor("Hamilton")}>
          Hamilton
        </button>
        <button className="author" onClick={() => setAuthor("Jay")}>
          Jay
        </button>
        <button className="mt-8 btn" onClick={() => req("burrows")}>
          Submit
        </button>
      </div>
      <div className="z-20 w-32 mt-8 ml-8">
        <Select
          options={options}
          placeholder={author}
          onChange={(e) =>
            setSelected({ disputedAuthor: author, disputedPaper: e.value })
          }
        />
      </div>
      {selected && (
        <p className="mt-8 ml-8 text-lg font-light">
          You selected paper {selected.disputedPaper} from{" "}
          {selected.disputedAuthor}
        </p>
      )}
      <div className="fixed z-0 flex flex-col items-center justify-center w-screen h-screen">
        {burrows && (
          <p className="mb-8 text-xl font-semibold text-red-700">
            {res === author
              ? `I guessed it correctly, it was in fact ${author}`
              : "I didn't guess correctly"}
          </p>
        )}
        {burrows && (
          <BarChart width={1000} height={500} data={burrows}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="freq" fill="#319795" />
          </BarChart>
        )}
      </div>
    </div>
  );
};

export default index;

{
  /*  <div className="flex flex-row mb-4">
        <div className="flex flex-col mx-6">
          <button className="btn" onClick={() => req("burrows")}>
            Burrow's
          </button>
        </div>
      </div> */
}
