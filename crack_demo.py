import bcrypt
import time
import string
import itertools

# --- 設定値 ---
# ⚠️ 試行する平文パスワード (検証目的のため1文字、文字種は英数字)
# 鍵空間を小さくするため、ここでは数字のみを使用
PLAINTEXT_PASSWORD = "1" 

# 総当たりで試行する文字セット (0-9の10文字)
CHAR_SET = string.digits 

# コストファクターの定義
COST_LOW = 4  # 最小設定（意図的に脆弱な設定）
COST_HIGH = 12 # 実運用で推奨されるコスト（デモ用）
# --- ここまで設定値 ---

def hash_password(password, cost):
    """指定されたコストでパスワードをハッシュ化し、ソルトとコストを埋め込む"""
    # bcrypt.gensalt()はデフォルトでコスト12
    # costパラメータを使って任意のコストを設定
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=cost))
    return hashed.decode('utf-8')

def get_cost_from_hash(hashed_password_str):
    """ハッシュ文字列からコストファクターを安全に抽出する"""
    # ハッシュ文字列を'$'で分割し、インデックス2（3番目の要素）がコスト値
    # 例: '$2b$12$...' の場合、分割すると ['', '2b', '12', ...] となり、'12'が取得できる
    try:
        cost_str = hashed_password_str.split('$')[2]
        return int(cost_str)
    except (IndexError, ValueError) as e:
        print(f"🚨 ハッシュ解析エラー: {e}")
        return 0 # エラー時は0を返す

def crack_hash(hashed_password, char_set):
    """総当たり攻撃をシミュレートし、クラック時間を計測する"""
    # hashed_password.encode() でバイト列にして、それをソルトとして利用してハッシュ化を試みる
    # hashpw()は成功すればハッシュ値を返すため、その結果から rounds 属性を取得できる
    cost = get_cost_from_hash(hashed_password)
    print(f"\n--- クラック開始 (COST: {cost}) ---")
    start_time = time.time()
    
    # ハッシュ値からソルトとコストを抽出 (照合に必要)
    # bcrypt.checkpwが内部でやってくれるため、ここでは抽出不要
    # 単に総当たりで生成したハッシュと比較する
    
    # 1文字の総当たりを試行
    for char in char_set:
        attempt_password = char
        # bcrypt.checkpw(平文, ハッシュ値) で照合
        # 内部でソルトとコストを使って再ハッシュ化される
        if bcrypt.checkpw(attempt_password.encode('utf-8'), hashed_password.encode('utf-8')):
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"🎉 クラック成功\n  -> パスワード: {attempt_password}")
            print(f"  -> 所要時間: {elapsed_time:.4f} 秒")
            return
    
    # 実際は1文字なのでここには来ないが、念のため
    print("❌ クラック失敗 (パスワードが長すぎるか、文字セットに含まれていません)")


if __name__ == "__main__":
    print("▶️  総当たり開始")
    print(f"ターゲットパスワード: '{PLAINTEXT_PASSWORD}' (1文字)")
    print(f"試行文字セット: {CHAR_SET}")
    
    # 1. 低コストのハッシュを生成し、クラック
    low_cost_hash = hash_password(PLAINTEXT_PASSWORD, COST_LOW)
    print(f"\n[1] 低コストハッシュ生成 (COST: {COST_LOW})")
    print(f"  -> ハッシュ値: {low_cost_hash}")
    crack_hash(low_cost_hash, CHAR_SET)

    # 2. 高コストのハッシュを生成し、クラック
    high_cost_hash = hash_password(PLAINTEXT_PASSWORD, COST_HIGH)
    print(f"\n[2] 高コストハッシュ生成 (COST: {COST_HIGH})")
    print(f"  -> ハッシュ値: {high_cost_hash}")
    crack_hash(high_cost_hash, CHAR_SET)

    print("\n✅  総当たり終了")