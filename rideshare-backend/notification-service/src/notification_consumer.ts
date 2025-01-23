import amqp, { Channel, Connection, ConsumeMessage } from 'amqplib';
import nodemailer, { Transporter } from 'nodemailer';
import axios, { AxiosResponse } from 'axios';

// Types for message data
interface NotificationMessage {
  type: 'notification';
  email: string;
  telegram_chat_id: string;
  content: string;
}

// Configuration types
interface ServiceConfig {
  SMTP_USER: string;
  SMTP_PASS: string;
  TELEGRAM_BOT_TOKEN: string;
  RABBITMQ_HOST: string;
  RABBITMQ_QUEUE_NAME: string;
}

// Configuration
const config: ServiceConfig = {
  SMTP_USER: "yohannesgetachew.e@gmail.com",
  SMTP_PASS: "bjlf npye ljfj zehy",
  TELEGRAM_BOT_TOKEN: "8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI",
  RABBITMQ_HOST: 'rabbitmq',
  RABBITMQ_QUEUE_NAME: 'notification_queue'
};

export async function connectAndConsume(): Promise<void> {
    try {
        const connection: Connection = await amqp.connect(`amqp://${config.RABBITMQ_HOST}`);
        const channel: Channel = await connection.createChannel();

        await channel.assertQueue(config.RABBITMQ_QUEUE_NAME, { durable: true });

        console.log(` [*] Waiting for messages in ${config.RABBITMQ_QUEUE_NAME}. To exit press CTRL+C`);

        channel.consume(config.RABBITMQ_QUEUE_NAME, async (msg: ConsumeMessage | null) => {
            if (msg !== null) {
                const messageData = JSON.parse(msg.content.toString()) as NotificationMessage;
                console.log(" [x] Received message:", messageData);

                if (messageData.type === 'notification') {
                    try {
                        await sendEmail(messageData.email, messageData.content);
                        await sendTelegram(messageData.telegram_chat_id, messageData.content);
                        console.log("  [√] Notifications sent successfully.");
                    } catch (error) {
                        console.error("  [!] Error sending notifications:", error);
                    }
                }

                channel.ack(msg);
            }
        }, {
            noAck: false
        });

    } catch (error) {
        console.error("Error connecting to RabbitMQ or consuming:", error);
    }
}

async function sendEmail(to: string, content: string): Promise<void> {
    try {
        const transporter: Transporter = nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 587,
            secure: false,
            auth: {
                user: config.SMTP_USER,
                pass: config.SMTP_PASS,
            },
        });

        const info = await transporter.sendMail({
            from: `"Ride Sharing App" <${config.SMTP_USER}>`,
            to: to,
            subject: "🚗 Ride Sharing Notification",
            html: `
                <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; border-radius: 5px;">
                    <h2 style="color: #333;">Hello!</h2>
                    <p style="color: #555;">${content}</p>
                    <p style="color: #555;">Thank you for using our service!</p>
                    <footer style="margin-top: 20px; font-size: 12px; color: #888;">
                        © ${new Date().getFullYear()} Ride Sharing App. All rights reserved.
                    </footer>
                </div>
            `,
        });

        console.log("Email sent to:", to, info.messageId);
    } catch (error) {
        console.error("Error sending email:", error);
        throw error;
    }
}

interface TelegramResponse {
    ok: boolean;
    result?: any;
    error?: string;
    description?: string;
}

async function sendTelegram(chatId: string, content: string): Promise<void> {
    try {
        const message = `
            *🚗 Ride Sharing Notification*

            _Hello!_

            ${content}

            Thank you for choosing our service! 🚀

            If you have any questions, feel free to reach out to us.
        `;

        const url = `https://api.telegram.org/bot${config.TELEGRAM_BOT_TOKEN}/sendMessage`;
        const payload = {
            chat_id: chatId,
            text: message,
            parse_mode: "Markdown"
        };

        const response: AxiosResponse<TelegramResponse> = await axios.post(url, payload);
        
        if (response.data.error) {
            console.error("Telegram API error:", response.data);
            throw new Error(`Telegram API error: ${response.data.description || 'Unknown error'}`);
        } else {
            console.log(`Message sent to chat ID ${chatId}`);
        }
    } catch (error) {
        console.error("Error sending Telegram message:", error);
        throw error;
    }
}


