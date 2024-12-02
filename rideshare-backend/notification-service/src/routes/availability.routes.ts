import { Router } from "express";
import {
  requestRide,
  notifyDriverFound,
  notifyNoDriver,
  getAvailability,
} from "../controllers/availability.controller";

const router = Router();
router.post("/request", requestRide);
router.post("/no-driver", notifyNoDriver);
router.post("/driver-found", notifyDriverFound);
router.get("/:userId", getAvailability);

export default router;
