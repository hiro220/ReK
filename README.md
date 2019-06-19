# ReK
## Clone
`git clone https://github.com/hiroki-inoue-git/ReK`

## 実行
`shooting.py`
## CPUの作成
1. CpuMachineクラスを継承したクラスを作成
1. 画像、体力などを設定する
1. 移動、銃を撃つタイミングなどupdateの処理を記述する
1. define.pyに作成したクラスを指定するための定義を記述する
1. 実際にステージ上に呼び出すために、stage.py内の辞書にクラスを追加
```python
# cpumachine.py

class SampleCPU(CpuMachine):
    def __init__(self, x, y, player, score):
        image = pygame.image.load("img/samplecpu.png").convert_alpha()  # 画像のロード
        super().__init__(1, x, y, image, players, score)  # 第1引数は体力
        self.dx, self.dy = -2, 0   # 移動量はself.dx, self.dyを用いる
        self.gun = Sample_Gun(self.machines, self, 10)  # 銃の設定

    def update(self):
        self.rect.move_ip(self.dx, self.dy)     # 移動
        x, y = self.rect.midleft                # 画像の左真ん中の座標を取得
        if R_time.get_ticks() - self.gun_start >= 1200:
            # 前回弾を撃ってから1200ミリ秒経過していれば以下が実行
            super().shoot(x, y)     # 弾を発射
            self.gun_start = R_time.get_ticks()
```
```python
# define.py

SAMPLECPU = "SAMPLECPU"     # 作成したCPUを指定するための定義
```
```python
# stage.py

class Stage:
    ...
    def createOneCpu(self, name, x, y):
        ...
        # 辞書に作成したクラスを追加する
        cpu_dic = {CPU1:cpu, CPU2:cpu2, ..., SAMPLECPU:SampleCPU}
```

### 利用できるGUN一覧
|Name|Shoot|
|:-:|:-:|
|`Gun`|右方向に通常弾を撃つ|
|`Opposite_Gun`|左方向に通常弾を撃つ|
|`Reflection_Gun`|左方向に画面内で反射する弾を撃つ|
|`Circle_Gun`|周囲へ同時に通常弾を撃つ|
|`Twist_Gun`|左方向へ周期的に弾を撃つ|
|`Beam_Gun`|左方向へビームを撃つ|



## アイテムの作成
1. Itemクラスを継承したクラスを作成する
1. 画面内に流れるアイテムの画像を設定する
1. アイテムを取得したときの処理を記述する
1. define.pyに作成したクラスを指定するための定義を記述する
1. 実際にステージ上に呼び出すために、stage.py内の辞書にクラスを追加

```python
# item.py

class SampleItem(Item):
    def __init__(self, x, y, machine):
        image = pygame.image.load("img/sampleitem.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, machine):
        print("sample")
```

```python
# define.py

SAMPLEITEM = "SAMPLEITEM"  # 作成したCPUを指定するための定義
```

```python
# stage.py

class Stage:
    ...
    def createOneCpu(self, name, x, y):
        ...
        # 辞書に作成したクラスを追加する
        item_dic = {RECOVERY:Recovery, ..., SAMPLEITEM:SampleItem}
```


## Timerの利用

- シンプルなタイマーの実行

```python
def method():
    print("result")

Timer(1000, method)
```

```python
# 1000ミリ秒後
result
```

- 実行する関数に引数を与えるとき

```python
def method(a, b):
    print(a+b)

a, b = 10, 5
Timer(1000, method, a, b)
```

```python
# 1000ミリ秒後
15
```

- 実行する関数の返り値を利用したいとき
```python
def method(a, b):
    return a + b

a, b = 3, 4
timer = Timer(1000, method, a, b)

while True:
    if timer.value != None:
        print(timer.value)      # 返り値の利用
        timer.value = None      # リセット
```

```python
# 1000ミリ秒後
7
```


## ステージの作成
stageフォルダにテキストファイルを作成し、指定の方式で記述する
### フォーマット
タブ/スペース区切りで指定する。
- `size` : ステージの大きさを指定する。ステージは1秒間に30移動する。
- `rule` : [ステージルール](#利用できるステージルール)を指定する。
- [アイテム](#利用できるアイテム) : 生成位置のy座標(0~600)を指定する。
- CPU : 生成位置のy座標(0~600)を指定する。

```
# sample.txt

size    200
rule    SCORE_BASED    150

0
CPU1    100
CPU1    300
CPU1    500

100
RECOVERY    300
CPU2    100
CPU2    100

200
CPU_SHIELD  300
CPU3    300
SCOREGET    150
CPU3    100
CPU3    500
```

### 利用できるステージルール
|Rule Name|GameClear|GameOver|Paramater|
|:-:|:-:|:-:|:-:|
|`NORMAL`|最終面で残敵機の全滅|自機の破壊|*|
|`SCORE_BASED`|指定したスコアの達成|自機の破壊*or*スコア未達成|必要スコア|

### 利用できるアイテム
- Item Nameの前に、`CPU_`を付けるとCPUが取得するアイテムとして利用できる。
    - `CPU_SHIELD`など

|Item Name|Effect|
|:--:|:--:|
|`RECOVERY`|取得した機体の体力を1回復する|
|`SHIELD`|取得した機体に体力3のシールドを付与|
|`SPEEDDOWN`|取得した機体のスピードが3秒間落ちる|
|`SCOREGET`|取得した時点で画面内に残る敵機数×5のスコアを獲得する|
|`METEORITE`|相手にダメージのある隕石を5つ落とす|
