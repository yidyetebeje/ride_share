import { sendEmail, sendTelegram } from "../utils/helper";

// Generate random waiting time (1-10 minutes)
export const getRandomWaitingTime = (): string =>
  `${Math.floor(Math.random() * 10) + 1} min`;

// Notify via Telegram
export const notifyViaTelegram = async (
  chatId: number,
  message: string
): Promise<void> => {
  try {
    await sendTelegram(chatId.toString(), message);
  } catch (error: any) {
    throw new Error(`Telegram notification failed: ${error.message}`);
  }
};

// Notify via Email
export const notifyViaEmail = async (
  email: string,
  message: string
): Promise<void> => {
  try {
    await sendEmail(email, message);
  } catch (error: any) {
    throw new Error(`Email notification failed: ${error.message}`);
  }
};
