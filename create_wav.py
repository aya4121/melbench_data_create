import subprocess
import os
from pathlib import Path
import pandas as pd
import argparse


def download_clip(
    video_identifier,
    output_filename,
    start_time,
    end_time,
    num_attempts=5,
    url_base='https://www.youtube.com/watch?v='
):
    status = False

    command = f"""
        yt-dlp --quiet --force-keyframes-at-cuts --no-warnings -x --audio-format wav -f bestaudio -o "{output_filename}" --download-sections "*{start_time}-{end_time}" "{url_base}{video_identifier}"
    """.strip()

    attempts = 0
    while True:
        try:
            output = subprocess.check_output(command, shell=True,
                                             stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            attempts += 1
            if attempts == num_attempts:
                return status, err.output
        else:
            break

    # Check if the video was successfully saved.
    status = os.path.exists(output_filename)
    return status, 'Downloaded'


def main(csv_path, data_dir, batch_size):
    """
    CSVファイルからYouTube動画のクリップをバッチ処理でダウンロード。

    Args:
        csv_path: 動画ID、開始・終了時間が記載されたCSVファイルのパス。
        data_dir: クリップを保存するディレクトリ。
        batch_size: 1バッチあたりの動画の数
    """
    # CSVファイルからデータを読み込み
    df = pd.read_csv(csv_path)

    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True, parents=True)

    success_count = 0
    failure_count = 0

    # バッチ処理の開始
    for i in range(0, len(df), batch_size):
        batch = df[i:i + batch_size]

        # バッチ内の各行を処理
        results = []
        for _, row in batch.iterrows():
            outfile_path = str(data_dir / f"{row['youtube_video_id']}_{int(row['start_second'])}_{int(row['end_second'])}.wav")
            status = True
            if not os.path.exists(outfile_path):
                status, log = download_clip(
                    row['youtube_video_id'],
                    outfile_path,
                    row['start_second'],
                    row['end_second'],
                )

            if status:
                success_count += 1
            else:
                failure_count += 1

            results.append({
                "youtube_video_id": row['youtube_video_id'],
                "audio": outfile_path,
                "download_status": status
            })
        print(f"Batch {i // batch_size + 1} processed: {len(batch)} items")

    # 全体のダウンロード成功・失敗数を表示
    print(f"Download completed. {success_count} succeeded, {failure_count} failed.")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download YouTube clips based on a CSV file with batch processing.")

    parser.add_argument('--csv_path', type=str, required=True, help="CSVファイルのパス")
    parser.add_argument('--data_dir', type=str, required=True, help="音声クリップ保存先ディレクトリ")
    parser.add_argument('--batch_size', type=int, default=10, help="バッチ処理のサイズ（1回に処理する動画数）")

    args = parser.parse_args()

    main(
        csv_path=args.csv_path,
        data_dir=args.data_dir,
        batch_size=args.batch_size
    )












