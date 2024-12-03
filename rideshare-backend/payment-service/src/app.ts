import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";
import cors from "cors";
import errorHandler from "./middlewares/errorHandler";

import payment from "./routes/payment.routes";
const app = express();

app.use(bodyParser.json());
app.use(cors());
app.use(morgan("dev"));

// Middleware to parse URL-encoded data
app.use(express.urlencoded({ extended: true }));
app.use("/api/payment", payment);
app.get("/", (req, res) => {
  res.send("Payment Service  Is  Running"); // Response message for the root route
});

app.use(errorHandler);

export default app;
