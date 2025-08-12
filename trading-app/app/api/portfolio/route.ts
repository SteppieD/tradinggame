import { NextRequest, NextResponse } from 'next/server';
import {
  Portfolio,
  Position,
  TradeOrder,
  CreateOrderInput,
  MarketOrder,
  LimitOrder,
  ApiResponse,
  ApiError,
  OrderType,
  OrderSide,
  OrderStatus,
  createStockSymbol,
  createUSD,
  createPercentage,
} from '@/lib/types';

/**
 * GET /api/portfolio - Fetch portfolio data
 * Query parameters:
 * - accountId: Account ID (optional, defaults to 'default')
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<ApiResponse<Portfolio> | ApiError>> {
  try {
    const { searchParams } = new URL(request.url);
    const accountId = searchParams.get('accountId') ?? 'default';

    const portfolio = await fetchPortfolio(accountId);

    const response: ApiResponse<Portfolio> = {
      success: true,
      data: portfolio,
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };

    return NextResponse.json(response);
  } catch (error) {
    const errorResponse: ApiError = {
      success: false,
      error: {
        code: 'PORTFOLIO_FETCH_ERROR',
        message:
          error instanceof Error ? error.message : 'Failed to fetch portfolio',
        details: error,
      },
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };
    return NextResponse.json(errorResponse, { status: 500 });
  }
}

/**
 * POST /api/portfolio/orders - Create a new trade order
 * Body: CreateOrderInput<TradeOrder>
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse<ApiResponse<TradeOrder> | ApiError>> {
  try {
    const body = (await request.json()) as unknown;

    if (!isValidOrderInput(body)) {
      const errorResponse: ApiError = {
        success: false,
        error: {
          code: 'INVALID_ORDER',
          message: 'Invalid order data provided',
          details: body,
        },
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    const order = await createTradeOrder(body);

    const response: ApiResponse<TradeOrder> = {
      success: true,
      data: order,
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };

    return NextResponse.json(response);
  } catch (error) {
    const errorResponse: ApiError = {
      success: false,
      error: {
        code: 'ORDER_CREATION_ERROR',
        message:
          error instanceof Error ? error.message : 'Failed to create order',
        details: error,
      },
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };
    return NextResponse.json(errorResponse, { status: 500 });
  }
}

/**
 * PUT /api/portfolio/orders/:orderId - Update an existing order
 */
export async function PUT(
  request: NextRequest
): Promise<NextResponse<ApiResponse<TradeOrder> | ApiError>> {
  try {
    const url = new URL(request.url);
    const orderId = url.pathname.split('/').pop();

    if (!orderId) {
      const errorResponse: ApiError = {
        success: false,
        error: {
          code: 'MISSING_ORDER_ID',
          message: 'Order ID is required',
        },
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    const body = (await request.json()) as Partial<TradeOrder>;
    const updatedOrder = await updateTradeOrder(orderId, body);

    const response: ApiResponse<TradeOrder> = {
      success: true,
      data: updatedOrder,
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };

    return NextResponse.json(response);
  } catch (error) {
    const errorResponse: ApiError = {
      success: false,
      error: {
        code: 'ORDER_UPDATE_ERROR',
        message:
          error instanceof Error ? error.message : 'Failed to update order',
        details: error,
      },
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };
    return NextResponse.json(errorResponse, { status: 500 });
  }
}

/**
 * DELETE /api/portfolio/orders/:orderId - Cancel an order
 */
export async function DELETE(
  request: NextRequest
): Promise<NextResponse<ApiResponse<{ cancelled: boolean }> | ApiError>> {
  try {
    const url = new URL(request.url);
    const orderId = url.pathname.split('/').pop();

    if (!orderId) {
      const errorResponse: ApiError = {
        success: false,
        error: {
          code: 'MISSING_ORDER_ID',
          message: 'Order ID is required',
        },
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    const cancelled = await cancelOrder(orderId);

    const response: ApiResponse<{ cancelled: boolean }> = {
      success: true,
      data: { cancelled },
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };

    return NextResponse.json(response);
  } catch (error) {
    const errorResponse: ApiError = {
      success: false,
      error: {
        code: 'ORDER_CANCELLATION_ERROR',
        message:
          error instanceof Error ? error.message : 'Failed to cancel order',
        details: error,
      },
      timestamp: {
        timestamp: Date.now(),
        date: new Date(),
      },
    };
    return NextResponse.json(errorResponse, { status: 500 });
  }
}

// Type guard for order input validation
function isValidOrderInput(
  input: unknown
): input is CreateOrderInput<TradeOrder> {
  if (typeof input !== 'object' || input === null) {
    return false;
  }

  const obj = input as Record<string, unknown>;

  return (
    typeof obj.symbol === 'string' &&
    typeof obj.side === 'string' &&
    (obj.side === OrderSide.BUY || obj.side === OrderSide.SELL) &&
    typeof obj.type === 'string' &&
    Object.values(OrderType).includes(obj.type as OrderType) &&
    typeof obj.quantity === 'number' &&
    obj.quantity > 0
  );
}

// Mock portfolio data fetching
async function fetchPortfolio(accountId: string): Promise<Portfolio> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 150));

  // Mock positions
  const positions: readonly Position[] = [
    {
      symbol: createStockSymbol('AAPL'),
      quantity: 100,
      averageCost: createUSD(150.5),
      currentPrice: createUSD(175.25),
      totalValue: createUSD(17525),
      unrealizedPnL: createUSD(2475),
      unrealizedPnLPercent: createPercentage(16.44),
      dayChange: createUSD(250),
      dayChangePercent: createPercentage(1.45),
    },
    {
      symbol: createStockSymbol('GOOGL'),
      quantity: 50,
      averageCost: createUSD(2800.0),
      currentPrice: createUSD(2950.75),
      totalValue: createUSD(147537.5),
      unrealizedPnL: createUSD(7537.5),
      unrealizedPnLPercent: createPercentage(5.38),
      dayChange: createUSD(-1250),
      dayChangePercent: createPercentage(-0.84),
    },
  ] as const;

  const totalValue = createUSD(165062.5);
  const totalCost = createUSD(155050.0);
  const totalPnL = createUSD(10012.5);
  const dayChange = createUSD(-1000);

  return {
    accountId,
    totalValue,
    totalCost,
    totalPnL,
    totalPnLPercent: createPercentage((totalPnL / totalCost) * 100),
    dayChange,
    dayChangePercent: createPercentage((dayChange / totalValue) * 100),
    cashBalance: createUSD(25000),
    buyingPower: createUSD(50000),
    positions,
    lastUpdated: {
      timestamp: Date.now(),
      date: new Date(),
    },
  };
}

// Mock order creation
async function createTradeOrder(
  orderInput: CreateOrderInput<TradeOrder>
): Promise<TradeOrder> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 100));

  const orderId = `order_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  const now = {
    timestamp: Date.now(),
    date: new Date(),
  };

  const baseOrder = {
    orderId,
    symbol: createStockSymbol(orderInput.symbol),
    side: orderInput.side,
    quantity: orderInput.quantity,
    status: OrderStatus.PENDING,
    createdAt: now,
    updatedAt: now,
  };

  switch (orderInput.type) {
    case OrderType.MARKET:
      return {
        ...baseOrder,
        type: OrderType.MARKET,
        estimatedPrice: createUSD(Math.random() * 500 + 50),
      } as MarketOrder;

    case OrderType.LIMIT:
      const limitInput = orderInput as CreateOrderInput<LimitOrder>;
      return {
        ...baseOrder,
        type: OrderType.LIMIT,
        limitPrice: createUSD(limitInput.limitPrice as number),
        timeInForce: limitInput.timeInForce ?? 'DAY',
      } as LimitOrder;

    default:
      throw new Error(`Unsupported order type: ${orderInput.type}`);
  }
}

// Mock order update
async function updateTradeOrder(
  _orderId: string,
  _updates: Partial<TradeOrder>
): Promise<TradeOrder> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 100));

  // Mock updated order - in real implementation, fetch existing order and apply updates
  const mockOrder: TradeOrder = {
    orderId: _orderId,
    symbol: createStockSymbol('AAPL'),
    side: OrderSide.BUY,
    type: OrderType.LIMIT,
    quantity: 100,
    limitPrice: createUSD(175.0),
    timeInForce: 'DAY',
    status: OrderStatus.FILLED,
    createdAt: {
      timestamp: Date.now() - 3600000, // 1 hour ago
      date: new Date(Date.now() - 3600000),
    },
    updatedAt: {
      timestamp: Date.now(),
      date: new Date(),
    },
  } as LimitOrder;

  return mockOrder;
}

// Mock order cancellation
async function cancelOrder(_orderId: string): Promise<boolean> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 100));

  // Mock cancellation logic - in real implementation, check if order can be cancelled
  return Math.random() > 0.1; // 90% success rate
}
