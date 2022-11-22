const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { PythonShell } = require("python-shell");
const { spawn } = require("child_process");
var package_name = "pytube";
let options = {
  args: [package_name],
};

const app = express();
const port = process.env.PORT || 5000;
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/api/hello", async (req, res) => {
  await PythonShell.run(
    "./install_package.py",
    options,
    function (err, results) {
      if (err) throw err;
      else console.log(results);
    }
  );
  await PythonShell.run("./script.py", options, function (err, results) {
    if (err) throw err;
    else console.log(results);
  });
  res.send({ express: "Hello From Express" });
});

app.post("/api/world", (req, res) => {
  console.log(req.body);
  res.send(
    `I received your POST request. This is what you sent me: ${req.body.post}`
  );
});

app.listen(port, () => console.log(`Listening on port ${port}`));
