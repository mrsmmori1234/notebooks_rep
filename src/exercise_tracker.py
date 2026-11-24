from datetime import datetime, date
from pathlib import Path
import calendar
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML


def _get_csv_file() -> Path:
    notebook_dir = Path.cwd()
    csv_file = notebook_dir.parent / "outputs" / "exercise.csv"
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    if not csv_file.exists():
        csv_file.write_text("Date,Exercise\n", encoding="utf-8")
    return csv_file


def load_data() -> pd.DataFrame:
    csv_file = _get_csv_file()
    if csv_file.exists():
        df = pd.read_csv(csv_file)
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            return df
    return pd.DataFrame(columns=["Date", "Exercise"])


def calculate_streak(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    unique_dates = sorted(df["Date"].dropna().unique(), reverse=True)
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


# セル間連携用の共有エリア
_calendar_output = widgets.Output(layout=widgets.Layout(height="auto", overflow="visible"))


def render_calendar(df: pd.DataFrame | None = None) -> None:
    if df is None:
        df = load_data()

    completed_dates = set(df["Date"].dropna()) if not df.empty else set()
    streak = calculate_streak(df)

    now = datetime.now()
    year, month = now.year, now.month

    # 日曜始まり (0=Mon ... 6=Sun なので SUNDAY=6 を指定)
    sun_cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    cal = sun_cal.monthdayscalendar(year, month)
    month_name = calendar.month_name[month]

    headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    th_html = "".join(
        f'<th style="padding: 8px; border: 1px solid #ddd;">{h}</th>' for h in headers
    )

    rows_html = ""
    for week in cal:
        rows_html += "<tr>"
        for day in week:
            if day == 0:
                rows_html += (
                    '<td style="padding: 10px; border: 1px solid #ddd; '
                    'background-color: #fafafa;"></td>'
                )
            else:
                target_date = date(year, month, day)
                is_completed = target_date in completed_dates

                if is_completed:
                    bg_color = "#e6f4ea"
                    text_content = (
                        f"<b>{day}</b><br>"
                        f"<span style='color: #137333; font-size: 11px; font-weight: bold;'>"
                        f"✅ Completed</span>"
                    )
                else:
                    bg_color = "#ffffff"
                    text_content = f"<span style='color: #888;'>{day}</span>"

                rows_html += (
                    f'<td style="padding: 10px; border: 1px solid #ddd; '
                    f'background-color: {bg_color}; height: 55px; vertical-align: top;">'
                    f"{text_content}</td>"
                )
        rows_html += "</tr>"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin-top: 10px; height: auto;">
        <h4 style="margin-bottom: 6px; color: #333;">📅 {month_name} {year} - Exercise Calendar</h4>
        <div style="margin-bottom: 10px; font-size: 14px; color: #444;">
            🔥 Current Streak: <b>{streak}</b> days in a row
        </div>
        <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 14px;">
            <thead>
                <tr style="background-color: #f2f2f2; color: #555;">
                    {th_html}
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """

    with _calendar_output:
        clear_output(wait=True)
        display(HTML(html))


def show_calendar() -> None:
    render_calendar()
    display(_calendar_output)


def show_tracker() -> None:
    csv_file = _get_csv_file()
    today_str = date.today().strftime("%Y-%m-%d")
    exercises = ["Stretching", "Plunk Training", "Sqwat Training"]
    checkboxes = [widgets.Checkbox(value=False, description=ex) for ex in exercises]

    note_input = widgets.Text(
        placeholder="Note",
        layout=widgets.Layout(width="120px"),
    )
    submit_btn = widgets.Button(
        description="✅ Log Today's Exercise", button_style="success"
    )
    status_area = widgets.Output(layout=widgets.Layout(height="auto", overflow="visible"))

    def on_submit(b):
        selected = [cb.description for cb in checkboxes if cb.value]
        if not selected:
            with status_area:
                clear_output(wait=True)
                print("⚠️ Please select at least one exercise!")
            return

        exercise_str = " / ".join(selected)
        note = note_input.value.strip()
        if note:
            exercise_str += f" ({note})"

        new_row = pd.DataFrame([[today_str, exercise_str]], columns=["Date", "Exercise"])

        df = load_data()
        if not df.empty:
            df = df[df["Date"] != date.today()]

        df = pd.concat([df, new_row], ignore_index=True)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df.to_csv(csv_file, index=False)

        with status_area:
            clear_output(wait=True)
            print("🎉 Logged successfully! Great job!")

        # 別セルに表示されているカレンダーも更新
        render_calendar(df)

    submit_btn.on_click(on_submit)

    main_container = widgets.VBox(
        [
            widgets.HTML(f"<h3>🏋️ Daily Exercise Check-in ({today_str})</h3>"),
            widgets.VBox(checkboxes),
            widgets.HBox([note_input, submit_btn]),
            status_area,
        ],
        layout=widgets.Layout(height="auto", overflow="visible"),
    )

    display(main_container)
