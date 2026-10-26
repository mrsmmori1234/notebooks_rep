from datetime import datetime, date
from pathlib import Path
import calendar
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

def show_tracker():
    notebook_dir = Path.cwd()
    csv_file = notebook_dir.parent / "outputs" / "exercise.csv"
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    if not csv_file.exists():
        csv_file.write_text("Date,Exercise\n", encoding="utf-8")

    today_str = date.today().strftime("%Y-%m-%d")
    exercises = ["Stretching", "Plank Training", "Sqwat Training"]
    checkboxes = [widgets.Checkbox(value=False, description=ex) for ex in exercises]

    note_input = widgets.Text(layout=widgets.Layout(width='30px'))
    submit_btn = widgets.Button(description="✅ Log Today's Exercise", button_style="success")
    
    # 【解決策1】出力エリアの高さ制限をなくし、スクロールバーを出さずにすべて展開するレイアウト設定
    output_area = widgets.Output(layout=widgets.Layout(height='auto', overflow='visible'))

    def load_data():
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            if not df.empty and 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                return df
        return pd.DataFrame(columns=['Date', 'Exercise'])

    def calculate_streak(df):
        if df.empty:
            return 0
        unique_dates = sorted(df['Date'].dropna().unique(), reverse=True)
        if not unique_dates:
            return 0

        today = date.today()
        yesterday = today - pd.Timedelta(days=1).to_pytimedelta()

        if unique_dates[0] != today and unique_dates[0] != yesterday:
            return 0

        streak = 0
        expected = unique_dates[0]
        for d in unique_dates:
            if d == expected:
                streak += 1
                expected = expected - pd.Timedelta(days=1).to_pytimedelta()
            else:
                break
        return streak

    def on_submit(b):
        selected = [cb.description for cb in checkboxes if cb.value]
        if not selected:
            with output_area:
                clear_output(wait=True)
                print("⚠️ Please select at least one exercise!")
            return

        exercise_str = " / ".join(selected)
        note = note_input.value.strip()
        if note:
            exercise_str += f" ({note})"

        new_row = pd.DataFrame([[today_str, exercise_str]], columns=['Date', 'Exercise'])

        df = load_data()
        if not df.empty:
            df = df[df['Date'] != date.today()]

        df = pd.concat([df, new_row], ignore_index=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df.to_csv(csv_file, index=False)

        with output_area:
            clear_output(wait=True)
            streak = calculate_streak(df)
            print(f"🎉 Logged successfully! Great job!")
            print(f"🔥 Current Streak: {streak} days in a row!")
            display_calendar(df)

    def display_calendar(df=None):
        if df is None:
            df = load_data()

        completed_dates = set(df['Date'].dropna()) if not df.empty else set()

        # 現在の年・月を取得
        now = datetime.now()
        year, month = now.year, now.month

        # カレンダーの生成 (月曜始まり)
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]

        # HTMLテーブルの組み立て
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin-top: 15px; height: auto;">
            <h4 style="margin-bottom: 10px; color: #333;">📅 {month_name} {year} - Exercise Calendar</h4>
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
                    is_completed = target_date in completed_dates
                    
                    if is_completed:
                        bg_color = "#e6f4ea"  # 薄い緑
                        text_content = f"<b>{day}</b><br><span style='color: #137333; font-size: 11px; font-weight: bold;'>✅ 完了</span>"
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

    submit_btn.on_click(on_submit)

    # 【解決策1】メインのVBoxコンテナにも高さの自動調整を設定
    main_container = widgets.VBox([
        widgets.HTML(f"<h3>🏋️ Daily Exercise Check-in ({today_str})</h3>"),
        widgets.VBox(checkboxes),
        widgets.HBox([note_input, submit_btn]),
        output_area
    ], layout=widgets.Layout(height='auto', overflow='visible'))

    display(main_container)
    display_calendar()
