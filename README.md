# README

**Docker イメージのビルド**

```bash
docker build -t bcrypt-crack-demo .
```

**Docker コンテナの実行**

```bash
docker run --rm bcrypt-crack-demo
```

**実行結果サンプル**

```
$ docker run --rm bcrypt-crack-demo

▶️  総当たり開始
ターゲットパスワード: '1' (1文字)
試行文字セット: 0123456789

[1] 低コストハッシュ生成 (COST: 4)
  -> ハッシュ値: $2b$04$mNEZq1lHWjOJuBNrYjO3k.NmFIR2fV.jooC97R.eRI7OvnqG8L64.

--- クラック開始 (COST: 4) ---
🎉 クラック成功
  -> パスワード: 1
  -> 所要時間: 0.0021 秒

[2] 高コストハッシュ生成 (COST: 12)
  -> ハッシュ値: $2b$12$8JTQBUGHntMvKo2TbnNtTuVkNdony9qCYrEH.rOTKu73Fv9Up49Am

--- クラック開始 (COST: 12) ---
🎉 クラック成功
  -> パスワード: 1
  -> 所要時間: 0.4263 秒

✅  総当たり終了
```
