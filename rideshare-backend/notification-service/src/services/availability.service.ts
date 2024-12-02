import { PrismaClient, DriverAvailability } from "@prisma/client";
import { sendEmail, sendTelegram } from "../utils/helper";

const prisma = new PrismaClient();

export class AvailabilityService {
  async requestRide(
    userId: string,
    chatId: string
  ): Promise<DriverAvailability> {
    return await prisma.driverAvailability.create({
      data: { userId, status: "pending" },
    });
  }

  async notifyNoDriver(
    userId: string,
    chatId: string,
    waitTime: number
  ): Promise<DriverAvailability> {
    const content = `No drivers are currently available. Please wait ${waitTime} minutes and try again.`;
    const notificationType = chatId ? "Telegram" : "email";

    await this.sendNotification({
      userId,
      chatId,
      type: notificationType,
      content,
    });
    return await prisma.driverAvailability.update({
      where: { id: userId },
      data: { status: "no_driver_available" },
    });
  }

  async notifyDriverFound(
    userId: string,
    chatId: string,
    etaInMinutes: number
  ): Promise<DriverAvailability> {
    const content = `A driver has been found! They will arrive in approximately ${etaInMinutes} minutes.`;
    const notificationType = chatId ? "Telegram" : "email";

    await this.sendNotification({
      userId,
      chatId,
      type: notificationType,
      content,
    });

    // Check if the record exists
    const existingRecord = await prisma.driverAvailability.findUnique({
      where: { id: userId }, // Assuming userId is unique in your model
    });

    if (!existingRecord) {
      throw new Error(`No availability record found for userId: ${userId}`);
    }

    return await prisma.driverAvailability.update({
      where: { id: existingRecord.id }, // Use the id of the found record
      data: { status: "driver_found", etaInMinutes },
    });
  }
  async getAvailability(userId: string): Promise<DriverAvailability | null> {
    return await prisma.driverAvailability.findUnique({
      where: { id: userId },
    });
  }

  private async sendNotification({
    userId,
    chatId,
    type,
    content,
  }: {
    userId: string;
    chatId: string;
    type: "email" | "Telegram";
    content: string;
  }): Promise<void> {
    if (type === "email") {
      await sendEmail(userId, content);
    } else if (type === "Telegram") {
      await sendTelegram(chatId, content);
    }
  }
}
