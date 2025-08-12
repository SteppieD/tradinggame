/**
 * Type-safe portfolio management service
 */

import {
  Portfolio,
  TradeOrder,
  CreateOrderInput,
  OrderStatus,
  OrderType,
  MarketOrder,
  LimitOrder,
  StopOrder,
  StopLimitOrder,
  ApiResponse,
  ApiError,
  Result,
  isApiError,
  isTradeOrder,
  createStockSymbol,
  createUSD,
} from '@/lib/types';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? '';

// Custom error classes
export class PortfolioServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode?: number,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = 'PortfolioServiceError';
  }
}

export class InsufficientFundsError extends PortfolioServiceError {
  constructor(requiredAmount: number, availableAmount: number) {
    super(
      `Insufficient funds: Required $${requiredAmount.toFixed(2)}, Available $${availableAmount.toFixed(2)}`,
      'INSUFFICIENT_FUNDS',
      400,
      { requiredAmount, availableAmount }
    );
    this.name = 'InsufficientFundsError';
  }
}

export class InvalidOrderError extends PortfolioServiceError {
  constructor(message: string, details?: unknown) {
    super(message, 'INVALID_ORDER', 400, details);
    this.name = 'InvalidOrderError';
  }
}

// Type-safe fetch wrapper
async function safeFetch<T>(
  url: string,
  options?: RequestInit
): Promise<Result<T, PortfolioServiceError>> {
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
        error: new PortfolioServiceError(
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
        error: new PortfolioServiceError(
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
    return {
      success: false,
      error: new PortfolioServiceError(
        error instanceof Error ? error.message : 'Unknown error occurred',
        'UNKNOWN_ERROR',
        undefined,
        error
      ),
    };
  }
}

// Portfolio management service
export class PortfolioService {
  /**
   * Fetch portfolio data for an account
   */
  static async getPortfolio(
    accountId = 'default'
  ): Promise<Result<Portfolio, PortfolioServiceError>> {
    const url = `${API_BASE_URL}/api/portfolio?accountId=${encodeURIComponent(accountId)}`;

    const result = await safeFetch<ApiResponse<Portfolio>>(url);

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success) {
      return {
        success: false,
        error: new PortfolioServiceError(
          'Failed to fetch portfolio data',
          'PORTFOLIO_FETCH_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Create a new trade order with validation
   */
  static async createOrder<T extends TradeOrder>(
    orderInput: CreateOrderInput<T>
  ): Promise<Result<T, PortfolioServiceError | InvalidOrderError>> {
    // Validate order input
    const validationResult = this.validateOrderInput(orderInput);
    if (!validationResult.success) {
      return validationResult;
    }

    const url = `${API_BASE_URL}/api/portfolio`;

    const result = await safeFetch<ApiResponse<TradeOrder>>(url, {
      method: 'POST',
      body: JSON.stringify(orderInput),
    });

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !isTradeOrder(response.data)) {
      return {
        success: false,
        error: new PortfolioServiceError(
          'Invalid order response from API',
          'INVALID_ORDER_RESPONSE'
        ),
      };
    }

    return {
      success: true,
      data: response.data as T,
    };
  }

  /**
   * Update an existing order
   */
  static async updateOrder(
    orderId: string,
    updates: Partial<TradeOrder>
  ): Promise<Result<TradeOrder, PortfolioServiceError>> {
    if (!orderId || typeof orderId !== 'string') {
      return {
        success: false,
        error: new InvalidOrderError('Order ID must be a non-empty string'),
      };
    }

    const url = `${API_BASE_URL}/api/portfolio/orders/${encodeURIComponent(orderId)}`;

    const result = await safeFetch<ApiResponse<TradeOrder>>(url, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !isTradeOrder(response.data)) {
      return {
        success: false,
        error: new PortfolioServiceError(
          'Invalid order update response from API',
          'INVALID_UPDATE_RESPONSE'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Cancel an order
   */
  static async cancelOrder(
    orderId: string
  ): Promise<Result<boolean, PortfolioServiceError>> {
    if (!orderId || typeof orderId !== 'string') {
      return {
        success: false,
        error: new InvalidOrderError('Order ID must be a non-empty string'),
      };
    }

    const url = `${API_BASE_URL}/api/portfolio/orders/${encodeURIComponent(orderId)}`;

    const result = await safeFetch<ApiResponse<{ cancelled: boolean }>>(url, {
      method: 'DELETE',
    });

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success) {
      return {
        success: false,
        error: new PortfolioServiceError(
          'Failed to cancel order',
          'ORDER_CANCELLATION_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data.cancelled,
    };
  }

  /**
   * Validate order input before submission
   */
  private static validateOrderInput<T extends TradeOrder>(
    orderInput: CreateOrderInput<T>
  ): Result<CreateOrderInput<T>, InvalidOrderError> {
    // Validate symbol
    if (!orderInput.symbol || typeof orderInput.symbol !== 'string') {
      return {
        success: false,
        error: new InvalidOrderError('Symbol is required and must be a string'),
      };
    }

    // Validate quantity
    if (
      !orderInput.quantity ||
      typeof orderInput.quantity !== 'number' ||
      orderInput.quantity <= 0
    ) {
      return {
        success: false,
        error: new InvalidOrderError('Quantity must be a positive number'),
      };
    }

    // Validate order type specific fields
    switch (orderInput.type) {
      case OrderType.LIMIT: {
        const limitOrder = orderInput as CreateOrderInput<LimitOrder>;
        if (
          !limitOrder.limitPrice ||
          typeof limitOrder.limitPrice !== 'number' ||
          limitOrder.limitPrice <= 0
        ) {
          return {
            success: false,
            error: new InvalidOrderError(
              'Limit price must be a positive number for limit orders'
            ),
          };
        }
        break;
      }

      case OrderType.STOP: {
        const stopOrder = orderInput as CreateOrderInput<StopOrder>;
        if (
          !stopOrder.stopPrice ||
          typeof stopOrder.stopPrice !== 'number' ||
          stopOrder.stopPrice <= 0
        ) {
          return {
            success: false,
            error: new InvalidOrderError(
              'Stop price must be a positive number for stop orders'
            ),
          };
        }
        break;
      }

      case OrderType.STOP_LIMIT: {
        const stopLimitOrder = orderInput as CreateOrderInput<StopLimitOrder>;
        if (
          !stopLimitOrder.stopPrice ||
          typeof stopLimitOrder.stopPrice !== 'number' ||
          stopLimitOrder.stopPrice <= 0
        ) {
          return {
            success: false,
            error: new InvalidOrderError(
              'Stop price must be a positive number for stop-limit orders'
            ),
          };
        }
        if (
          !stopLimitOrder.limitPrice ||
          typeof stopLimitOrder.limitPrice !== 'number' ||
          stopLimitOrder.limitPrice <= 0
        ) {
          return {
            success: false,
            error: new InvalidOrderError(
              'Limit price must be a positive number for stop-limit orders'
            ),
          };
        }
        break;
      }

      case OrderType.MARKET:
        // Market orders don't need additional validation
        break;

      default:
        return {
          success: false,
          error: new InvalidOrderError(
            `Unsupported order type: ${orderInput.type}`
          ),
        };
    }

    return {
      success: true,
      data: orderInput,
    };
  }

  /**
   * Calculate order value and validate buying power
   */
  static async validateBuyingPower(
    orderInput: CreateOrderInput<TradeOrder>,
    portfolio: Portfolio
  ): Promise<
    Result<
      { estimatedCost: number; hasEnoughBuyingPower: boolean },
      PortfolioServiceError
    >
  > {
    let estimatedPrice: number;

    switch (orderInput.type) {
      case OrderType.LIMIT:
        estimatedPrice = (orderInput as CreateOrderInput<LimitOrder>)
          .limitPrice as number;
        break;
      case OrderType.STOP_LIMIT:
        estimatedPrice = (orderInput as CreateOrderInput<StopLimitOrder>)
          .limitPrice as number;
        break;
      case OrderType.MARKET:
      case OrderType.STOP:
        // For market and stop orders, we need to get current market price
        // This would typically involve calling the stock service
        estimatedPrice = 100; // Mock price for now
        break;
      default:
        return {
          success: false,
          error: new InvalidOrderError(
            `Cannot estimate price for order type: ${orderInput.type}`
          ),
        };
    }

    const estimatedCost = estimatedPrice * orderInput.quantity;
    const hasEnoughBuyingPower = portfolio.buyingPower >= estimatedCost;

    if (!hasEnoughBuyingPower) {
      return {
        success: false,
        error: new InsufficientFundsError(
          estimatedCost,
          portfolio.buyingPower as number
        ),
      };
    }

    return {
      success: true,
      data: {
        estimatedCost,
        hasEnoughBuyingPower,
      },
    };
  }

  /**
   * Get order history for an account
   */
  static async getOrderHistory(
    accountId = 'default',
    options: {
      limit?: number;
      offset?: number;
      status?: OrderStatus[];
      symbol?: string;
    } = {}
  ): Promise<Result<TradeOrder[], PortfolioServiceError>> {
    const searchParams = new URLSearchParams();
    searchParams.set('accountId', accountId);

    if (options.limit) searchParams.set('limit', options.limit.toString());
    if (options.offset) searchParams.set('offset', options.offset.toString());
    if (options.status) searchParams.set('status', options.status.join(','));
    if (options.symbol) searchParams.set('symbol', options.symbol);

    const url = `${API_BASE_URL}/api/portfolio/orders?${searchParams.toString()}`;

    // Mock implementation - in reality this would be a separate endpoint
    const mockOrders: TradeOrder[] = [
      {
        orderId: 'order_1',
        symbol: createStockSymbol('AAPL'),
        side: 'BUY',
        type: OrderType.LIMIT,
        quantity: 100,
        limitPrice: createUSD(175.0),
        timeInForce: 'DAY',
        status: OrderStatus.FILLED,
        createdAt: {
          timestamp: Date.now() - 86400000,
          date: new Date(Date.now() - 86400000),
        },
        updatedAt: {
          timestamp: Date.now() - 86400000 + 3600000,
          date: new Date(Date.now() - 86400000 + 3600000),
        },
      } as LimitOrder,
    ];

    return {
      success: true,
      data: mockOrders,
    };
  }

  /**
   * Calculate portfolio performance metrics
   */
  static calculatePerformanceMetrics(portfolio: Portfolio): {
    totalReturn: number;
    totalReturnPercent: number;
    dayReturn: number;
    dayReturnPercent: number;
    realizedGains: number;
    unrealizedGains: number;
  } {
    const totalReturn = portfolio.totalPnL as number;
    const totalReturnPercent =
      (totalReturn / (portfolio.totalCost as number)) * 100;
    const dayReturn = portfolio.dayChange as number;
    const dayReturnPercent =
      (dayReturn / (portfolio.totalValue as number)) * 100;

    // For realized/unrealized gains, we'd need transaction history
    // This is a simplified calculation
    const unrealizedGains = portfolio.positions.reduce(
      (sum, position) => sum + (position.unrealizedPnL as number),
      0
    );

    return {
      totalReturn,
      totalReturnPercent,
      dayReturn,
      dayReturnPercent,
      realizedGains: 0, // Would require transaction history
      unrealizedGains,
    };
  }

  /**
   * Get position by symbol
   */
  static getPositionBySymbol(portfolio: Portfolio, symbol: string) {
    return (
      portfolio.positions.find(
        (position) =>
          position.symbol === createStockSymbol(symbol.toUpperCase())
      ) ?? null
    );
  }

  /**
   * Check if user can afford to buy a position
   */
  static canAffordPosition(
    portfolio: Portfolio,
    quantity: number,
    pricePerShare: number
  ): boolean {
    const totalCost = quantity * pricePerShare;
    return (portfolio.buyingPower as number) >= totalCost;
  }

  /**
   * Check if user has enough shares to sell
   */
  static hasEnoughShares(
    portfolio: Portfolio,
    symbol: string,
    quantity: number
  ): boolean {
    const position = this.getPositionBySymbol(portfolio, symbol);
    return position ? position.quantity >= quantity : false;
  }
}
