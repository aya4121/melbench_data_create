import os
import argparse

def delete_files(directory):
    """
    指定されたディレクトリ内で、'temp'がファイル名に含まれるか、
    拡張子が'.wav'以外のファイルを削除する関数。

    Args:
        directory (str): 削除対象のディレクトリパス
    """
    # 削除したファイル数のカウンター
    deleted_count = 0

    # ディレクトリ内のファイルをリスト
    for filename in os.listdir(directory):
        # ファイルのフルパスを取得
        file_path = os.path.join(directory, filename)
        _, extension = os.path.splitext(filename)

        # "temp" が含まれているか、拡張子が ".wav" 以外のファイルを削除
        if 'temp' in filename or extension != '.wav':
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1  # 削除したファイル数をカウント
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    # 総削除ファイル数を表示
    print(f"Total files deleted: {deleted_count}")

if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="指定ディレクトリ内の不要なファイルを削除します。")
    parser.add_argument('directory', type=str, help='削除対象のディレクトリパス')

    # 引数をパース
    args = parser.parse_args()

    # 関数を実行
    if os.path.isdir(args.directory):
        delete_files(args.directory)
    else:
        print(f"指定されたディレクトリが存在しません: {args.directory}")


