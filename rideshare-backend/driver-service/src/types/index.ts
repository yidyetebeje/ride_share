export type ServerResponse<Data> = {
  isSuccess: boolean;
  message: string;
  data: Data | null;
};


export type Transaction = {
  id: string;
  userId: string;
  amount: number;
  paymentMethod: string;
  status: string;
  createdAt: Date;
};
