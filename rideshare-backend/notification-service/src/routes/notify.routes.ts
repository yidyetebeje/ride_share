import { Router } from "express";
import { sendNotification } from "../controllers/notify.controller";

const router = Router();
router.post("/", sendNotification);

export default router;
