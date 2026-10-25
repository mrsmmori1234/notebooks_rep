from datetime import datetime, date
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output

def show_tracker():
    notebook_dir = Path.cwd()
    csv_file = notebook_dir.parent / "outputs" / "exercise.csv"
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    if not csv_file.exists():
        csv_file.write_text("Date,Exercise\n", encoding="utf-8")

    today_str = date.today().strftime("%Y-%m-%d")
    exercises = ["9min Strength Training", "Plank Trainign", "sqwat training"]
    checkboxes = [widgets.Checkbox(value=False, description=ex) for ex in exercises]

    note_input = widgets.Text(placeholder="xxx", layout=widgets.Layout(width='300px'))
    submit_btn = widgets.Button(description="✅ Log Today's Exercise", button_style="success")
    output_area = widgets.Output()

    def load_data():
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        return pd.DataFrame(columns=['Date', 'Exercise'])

    def calculate_streak(df):
        if df.empty:
            return 0
        unique_dates = sorted(df['Date'].unique(), reverse=True)
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
        df = df[df['Date'] != date.today()]
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_file, index=False)
        
        with output_area:
            clear_output(wait=True)
            streak = calculate_streak(df)
            print(f"🎉 Logged successfully! Great job!")
            print(f"🔥 Current Streak: {streak} days in a row!")
            display_chart(df)

    def display_chart(df=None):
        if df is None:
            df = load_data()
        
        if df.empty:
            print("No logs found yet. Check your exercise above and log today's session!")
            return
            
        fig, ax = plt.subplots(figsize=(8, 3))
        df['Count'] = 1
        daily = df.groupby('Date')['Count'].sum().reset_index()
        
        sns.barplot(
            data=daily.tail(14), 
            x='Date', 
            y='Count', 
            hue='Date', 
            palette='Greens_d', 
            legend=False, 
            ax=ax
        )
        
        ax.set_title("Recent Exercise Streak (Last 14 Days)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Done", fontsize=10)
        ax.set_yticks([0, 1])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    submit_btn.on_click(on_submit)

    display(widgets.VBox([
        widgets.HTML(f"<h3>🏋️ Daily Exercise Check-in ({today_str})</h3>"),
        widgets.VBox(checkboxes),
        widgets.HBox([note_input, submit_btn]),
        output_area
    ]))

    display_chart()
