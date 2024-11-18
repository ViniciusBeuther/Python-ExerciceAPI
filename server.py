from fastapi import FastAPI
import pandas as pd
from Wallet import Wallet
from fastapi.middleware.cors import CORSMiddleware
# file paths
transactionFile = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets//Negociações.xlsx'
dividendTransactions = 'C:/Users/vinic/Downloads/PROJETOS DE DESENVOLVIMENTO/Controle de Rendimento/assets/Dividendos Recebidos.xlsx'

# Initialize and read investments spreadsheet
myWallet = Wallet(transactionFile, dividendTransactions)


app = FastAPI()

# setup CORS configuration
origins = [
    "http://localhost",
    "http://localhost:5173",
]
# allow origins to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/wallet')
def getWalletDf():
  objArray = []
  for index, row in myWallet.investment_df.iterrows():
    objArray.append(row[["Código de Negociação", "Quantidade", "Valor", "Preço Médio", "Tipo"]])
  
  return objArray

@app.get('/wallet/totals')
def getTotals():
  return {
      "totalInvestido": myWallet.getTotal(),
      "totalDividendos": myWallet.getDividends()
    }

@app.get('/wallet/dividends/{year}/{month}')
def getDividendsFromPeriod(year, month):
  return myWallet.dividends.getDividendFromYearAndMonth(month, year)