// src/controllers/paymentController.ts
import { Request, Response } from "express";
import { PaymentService } from "../services/payment.service";

const paymentService = new PaymentService();

export const makePayment = async (req: Request, res: Response) => {
  const { userId, amount, paymentMethod } = req.body;
  try {
    const transaction = await paymentService.processPayment(
      userId,
      amount,
      paymentMethod
    );
    paymentService.logTransaction(transaction);
    res
      .status(200)
      .json({ message: "Payment processed successfully", transaction });
  } catch (error) {
    res.status(500).json({ error: "Payment processing failed" });
  }
};

export const calculateFare = (req: Request, res: Response) => {
  const { distance, time, baseFare, ratePerMile, ratePerMinute } = req.body;
  const fare = paymentService.calculateFare(
    distance,
    time,
    baseFare,
    ratePerMile,
    ratePerMinute
  );
  res.status(200).json({ fare });
};
