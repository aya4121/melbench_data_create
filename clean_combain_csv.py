import os
import pandas as pd
import argparse

def combine_and_clean_csv_files(input_directory, output_file):
    """
    指定されたフォルダ内の '_clean.csv' で終わるファイルをすべて結合し、
    動画IDを抽出し、完全一致の重複を削除した新しいCSVファイルとして保存する関数。

    Args:
        input_directory (str): CSVファイルが保存されているフォルダのパス
        output_file (str): 結合後のクリーンなCSVファイルの保存先パス
    """
    
    # DataFrameを保存するリスト
    dfs = []
    file_count = 0  # 結合されたファイル数をカウント

    # フォルダ内のすべてのファイルをループ
    for filename in os.listdir(input_directory):
        if filename.endswith("_clean.csv"):  # "_clean.csv"で終わるファイルのみ対象
            filepath = os.path.join(input_directory, filename)
            # CSVファイルをDataFrameとして読み込む
            df = pd.read_csv(filepath)
            # DataFrameをリストに追加
            dfs.append(df)
            file_count += 1  # ファイルカウントを増やす
    
    # ファイルが見つからなかった場合の処理
    if file_count == 0:
        print("結合するファイルが見つかりませんでした。")
        return

    # すべてのDataFrameを結合
    combined_df = pd.concat(dfs, ignore_index=True)

    # 動画IDのみを抽出し、youtube_video_id列を更新
    combined_df['youtube_video_id'] = combined_df['youtube_video_id'].str.extract(r'youtu\.be/([^?]+)')

    # 重複を取り除く前の行数
    initial_count = len(combined_df)

    # 完全一致の重複を削除し、最初の1つだけを残す
    cleaned_df = combined_df.drop_duplicates(subset=['youtube_video_id', 'start_second', 'end_second'], keep='first')

    # 重複を取り除いた後の行数
    final_count = len(cleaned_df)
    removed_count = initial_count - final_count

    # 新しいCSVファイルに保存
    cleaned_df.to_csv(output_file, index=False)

    # 結合されたファイル数、行数、重複削除情報を表示
    print(f"結合されたファイル数: {file_count}")
    print(f"元のCSVの行数: {initial_count}")
    print(f"重複により削除された行数: {removed_count}")
    print(f"クリーンアップされたCSVファイルが {output_file} に保存されました。")


if __name__ == '__main__':
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='指定したフォルダ内の"_clean.csv"で終わるファイルを結合し、クリーンアップして新しいCSVファイルに保存します。')
    parser.add_argument('input_directory', type=str, help='入力フォルダのパス')
    parser.add_argument('output_file', type=str, help='クリーンアップされたCSVファイルの出力先パス')

    # 引数をパース
    args = parser.parse_args()

    # 関数を呼び出し
    combine_and_clean_csv_files(args.input_directory, args.output_file)

