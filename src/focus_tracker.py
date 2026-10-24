from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_focus_chart():
    # Graph style settings
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 4))

    # Relative path configuration (compatible with GitHub & any environment)
    notebook_dir = Path.cwd()
    csv_path = notebook_dir.parent / "outputs" / "focustime.csv"

    try:
        if not csv_path.exists():
            print(f"No focus time records found yet at: {csv_path}")
            return

        # Load CSV
        df = pd.read_csv(csv_path)
        
        if df.empty:
            print("No data available yet. Run the timer to create records!")
        else:
            # Convert Timestamp to date type
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            
            # Group and sum focus time by date (Minutes)
            daily_df = df.groupby('Date')['Minutes'].sum().reset_index()
            
            # Draw bar plot
            sns.barplot(
                data=daily_df, 
                x='Date', 
                y='Minutes', 
                hue='Date', 
                palette='Blues_d', 
                legend=False, 
                ax=ax
            )
            
            ax.set_title("Daily Focus Time Log", fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Total Minutes", fontsize=12)
            plt.xticks(rotation=45)
            
            # Display total focus time text box
            total_all_time = df['Minutes'].sum()
            total_hours = total_all_time / 60
            ax.text(
                0.02, 0.85, 
                f"Total Focus: {total_all_time} min ({total_hours:.1f} hours)", 
                transform=ax.transAxes, 
                fontsize=12, 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3)
            )
            
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"An error occurred while loading the CSV: {e}")
