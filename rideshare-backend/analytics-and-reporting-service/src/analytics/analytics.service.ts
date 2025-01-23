import { Injectable } from '@nestjs/common';
import { generateDummyRides } from '../utils/dataGenerator';
import {
  AnalyticsReport,
  UserStats,
  DriverStats,
  Ride,
} from '../types/analytics.types';
import { sendNotification } from 'src/utils/notification';

@Injectable()
export class AnalyticsService {
  private readonly dummyRides: Ride[] = generateDummyRides(1000);

  getAnalyticsReport(): AnalyticsReport {
    const rideVolume = this.dummyRides.length;
    const revenue = this.dummyRides.reduce((sum, ride) => sum + ride.fare, 0);

    const userStats = this.aggregateUserStats();
    const driverStats = this.aggregateDriverStats();

    // Create a better formatted message with updated emojis
    const message = `
    📊 **Analytics Report**

    🚘 **Total Ride Volume**: ${rideVolume} rides
    💰 **Total Revenue**: $${revenue.toFixed(2)}

    👥 **User Statistics**:
     - Total Users:   ${userStats.length}
  

    🏎️ **Driver Statistics**:
    - Total Drivers:  ${driverStats.length}
  

    🔄 **Summary**:
    - Ride Volume: ${rideVolume} rides
    - Revenue: $${revenue.toFixed(2)}

    Keep up the great work! 🚀
  `;

    // Send the formatted notification message
    sendNotification('923913833', message);

    return { rideVolume, revenue, userStats, driverStats };
  }

  getUserStats(userId: number): UserStats {
    const ridesForUser = this.dummyRides.filter(
      (ride) => ride.userId === userId,
    );

    const totalRides = ridesForUser.length;
    const totalSpent = ridesForUser.reduce((sum, ride) => sum + ride.fare, 0);

    // Create a better formatted message with updated emojis
    const message = `
    🧑‍🤝‍🧑 **User Statistics Report** for User ID: ${userId}
    
    🚗 **Total Rides Taken**: ${totalRides} rides
    💵 **Total Spent**: $${totalSpent.toFixed(2)}

    Keep riding and enjoy the journey! 🚀
  `;

    // Send the formatted notification message
    sendNotification('923913833', message);

    return { userId, totalRides, totalSpent };
  }

  getAllUserStats(): UserStats[] {
    return this.aggregateUserStats();
  }

  getDriverStats(driverId: number): DriverStats {
    const ridesForDriver = this.dummyRides.filter(
      (ride) => ride.driverId === driverId,
    );

    const totalRides = ridesForDriver.length;
    const totalEarnings = ridesForDriver.reduce(
      (sum, ride) => sum + ride.fare,
      0,
    );

    // Format the message
    const message = `
  🏎️ **Driver Stats for Driver ID: ${driverId}**

  🚗 **Total Rides**: ${totalRides} rides
  💵 **Total Earnings**: $${totalEarnings.toFixed(2)}

  Keep up the great work! 🚀
  `;

    // Send the notification message
    sendNotification('923913833', message);

    return { driverId, totalRides, totalEarnings };
  }

  getAllDriverStats(): DriverStats[] {
    return this.aggregateDriverStats();
  }

  private aggregateUserStats(): UserStats[] {
    return this.dummyRides.reduce((acc, ride) => {
      const user = acc.find((u) => u.userId === ride.userId);
      if (user) {
        user.totalRides += 1;
        user.totalSpent += ride.fare;
      } else {
        acc.push({ userId: ride.userId, totalRides: 1, totalSpent: ride.fare });
      }
      return acc;
    }, [] as UserStats[]);
  }

  private aggregateDriverStats(): DriverStats[] {
    return this.dummyRides.reduce((acc, ride) => {
      const driver = acc.find((d) => d.driverId === ride.driverId);
      if (driver) {
        driver.totalRides += 1;
        driver.totalEarnings += ride.fare;
      } else {
        acc.push({
          driverId: ride.driverId,
          totalRides: 1,
          totalEarnings: ride.fare,
        });
      }
      return acc;
    }, [] as DriverStats[]);
  }
}
