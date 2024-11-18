import json
import random
import argparse
import os

def split_json_data(input_file, train_ratio, val_ratio):
    """
    JSONデータをトレーニング、検証、テストに分割して保存する関数。

    Args:
        input_file (str): 入力JSONファイルのパス
        train_ratio (float): トレーニングデータの割合 (例: 0.6)
        val_ratio (float): 検証データの割合 (例: 0.2)
    """
    # 入力ファイルのディレクトリを取得
    input_dir = os.path.dirname(input_file)

    # 出力ファイル名を生成
    train_file = os.path.join(input_dir, 'train_data.json')
    val_file = os.path.join(input_dir, 'val_data.json')
    test_file = os.path.join(input_dir, 'test_data.json')

    # JSONファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # データをシャッフルする
    random.shuffle(data)

    # データの分割割合を計算
    total_len = len(data)
    train_size = int(total_len * train_ratio)
    val_size = int(total_len * val_ratio)

    # データの分割
    train_data = data[:train_size]
    val_data = data[train_size:train_size + val_size]
    test_data = data[train_size + val_size:]

    # 各データセットをJSONファイルに保存
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=4)

    with open(val_file, 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=4)

    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=4)

    print("データを分割して、トレーニング、検証、テストのJSONファイルに保存しました。")
    print(f"トレーニングデータ: {len(train_data)} 行 -> {train_file}")
    print(f"検証データ: {len(val_data)} 行 -> {val_file}")
    print(f"テストデータ: {len(test_data)} 行 -> {test_file}")

if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='JSONデータを分割して保存します。')
    parser.add_argument('input_file', type=str, help='入力JSONファイルのパス')
    parser.add_argument('--train_ratio', type=float, default=0.6, help='トレーニングデータの割合 (例: 0.6)')
    parser.add_argument('--val_ratio', type=float, default=0.2, help='検証データの割合 (例: 0.2)')

    # 引数をパース
    args = parser.parse_args()

    # 検証データとテストデータの割合チェック
    if args.train_ratio + args.val_ratio >= 1.0:
        raise ValueError("トレーニングデータと検証データの割合の合計は1未満である必要があります。")

    # 関数を実行
    split_json_data(
        input_file=args.input_file,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio
    )

