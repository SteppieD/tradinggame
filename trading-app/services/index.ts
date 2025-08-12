/**
 * Centralized exports for all trading services
 * Provides type-safe access to stock, portfolio, and analysis services
 */

export {
  StockService,
  StockServiceError,
  NetworkError,
  ValidationError,
} from './stockService';
export {
  PortfolioService,
  PortfolioServiceError,
  InsufficientFundsError,
  InvalidOrderError,
} from './portfolioService';
export {
  AnalysisService,
  AnalysisServiceError,
  InvalidAnalysisParameterError,
} from './analysisService';

// Re-export all types for convenience
export type {
  StockData,
  HistoricalData,
  Portfolio,
  Position,
  TradeOrder,
  CreateOrderInput,
  AnalysisReport,
  CongressionalTrade,
  TradingSignal,
  StockSymbol,
  Result,
} from '@/lib/types';
