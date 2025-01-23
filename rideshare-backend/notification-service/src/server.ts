import { createServer } from "http";
import app from "./app";
import { connectAndConsume } from "./notification_consumer";
const PORT = process.env.PORT || 5500;

const server = createServer(app);

server.listen(PORT, () => {
  connectAndConsume().catch(console.warn);
  console.log(`🚀  http://localhost:${PORT}`);
});
