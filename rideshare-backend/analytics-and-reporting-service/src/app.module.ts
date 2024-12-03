import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AnalyticsModule } from './analytics/analytics.module';
import { ReportModule } from './report/report.module';

@Module({
  imports: [AnalyticsModule, ReportModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
