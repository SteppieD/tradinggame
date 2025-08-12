/**
 * Type-safe analysis service for trading insights and congressional trades
 */

import {
  AnalysisReport,
  CongressionalTrade,
  TradingSignal,
  StockSymbol,
  ApiResponse,
  ApiError,
  Result,
  isApiError,
  createStockSymbol,
} from '@/lib/types';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? '';

// Custom error classes
export class AnalysisServiceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode?: number,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = 'AnalysisServiceError';
  }
}

export class InvalidAnalysisParameterError extends AnalysisServiceError {
  constructor(message: string, details?: unknown) {
    super(message, 'INVALID_ANALYSIS_PARAMETER', 400, details);
    this.name = 'InvalidAnalysisParameterError';
  }
}

// Type-safe fetch wrapper
async function safeFetch<T>(
  url: string,
  options?: RequestInit
): Promise<Result<T, AnalysisServiceError>> {
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
        error: new AnalysisServiceError(
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
        error: new AnalysisServiceError(
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
      error: new AnalysisServiceError(
        error instanceof Error ? error.message : 'Unknown error occurred',
        'UNKNOWN_ERROR',
        undefined,
        error
      ),
    };
  }
}

// Analysis service
export class AnalysisService {
  /**
   * Get comprehensive trading analysis for a stock
   */
  static async getAnalysisReport(
    symbol: string
  ): Promise<Result<AnalysisReport, AnalysisServiceError>> {
    if (!symbol || typeof symbol !== 'string') {
      return {
        success: false,
        error: new InvalidAnalysisParameterError(
          'Symbol must be a non-empty string'
        ),
      };
    }

    const normalizedSymbol = symbol.trim().toUpperCase();
    const url = `${API_BASE_URL}/api/analysis?symbol=${encodeURIComponent(normalizedSymbol)}`;

    const result = await safeFetch<ApiResponse<AnalysisReport>>(url);

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success) {
      return {
        success: false,
        error: new AnalysisServiceError(
          'Failed to fetch analysis report',
          'ANALYSIS_FETCH_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Get congressional trading data for a stock
   */
  static async getCongressionalTrades(
    symbol: string,
    options: {
      limit?: number;
      offset?: number;
      party?: 'Republican' | 'Democrat' | 'Independent';
      chamber?: 'House' | 'Senate';
      dateRange?: {
        start: Date;
        end: Date;
      };
    } = {}
  ): Promise<Result<CongressionalTrade[], AnalysisServiceError>> {
    if (!symbol || typeof symbol !== 'string') {
      return {
        success: false,
        error: new InvalidAnalysisParameterError(
          'Symbol must be a non-empty string'
        ),
      };
    }

    const normalizedSymbol = symbol.trim().toUpperCase();
    const searchParams = new URLSearchParams();
    searchParams.set('symbol', normalizedSymbol);
    searchParams.set('analysisType', 'congressional');

    if (options.limit) searchParams.set('limit', options.limit.toString());
    if (options.offset) searchParams.set('offset', options.offset.toString());
    if (options.party) searchParams.set('party', options.party);
    if (options.chamber) searchParams.set('chamber', options.chamber);
    if (options.dateRange) {
      searchParams.set('startDate', options.dateRange.start.toISOString());
      searchParams.set('endDate', options.dateRange.end.toISOString());
    }

    const url = `${API_BASE_URL}/api/analysis?${searchParams.toString()}`;

    const result = await safeFetch<ApiResponse<CongressionalTrade[]>>(url);

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !Array.isArray(response.data)) {
      return {
        success: false,
        error: new AnalysisServiceError(
          'Failed to fetch congressional trades',
          'CONGRESSIONAL_TRADES_FETCH_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Get batch analysis for multiple stocks
   */
  static async getBatchAnalysis(
    symbols: readonly string[],
    analysisType: 'technical' | 'congressional' | 'all' = 'all'
  ): Promise<Result<AnalysisReport[], AnalysisServiceError>> {
    if (!Array.isArray(symbols) || symbols.length === 0) {
      return {
        success: false,
        error: new InvalidAnalysisParameterError(
          'Symbols must be a non-empty array'
        ),
      };
    }

    const invalidSymbols = symbols.filter((s) => !s || typeof s !== 'string');
    if (invalidSymbols.length > 0) {
      return {
        success: false,
        error: new InvalidAnalysisParameterError(
          'All symbols must be non-empty strings',
          { invalidSymbols }
        ),
      };
    }

    const normalizedSymbols = symbols.map((s) => s.trim().toUpperCase());
    const url = `${API_BASE_URL}/api/analysis/batch`;

    const result = await safeFetch<ApiResponse<AnalysisReport[]>>(url, {
      method: 'POST',
      body: JSON.stringify({ symbols: normalizedSymbols, analysisType }),
    });

    if (!result.success) {
      return result;
    }

    const { data: response } = result;

    if (!response.success || !Array.isArray(response.data)) {
      return {
        success: false,
        error: new AnalysisServiceError(
          'Failed to fetch batch analysis',
          'BATCH_ANALYSIS_FETCH_ERROR'
        ),
      };
    }

    return {
      success: true,
      data: response.data,
    };
  }

  /**
   * Analyze trading signals and provide recommendations
   */
  static analyzeSignals(signals: readonly TradingSignal[]): {
    overallRecommendation: 'BUY' | 'SELL' | 'HOLD';
    confidence: number;
    reasoning: string;
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  } {
    if (signals.length === 0) {
      return {
        overallRecommendation: 'HOLD',
        confidence: 0,
        reasoning: 'No signals available for analysis',
        riskLevel: 'HIGH',
      };
    }

    // Calculate signal weights
    const signalWeights = {
      STRONG_BUY: 2,
      BUY: 1,
      HOLD: 0,
      SELL: -1,
      STRONG_SELL: -2,
    };

    const totalWeight = signals.reduce((sum, signal) => {
      const weight = signalWeights[signal.signal];
      const confidence = (signal.confidence as number) / 100;
      return sum + weight * confidence;
    }, 0);

    const averageWeight = totalWeight / signals.length;
    const averageConfidence =
      signals.reduce((sum, signal) => sum + (signal.confidence as number), 0) /
      signals.length;

    let overallRecommendation: 'BUY' | 'SELL' | 'HOLD';
    if (averageWeight > 0.5) {
      overallRecommendation = 'BUY';
    } else if (averageWeight < -0.5) {
      overallRecommendation = 'SELL';
    } else {
      overallRecommendation = 'HOLD';
    }

    const riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' =
      averageConfidence > 80
        ? 'LOW'
        : averageConfidence > 60
          ? 'MEDIUM'
          : 'HIGH';

    const reasoning = this.generateSignalReasoning(
      signals,
      overallRecommendation,
      averageConfidence
    );

    return {
      overallRecommendation,
      confidence: averageConfidence,
      reasoning,
      riskLevel,
    };
  }

  /**
   * Get trending stocks based on congressional activity
   */
  static async getTrendingCongressionalStocks(
    options: {
      timeframe?: '7d' | '30d' | '90d';
      minTradeCount?: number;
      party?: 'Republican' | 'Democrat' | 'Independent';
    } = {}
  ): Promise<
    Result<
      Array<{
        symbol: StockSymbol;
        tradeCount: number;
        totalVolume: number;
        netSentiment: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
        recentTrades: CongressionalTrade[];
      }>,
      AnalysisServiceError
    >
  > {
    // Mock implementation - in reality, this would aggregate congressional trade data
    const mockTrendingStocks = [
      {
        symbol: createStockSymbol('AAPL'),
        tradeCount: 15,
        totalVolume: 2500000,
        netSentiment: 'BULLISH' as const,
        recentTrades: [],
      },
      {
        symbol: createStockSymbol('GOOGL'),
        tradeCount: 12,
        totalVolume: 1800000,
        netSentiment: 'NEUTRAL' as const,
        recentTrades: [],
      },
      {
        symbol: createStockSymbol('MSFT'),
        tradeCount: 10,
        totalVolume: 3200000,
        netSentiment: 'BULLISH' as const,
        recentTrades: [],
      },
    ];

    return {
      success: true,
      data: mockTrendingStocks,
    };
  }

  /**
   * Generate market sentiment analysis
   */
  static async getMarketSentiment(): Promise<
    Result<
      {
        overallSentiment: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
        confidence: number;
        factors: Array<{
          factor: string;
          impact: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
          weight: number;
        }>;
        lastUpdated: Date;
      },
      AnalysisServiceError
    >
  > {
    // Mock implementation - in reality, this would analyze various market factors
    const sentimentFactors = [
      {
        factor: 'Congressional Trading Activity',
        impact: 'POSITIVE' as const,
        weight: 0.3,
      },
      {
        factor: 'Technical Indicators',
        impact: 'NEUTRAL' as const,
        weight: 0.25,
      },
      {
        factor: 'Market Volatility',
        impact: 'NEGATIVE' as const,
        weight: 0.2,
      },
      {
        factor: 'Economic Indicators',
        impact: 'POSITIVE' as const,
        weight: 0.25,
      },
    ];

    const positiveWeight = sentimentFactors
      .filter((f) => f.impact === 'POSITIVE')
      .reduce((sum, f) => sum + f.weight, 0);

    const negativeWeight = sentimentFactors
      .filter((f) => f.impact === 'NEGATIVE')
      .reduce((sum, f) => sum + f.weight, 0);

    const netSentiment = positiveWeight - negativeWeight;

    let overallSentiment: 'BULLISH' | 'BEARISH' | 'NEUTRAL';
    if (netSentiment > 0.1) {
      overallSentiment = 'BULLISH';
    } else if (netSentiment < -0.1) {
      overallSentiment = 'BEARISH';
    } else {
      overallSentiment = 'NEUTRAL';
    }

    const confidence = Math.abs(netSentiment) * 100;

    return {
      success: true,
      data: {
        overallSentiment,
        confidence,
        factors: sentimentFactors,
        lastUpdated: new Date(),
      },
    };
  }

  /**
   * Generate reasoning text for signal analysis
   */
  private static generateSignalReasoning(
    signals: readonly TradingSignal[],
    recommendation: 'BUY' | 'SELL' | 'HOLD',
    confidence: number
  ): string {
    const strongSignals = signals.filter(
      (s) => s.signal === 'STRONG_BUY' || s.signal === 'STRONG_SELL'
    );

    const positiveSignals = signals.filter(
      (s) => s.signal === 'STRONG_BUY' || s.signal === 'BUY'
    );

    const negativeSignals = signals.filter(
      (s) => s.signal === 'STRONG_SELL' || s.signal === 'SELL'
    );

    switch (recommendation) {
      case 'BUY':
        return (
          `Analysis suggests a BUY recommendation with ${confidence.toFixed(1)}% confidence. ` +
          `${positiveSignals.length} out of ${signals.length} signals are positive` +
          (strongSignals.length > 0
            ? `, including ${strongSignals.length} strong signals`
            : '') +
          '. Market conditions and technical indicators support an upward trend.'
        );

      case 'SELL':
        return (
          `Analysis suggests a SELL recommendation with ${confidence.toFixed(1)}% confidence. ` +
          `${negativeSignals.length} out of ${signals.length} signals are negative` +
          (strongSignals.length > 0
            ? `, including ${strongSignals.length} strong signals`
            : '') +
          '. Technical indicators suggest downward pressure.'
        );

      case 'HOLD':
      default:
        return (
          `Analysis suggests a HOLD recommendation with ${confidence.toFixed(1)}% confidence. ` +
          `Signals are mixed with ${positiveSignals.length} positive and ${negativeSignals.length} negative indicators. ` +
          'Current market conditions suggest maintaining current position until clearer trends emerge.'
        );
    }
  }

  /**
   * Calculate correlation between congressional trades and stock performance
   */
  static calculateCongressionalCorrelation(
    trades: readonly CongressionalTrade[],
    priceHistory: readonly { date: Date; price: number }[]
  ): {
    correlation: number;
    significance: 'HIGH' | 'MEDIUM' | 'LOW';
    tradingDays: number;
    averageReturn: number;
  } {
    if (trades.length === 0 || priceHistory.length === 0) {
      return {
        correlation: 0,
        significance: 'LOW',
        tradingDays: 0,
        averageReturn: 0,
      };
    }

    // Simplified correlation calculation
    // In reality, this would use proper statistical methods
    const tradingDays = trades.length;
    const mockCorrelation = Math.random() * 0.8 - 0.4; // -0.4 to 0.4
    const significance =
      Math.abs(mockCorrelation) > 0.3
        ? 'HIGH'
        : Math.abs(mockCorrelation) > 0.15
          ? 'MEDIUM'
          : 'LOW';

    const averageReturn =
      priceHistory.length > 1
        ? (((priceHistory[priceHistory.length - 1]?.price ?? 0) -
            (priceHistory[0]?.price ?? 0)) /
            (priceHistory[0]?.price ?? 1)) *
          100
        : 0;

    return {
      correlation: mockCorrelation,
      significance,
      tradingDays,
      averageReturn,
    };
  }
}
