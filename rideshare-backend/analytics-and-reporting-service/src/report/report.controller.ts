import { Controller, Get, Query } from '@nestjs/common';
import { ReportService } from './report.service';

@Controller('reports')
export class ReportController {
  constructor(private readonly reportsService: ReportService) {}

  @Get('summary')
  getSummaryReport() {
    return this.reportsService.generateSummaryReport();
  }

  @Get('date-range')
  getDateRangeReport(
    @Query('start') startDate: string,
    @Query('end') endDate: string,
  ) {
    return this.reportsService.generateDateRangeReport(startDate, endDate);
  }

  @Get('export')
  exportReport(
    @Query('format') format: 'json' | 'csv',
    @Query('type') type: 'summary' | 'date-range',
    @Query('start') startDate?: string,
    @Query('end') endDate?: string,
  ) {
    let data;
    if (type === 'summary') {
      data = this.reportsService.generateSummaryReport();
    } else if (type === 'date-range' && startDate && endDate) {
      data = this.reportsService.generateDateRangeReport(startDate, endDate);
    } else {
      return { error: 'Invalid report type or missing parameters' };
    }

    return this.reportsService.exportReport(format, data);
  }
}
