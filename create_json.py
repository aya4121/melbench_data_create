import pandas as pd
import json
import os
import argparse

def create_json_from_csv(csv_file_path, wav_files_dir, img_files_dir, output_json_file):
    """
    指定されたCSVファイル、WAVファイルのディレクトリ、画像ファイルのディレクトリを基に、
    JSONファイルを生成する。

    Args:
        csv_file_path (str): 入力CSVファイルのパス
        wav_files_dir (str): WAVファイルが格納されたディレクトリのパス
        img_files_dir (str): 画像ファイルが格納されたディレクトリのパス
        output_json_file (str): 出力するJSONファイルのパス
    """
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    # JSONに変換するためのリストを作成
    json_data = []

    # カウンターの初期化
    wav_missing_count = 0
    png_missing_count = 0
    skipped_count = 0

    # 各行について処理
    for _, row in df.iterrows():
        # 各フィールドの生成
        captions = row['Annotation']
        start_second = int(row['start_second'])
        end_second = int(row['end_second'])
        
        # wav ファイルのパスを生成し、スラッシュに統一
        location = os.path.join(
            wav_files_dir,
            f"{row['youtube_video_id']}_{start_second}_{end_second}.wav"
        ).replace("\\", "/")  # バックスラッシュをスラッシュに変換
        
        # img_path のフルパスを生成し、スラッシュに統一
        img_path = os.path.join(img_files_dir, row['image_path']).replace("\\", "/")

        # wav ファイルと画像ファイルが存在するかを確認
        if os.path.exists(location) and os.path.exists(img_path):
            # JSONのエントリを追加
            json_data.append({
                "captions": captions,
                "location": location,
                "img_path": img_path
            })
        else:
            # 存在しないファイルについてカウントし、スキップ
            if not os.path.exists(location):
                wav_missing_count += 1
                print(f"WAVファイルが存在しないためスキップされました: {location}")
            if not os.path.exists(img_path):
                png_missing_count += 1
                print(f"画像ファイルが存在しないためスキップされました: {img_path}")
            
            skipped_count += 1

    # JSONファイルに保存
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    # 結果を表示
    print(f"JSONファイルが正常に作成されました: {output_json_file}")
    print(f"WAVファイルが見つからなかった数: {wav_missing_count}")
    print(f"PNGファイルが見つからなかった数: {png_missing_count}")
    print(f"スキップされたCSVの行数: {skipped_count}")
    print(f"生成されたJSONファイルの行数: {len(json_data)}")


if __name__ == '__main__':
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='CSVファイルからJSONを生成します。')
    parser.add_argument('csv_file_path', type=str, help='入力CSVファイルのパス')
    parser.add_argument('wav_files_dir', type=str, help='WAVファイルのディレクトリパス')
    parser.add_argument('img_files_dir', type=str, help='画像ファイルのディレクトリパス')
    parser.add_argument('output_json_file', type=str, help='出力JSONファイルのパス')

    # 引数をパース
    args = parser.parse_args()

    # 関数を実行
    create_json_from_csv(args.csv_file_path, args.wav_files_dir, args.img_files_dir, args.output_json_file)


