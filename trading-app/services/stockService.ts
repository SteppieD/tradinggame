/**
 * Type-safe stock data service with comprehensive error handling
 */

import {
  StockData,
  HistoricalData,
  StockSymbol,
  ApiResponse,
  ApiError,
  Result,
  isApiError,
  isStockData,
  createStockSymbol,
} from '@/lib/types';

// Configuration for API endpoints
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? '';

// Custom error classes for better error handling
export class StockServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode?: number,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = 'StockServiceError';
  }
}

export class NetworkError extends StockServiceError {
  constructor(message: string, details?: unknown) {
    super(message, 'NETWORK_ERROR', undefined, details);
    this.name = 'NetworkError';
  }
}

export class ValidationError extends StockServiceError {
  constructor(message: string, details?: unknown) {
    super(message, 'VALIDATION_ERROR', 400, details);
    this.name = 'ValidationError';
  }
}

// Type-safe fetch wrapper with error handling
async function safeFetch<T>(
  url: string,
  options?: RequestInit
): Promise<Result<T, StockServiceError>> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      return {
        success: false,
        error: new StockServiceError(
          `HTTP ${response.status}: ${response.statusText}`,
          'HTTP_ERROR',
          response.status
        ),
      };
    }

    const data = (await response.json()) as unknown;

    if (isApiError(data)) {
      return {
        success: false,
        error: new StockServiceError(
          data.error.message,
          data.error.code,
          response.status,
          data.error.details
        ),
      };
    }

    return {
      success: true,
      data: data as T,
    };
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return {
        success: false,
        error: new NetworkError('Network request failed', error),
      };
    }

    return {
      success: false,
      error: new StockServiceError(
        error instanceof Error ? error.message : 'Unknown error occurred',
        'UNKNOWN_ERROR',
        undefined,
        error
      ),
    };
  }
}

// Stock data fetching functions
export class StockService {
  /**
   * Fetch current stock data for a single symbol
   */
  static async getStockData(
    symbol: string
  ): Promise<Result<StockData, StockServiceError>> {
    if (!symbol || typeof symbol !== 'string') {
      return {
        success: false,
        error: new ValidationError('Symbol must be a non-empty string'),
      };
    }

    const normalizedSymbol = symbol.trim().toUpperCase();
    const url = `${API_BASE_URL}/api/stocks?symbol=${encodeURIComponent(normalizedSymbol)}`;

    const result = await safeFetch<ApiResponse<StockData>>(url);

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !isStockData(response.data)) {
      return {
        success: false,
        error: new StockServiceError(
          'Invalid stock data received from API',
          'INVALID_RESPONSE'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Fetch historical data for a symbol
   */
  static async getHistoricalData(
    symbol: string,
    timeframe: HistoricalData['timeframe']
  ): Promise<Result<HistoricalData, StockServiceError>> {
    if (!symbol || typeof symbol !== 'string') {
      return {
        success: false,
        error: new ValidationError('Symbol must be a non-empty string'),
      };
    }

    const normalizedSymbol = symbol.trim().toUpperCase();
    const url = `${API_BASE_URL}/api/stocks?symbol=${encodeURIComponent(normalizedSymbol)}&timeframe=${timeframe}`;

    const result = await safeFetch<ApiResponse<HistoricalData>>(url);

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success) {
      return {
        success: false,
        error: new StockServiceError(
          'Failed to fetch historical data',
          'HISTORICAL_DATA_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Fetch multiple stocks data in batch
   */
  static async getBatchStockData(
    symbols: readonly string[]
  ): Promise<Result<StockData[], StockServiceError>> {
    if (!Array.isArray(symbols) || symbols.length === 0) {
      return {
        success: false,
        error: new ValidationError('Symbols must be a non-empty array'),
      };
    }

    const invalidSymbols = symbols.filter((s) => !s || typeof s !== 'string');
    if (invalidSymbols.length > 0) {
      return {
        success: false,
        error: new ValidationError('All symbols must be non-empty strings', {
          invalidSymbols,
        }),
      };
    }

    const normalizedSymbols = symbols.map((s) => s.trim().toUpperCase());
    const url = `${API_BASE_URL}/api/stocks`;

    const result = await safeFetch<ApiResponse<StockData[]>>(url, {
      method: 'POST',
      body: JSON.stringify({ symbols: normalizedSymbols }),
    });

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !Array.isArray(response.data)) {
      return {
        success: false,
        error: new StockServiceError(
          'Invalid batch stock data received from API',
          'INVALID_BATCH_RESPONSE'
        ),
      };
    }

    // Validate each stock data item
    const invalidItems = response.data.filter((item) => !isStockData(item));
    if (invalidItems.length > 0) {
      return {
        success: false,
        error: new StockServiceError(
          'Some stock data items are invalid',
          'INVALID_STOCK_DATA_ITEMS',
          undefined,
          { invalidItemsCount: invalidItems.length }
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Search for stocks by query
   */
  static async searchStocks(
    query: string
  ): Promise<Result<StockData[], StockServiceError>> {
    if (!query || typeof query !== 'string' || query.trim().length < 1) {
      return {
        success: false,
        error: new ValidationError('Search query must be at least 1 character'),
      };
    }

    const trimmedQuery = query.trim();

    // For demo purposes, return mock search results
    // In a real implementation, this would call a search API endpoint
    const mockSymbols = [
      'AAPL',
      'GOOGL',
      'MSFT',
      'AMZN',
      'TSLA',
      'META',
      'NFLX',
      'NVDA',
    ].filter((symbol) =>
      symbol.toLowerCase().includes(trimmedQuery.toLowerCase())
    );

    if (mockSymbols.length === 0) {
      return {
        success: true,
        data: [],
      };
    }

    return this.getBatchStockData(mockSymbols);
  }

  /**
   * Get real-time price updates (WebSocket simulation)
   */
  static subscribeToRealTimeData(
    symbols: readonly string[],
    onData: (data: StockData) => void,
    onError: (error: StockServiceError) => void
  ): () => void {
    if (!Array.isArray(symbols) || symbols.length === 0) {
      onError(new ValidationError('Symbols must be a non-empty array'));
      return () => {};
    }

    const normalizedSymbols = symbols.map((s) => s.trim().toUpperCase());

    // Simulate real-time updates with intervals
    const intervals = normalizedSymbols.map((symbol) => {
      return setInterval(
        async () => {
          const result = await this.getStockData(symbol);
          if (result.success) {
            onData(result.data);
          } else {
            onError(result.error);
          }
        },
        5000 + Math.random() * 5000
      ); // Update every 5-10 seconds
    });

    // Return cleanup function
    return () => {
      intervals.forEach((interval) => clearInterval(interval));
    };
  }

  /**
   * Validate stock symbol format
   */
  static validateSymbol(symbol: string): Result<StockSymbol, ValidationError> {
    if (!symbol || typeof symbol !== 'string') {
      return {
        success: false,
        error: new ValidationError('Symbol must be a non-empty string'),
      };
    }

    const trimmed = symbol.trim().toUpperCase();

    // Basic symbol validation (alphanumeric, 1-5 characters)
    if (!/^[A-Z]{1,5}$/.test(trimmed)) {
      return {
        success: false,
        error: new ValidationError(
          'Symbol must contain 1-5 alphabetic characters only',
          { providedSymbol: symbol }
        ),
      };
    }

    return {
      success: true,
      data: createStockSymbol(trimmed),
    };
  }

  /**
   * Check if market is currently open
   */
  static isMarketOpen(): boolean {
    const now = new Date();
    const day = now.getDay(); // 0 = Sunday, 6 = Saturday
    const hour = now.getHours();
    const minute = now.getMinutes();
    const timeInMinutes = hour * 60 + minute;

    // Market closed on weekends
    if (day === 0 || day === 6) {
      return false;
    }

    // Market hours: 9:30 AM - 4:00 PM EST (570 - 960 minutes)
    const marketOpen = 9 * 60 + 30; // 9:30 AM
    const marketClose = 16 * 60; // 4:00 PM

    return timeInMinutes >= marketOpen && timeInMinutes < marketClose;
  }

  /**
   * Get market status with detailed information
   */
  static getMarketStatus(): {
    isOpen: boolean;
    nextOpen?: Date;
    nextClose?: Date;
    timeUntilNextEvent?: number;
  } {
    const isOpen = this.isMarketOpen();
    const now = new Date();

    if (isOpen) {
      // Market is open, calculate next close
      const nextClose = new Date(now);
      nextClose.setHours(16, 0, 0, 0); // 4:00 PM today

      return {
        isOpen: true,
        nextClose,
        timeUntilNextEvent: nextClose.getTime() - now.getTime(),
      };
    } else {
      // Market is closed, calculate next open
      const nextOpen = new Date(now);

      // If it's weekend, move to Monday
      if (now.getDay() === 0) {
        // Sunday
        nextOpen.setDate(now.getDate() + 1); // Monday
      } else if (now.getDay() === 6) {
        // Saturday
        nextOpen.setDate(now.getDate() + 2); // Monday
      } else if (now.getHours() >= 16) {
        // After market close
        nextOpen.setDate(now.getDate() + 1); // Next day
      }

      nextOpen.setHours(9, 30, 0, 0); // 9:30 AM

      return {
        isOpen: false,
        nextOpen,
        timeUntilNextEvent: nextOpen.getTime() - now.getTime(),
      };
    }
  }
}
