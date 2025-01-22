import amqp from 'amqplib';

class RabbitMQService {
    private connection: amqp.Connection | null = null;
    private channel: amqp.Channel | null = null;

    async connect() {
        try {
            // Use localhost when running locally, rabbitmq when in Docker
            const host = process.env.NODE_ENV === 'production' ? 'rabbitmq' : 'localhost';
            this.connection = await amqp.connect(`amqp://guest:guest@${host}:5672`);
            this.channel = await this.connection.createChannel();
            
            // Declare queues
            await this.channel.assertQueue('driver_updates', { durable: true });
            await this.channel.assertQueue('ride_requests', { durable: true });
            
            console.log('Connected to RabbitMQ');
        } catch (error) {
            console.error('RabbitMQ Connection Error:', error);
            throw error;
        }
    }

    async publishDriverUpdate(driverId: number, status: string) {
        if (!this.channel) throw new Error('RabbitMQ channel not established');
        
        const message = {
            driverId,
            status,
            timestamp: new Date().toISOString()
        };

        this.channel.sendToQueue(
            'driver_updates',
            Buffer.from(JSON.stringify(message))
        );
    }

    async consumeRideRequests(callback: (data: any) => Promise<void>) {
        if (!this.channel) throw new Error('RabbitMQ channel not established');

        await this.channel.consume('ride_requests', async (msg) => {
            if (msg) {
                const content = JSON.parse(msg.content.toString());
                await callback(content);
                this.channel?.ack(msg);
            }
        });
    }
}

export default new RabbitMQService();