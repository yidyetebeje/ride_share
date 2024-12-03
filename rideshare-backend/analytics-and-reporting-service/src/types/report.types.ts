export interface ReportSummary {
  totalRides: number;
  totalRevenue: number;
  activeUsers: number;
  activeDrivers: number;
}

export interface ReportDetail {
  date: string;
  rides: number;
  revenue: number;
}

export interface ExportReport {
  format: 'json' | 'csv';
  data: any;
}
