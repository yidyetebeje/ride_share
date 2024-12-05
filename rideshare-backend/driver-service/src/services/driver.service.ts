// src/services/driver.service.ts
import { PrismaClient, Driver, DriverStatus, Vehicle } from "@prisma/client";

const prisma = new PrismaClient();

class DriverService {
  async onboardDriver(
    data: Omit<Driver, "id" | "createdAt" | "updatedAt"> & {
      vehicle: Omit<Vehicle, "id" | "createdAt" | "updatedAt">; // Include vehicle data in the input
    }
  ): Promise<Driver> {
    return await prisma.driver.create({
      data: {
        name: data.name,
        email: data.email,
        phoneNumber: data.phoneNumber,
        profilePicture: data.profilePicture,
        licenseNumber: data.licenseNumber,
        licenseExpiryDate: data.licenseExpiryDate,
        insuranceVerified: data.insuranceVerified,
        backgroundCheck: data.backgroundCheck,
        status: data.status,
        vehicles: {
          create: {
            // Create a new vehicle
            make: data.vehicle.make,
            model: data.vehicle.model,
            year: data.vehicle.year,
            plateNumber: data.vehicle.plateNumber,
            color: data.vehicle.color,
            registered: data.vehicle.registered,
          },
        },
      },
    });
  }

  async updateDriver(
    id: number,
    data: Partial<Omit<Driver, "id" | "createdAt" | "updatedAt">>
  ): Promise<Driver> {
    const status: DriverStatus = data.status as DriverStatus; // Ensure it's of type DriverStatus
    return await prisma.driver.update({
      where: { id },
      data: { ...data, status }, // Spread data and include status
    });
  }

  async getDriver(id: number): Promise<Driver | null> {
    return await prisma.driver.findUnique({ where: { id } });
  }

  async setDriverStatus(id: number, status: DriverStatus): Promise<Driver> {
    return await prisma.driver.update({
      where: { id },
      data: { status },
    });
  }

  async trackPerformance(driverId: number) {
    return await prisma.performance.findMany({ where: { driverId } }); // Use findMany
  }

  async trackEarnings(driverId: number) {
    return await prisma.earning.findMany({ where: { driverId } });
  }
}

export default new DriverService();
