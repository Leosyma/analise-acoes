# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:28:19 2024

@author: leoja
"""

#%% Bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import  yfinance as yf
from datetime import datetime, timedelta

#%% Exemplo da Biblioteca yfinance
# Ação
petr = yf.Ticker('PETR4.SA')

# Histórico da Ação
petr.history(period='max')

# Gráfico da Ação
petr.history(period='max')['Close'].plot()

# Informações
petr.info

# show actions (dividends, splits)
petr.actions

# show dividends
petr.dividends

# show splits
petr.splits

# Relatorio Financeiro
petr.financials
petr.quarterly_financials

# show major holders
petr.major_holders

# show institutional holders
petr.institutional_holders

# show balance sheet
petr.balance_sheet
petr.quarterly_balance_sheet

# show cashflow
petr.cashflow
petr.quarterly_cashflow

# show earnings
petr.earnings
petr.quarterly_earnings


# %% Analise de Ações
# Leitura dos dados
df_ibov = pd.read_csv(r'C:\Users\leoja\OneDrive\Documentos\Projetos\Dados\IBOVDia_18-07-24.csv',header=1,sep=';',decimal=',',thousands=',',encoding='ANSI',index_col=False,dtype='str')
df_ibov = df_ibov.dropna()

# Orderna os valores
df_ibov[['Part. (%)']] = df_ibov[['Part. (%)']].apply(lambda x: x.str.replace(',','.'))
df_ibov['Part. (%)'] = pd.to_numeric(df_ibov['Part. (%)'])
df_ibov = df_ibov.sort_values(by='Part. (%)',ascending=False).reset_index(drop=True)

# Seleciona as 10 melhores ações
top_acoes = df_ibov.iloc[0:10,:]

# Manipulação dos nomes das ações
nomes = top_acoes['Código'].to_list()
nomes_acoes=[]
for i in nomes:
    nome = i + '.SA'
    nomes_acoes.append(nome)

# Seleciona as ações do yfinance
tickers = yf.Tickers(nomes_acoes)

# Dicionário com as ações e seu respectivo preço
dict_acoes = {}
for ticker in tickers.tickers.keys():
    dict_acoes[ticker] = tickers.tickers[ticker].history(period='max')

# Dataframe com as ações de fechamento
df = pd.DataFrame()
for ticker in dict_acoes.keys():
    dict_acoes[ticker] = dict_acoes[ticker].rename(columns={'Close':ticker})
    df = pd.concat([df,dict_acoes[ticker][ticker]],axis=1)
    
# Data em todos ativos estavam no bolsa
df[df.notnull()].index[0]

# Variação percentual diária de cada ativo
df_var = df / df.shift(1) - 1

# Data em houve a pior oscilação
df_var.idxmin()
df_var.min()

# Variação de quando o retorno do dia anterior foi negativo
df_var[df_var.shift(1) < 0].mean() # Em média as ações não tem retorno positivo no dia seguinte após uma queda
df_var[df_var.shift(1) < 0].std()

# Gráfico
df_study = df_var[df_var.shift(1) < 0]
fig, ax = plt.subplots(figsize=(10,6))
sns.histplot(df_study, kde=True)

print('Média dos retornos')
for acao in nomes_acoes:
    print('{} - {}'.format(acao, df_study[acao].mean()*100))

print('Desvio padrão dos retornos')
for acao in nomes_acoes:
    print('{} - {}'.format(acao, df_study[acao].std()*100))

# Conclusão: não vale a pena ação comprar que sofre uma queda e vender no dia seguinte, pois a variação média está centrada muito perto do zero


#%% Dividend Yield (DY)
df_dividends = pd.DataFrame()

# Empilha os dados de dividendos
for ticker in tickers.tickers.keys():
    df_dividends_aux = tickers.tickers[ticker].dividends
    df_dividends_aux = df_dividends_aux.to_frame().rename(columns={'Dividends':ticker})
    df_dividends = pd.concat([df_dividends,df_dividends_aux],axis=1)

# Cria uma coluna com o ano
df_dividends['year'] = df_dividends.index.year
df.index = pd.to_datetime(df.index)
df['year'] = df.index.year

# Agrupa por ano
df_dividends_year = df_dividends.groupby(by='year').sum()
df_last_price = df.dropna().groupby('year').last()

# DY
df_yield = df_dividends_year / df_last_price * 100

# Retorno de cada ano
df_ret_year = df_last_price / df_last_price.shift(1) - 1

### Carteira Global
# Retorno por cada ação
(df_ret_year / 10).sum(axis=1)

# Retorno acumulado, ou seja, reinvestir o retorno
((df_ret_year / 10).sum(axis=1) + 1).cumprod().plot()

### Carteira com as 3 maiores pagadores de dividendos
# 3 maiores, exemplo 2008
df_yield = df_yield.dropna()
df_yield.iloc[0,:].nlargest(3).index # 3 ações para serem investidas em 2009

# Estratégia
strategy_return = []
for i in range(len(df_yield) - 1):
    stocks = df_yield.iloc[i, :].nlargest(3).index    
    strategy_return += [(df_ret_year[stocks].iloc[i+1] / 3).sum() + 1]

# Gráfico
df_global = df_ret_year / 10

fig, ax = plt.subplots()
pd.DataFrame(strategy_return, index=df_global.index[1:]).cumprod().plot(color="red", ax=ax)
(df_global.sum(axis=1) + 1).cumprod().plot(color="blue", ax=ax)

# Carteira Global deu um retorno maior









