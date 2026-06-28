# src/clock_util.py
from datetime import datetime
import time
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np


def draw_clock():
    """Jupyter Notebook上でリアルタイムに更新されるアナログ時計を描画します。

    停止するにはJupyterの「停止（■）」ボタンを押してください。
    """
    # 描画用のフィギュアと軸を設定
    fig, ax = plt.subplots(figsize=(4, 4))
    display_handle = display(fig, display_id=True)
    plt.close(fig)  # 重複表示を防ぐために一度クローズ

    try:
        while True:
            ax.clear()

            # 現在時刻を取得
            now = datetime.now()
            hour = now.hour % 12
            minute = now.minute
            second = now.second

            # 時計の外枠と目盛り
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_aspect("equal")
            ax.axis("off")

            # 文字盤の円
            circle = plt.Circle((0, 0), 1, fill=False, color="black", linewidth=2)
            ax.add_patch(circle)

            # 1〜12の文字盤
            for i in range(1, 13):
                angle = np.deg2rad(90 - i * 30)
                ax.text(
                    0.85 * np.cos(angle),
                    0.85 * np.sin(angle),
                    str(i),
                    ha="center",
                    va="center",
                    fontsize=12,
                    fontweight="bold",
                )

            # 各針の角度計算（12時方向を基準、時計回り）
            # 1秒 = 6度
            angle_sec = np.deg2rad(90 - second * 6)
            # 1分 = 6度 + 秒の補正
            angle_min = np.deg2rad(90 - (minute * 6 + second * 0.1))
            # 1時間 = 30度 + 分の補正
            angle_hour = np.deg2rad(90 - (hour * 30 + minute * 0.5))

            # 針の描画 (長さと太さを調整)
            # 時針 (短・太)
            ax.plot(
                [0, 0.5 * np.cos(angle_hour)],
                [0, 0.5 * np.sin(angle_hour)],
                color="black",
                linewidth=6,
                solid_capstyle="round",
            )
            # 分針 (長・中)
            ax.plot(
                [0, 0.75 * np.cos(angle_min)],
                [0, 0.75 * np.sin(angle_min)],
                color="black",
                linewidth=4,
                solid_capstyle="round",
            )
            # 秒針 (長・細・赤)
            ax.plot(
                [0, 0.85 * np.cos(angle_sec)],
                [0, 0.85 * np.sin(angle_sec)],
                color="red",
                linewidth=1.5,
            )

            # 中心点
            ax.plot(0, 0, "o", color="black", markersize=8)

            # タイトルにデジタル時刻も表示
            ax.set_title(
                now.strftime("%Y-%m-%d %H:%M:%S"), fontsize=14, fontname="monospace"
            )

            # Jupyterの同じセル出力を更新
            display_handle.update(fig)

            # 1秒待機
            time.sleep(1)

    except KeyboardInterrupt:
        # Jupyter上で停止ボタン（■）を押すと安全に終了します
        print("時計を停止しました。")
