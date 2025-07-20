performance_ratio = """
### Importance Ranking of Financial Efficiency Ratios

These financial ratios are critical for evaluating a company's operational efficiency, profitability, and cash flow management. Here's the ranked order of importance with a normalized importance coefficient (1.0 = highest):

| Rank | Metric             | Importance Coefficient | Rationale                                                                 |
|------|--------------------|------------------------|---------------------------------------------------------------------------|
| 1    | **ROCE**           | 1.00                   | Measures overall efficiency of capital employed; reflects true profitability. |
| 2    | **ROE**            | 0.90                   | Shows return to shareholders; essential for equity investors.             |
| 3    | **Cash Conversion**| 0.85                   | Indicates how quickly a company converts operations into cash flow.       |
| 4    | **Working Capital**| 0.75                   | Reveals short-term liquidity and operational soundness.                   |
| 5    | **Inventory Days** | 0.65                   | Long inventory cycles can tie up capital and increase holding costs.      |
| 6    | **Debtor Days**    | 0.60                   | Reflects collection efficiency; delays can stress cash flow.              |
| 7    | **Days Payable**   | 0.50                   | Delayed payments help liquidity but may hurt supplier relationships.      |

> 💡 Higher ROCE with improving cash conversion and stable working capital signals a financially disciplined company.
"""

sharholding_pattern = """
### Importance Ranking of Shareholding Pattern Metrics

The shareholding pattern offers insights into investor confidence, stock stability, and market sentiment. Here's the ranked order of importance with a normalized importance coefficient (1.0 = highest):

| Rank | Category             | Importance Coefficient | Rationale                                                                 |
|------|----------------------|------------------------|---------------------------------------------------------------------------|
| 1    | **Promoters**        | 1.00                   | Indicates control and confidence of company founders/owners.              |
| 2    | **FIIs**             | 0.90                   | Reflects foreign institutional trust, often tied to strong fundamentals. |
| 3    | **DIIs**             | 0.80                   | Domestic institutional support shows stability and informed conviction.   |
| 4    | **Public**           | 0.60                   | High public holding may mean low insider control; can increase volatility.|
| 5    | **No. of Shareholders** | 0.40                | Indicates retail participation; higher numbers may dilute decision power. |
| 6    | **Government**       | 0.30                   | Often non-strategic or legacy holding; limited direct market signals.     |

> 💡 A rising FII/DII trend with stable promoter holding is generally considered a strong bullish signal.
"""

cash_flow = """
### Importance Ranking of Cash Flow Metrics

Cash flow metrics offer a real picture of a company's liquidity, financial discipline, and sustainability—beyond paper profits. Here's the ranked order of importance with a normalized importance coefficient (1.0 = highest):

| Rank | Category              | Importance Coefficient | Rationale                                                                 |
|------|-----------------------|------------------------|---------------------------------------------------------------------------|
| 1    | **Operating Cash Flow** | 1.00                 | Core measure of business health; reflects ability to generate cash from operations. |
| 2    | **Investing Cash Flow** | 0.70                 | Indicates capital allocation strategy; negative values can signal growth investments. |
| 3    | **Financing Cash Flow** | 0.50                 | Reveals how a company funds operations—through debt, equity, or distributions.         |

> 💡 Positive operating cash flow with controlled financing outflows and strategic investing outflows usually signals a fundamentally strong business.
"""

balance_sheet = """
### Importance Ranking of Balance Sheet

The balance sheet reveals a company’s financial position, stability, and capital structure. Below is a ranked list of key metrics with normalized importance coefficients (1.0 = highest):

| Rank | Metric              | Importance Coefficient | Rationale                                                                 |
|------|---------------------|------------------------|---------------------------------------------------------------------------|
| 1    | **Total Assets**    | 1.00                   | Captures the complete asset base; reflects operational and investment scale. |
| 2    | **Total Liabilities** | 0.92                | Indicates total obligations; key to assessing solvency and leverage.      |
| 3    | **Equity Capital**  | 0.88                   | Core funding source; affects ownership, dilution, and capital structure.  |
| 4    | **Reserves**        | 0.85                   | Retained earnings show internal funding and business sustainability.     |
| 5    | **Borrowings**      | 0.82                   | Reflects leverage; impacts risk profile and interest burden.              |
| 6    | **Investments**     | 0.72                   | Reveals capital deployment outside core operations; can drive future gains.|
| 7    | **Fixed Assets**    | 0.70                   | Tangible production capacity; essential for asset-heavy industries.       |
| 8    | **CWIP**            | 0.60                   | Signals upcoming capacity or projects in progress.                        |
| 9    | **Other Liabilities** | 0.55                | Includes provisions or payables; impacts working capital.                 |
|10    | **Other Assets**    | 0.50                   | Typically less productive or short-term; variable quality.                |

> 💡 A strong balance sheet has high reserves and stable borrowings relative to total assets.
"""

pnl_quarters = """
### Importance Ranking of Profit & Loss

These KPIs reflect a company's operational efficiency, profitability, and return to shareholders. Below is a ranked list with normalized importance coefficients (1.0 = highest):

| Rank | Metric               | Importance Coefficient | Rationale                                                                 |
|------|----------------------|------------------------|---------------------------------------------------------------------------|
| 1    | **Net Profit**       | 1.00                   | Final measure of profitability; directly impacts valuation and sentiment. |
| 2    | **Operating Profit** | 0.95                   | Reflects core business earnings before non-operational factors.           |
| 3    | **EPS in Rs**        | 0.90                   | Shows earnings per share; critical for equity investors.                  |
| 4    | **OPM (Operating Profit Margin)** | 0.85       | Assesses operational efficiency relative to revenue.                      |
| 5    | **Profit Before Tax**| 0.80                   | Captures profit before tax impact; key for margin trend analysis.         |
| 6    | **Sales**            | 0.75                   | Topline growth is vital but must be backed by margins.                    |
| 7    | **Expenses**         | 0.70                   | Monitored for cost control and scalability.                               |
| 8    | **Tax**              | 0.60                   | Affects net profitability; relevant for net margin trends.                |
| 9    | **Depreciation**     | 0.55                   | Impacts operating profit; reflects capital intensity.                     |
| 10   | **Interest**         | 0.50                   | Indicates debt burden; high interest reduces profitability.               |
| 11   | **Other Income**     | 0.45                   | Non-core income; less reliable indicator of core performance.             |
| 12   | **Dividend Payout**  | 0.35                   | Useful for income-focused investors; less important for growth analysis.  |

> 💡 A rising Net Profit with stable or rising OPM is often a strong indicator of sustainable growth.
"""