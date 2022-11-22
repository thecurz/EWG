import React from "react";
import axios from "axios";
import graph from './test.png'
import { useEffect } from "react";
const fetchData = async () => {
  const data = await fetch("http://localhost:5000/api/hello");
  const jsonData = await data.json();
  console.log(jsonData);
};

function App() {
  return (
    <main>
      <h1 className=" text-3xl pb-8">English Words Graph</h1>
      <div>
        <h2 className="text-xl">
          How related are the following words in meaning? (Please rate on a
          scale of 0 to 10, where 0 means both words could hardly be found in
          the same sentence, 5 means they're generally related, 7 means they're
          both used to talk about a specific topic and 10 means they're close
          synonyms.)
        </h2>
        <div className="mt-4 mb-4">
          <span> Word1 </span>
          <input className="border-2 border-black" type="text" />
          <span> Word2</span>
          <button className="mt-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded block">
            Submit
          </button>
        </div>
        <div className="mt-4 mb-4">
          <h2 className="text-xl">
            Insert two words whose relatedness you want to find.
          </h2>
          <div className="mt-4 mb-4">
            <span>Word 1:</span>
            <input className="border-2 border-black" type="text" />
            <span>Word 2:</span>
            <input className="border-2 border-black" type="text" />
            <button className="mt-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded block">
              Consult
            </button>
          </div>
        </div>
      </div>
      <div><img src={graph} alt="" /></div>
    </main>
  );
}

export default App;
