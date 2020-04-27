Backtesting.py (modified version)
==============

Fork元のオリジナルはこちら→ [**original version**](https://kernc.github.io/backtesting.py/)

* Backtesting.pyをもとに、いくつか分析用の項目を追加したものです。
* original versionでの「Open」「High」「Low」「Close」「Volume」の5項目に以下の項目を追加しています。
    * Open2
    * High2
    * Low2
    * Close2
    * Volume2
    * Open3
    * High3
    * Low3
    * Close3
    * Volume3
    * Flg1
    * Flg2
    * Flg3
    * Flg4
    * Flg5

インストール方法
-----
```python
$ pip install git+https://github.com/2kg-jp/backtesting.py
```


使い方
-----
```python
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG


class SmaCross(Strategy):
    def init(self):
        Close = self.data.Close
        self.ma1 = self.I(SMA, Close, 10)
        self.ma2 = self.I(SMA, Close, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002)
bt.run()
bt.plot()
```

Results in:

```text
Start                     2004-08-19 00:00:00 <- テストデータの開始日時
End                       2013-03-01 00:00:00 <- テストデータの終了日時
Duration                   3116 days 00:00:00 テストデータの期間
Exposure [%]                            94.29 エクスポージャー。テストデータ期間のうちポジションを持っていた期間の割合（ポジションあり期間 / テストデータ期間）
Equity Final [$]                     69665.12 テスト終了時の資産金額
Equity Peak [$]                      69722.15 テスト期間中の資産の最高金額
Return [%]                             596.65 収益率（（テスト終了時の資産金額 - テスト開始時の資産金額） /  テスト開始時の資産金額）
Buy & Hold Return [%]                  703.46 バイアンドホールドの投資戦略をとった場合の収益率（（テスト終了時の終値 - テスト開始時の終値） / テスト開始時の終値）
Max. Drawdown [%]                      -33.61 最大下落率
Avg. Drawdown [%]                       -5.68 平均下落率
Max. Drawdown Duration      689 days 00:00:00 最大下落期間
Avg. Drawdown Duration       41 days 00:00:00 平均下落期間
# Trades                                   93 全取引回数
Win Rate [%]                            53.76 勝率（勝ち取引回数 / 全取引回数）
Best Trade [%]                          56.98 最大利益率（1回の取引での最大利益金額 / 資産金額）
Worst Trade [%]                        -17.03 最大損失率（1回の取引での最大損失金額 / 資産金額）
Avg. Trade [%]                           2.44 平均損益率（損益の平均金額 / 資産金額）
Max. Trade Duration         121 days 00:00:00 最長取引期間
Avg. Trade Duration          32 days 00:00:00 平均取引期間
Expectancy [%]                           6.92 期待値（（平均利益金額 x 勝率） + （平均損失金額 x 敗率））
SQN                                      1.77 Van K. Tharp考案の取引システムの評価方法（System Quality Number）2.5以上が良いとされる
Sharpe Ratio                             0.22 シャープ・レシオ。「収益率の標準偏差＝リスク」当たりの超過収益を計算したもので高いほど効率的である。（（収益率 - 利回り） / 収益率の標準偏差）
Sortino Ratio                            0.54 ソルティノレシオ。下落リスクを重視したシャープ・レシオの改良版。（（収益率 - 利回り） / 収益率の下方偏差）
Calmar Ratio                             0.07 カルマーレシオ。平均収益率を最大ドローダウンで割った値。
_strategy                            SmaCross
```
