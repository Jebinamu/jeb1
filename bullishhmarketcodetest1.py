import pandas as pd
import time
import ccxt
import numpy as np

# 업비트 API 키 설정
API_KEY = 'acc.key'
API_SECRET = 'sec.key'

# 업비트 API 객체 생성
upbit = ccxt.upbit({'apiKey': API_KEY, 'secret': API_SECRET})

# 비트코인 데이터 가져오기
def fetch_bitcoin_data(market, timeframe, count):
    candles = upbit.fetch_ohlcv(market, timeframe, limit=count)
    timestamps = [candle[0] for candle in candles]
    opens = [candle[1] for candle in candles]
    highs = [candle[2] for candle in candles]
    lows = [candle[3] for candle in candles]
    closes = [candle[4] for candle in candles]
    volumes = [candle[5] for candle in candles]
    df = pd.DataFrame({'timestamp': timestamps, 'open': opens, 'high': highs, 'low': lows, 'close': closes, 'volume': volumes})
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# 이동평균 크로스오버 전략
def moving_average_crossover_strategy(data, short_window, long_window):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # 단기 이동평균
    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()

    # 장기 이동평균
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # 단기 이동평균이 장기 이동평균을 상향 돌파하면 매수 신호
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # 매수/매도 신호가 바뀌는 지점을 찾아냄
    signals['positions'] = signals['signal'].diff()

    return signals

# 현재 보유 중인 포지션을 저장하는 변수
current_position = 0
# 수수료율 (단위: 퍼센트)
commission_rate = 0.1  # 예시 수수료율, 실제로는 계정에 설정된 수수료율을 사용

# 매수 주문 실행 함수
def execute_buy_order(market, current_position, amount, bitcoin_data):
    try:
        # createMarketBuyOrderRequiresPrice 옵션을 사용하여 가격 자동 계산
        response = upbit.create_market_buy_order(f'{market}', amount=amount, createMarketBuyOrderRequiresPrice=False)
        print("매수 주문이 실행되었습니다.")
        print(response)
        
        # 매수 금액에 수수료 추가
        amount_with_commission = amount * (1 + commission_rate / 100)
        current_position = 1  # 매수 완료 후 포지션을 보유 중으로 설정
        return amount_with_commission
    except Exception as e:
        print("매수 주문이 실패했습니다.")
        print(e)
        return None

# 매도 주문 실행 함수
def execute_sell_order(market, current_position, amount):
    try:
        response = upbit.create_market_sell_order(f'{market}', amount)
        print("매도 주문이 실행되었습니다.")
        print(response)
        current_position = 0  # 매도 완료 후 포지션을 보유 중이 아닌 상태로 설정
    except Exception as e:
        print("매도 주문이 실패했습니다.")
        print(e)

# 비트코인 시장 정보
market = 'BTC/KRW'
timeframe = '1h'
count = 100

# 이동평균 크로스오버 전략 적용
short_window = 10
long_window = 50
bitcoin_data = fetch_bitcoin_data(market, timeframe, count)
signals = moving_average_crossover_strategy(bitcoin_data, short_window, long_window)

# 매수 또는 매도 주문 실행
for i in range(len(signals)):
    if signals['positions'].iloc[i] == 1.0 and current_position == 0:
        execute_buy_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매수
    elif signals['positions'].iloc[i] == -1.0 and current_position == 1:
        execute_sell_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매도

    time.sleep(60)  # 1분에 한 번씩 주문 실행

# 비트코인 시장 정보
market = 'BTC/KRW'
timeframe = '1h'
count = 100

# 이동평균 크로스오버 전략 적용
short_window = 10
long_window = 50
bitcoin_data = fetch_bitcoin_data(market, timeframe, count)
signals = moving_average_crossover_strategy(bitcoin_data, short_window, long_window)

# 매수 또는 매도 주문 실행
for i in range(len(signals)):
    if signals['positions'].iloc[i] == 1.0 and current_position == 0:
        execute_buy_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매수
    elif signals['positions'].iloc[i] == -1.0 and current_position == 1:
        execute_sell_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매도

    if signals['positions'].iloc[i] != 0.0:
        time.sleep(60)  # 주문이 발생한 경우에만 1분에 한 번씩 주문 실행

# 두 번째 루프 제거

# 비트코인 시장 정보
market = 'BTC/KRW'
timeframe = '1h'
count = 100

# 이동평균 크로스오버 전략 적용
short_window = 10
long_window = 50
bitcoin_data = fetch_bitcoin_data(market, timeframe, count)
signals = moving_average_crossover_strategy(bitcoin_data, short_window, long_window)

# 매수 또는 매도 주문 실행
for i in range(len(signals)):
    if signals['positions'].iloc[i] == 1.0 and current_position == 0:
        execute_buy_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매수
    elif signals['positions'].iloc[i] == -1.0 and current_position == 1:
        execute_sell_order(market, current_position, bitcoin_data['close'].iloc[i])  # 현재 종가로 매도

    if signals['positions'].iloc[i] != 0.0:
        time.sleep(60)  # 주문이 발생한 경우에만 1분에 한 번씩 주문 실행

    # 수정된 부분: 두 번째 루프에서도 `current_position`을 업데이트합니다.
    current_position = signals['positions'].iloc[i]