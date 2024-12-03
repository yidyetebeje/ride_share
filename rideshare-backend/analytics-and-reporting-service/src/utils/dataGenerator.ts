import { Ride } from '../types/analytics.types';

const randomInt = (min: number, max: number): number =>
  Math.floor(Math.random() * (max - min + 1)) + min;

const randomDate = (start: Date, end: Date): string => {
  const date = new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime()),
  );
  return date.toISOString().split('T')[0];
};

// Generate dummy rides
export const generateDummyRides = (count: number): Ride[] => {
  const rides: Ride[] = [];
  for (let i = 0; i < count; i++) {
    rides.push({
      id: i + 1,
      date: randomDate(new Date('2024-01-01'), new Date('2024-12-31')),
      userId: randomInt(1, 100), // 100 users
      driverId: randomInt(1, 50), // 50 drivers
      fare: randomInt(10, 100), // Fare between 10-100
      distance: parseFloat((Math.random() * 20).toFixed(2)), // Distance up to 20km
    });
  }
  return rides;
};
