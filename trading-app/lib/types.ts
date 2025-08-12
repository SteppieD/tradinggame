/**
 * Core financial data types for trading application
 * All types are strictly typed with no 'any' usage
 */

// Branded types for enhanced type safety
export type StockSymbol = string & { readonly __brand: unique symbol };
export type USD = number & { readonly __brand: unique symbol };
export type Percentage = number & { readonly __brand: unique symbol };
export type Volume = number & { readonly __brand: unique symbol };
export type MarketCap = number & { readonly __brand: unique symbol };

// Utility function to create branded types
export const createStockSymbol = (symbol: string): StockSymbol =>
  symbol as StockSymbol;
export const createUSD = (amount: number): USD => amount as USD;
export const createPercentage = (percent: number): Percentage =>
  percent as Percentage;
export const createVolume = (volume: number): Volume => volume as Volume;
export const createMarketCap = (marketCap: number): MarketCap =>
  marketCap as MarketCap;

// Time-based types
export interface TimeStamp {
  readonly timestamp: number;
  readonly date: Date;
}

// Market data enums
export const MarketStatus = {
  OPEN: 'OPEN',
  CLOSED: 'CLOSED',
  PRE_MARKET: 'PRE_MARKET',
  AFTER_HOURS: 'AFTER_HOURS',
} as const;

export type MarketStatus = (typeof MarketStatus)[keyof typeof MarketStatus];

export const OrderType = {
  MARKET: 'MARKET',
  LIMIT: 'LIMIT',
  STOP: 'STOP',
  STOP_LIMIT: 'STOP_LIMIT',
} as const;

export type OrderType = (typeof OrderType)[keyof typeof OrderType];

export const OrderSide = {
  BUY: 'BUY',
  SELL: 'SELL',
} as const;

export type OrderSide = (typeof OrderSide)[keyof typeof OrderSide];

export const OrderStatus = {
  PENDING: 'PENDING',
  FILLED: 'FILLED',
  PARTIALLY_FILLED: 'PARTIALLY_FILLED',
  CANCELLED: 'CANCELLED',
  REJECTED: 'REJECTED',
} as const;

export type OrderStatus = (typeof OrderStatus)[keyof typeof OrderStatus];

// Stock data interfaces
export interface StockPrice {
  readonly current: USD;
  readonly open: USD;
  readonly high: USD;
  readonly low: USD;
  readonly previousClose: USD;
  readonly change: USD;
  readonly changePercent: Percentage;
}

export interface StockVolume {
  readonly current: Volume;
  readonly average: Volume;
  readonly dayRange: readonly [Volume, Volume];
}

export interface StockMetrics {
  readonly marketCap: MarketCap;
  readonly peRatio: number | null;
  readonly eps: USD | null;
  readonly dividend: USD | null;
  readonly dividendYield: Percentage | null;
  readonly beta: number | null;
}

export interface StockData {
  readonly symbol: StockSymbol;
  readonly name: string;
  readonly price: StockPrice;
  readonly volume: StockVolume;
  readonly metrics: StockMetrics;
  readonly timestamp: TimeStamp;
  readonly marketStatus: MarketStatus;
}

// Historical data
export interface StockDataPoint extends TimeStamp {
  readonly symbol: StockSymbol;
  readonly open: USD;
  readonly high: USD;
  readonly low: USD;
  readonly close: USD;
  readonly volume: Volume;
  readonly adjustedClose?: USD;
}

export interface HistoricalData {
  readonly symbol: StockSymbol;
  readonly timeframe:
    | '1D'
    | '5D'
    | '1M'
    | '3M'
    | '6M'
    | '1Y'
    | '2Y'
    | '5Y'
    | 'MAX';
  readonly data: readonly StockDataPoint[];
}

// Portfolio types
export interface Position {
  readonly symbol: StockSymbol;
  readonly quantity: number;
  readonly averageCost: USD;
  readonly currentPrice: USD;
  readonly totalValue: USD;
  readonly unrealizedPnL: USD;
  readonly unrealizedPnLPercent: Percentage;
  readonly dayChange: USD;
  readonly dayChangePercent: Percentage;
}

export interface Portfolio {
  readonly accountId: string;
  readonly totalValue: USD;
  readonly totalCost: USD;
  readonly totalPnL: USD;
  readonly totalPnLPercent: Percentage;
  readonly dayChange: USD;
  readonly dayChangePercent: Percentage;
  readonly cashBalance: USD;
  readonly buyingPower: USD;
  readonly positions: readonly Position[];
  readonly lastUpdated: TimeStamp;
}

// Trade order types
export interface BaseOrder {
  readonly orderId: string;
  readonly symbol: StockSymbol;
  readonly side: OrderSide;
  readonly quantity: number;
  readonly status: OrderStatus;
  readonly createdAt: TimeStamp;
  readonly updatedAt: TimeStamp;
}

export interface MarketOrder extends BaseOrder {
  readonly type: typeof OrderType.MARKET;
  readonly estimatedPrice?: USD;
}

export interface LimitOrder extends BaseOrder {
  readonly type: typeof OrderType.LIMIT;
  readonly limitPrice: USD;
  readonly timeInForce: 'DAY' | 'GTC' | 'IOC' | 'FOK';
}

export interface StopOrder extends BaseOrder {
  readonly type: typeof OrderType.STOP;
  readonly stopPrice: USD;
}

export interface StopLimitOrder extends BaseOrder {
  readonly type: typeof OrderType.STOP_LIMIT;
  readonly stopPrice: USD;
  readonly limitPrice: USD;
  readonly timeInForce: 'DAY' | 'GTC' | 'IOC' | 'FOK';
}

// Discriminated union for all order types
export type TradeOrder = MarketOrder | LimitOrder | StopOrder | StopLimitOrder;

// Order execution details
export interface OrderExecution {
  readonly executionId: string;
  readonly orderId: string;
  readonly quantity: number;
  readonly price: USD;
  readonly timestamp: TimeStamp;
  readonly commission: USD;
}

// Congressional trading data
export const CongressionalTradeType = {
  PURCHASE: 'PURCHASE',
  SALE: 'SALE',
  EXCHANGE: 'EXCHANGE',
} as const;

export type CongressionalTradeType =
  (typeof CongressionalTradeType)[keyof typeof CongressionalTradeType];

export interface CongressionalTrade {
  readonly tradeId: string;
  readonly representative: string;
  readonly party: 'Republican' | 'Democrat' | 'Independent';
  readonly chamber: 'House' | 'Senate';
  readonly symbol: StockSymbol;
  readonly tradeType: CongressionalTradeType;
  readonly amount: readonly [USD, USD]; // Min and max range
  readonly tradeDate: Date;
  readonly disclosureDate: Date;
  readonly description?: string;
}

// API Response types
export interface ApiResponse<T> {
  readonly success: boolean;
  readonly data: T;
  readonly timestamp: TimeStamp;
}

export interface ApiError {
  readonly success: false;
  readonly error: {
    readonly code: string;
    readonly message: string;
    readonly details?: unknown;
  };
  readonly timestamp: TimeStamp;
}

// Result type for error handling
export type Result<T, E = Error> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

// Market data subscription types
export interface MarketDataSubscription {
  readonly symbols: readonly StockSymbol[];
  readonly fields: readonly ('price' | 'volume' | 'metrics')[];
  readonly onData: (data: StockData) => void;
  readonly onError: (error: Error) => void;
}

// Trading analysis types
export interface TechnicalIndicator {
  readonly name: string;
  readonly value: number;
  readonly signal: 'BUY' | 'SELL' | 'HOLD';
  readonly timestamp: TimeStamp;
}

export interface TradingSignal {
  readonly symbol: StockSymbol;
  readonly signal: 'STRONG_BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG_SELL';
  readonly confidence: Percentage;
  readonly indicators: readonly TechnicalIndicator[];
  readonly reasoning: string;
  readonly timestamp: TimeStamp;
}

export interface AnalysisReport {
  readonly reportId: string;
  readonly symbol: StockSymbol;
  readonly signals: readonly TradingSignal[];
  readonly recommendation: 'BUY' | 'SELL' | 'HOLD';
  readonly targetPrice: USD | null;
  readonly stopLoss: USD | null;
  readonly riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  readonly generatedAt: TimeStamp;
}

// Type guards for runtime type checking
export const isStockData = (data: unknown): data is StockData => {
  return (
    typeof data === 'object' &&
    data !== null &&
    'symbol' in data &&
    'price' in data &&
    'volume' in data &&
    'metrics' in data &&
    'timestamp' in data
  );
};

export const isTradeOrder = (order: unknown): order is TradeOrder => {
  return (
    typeof order === 'object' &&
    order !== null &&
    'orderId' in order &&
    'symbol' in order &&
    'side' in order &&
    'type' in order &&
    'status' in order
  );
};

export const isApiError = (response: unknown): response is ApiError => {
  return (
    typeof response === 'object' &&
    response !== null &&
    'success' in response &&
    (response as { success: unknown }).success === false &&
    'error' in response
  );
};

// Utility types for advanced TypeScript features
export type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
export type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Extract symbol from any type that has a symbol property
export type ExtractSymbol<T> = T extends { readonly symbol: infer S }
  ? S
  : never;

// Create order input types (without readonly and generated fields)
export type CreateOrderInput<T extends TradeOrder> = Omit<
  T,
  'orderId' | 'status' | 'createdAt' | 'updatedAt'
>;

// Portfolio update types
export type PortfolioUpdate = PartialBy<Portfolio, 'positions' | 'lastUpdated'>;
