FROM node:20-slim

WORKDIR /app
RUN apt-get update -y && apt-get install -y openssl libssl-dev
COPY package*.json ./
COPY . .
RUN npm install



RUN npm run build


ENV DATABASE_URL=postgresql://distributed-systems_owner:I2JU3gyYRjMQ@ep-shy-voice-a5w5qigi.us-east-2.aws.neon.tech/distributed-systems?sslmode=require
ENV SMTP_HOST=smtp.example.com
ENV SMTP_PORT=587
ENV SMTP_USER=yohannesgetachew.e@gmail.com 
ENV SMTP_PASS="bjlf npye ljfj zehy"
ENV TELEGRAM_BOT_TOKEN=8042429948:AAGbdGpsvVJQPjdtDbb5dLqeVA6ULym5QKI

EXPOSE 3001

CMD ["npm", "start"]