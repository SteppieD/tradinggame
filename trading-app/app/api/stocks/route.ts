import { NextRequest, NextResponse } from 'next/server';
import {
  StockData,
  StockSymbol,
  HistoricalData,
  ApiResponse,
  ApiError,
  createStockSymbol,
  createUSD,
  createPercentage,
  createVolume,
  createMarketCap,
  MarketStatus,
} from '@/lib/types';

/**
 * GET /api/stocks - Fetch stock data
 * Query parameters:
 * - symbol: Stock symbol (required)
 * - timeframe: Historical data timeframe (optional)
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<ApiResponse<StockData | HistoricalData> | ApiError>> {
  try {
    const { searchParams } = new URL(request.url);
    const symbolParam = searchParams.get('symbol');
    const timeframe = searchParams.get('timeframe') as
      | HistoricalData['timeframe']
      | null;

    if (!symbolParam) {
      const errorResponse: ApiError = {
        success: false,
        error: {
          code: 'MISSING_SYMBOL',
          message: 'Stock symbol is required',
        },
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    const symbol = createStockSymbol(symbolParam.toUpperCase());

    // If timeframe is requested, return historical data
    if (timeframe) {
      const historicalData = await fetchHistoricalData(symbol, timeframe);
      const response: ApiResponse<HistoricalData> = {
        success: true,
        data: historicalData,
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(response);
    }

    // Otherwise return current stock data
    const stockData = await fetchStockData(symbol);
    const response: ApiResponse<StockData> = {
      success: true,
      data: stockData,
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
        code: 'INTERNAL_ERROR',
        message:
          error instanceof Error ? error.message : 'Unknown error occurred',
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
 * POST /api/stocks - Fetch multiple stocks data
 * Body: { symbols: string[] }
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse<ApiResponse<StockData[]> | ApiError>> {
  try {
    const body = (await request.json()) as { symbols?: string[] };

    if (!body.symbols || !Array.isArray(body.symbols)) {
      const errorResponse: ApiError = {
        success: false,
        error: {
          code: 'INVALID_SYMBOLS',
          message: 'Symbols array is required',
        },
        timestamp: {
          timestamp: Date.now(),
          date: new Date(),
        },
      };
      return NextResponse.json(errorResponse, { status: 400 });
    }

    const symbols = body.symbols.map((s) => createStockSymbol(s.toUpperCase()));
    const stocksData = await Promise.all(
      symbols.map((symbol) => fetchStockData(symbol))
    );

    const response: ApiResponse<StockData[]> = {
      success: true,
      data: stocksData,
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
        code: 'INTERNAL_ERROR',
        message:
          error instanceof Error ? error.message : 'Unknown error occurred',
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

// Mock data fetching functions (replace with real API calls)
async function fetchStockData(symbol: StockSymbol): Promise<StockData> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 100));

  // Mock data - replace with actual API integration
  const mockPrice = Math.random() * 500 + 50;
  const mockChange = (Math.random() - 0.5) * 20;

  return {
    symbol,
    name: `${symbol} Corporation`,
    price: {
      current: createUSD(mockPrice),
      open: createUSD(mockPrice - 5),
      high: createUSD(mockPrice + 10),
      low: createUSD(mockPrice - 8),
      previousClose: createUSD(mockPrice - mockChange),
      change: createUSD(mockChange),
      changePercent: createPercentage(
        (mockChange / (mockPrice - mockChange)) * 100
      ),
    },
    volume: {
      current: createVolume(Math.floor(Math.random() * 10000000)),
      average: createVolume(Math.floor(Math.random() * 8000000)),
      dayRange: [createVolume(1000000), createVolume(15000000)] as const,
    },
    metrics: {
      marketCap: createMarketCap(Math.random() * 1000000000000),
      peRatio: Math.random() * 50 + 5,
      eps: createUSD(Math.random() * 10),
      dividend: Math.random() > 0.5 ? createUSD(Math.random() * 5) : null,
      dividendYield:
        Math.random() > 0.5 ? createPercentage(Math.random() * 5) : null,
      beta: Math.random() * 2,
    },
    timestamp: {
      timestamp: Date.now(),
      date: new Date(),
    },
    marketStatus: MarketStatus.OPEN,
  };
}

async function fetchHistoricalData(
  symbol: StockSymbol,
  timeframe: HistoricalData['timeframe']
): Promise<HistoricalData> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 200));

  // Generate mock historical data
  const days = getTimeframeDays(timeframe);
  const data = Array.from({ length: days }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (days - i));

    const basePrice = Math.random() * 500 + 50;
    const open = createUSD(basePrice);
    const close = createUSD(basePrice + (Math.random() - 0.5) * 20);
    const high = createUSD(
      Math.max(basePrice, close as number) + Math.random() * 10
    );
    const low = createUSD(
      Math.min(basePrice, close as number) - Math.random() * 10
    );

    return {
      symbol,
      timestamp: date.getTime(),
      date,
      open,
      high,
      low,
      close,
      volume: createVolume(Math.floor(Math.random() * 10000000)),
    };
  });

  return {
    symbol,
    timeframe,
    data,
  };
}

function getTimeframeDays(timeframe: HistoricalData['timeframe']): number {
  switch (timeframe) {
    case '1D':
      return 1;
    case '5D':
      return 5;
    case '1M':
      return 30;
    case '3M':
      return 90;
    case '6M':
      return 180;
    case '1Y':
      return 365;
    case '2Y':
      return 730;
    case '5Y':
      return 1825;
    case 'MAX':
      return 3650; // 10 years max
    default:
      return 30;
  }
}
