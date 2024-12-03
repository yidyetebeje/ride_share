export type ServerResponse<Data> = {
  isSuccess: boolean;
  message: string;
  data: Data | null;
};

export interface NotificationRequest {
  userId: number;
  chatId?: number;
  email?: string;
  carfound: "yes" | "no";
  waitingTime?: string;
  arrivingTime?: string;
}
