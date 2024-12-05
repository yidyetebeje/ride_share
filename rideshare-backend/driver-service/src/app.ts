import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";
import cors from "cors";
import errorHandler from "./middlewares/errorHandler";

import driver from "./routes/driver.routes";
const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use(morgan("dev"));

// Middleware to parse URL-encoded data
app.use(express.urlencoded({ extended: true }));
app.use("/api/drivers", driver);
app.get("/", (req, res) => {
  res.send("Driver Service  Is  Running");
});

app.use(errorHandler);

export default app;
