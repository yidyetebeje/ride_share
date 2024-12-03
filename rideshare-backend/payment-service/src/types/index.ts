export type ServerResponse<Data> = {
  isSuccess: boolean;
  message: string;
  data: Data | null;
};

// src/models/transaction.ts
export interface Transaction {
  id: string;
  userId: string;
  amount: number;
  paymentMethod: string;
  status: "pending" | "completed" | "failed" | "refunded";
  createdAt: Date;
}
