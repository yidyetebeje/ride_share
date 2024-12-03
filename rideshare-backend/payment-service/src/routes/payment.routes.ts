// src/routes/paymentRoutes.ts
import { Router } from "express";
import { makePayment, calculateFare } from "../controllers/payment.controller";

const router = Router();

router.post("/", makePayment);
router.post("/fare", calculateFare);

export default router;
