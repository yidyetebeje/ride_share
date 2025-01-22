FROM node:16-slim

WORKDIR /app

# Install OpenSSL and other required dependencies
RUN apt-get update -y && \
    apt-get install -y openssl curl git && \
    rm -rf /var/lib/apt/lists/*

# Set npm configurations for better reliability
RUN npm config set fetch-retry-maxtimeout 600000 && \
    npm config set fetch-retry-mintimeout 10000 && \
    npm config set fetch-retries 5

# Copy package files
COPY package*.json ./

# Install dependencies with retry mechanism
RUN for i in 1 2 3; do npm install --no-audit --no-fund && break || sleep 15; done

# Copy Prisma files and generate client
COPY prisma ./prisma/
RUN npx prisma generate

# Copy the rest of the application
COPY . .

# Build TypeScript
RUN npm run build

EXPOSE 4343

CMD ["npm", "start"]