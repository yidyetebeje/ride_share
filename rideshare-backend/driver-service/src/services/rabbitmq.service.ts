import amqplib, { Connection, Channel } from 'amqplib';

class RabbitMQService {
    private connection: Connection | null = null;
    private channel: Channel | null = null;
    private isConnecting: boolean = false;

    async connect() {
        if (this.isConnecting) return;
        this.isConnecting = true;

        try {
            // Close existing connections if any
            if (this.channel) await this.channel.close();
            if (this.connection) await this.connection.close();

            // Create new connection
            this.connection = await amqplib.connect(
                process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672'
            );

            // Handle connection errors and reconnection
            this.connection.on('error', (err) => {
                console.error('RabbitMQ connection error:', err);
                this.reconnect();
            });

            this.connection.on('close', () => {
                console.error('RabbitMQ connection closed. Reconnecting...');
                this.reconnect();
            });

            // Create channel
            this.channel = await this.connection.createChannel();
            
            // Declare exchanges
            await this.channel.assertExchange('user_events', 'topic', { durable: true });
            await this.channel.assertExchange('driver_events', 'topic', { durable: true });
            
            console.log('Successfully connected to RabbitMQ');
        } catch (error) {
            console.error('Failed to connect to RabbitMQ:', error);
            this.reconnect();
        } finally {
            this.isConnecting = false;
        }
    }

    private async reconnect() {
        setTimeout(async () => {
            console.log('Attempting to reconnect to RabbitMQ...');
            await this.connect();
        }, 5000); // Wait 5 seconds before reconnecting
    }

    private async ensureConnection() {
        if (!this.channel || !this.connection) {
            await this.connect();
        }
    }

    async publishDriverUpdate(driverId: number, event: string, data: any) {
        try {
            await this.ensureConnection();
            
            if (!this.channel) {
                throw new Error('RabbitMQ channel not established');
            }

            const message = {
                driverId,
                event,
                data,
                timestamp: new Date().toISOString()
            };

            const success = this.channel.publish(
                'driver_events',
                event,
                Buffer.from(JSON.stringify(message))
            );

            if (!success) {
                throw new Error('Message was not published successfully');
            }

            console.log(`Published driver update: ${event}`, { driverId, data });
        } catch (error) {
            console.error('Error publishing driver update:', error);
            throw error;
        }
    }

    async subscribeToUserEvents(callback: (data: any) => Promise<void>) {
        try {
            await this.ensureConnection();
            
            if (!this.channel) {
                throw new Error('RabbitMQ channel not established');
            }

            const q = await this.channel.assertQueue('driver_service_queue', { 
                exclusive: true,
                durable: true 
            });

            await this.channel.bindQueue(q.queue, 'user_events', '#');

            await this.channel.consume(q.queue, async (msg) => {
                if (msg) {
                    try {
                        const content = JSON.parse(msg.content.toString());
                        await callback(content);
                        this.channel?.ack(msg);
                    } catch (error) {
                        console.error('Error processing message:', error);
                        // Reject the message and requeue it
                        this.channel?.nack(msg, false, true);
                    }
                }
            });

            console.log('Successfully subscribed to user events');
        } catch (error) {
            console.error('Error subscribing to user events:', error);
            throw error;
        }
    }

    async closeConnection() {
        try {
            if (this.channel) await this.channel.close();
            if (this.connection) await this.connection.close();
        } catch (error) {
            console.error('Error closing RabbitMQ connection:', error);
        }
    }
}

export default new RabbitMQService();