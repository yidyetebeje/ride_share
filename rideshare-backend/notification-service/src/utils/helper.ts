// src/utils/notificationSender.ts
import nodemailer from "nodemailer";
import axios from "axios";

// Nodemailer setup
const transporter = nodemailer.createTransport({
  host: "smtp.example.com", // Replace with your SMTP server
  port: 587, // Replace with your SMTP port
  secure: false, // true for 465, false for other ports
  auth: {
    user: "your-email@example.com", // Replace with your email
    pass: "your-email-password", // Replace with your email password
  },
});

// Telegram Bot Token
const TELEGRAM_BOT_TOKEN = "8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI"; // Replace with your Telegram bot token

// Function to send email
export const sendEmail = async (to: string, content: string): Promise<void> => {
  const mailOptions = {
    from: '"Your Service Name" <your-email@example.com>', // Sender address
    to, // List of recipients
    subject: "Notification from Your Service", // Subject line
    text: content, // Plain text body
    // html: "<b>Hello world?</b>", // HTML body (optional)
  };

  try {
    await transporter.sendMail(mailOptions);
    console.log(`Email sent to ${to}`);
  } catch (error) {
    console.error("Error sending email:", error);
    throw new Error("Failed to send email");
  }
};

// Function to send Telegram message
export const sendTelegram = async (
  chatId: string,
  content: string
): Promise<void> => {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;

  try {
    await axios.post(url, {
      chat_id: chatId,
      text: content,
    });
    console.log(`Message sent to chat ID ${chatId}`);
  } catch (error) {
    console.error("Error sending Telegram message:", error);
    throw new Error("Failed to send Telegram message");
  }
};
