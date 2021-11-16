class loadData:
    """ Holds the Volume, Price, and Technical Data for the
        chosen indicators in a DataFrame

        Args:
            client (object): Binance API client
            pair (str): e.g 'BTCUSDT'
            interval (str): e.g '1m'
            start_str (str): Time in milliseconds/1000 .. not done <
            end_str (str): optional: end time of datasampling in millisec
            indicators (bool, [optional]): returns DataFrame of technicals if True. Defaults to False.
    """
    import sys
    from time import sleep
    from datetime import datetime
    import pandas as pd
    
    def __init__(self, client, tickers, interval, start_str, end_str):
        self.client = client
        self.tickers = tickers
        self.interval = interval
        self.start_str = start_str
        self.end_str = end_str
        
    def priceFrame(self): #pair, interval, start_str, end_str):
        """Generates a simple DataFrame of the main price data

            Args:
                pair ([type]): [description]
                interval ([type]): [description]
                start_str ([type]): [description]
                end_str ([type]): [description]
        """
        return None

    def load(self):
        """ #2 - RUN DATA COLLECTOR >>>>>>
        """
        #TODO lage et lite api av progressbar funksjonene
        #coins = ['BTC', 'ETH', 'XRP']       # Specify which currency to include in data collection
        coins = self.tickers
        
        # MAIN REQUEST LOOP    ---------->
        for i, coin in enumerate(coins):
            if not i: self.sys.stdout.write("[%-20s] %d%%" % ('='*0, 30*i))  #Progress bar
            print(f' Gathering {coin}...')
            klines = self.client.get_historical_klines(
                symbol=f'{coin}USDT',
                interval=self.interval,
                start_str=self.start_str,
                end_str=self.end_str)
            
            # PROGRESS BAR PROGRESSING ---->
            currentbar = (i+1)*7
            lastbar = i*7
            barPercent = float(currentbar/21)
            for nbar in range(lastbar, currentbar):
                self.sys.stdout.write('\r')
                self.sys.stdout.write("[%-20s] %d%%" % ('='*nbar, (nbar/currentbar)*100*barPercent))
                self.sys.stdout.flush()
                self.sleep(0.04)

            # Create column name list for corresponding data
            cols = ['OpenTime',
                    f'{coin}/USDT_Open',
                    f'{coin}/USDT_High',
                    f'{coin}/USDT_Low',
                    f'{coin}/USDT_Close',
                    f'{coin}/USDT_Volume',
                    'CloseTime',
                    f'{coin}-QuoteAssetVolume',
                    f'{coin}-NumberOfTrades',
                    f'{coin}-TBBAV',
                    f'{coin}-TBQAV',
                    f'{coin}-ignore',]
            coin_df = self.pd.DataFrame(klines,columns=cols)
            
            # FINAL DATAFRAME
            df = coin_df if i <= 0 else self.pd.merge(df, coin_df, how='inner', on=['OpenTime', 'CloseTime'])

            # Confirm download success and update progress bar
            if i >= len(coins)-1:
                self.sys.stdout.write(f" Dataset downloaded successfully!\n")
            
            # Prevent API max request
            self.sleep(1)

        # Convert raw timedata to datedime format
        df['OpenTime'] = [self.datetime.fromtimestamp(ts / 1000) for ts in df['OpenTime']]
        df['CloseTime'] = [self.datetime.fromtimestamp(ts / 1000) for ts in df['CloseTime']]
        for col in df.columns:
            if not 'Time' in col:
                df[col] = df[col].astype(float)

        # Progress bar >    # TODO - Animate progressbar at 100%
        #for nbars in range(0, currentbar):   
        if i >= len(coins)-1:       
            self.sys.stdout.write(f"[====================] {100}% DataFrame:'df' ready for deployment!")
        else:
            self.sys.stdout.write('\r')
            self.sys.stdout.write("[%-20s] %d%%" % ('='*(i+1)*7, 30*(i+1)))
            self.sys.stdout.flush()
            
        return df
        

class TradingEnv:
    # Initialize virtual trading account ->
    def __init__(self, balance_amount, balance_unit, trading_fee_multiplier):
        self.balance_amount = balance_amount                    # Account balance
        self.balance_unit = balance_unit                        # Display currency
        self.buys = []                                          # Buy history
        self.sells = []                                         # Sell history
        self.trading_fee_multiplier = trading_fee_multiplier    # Fee multiplier [VIP level 0, paying fees with 'BNB']
        
        
    # Virtual BUY ->
    def buy(self, symbol, buy_price, time):
        self.balance_amount = (self.balance_amount / buy_price) * self.trading_fee_multiplier   # 1. Sets the balance of the bought asset based on buyprice
        self.balance_unit = symbol                                                              # 2. The currency unit of the bougt asset 
        self.buys.append([symbol, time, buy_price])                                             # 3. Save buy action in a list
        
    # Virtual SELL >
    def sell(self, sell_price, time):
        self.balance_amount = self.balance_amount * sell_price * self.trading_fee_multiplier    # 1. Sets the account balance after sell
        self.sells.append( [self.balance_unit, time, sell_price] )                              # 2. Save sell action in a list
        self.balance_unit = 'USDT'                                                              # 3. Sets the balance unit to 'USDT' for account balance


class Indicators:
   # Class for collecting custom technical indicators
    def __init__(self, dataframe, window, nstd):
        self.data = dataframe
        self.window = window
        self.nstd = nstd           # Number of standard deviations
        
    def sma(self, data, window):
        return(data.rolling(window=window).mean())

    def bollinger_band(self):
        self.window = window
        self.nstd = nstd
        std = self.data.rolling(window = self.window).std()
        upper_band = sma(self.data, window) + std * nstd
        lower_band = sma(self.data, self.window) - std * self.nstd
        
        return upper_band, lower_band
  
        
        
  
   