# README

## 🚫🚫🚫 Disclaimer 🚫🚫🚫

Use of this code on unauthorized systems is strictly prohibited.

## 📖 How to Use

### 🔧 Docker イメージのビルド

```bash
docker build -t bcrypt-crack-demo .
```

### 🚀 **Docker コンテナの実行**

```bash
docker run --rm bcrypt-crack-demo python crack_demo.py 12 5
```

### 🎉 **実行結果サンプル**

```
$ docker run --rm bcrypt-crack-demo python crack_demo.py 12 5

▶️  総当たり開始
ターゲットパスワード: '12' (文字数: 2)
試行文字セット: ['1', '2'] (総当たりは1文字から3文字まで)

--- 検証 [1/2] 低コスト ---
  -> ハッシュ値: $2b$04$QZx3Dnd9lRVAnH5LG1xZEOsZvQfKa3iS6HOevL9CE.iQr2wP5/cLe

--- クラック試行開始 (COST: 4, 制限時間: 5.0秒) ---
🔥 クラック成功！🚨
  -> パスワード: 12
  -> 所要時間: **0.0043 秒**

--- 検証 [2/2] 高コスト ---
  -> ハッシュ値: $2b$12$U/KPBRi59PIPlxny58OqWejTG.xCFviGbsNSVzvegjWWB3S9/INu.

--- クラック試行開始 (COST: 12, 制限時間: 5.0秒) ---
🔥 クラック成功！🚨
  -> パスワード: 12
  -> 所要時間: **0.8590 秒**

✅  総当たり終了
```
