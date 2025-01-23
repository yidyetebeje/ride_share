import { Controller, Get, Param } from '@nestjs/common';
import { AnalyticsService } from './analytics.service';

@Controller('/api/analytics')
export class AnalyticsController {
  constructor(private readonly analyticsService: AnalyticsService) {}

  @Get()
  getAnalyticsReport() {
    return this.analyticsService.getAnalyticsReport();
  }

  @Get('user/:id')
  getUserStats(@Param('id') id: string) {
    const userId = parseInt(id, 10);
    return this.analyticsService.getUserStats(userId);
  }

  @Get('user')
  getAllUserStats() {
    return this.analyticsService.getAllUserStats();
  }

  @Get('driver/:id')
  getDriverStats(@Param('id') id: string) {
    const driverId = parseInt(id, 10);
    return this.analyticsService.getDriverStats(driverId);
  }

  @Get('driver')
  getAllDriverStats() {
    return this.analyticsService.getAllDriverStats();
  }
}
