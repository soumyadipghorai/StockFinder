from md.cashflow import *
from md.ratios import *
from md.shareholder import *
from md.balancesheet import *
from md.pnl import *
from md.ranking import *

MAPPER = {
    "others" : "Google it! :)", 
    
    # performance ratios 
    "Debtor Days" : debtor_days,
    "Inventory Days" : inventory_days, 
    "Days Payable" : days_payable, 
    "Cash Conversion Cycle" : cash_conversion, 
    "Working Capital Days" : working_capital,
    "ROCE" : ROCE, 
    "ROE" : ROE,
    "performance_ranking" : performance_ratio,
    
    # shareholding pattern 
    "Promoters" : promoter_md, 
    "FIIs" : FII_md, 
    "DIIs" : DII_md, 
    "Public" : public_md, 
    "Government" : gov_md, 
    "No. of Shareholders" : num_sh_md, 
    "sharholding_pattern" : sharholding_pattern,

    # cash flow 
    "Operating" : operating_cashflow,
    "Investing" : investing_cashflow,
    "Financing" : financing_cashflow,
    "Net Cash Flow" : "Total of the other 3 Cashflow",
    "cash_flow" : cash_flow, 

    # balance sheet 
    "Equity Capital" : equity_capital, 
    "Reserves" : reserves,
    "Borrowings" : borrowings, 
    "Other Liabilities" : other_liabilities, 
    "Total Liabilities" : total_liabilities,
    "Fixed Assets" : fixed_assets, 
    "CWIP" : CWIP,
    "Investments" : investments, 
    "Other Assets" : other_assets,
    "Total Assets" : total_assets, 
    "balance_sheet" : balance_sheet,

    # quarters & pnl 
    "Sales" : sales, 
    "Expenses" : expenses,
    "Operating Profit" : operating_profit, 
    "OPM" : OPM,
    "Other Income" : other_income,
    "Interest" : interest,
    "Depreciation" : depreciation,
    "Profit before tax" : PBT,
    "Tax" : tax, 
    "Net Profit" : net_profit, 
    "EPS in Rs" : EPS, 
    "Dividend Payout" : dividend_payout, 
    "pnl_quarters" : pnl_quarters,
} 