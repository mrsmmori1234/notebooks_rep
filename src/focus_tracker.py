from datetime import datetime, date
from pathlib import Path
import calendar
import pandas as pd
from IPython.display import display, HTML

def show_focus_chart():
    notebook_dir = Path.cwd()
    csv_file = notebook_dir.parent / "outputs" / "focustime.csv"
    
    if not csv_file.exists():
        print(f"No focus time records found yet at: {csv_file}")
        return

    # データのロード
    df = pd.read_csv(csv_file)
    if df.empty or 'Timestamp' not in df.columns:
        print("No data available yet.")
        return

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date

    # 日ごとの合計分数を集計
    daily_sum = df.groupby('Date')['Minutes'].sum()
    daily_dict = daily_sum.to_dict()

    # 現在の年・月を取得
    now = datetime.now()
    year, month = now.year, now.month

    # カレンダーの生成 (月曜始まり)
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # HTMLテーブルの組み立て
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin-top: 15px; height: auto;">
        <h4 style="margin-bottom: 10px; color: #333;">⏱️ {month_name} {year} - Focus Time Calendar</h4>
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 14px;">
            <thead>
                <tr style="background-color: #f2f2f2; color: #555;">
                    <th style="padding: 8px; border: 1px solid #ddd;">Mon</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Tue</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Wed</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Thu</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Fri</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Sat</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Sun</th>
                </tr>
            </thead>
            <tbody>
    """

    for week in cal:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += '<td style="padding: 10px; border: 1px solid #ddd; background-color: #fafafa;"></td>'
            else:
                target_date = date(year, month, day)
                focus_mins = daily_dict.get(target_date, 0)
                
                if focus_mins > 0:
                    bg_color = "#e6f4ea"  # 薄い緑
                    text_content = f"<b>{day}</b><br><span style='color: #137333; font-size: 11px; font-weight: bold;'>{focus_mins} min</span>"
                else:
                    bg_color = "#ffffff"
                    text_content = f"<span style='color: #888;'>{day}</span>"

                html += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: {bg_color}; height: 55px; vertical-align: top;">{text_content}</td>'
        html += "</tr>"

    html += """
            </tbody>
        </table>
    </div>
    """
    
    display(HTML(html))
