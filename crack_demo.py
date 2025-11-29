import bcrypt
import time
import string
import itertools
import sys

# --- 設定値 ---
# コストファクターの定義
COST_LOW = 4    # 最小設定（意図的に脆弱な設定）
COST_HIGH = 12  # 実運用で推奨されるコスト（デモ用）
# --- ここまで設定値 ---

def hash_password(password, cost):
    """指定されたコストでパスワードをハッシュ化し、ソルトとコストを埋め込む"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=cost))
    return hashed.decode('utf-8')

def get_cost_from_hash(hashed_password_str):
    """ハッシュ文字列からコストファクターを安全に抽出する"""
    try:
        # 例: '$2b$12$...' の場合、'12'が取得できる
        cost_str = hashed_password_str.split('$')[2]
        return int(cost_str)
    except (IndexError, ValueError):
        return 0

def attempt_crack(hashed_password, char_set, max_time):
    """総当たり攻撃をシミュレートし、時間制限内でクラックを試行する"""
    
    cost = get_cost_from_hash(hashed_password)
    print(f"\n--- クラック試行開始 (COST: {cost}, 制限時間: {max_time}秒) ---") 
    
    start_time = time.time()
    
    # 試行する文字の組み合わせを生成 (パスワードが長くなると試行回数が指数関数的に増える)
    # ここでは平文の文字数に合わせて、1文字から最大3文字までを試す
    for length in range(1, 4): 
        for attempt_tuple in itertools.product(char_set, repeat=length):
            if time.time() - start_time > max_time:
                # タイムアウト
                elapsed_time = time.time() - start_time
                print(f"⌛ タイムアウト！\n  -> 所要時間: {elapsed_time:.4f}秒 ({max_time}秒以内に完了せず)")
                return False # 失敗（セキュリティ成功）

            attempt_password = "".join(attempt_tuple)

            # bcrypt.checkpw(平文, ハッシュ値) で照合
            if bcrypt.checkpw(attempt_password.encode('utf-8'), hashed_password.encode('utf-8')):
                # クラック成功
                elapsed_time = time.time() - start_time
                print(f"🔥 クラック成功！🚨\n  -> パスワード: {attempt_password}")
                print(f"  -> 所要時間: **{elapsed_time:.4f} 秒**")
                return True # 成功（セキュリティ失敗）
    
    # 制限時間内に見つからず、かつ、すべての組み合わせを試行し終えた場合
    elapsed_time = time.time() - start_time
    print(f"🔒 試行完了 (クラック失敗)\n  -> 所要時間: {elapsed_time:.4f}秒 (すべての組み合わせを試行)")
    return False # 失敗（セキュリティ成功


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("🚨 使用方法: python crack_demo.py <検証パスワード> <制限時間(秒)>")
        print("例: python crack_demo.py 123 5")
        sys.exit(1)

    # コマンドライン引数から値を取得
    PLAINTEXT_PASSWORD = sys.argv[1]
    try:
        MAX_TIME = float(sys.argv[2])
    except ValueError:
        print("🚨 制限時間(秒)は数値で指定してください。")
        sys.exit(1)

    # 検証に使う文字セット (引数で渡されたパスワードに含まれる文字をベースにする)
    CHAR_SET = sorted(list(set(PLAINTEXT_PASSWORD)))

    print("▶️  総当たり開始")
    print(f"ターゲットパスワード: '{PLAINTEXT_PASSWORD}' (文字数: {len(PLAINTEXT_PASSWORD)})")
    print(f"試行文字セット: {CHAR_SET} (総当たりは1文字から3文字まで)")
    
    # 1. 低コストのハッシュを生成し、検証
    low_cost_hash = hash_password(PLAINTEXT_PASSWORD, COST_LOW)
    print(f"\n--- 検証 [1/2] 低コスト ---")
    print(f"  -> ハッシュ値: {low_cost_hash}")
    attempt_crack(low_cost_hash, CHAR_SET, MAX_TIME)

    # 2. 高コストのハッシュを生成し、検証
    high_cost_hash = hash_password(PLAINTEXT_PASSWORD, COST_HIGH)
    print(f"\n--- 検証 [2/2] 高コスト ---")
    print(f"  -> ハッシュ値: {high_cost_hash}")
    attempt_crack(high_cost_hash, CHAR_SET, MAX_TIME)

    print("\n✅  総当たり終了")