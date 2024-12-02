// src/controllers/availability.Controller.ts
import { Request, Response } from "express";
import { PrismaClient, DriverAvailability } from "@prisma/client";
import { AvailabilityService } from "../services/availability.service";
const prisma = new PrismaClient();
const availabilityService = new AvailabilityService();

export const requestRide = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const { userId, chatId } = req.body;
    const availability: DriverAvailability =
      await availabilityService.requestRide(userId, chatId);
    return res.status(200).json(availability);
  } catch (error: any) {
    console.error("Error requesting ride:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const notifyNoDriver = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const { userId, chatId, waitTime } = req.body;
    const notification: DriverAvailability =
      await availabilityService.notifyNoDriver(userId, chatId, waitTime);
    return res.status(200).json(notification);
  } catch (error: any) {
    console.error("Error notifying no driver:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const notifyDriverFound = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const { userId, chatId, etaInMinutes } = req.body;
    const notification: DriverAvailability =
      await availabilityService.notifyDriverFound(userId, chatId, etaInMinutes);
    return res.status(200).json(notification);
  } catch (error: any) {
    console.error("Error notifying driver found:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const getAvailability = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const { userId } = req.params; // Assuming userId is passed as a URL parameter
    const status: DriverAvailability | null =
      await availabilityService.getAvailability(userId);
    return res.status(200).json(status);
  } catch (error: any) {
    console.error("Error fetching availability:", error);
    return res.status(500).json({ message: error.message });
  }
};
