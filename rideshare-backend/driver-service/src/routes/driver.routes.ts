// path/to/routes/driverRoutes.ts
import { Router } from "express";
import {
  onboardDriver,
  updateDriver,
  setDriverStatus,
  getDriver,
  trackPerformance,
  trackEarnings,
} from "../controllers/driver.controller";

const router = Router();

router.post("/", onboardDriver);
router.put("/:id", updateDriver);
router.get("/:id", getDriver);
router.patch("/:id/status", setDriverStatus);
router.get("/:id/performance", trackPerformance);
router.get("/:id/earnings", trackEarnings);

export default router;
