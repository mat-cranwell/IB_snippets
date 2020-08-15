from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle

	def historicalData(self, reqId, bar):
		print(f'Time: {bar.date} Close: {bar.close}')
		self.data.append([bar.date, bar.close])
		
def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'AUD'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'JPY'

#Request historical candles
app.reqHistoricalData(1, eurusd_contract, '', '5 D', '5 mins', 'BID', 0, 2, False, [])

time.sleep(5) #sleep to allow enough time for data to be returned

#Working with Pandas DataFrames
import pandas

df = pandas.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pandas.to_datetime(df['DateTime'],unit='s') 
df.to_csv('AUDJPY_5mins.csv')  

print(df)


app.disconnect()