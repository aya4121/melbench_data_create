# clean_csv_1.py
import pandas as pd
import argparse
import os

def clean_and_save_csv(input_file_path):
    """
    指定されたCSVファイルを読み込み、start_secondとend_second列をクリーンアップし、
    欠損データを削除して、新しいファイルとして保存する関数。
    
    Args:
        input_file_path (str): 入力となるCSVファイルのパス
    """
    
    print(f"処理中のファイル: {input_file_path}")

    # CSVファイルの読み込み
    data = pd.read_csv(input_file_path)
    
    # start_secondとend_secondから数字以外の文字を削除する関数
    def clean_time_column(column):
        return pd.to_numeric(column.str.replace(r'\D', '', regex=True), errors='coerce')

    # 必要な列を選択してコピー
    selected_columns = data[['youtube_video_id', 'start_second', 'end_second', 'Annotation', 'image_path']].copy()

    # start_secondとend_second列をクリーンアップ
    selected_columns['start_second'] = clean_time_column(selected_columns['start_second'])
    selected_columns['end_second'] = clean_time_column(selected_columns['end_second'])

    # 欠損データがある行を削除する前の行数
    initial_row_count = len(selected_columns)

    # 欠損データがある行を削除
    cleaned_data = selected_columns.dropna()

    # 削除された行数を計算
    deleted_row_count = initial_row_count - len(cleaned_data)

    # 元のデータの行数と削除された行数を表示
    print(f"元のデータの行数: {initial_row_count}")
    print(f"削除された行数: {deleted_row_count}")
    print(f"現在の行数: {len(cleaned_data)}")

    # 出力ファイル名を生成 (元のファイル名に "_clean" を追加)
    base, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base}_clean{ext}"

    # 新しいファイルに保存
    cleaned_data.to_csv(output_file_path, index=False)

    print(f"クリーンアップされたデータを新しいファイルに保存しました: {output_file_path}")
    print("-" * 50)  


if __name__ == '__main__':
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='CSVファイルをクリーンアップして新しいファイルに保存します。')
    
    # 複数の入力ファイルを受け取るために `nargs='+'` を使用
    parser.add_argument('input_files', type=str, nargs='+', help='入力CSVファイルのパス（複数指定可能）')

    # 引数をパース
    args = parser.parse_args()

    # 複数のファイルパスをループで処理
    for input_file in args.input_files:
        clean_and_save_csv(input_file)

