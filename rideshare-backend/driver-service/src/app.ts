import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";
import cors from "cors";
import errorHandler from "./middlewares/errorHandler";

import driver from "./routes/driver.routes";
import rabbitmqService from "./services/rabbitmq.service";

const app = express();
// Initialize RabbitMQ
const initRabbitMQ = async (retries = 5) => {
  for (let i = 0; i < retries; i++) {
      try {
          await rabbitmqService.connect();
          console.log('Successfully connected to RabbitMQ');
          return;
      } catch (error) {
          console.error(`Failed to connect to RabbitMQ (attempt ${i + 1}/${retries}):`, error);
          if (i < retries - 1) {
              await new Promise(resolve => setTimeout(resolve, 5000));
          }
      }
  }
  console.error('Failed to connect to RabbitMQ after all retries');
};

initRabbitMQ().catch(console.error);

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
