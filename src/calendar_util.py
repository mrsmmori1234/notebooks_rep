# src/calendar_util.py
import calendar
from datetime import datetime
from IPython.display import HTML, display

# --------------------------------------------------------------------
# DEFINE MODERN CSS STYLING
# --------------------------------------------------------------------
HTML_STYLE = """
<style>
    .cal-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        background-color: #1e1e24;
        padding: 20px;
        border-radius: 12px;
    }
    .cal-box {
        background-color: #2a2a35;
        border-radius: 8px;
        padding: 15px;
        width: 260px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .cal-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 12px;
        border-bottom: 2px solid #3e3e50;
        padding-bottom: 6px;
    }
    .cal-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        text-align: center;
    }
    .day-header {
        color: #8e8e9f;
        font-size: 0.8rem;
        font-weight: bold;
        padding-bottom: 4px;
    }
    .day-cell {
        color: #e0e0e0;
        font-size: 0.9rem;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
    }
    .day-empty {
        height: 30px;
    }
    
    /* Neon Highlighting Variables */
    .today-highlight {
        background-color: #ff007f !important;
        color: #ffffff !important;
        font-weight: bold;
        box-shadow: 0 0 8px #ff007f;
    }
    .sg-highlight {
        background-color: rgba(0, 240, 255, 0.2);
        color: #00f0ff !important;
        font-weight: bold;
        border: 1px solid #00f0ff;
    }
    .jp-highlight {
        background-color: rgba(255, 235, 59, 0.15);
        color: #ffeb3b !important;
        font-weight: bold;
        border: 1px solid #ffeb3b;
    }
    .both-highlight {
        background-color: #7f1d1d;
        color: #fca5a5 !important;
        font-weight: bold;
        border: 1px solid #ef4444;
    }
    
    /* Legend Styles */
    .legend-container {
        display: flex;
        gap: 20px;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid #3e3e50;
        width: 100%;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #b0b0c0;
        font-size: 0.85rem;
    }
    .legend-badge {
        width: 16px;
        height: 16px;
        border-radius: 3px;
    }
</style>
"""


def display_holiday_calendar(months_to_show: int = 4):
    """シンガポールと日本の祝日をハイライトしたカレンダーをJupyter上に描画します。"""
    # 1. SETUP BASE DATE INFO
    today = datetime.now()
    base_year = today.year
    base_month = today.month
    current_day = today.day

    # 3. GENERATE CALENDAR PANELS
    cal = calendar.Calendar(calendar.SUNDAY)
    html_output = '<div class="cal-container">'

    for i in range(months_to_show):
        target_month = base_month + i
        target_year = base_year

        if target_month > 12:
            target_month -= 12
            target_year += 1

        active_sg = []
        active_jp = []

        # Dynamic package processing
        try:
            import holidays

            sg_package = holidays.country_holidays("SG", years=target_year)
            jp_package = holidays.country_holidays("JP", years=target_year)

            for date_obj in sg_package.keys():
                if date_obj.month == target_month:
                    active_sg.append(date_obj.day)
            for date_obj in jp_package.keys():
                if date_obj.month == target_month:
                    active_jp.append(date_obj.day)
        except (ImportError, Exception):
            sg_fallback = {
                1: [1, 30, 31],
                3: [29],
                4: [2],
                5: [1, 27],
                6: [15],
                8: [9, 10],
                11: [8],
                12: [25],
            }
            jp_fallback = {
                1: [1, 2, 3, 12],
                2: [11, 23],
                3: [21],
                4: [29],
                5: [3, 4, 5, 6],
                7: [20],
                8: [11],
                9: [21, 22, 23],
                10: [12],
                11: [3, 23],
                12: [31],
            }
            if target_year == base_year:
                active_sg = sg_fallback.get(target_month, [])
                active_jp = jp_fallback.get(target_month, [])

        month_name = calendar.month_name[target_month]

        # Start Calendar Box Component
        html_output += '<div class="cal-box">'
        html_output += (
            f'<div class="cal-title">{month_name.upper()} {target_year}</div>'
        )
        html_output += '<div class="cal-grid">'

        # Day Names Header Row
        for day_name in ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]:
            html_output += f'<div class="day-header">{day_name}</div>'

        weeks = cal.monthdayscalendar(target_year, target_month)
        for week in weeks:
            for day in week:
                if day == 0:
                    html_output += '<div class="day-empty"></div>'
                else:
                    is_today = (
                        day == current_day
                        and target_month == base_month
                        and target_year == base_year
                    )
                    is_sg = day in active_sg
                    is_jp = day in active_jp

                    # Determine structural highlight assignments
                    class_tag = "day-cell"
                    if is_today:
                        class_tag += " today-highlight"
                    elif is_sg and is_jp:
                        class_tag += " both-highlight"
                    elif is_sg:
                        class_tag += " sg-highlight"
                    elif is_jp:
                        class_tag += " jp-highlight"

                    html_output += f'<div class="{class_tag}">{day}</div>'

        html_output += "</div></div>"  # Close cal-grid and cal-box

    # Append Global Legend Component
    html_output += """
        <div class="legend-container">
            <div class="legend-item"><div class="legend-badge" style="background-color: #ff007f;"></div>Today</div>
            <div class="legend-item"><div class="legend-badge" style="background-color: rgba(0, 240, 255, 0.2); border: 1px solid #00f0ff;"></div>Singapore</div>
            <div class="legend-item"><div class="legend-badge" style="background-color: rgba(255, 235, 59, 0.15); border: 1px solid #ffeb3b;"></div>Japan</div>
            <div class="legend-item"><div class="legend-badge" style="background-color: #7f1d1d; border: 1px solid #ef4444;"></div>Overlap</div>
        </div>
    """
    html_output += "</div>"  # Close cal-container

    # Render structural DOM node back cleanly into Jupyter
    display(HTML(HTML_STYLE + html_output))
