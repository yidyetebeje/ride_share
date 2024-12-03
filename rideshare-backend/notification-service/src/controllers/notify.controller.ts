import { Request, Response } from "express";
import {
  notifyViaTelegram,
  notifyViaEmail,
  getRandomWaitingTime,
} from "../services/notify.service";
import { NotificationRequest } from "../types/index";

export const sendNotification = async (
  req: Request,
  res: Response
): Promise<Response> => {
  const { userId, chatId, email, carfound, arrivingTime }: NotificationRequest =
    req.body;

  // Validate required fields
  if (!userId || carfound === undefined) {
    return res.status(400).json({ error: "Missing required fields!" });
  }

  let message: string;
  if (carfound === "yes") {
    message = `Car found! It will arrive in ${arrivingTime || "N/A"}.`;
  } else {
    const randomWaitingTime = getRandomWaitingTime();
    message = `No car found yet. Estimated waiting time: ${randomWaitingTime}.`;
  }

  try {
    if (email && chatId) {
      await notifyViaEmail(email, message);
      await notifyViaTelegram(chatId, message);
    } else if (chatId) {
      await notifyViaTelegram(chatId, message);
    } else if (email) {
      await notifyViaEmail(email, message);
    } else {
      return res
        .status(400)
        .json({ error: "No valid notification method provided!" });
    }

    return res.status(200).json({
      message: "Notification sent successfully!",
      details: { message },
    });
  } catch (error) {
    console.error("Error sending notification:", error);
    return res.status(500).json({ error: "Failed to send notification!" });
  }
};
