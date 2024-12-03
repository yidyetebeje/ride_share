import { Injectable } from '@nestjs/common';
import {
  ReportSummary,
  ReportDetail,
  ExportReport,
} from '../types/report.types';
import { generateDummyRides } from '../utils/dataGenerator';

@Injectable()
export class ReportService {
  private readonly dummyRides = generateDummyRides(1000);

  generateSummaryReport(): ReportSummary {
    const totalRides = this.dummyRides.length;
    const totalRevenue = this.dummyRides.reduce(
      (sum, ride) => sum + ride.fare,
      0,
    );

    const activeUsers = new Set(this.dummyRides.map((ride) => ride.userId))
      .size;
    const activeDrivers = new Set(this.dummyRides.map((ride) => ride.driverId))
      .size;

    return { totalRides, totalRevenue, activeUsers, activeDrivers };
  }

  generateDateRangeReport(startDate: string, endDate: string): ReportDetail[] {
    const start = new Date(startDate).getTime();
    const end = new Date(endDate).getTime();

    const filteredRides = this.dummyRides.filter((ride) => {
      const rideDate = new Date(ride.date).getTime();
      return rideDate >= start && rideDate <= end;
    });

    const report: ReportDetail[] = [];
    filteredRides.forEach((ride) => {
      const date = ride.date.split('T')[0]; // Extract the date part
      const existing = report.find((r) => r.date === date);
      if (existing) {
        existing.rides += 1;
        existing.revenue += ride.fare;
      } else {
        report.push({ date, rides: 1, revenue: ride.fare });
      }
    });

    return report;
  }

  exportReport(format: 'json' | 'csv', data: any): ExportReport {
    if (format === 'json') {
      return { format: 'json', data };
    }

    // CSV Conversion
    const csvRows = [Object.keys(data[0]).join(',')]; // Header row
    data.forEach((row: any) => {
      const values = Object.values(row).join(',');
      csvRows.push(values);
    });

    return { format: 'csv', data: csvRows.join('\n') };
  }
}
