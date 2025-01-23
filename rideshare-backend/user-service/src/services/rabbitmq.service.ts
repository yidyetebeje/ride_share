import amqplib from 'amqplib';

class RabbitMQService {
    private connection: amqplib.Connection | null = null;
    private channel: amqplib.Channel | null = null;

    async connect() {
        try {
            this.connection = await amqplib.connect(process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672');
            this.channel = await this.connection.createChannel();
            
            // Declare exchanges for user-driver communication
            await this.channel.assertExchange('user_events', 'topic', { durable: true });
            await this.channel.assertExchange('driver_events', 'topic', { durable: true });
            
            console.log('Connected to RabbitMQ');
        } catch (error) {
            console.error('RabbitMQ Connection Error:', error);
            throw error;
        }
    }

    async publishUserUpdate(userId: string, event: string, data: any) {
        if (!this.channel) throw new Error('RabbitMQ channel not established');
        
        const message = {
            userId,
            event,
            data,
            timestamp: new Date().toISOString()
        };

        this.channel.publish(
            'user_events',
            event,
            Buffer.from(JSON.stringify(message))
        );
    }

    async subscribeToDriverEvents(callback: (data: any) => Promise<void>) {
        if (!this.channel) throw new Error('RabbitMQ channel not established');

        const q = await this.channel.assertQueue('', { exclusive: true });
        await this.channel.bindQueue(q.queue, 'driver_events', '#');

        await this.channel.consume(q.queue, async (msg) => {
            if (msg) {
                const content = JSON.parse(msg.content.toString());
                await callback(content);
                this.channel?.ack(msg);
            }
        });
    }
}

export default new RabbitMQService();