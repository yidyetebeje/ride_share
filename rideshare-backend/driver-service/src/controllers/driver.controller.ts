// src/controllers/driver.controller.ts
import { Request, Response } from "express";
import driverService from "../services/driver.service";
import { Driver } from "@prisma/client";

export const onboardDriver = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const driver: Driver = await driverService.onboardDriver(req.body);
    return res.status(201).json(driver);
  } catch (error: any) {
    console.error("Error onboarding driver:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const updateDriver = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const driver: Driver = await driverService.updateDriver(
      Number(req.params.id),
      req.body
    );
    return res.json(driver);
  } catch (error: any) {
    console.error("Error updating driver:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const getDriver = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const driver: Driver | null = await driverService.getDriver(
      Number(req.params.id)
    );
    return res.json(driver);
  } catch (error: any) {
    console.error("Error fetching driver:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const setDriverStatus = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const driver: Driver = await driverService.setDriverStatus(
      Number(req.params.id),
      req.body.status
    );
    return res.json(driver);
  } catch (error: any) {
    console.error("Error setting driver status:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const trackPerformance = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const performance = await driverService.trackPerformance(
      Number(req.params.id)
    );
    return res.json(performance);
  } catch (error: any) {
    console.error("Error tracking performance:", error);
    return res.status(500).json({ message: error.message });
  }
};

export const trackEarnings = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const earnings = await driverService.trackEarnings(Number(req.params.id));
    return res.json(earnings);
  } catch (error: any) {
    console.error("Error tracking earnings:", error);
    return res.status(500).json({ message: error.message });
  }
};
