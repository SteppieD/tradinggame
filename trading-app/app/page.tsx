'use client';

import { useState, useEffect } from 'react';
import { StockService, PortfolioService, AnalysisService } from '@/services';
import type { StockData, Portfolio, AnalysisReport } from '@/lib/types';

export default function Home() {
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Example of type-safe data fetching
  const fetchSampleData = async (): Promise<void> => {
    setLoading(true);
    setError(null);

    try {
      // Fetch stock data with type safety
      const stockResult = await StockService.getStockData('AAPL');

      if (stockResult.success) {
        setStockData(stockResult.data);
      } else {
        setError(`Stock data error: ${stockResult.error.message}`);
      }

      // Fetch portfolio data
      const portfolioResult = await PortfolioService.getPortfolio();
      if (portfolioResult.success) {
        setPortfolio(portfolioResult.data);
      }

      // Fetch analysis data
      const analysisResult = await AnalysisService.getAnalysisReport('AAPL');
      if (analysisResult.success) {
        setAnalysis(analysisResult.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSampleData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Trading App</h1>
          <p className="text-xl text-gray-600 mb-8">
            Type-safe Next.js 14 trading application with TypeScript strict mode
          </p>

          <button
            onClick={fetchSampleData}
            disabled={loading}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading...' : 'Fetch Sample Data'}
          </button>
        </div>

        {error && (
          <div className="mb-8 p-4 border border-red-300 rounded-md bg-red-50">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Error occurred
                </h3>
                <div className="mt-2 text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Stock Data Card */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Stock Data
              </h3>
              {stockData ? (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Symbol:
                    </span>
                    <span className="text-sm text-gray-900">
                      {stockData.symbol}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Name:
                    </span>
                    <span className="text-sm text-gray-900">
                      {stockData.name}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Current Price:
                    </span>
                    <span className="text-sm text-gray-900">
                      ${(stockData.price.current as number).toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Change:
                    </span>
                    <span
                      className={`text-sm ${(stockData.price.change as number) >= 0 ? 'text-green-600' : 'text-red-600'}`}
                    >
                      ${(stockData.price.change as number).toFixed(2)} (
                      {(stockData.price.changePercent as number).toFixed(2)}%)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Market Cap:
                    </span>
                    <span className="text-sm text-gray-900">
                      $
                      {((stockData.metrics.marketCap as number) / 1e9).toFixed(
                        2
                      )}
                      B
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">No stock data available</p>
              )}
            </div>
          </div>

          {/* Portfolio Card */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Portfolio
              </h3>
              {portfolio ? (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Total Value:
                    </span>
                    <span className="text-sm text-gray-900">
                      ${(portfolio.totalValue as number).toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Total P&L:
                    </span>
                    <span
                      className={`text-sm ${(portfolio.totalPnL as number) >= 0 ? 'text-green-600' : 'text-red-600'}`}
                    >
                      ${(portfolio.totalPnL as number).toLocaleString()} (
                      {(portfolio.totalPnLPercent as number).toFixed(2)}%)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Day Change:
                    </span>
                    <span
                      className={`text-sm ${(portfolio.dayChange as number) >= 0 ? 'text-green-600' : 'text-red-600'}`}
                    >
                      ${(portfolio.dayChange as number).toLocaleString()} (
                      {(portfolio.dayChangePercent as number).toFixed(2)}%)
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Cash Balance:
                    </span>
                    <span className="text-sm text-gray-900">
                      ${(portfolio.cashBalance as number).toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Positions:
                    </span>
                    <span className="text-sm text-gray-900">
                      {portfolio.positions.length}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">
                  No portfolio data available
                </p>
              )}
            </div>
          </div>

          {/* Analysis Card */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Analysis
              </h3>
              {analysis ? (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Symbol:
                    </span>
                    <span className="text-sm text-gray-900">
                      {analysis.symbol}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Recommendation:
                    </span>
                    <span
                      className={`text-sm font-medium ${
                        analysis.recommendation === 'BUY'
                          ? 'text-green-600'
                          : analysis.recommendation === 'SELL'
                            ? 'text-red-600'
                            : 'text-yellow-600'
                      }`}
                    >
                      {analysis.recommendation}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Risk Level:
                    </span>
                    <span
                      className={`text-sm ${
                        analysis.riskLevel === 'LOW'
                          ? 'text-green-600'
                          : analysis.riskLevel === 'MEDIUM'
                            ? 'text-yellow-600'
                            : 'text-red-600'
                      }`}
                    >
                      {analysis.riskLevel}
                    </span>
                  </div>
                  {analysis.targetPrice && (
                    <div className="flex justify-between">
                      <span className="text-sm font-medium text-gray-500">
                        Target Price:
                      </span>
                      <span className="text-sm text-gray-900">
                        ${(analysis.targetPrice as number).toFixed(2)}
                      </span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-sm font-medium text-gray-500">
                      Signals:
                    </span>
                    <span className="text-sm text-gray-900">
                      {analysis.signals.length}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500">
                  No analysis data available
                </p>
              )}
            </div>
          </div>
        </div>

        {/* API Routes Documentation */}
        <div className="mt-12 bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Available API Routes
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Type-safe API endpoints with comprehensive TypeScript interfaces
            </p>
          </div>
          <ul className="divide-y divide-gray-200">
            <li>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-blue-600 truncate">
                    GET /api/stocks?symbol=AAPL
                  </div>
                  <div className="ml-2 flex-shrink-0 flex">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Stock Data
                    </span>
                  </div>
                </div>
                <div className="mt-2 sm:flex sm:justify-between">
                  <div className="sm:flex">
                    <p className="flex items-center text-sm text-gray-500">
                      Fetch current stock data with price, volume, and metrics
                    </p>
                  </div>
                </div>
              </div>
            </li>
            <li>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-blue-600 truncate">
                    GET /api/portfolio?accountId=default
                  </div>
                  <div className="ml-2 flex-shrink-0 flex">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                      Portfolio
                    </span>
                  </div>
                </div>
                <div className="mt-2 sm:flex sm:justify-between">
                  <div className="sm:flex">
                    <p className="flex items-center text-sm text-gray-500">
                      Get portfolio data including positions, P&L, and balances
                    </p>
                  </div>
                </div>
              </div>
            </li>
            <li>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-blue-600 truncate">
                    GET /api/analysis?symbol=AAPL
                  </div>
                  <div className="ml-2 flex-shrink-0 flex">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      Analysis
                    </span>
                  </div>
                </div>
                <div className="mt-2 sm:flex sm:justify-between">
                  <div className="sm:flex">
                    <p className="flex items-center text-sm text-gray-500">
                      Get trading analysis with technical indicators and
                      congressional trades
                    </p>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
