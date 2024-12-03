export interface Ride {
  id: number;
  date: string;
  userId: number;
  driverId: number;
  fare: number;
  distance: number;
}

export interface UserStats {
  userId: number;
  totalRides: number;
  totalSpent: number;
}

export interface DriverStats {
  driverId: number;
  totalRides: number;
  totalEarnings: number;
}

export interface AnalyticsReport {
  rideVolume: number;
  revenue: number;
  userStats: UserStats[];
  driverStats: DriverStats[];
}
