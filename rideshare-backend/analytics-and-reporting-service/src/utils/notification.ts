import axios from 'axios';
const TELEGRAM_BOT_TOKEN = '8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI';
export const sendNotification = async (
  chatId: string,
  content: string,
  textMessage = (content: string) => content,
): Promise<void> => {
  const message = textMessage(content);

  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;

  try {
    await axios.post(url, {
      chat_id: chatId,
      text: message,
      parse_mode: 'Markdown',
    });
    console.log(`Message sent to chat ID ${chatId}`);
  } catch (error) {
    console.error('Error sending Telegram message:', error);
    throw new Error('Failed to send Telegram message');
  }
};
