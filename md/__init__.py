from md.cashflow import *
from md.ratios import *
from md.shareholder import *
from md.balancesheet import *

MAPPER = {
    "others" : "Google it! :)", 
    "Debtor Days" : debtor_days,
    "Inventory Days" : inventory_days, 
    "Days Payable" : days_payable, 
    "Cash Conversion Cycle" : cash_conversion, 
    "Working Capital Days" : working_capital,
    "ROCE %" : ROCE, 
    "Pro" : promoter_md, 
    "FII" : FII_md, 
    "DII" : DII_md, 
    "Pub" : public_md, 
    "Gov" : gov_md, 
    "No." : num_sh_md, 
    "Operating" : operating_cashflow,
    "Investing" : investing_cashflow,
    "Financing" : financing_cashflow,
    "Net Cash Flow" : "Total of the other 3 Cashflow",
    "Equity Capital" : equity_capital, 
    "Reserves" : reserves,
    "Borrowings" : borrowings, 
    "Other Liabilities" : other_liabilities, 
    "Total Liabilities" : total_liabilities,
    "Fixed Assets" : fixed_assets, 
    "CWIP" : CWIP,
    "Investments" : investments, 
    "Other Assets" : other_assets,
    "Total Assets" : total_assets
} 