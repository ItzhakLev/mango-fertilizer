"""
אפליקציית ניהול דישון למטע מנגו
Mango Orchard Fertilization Management System

מפותח עם Streamlit ו-Pandas
נתונים נשמרים בקבצי CSV מקומיים
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# =============================================================================
# הגדרות עמוד ו-RTL
# =============================================================================
st.set_page_config(
    page_title="ניהול דישון - מטע מנגו",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS מותאם לעברית ו-RTL - עיצוב טבעי/חקלאי
st.markdown("""
<style>
    /* ייבוא גופן */
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');

    /* רקע כללי - גרדיאנט טבעי */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 25%, #fff8e1 50%, #f1f8e9 75%, #e8f5e9 100%);
        background-attachment: fixed;
    }

    /* הגדרת RTL ופונט לכל האפליקציה */
    .main, .block-container {
        direction: rtl;
        text-align: right;
    }

    /* פונט Calibri */
    * {
        font-family: 'Calibri', 'Assistant', 'Arial', sans-serif !important;
    }

    /* כותרות */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right;
        color: #2e7d32 !important;
        font-weight: 700 !important;
    }

    h1 {
        background: linear-gradient(90deg, #1b5e20, #4caf50, #81c784);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
    }

    /* טבלאות */
    .dataframe {
        direction: rtl;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px;
    }

    /* כפתורים - סגנון טבעי */
    .stButton > button {
        width: 100%;
        direction: rtl;
        background: linear-gradient(135deg, #4caf50 0%, #81c784 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #388e3c 0%, #66bb6a 100%) !important;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* כפתור שמירה ירוק גדול */
    .big-save-button > button {
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 50%, #81c784 100%) !important;
        color: white !important;
        font-size: 24px !important;
        padding: 20px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 8px 25px rgba(46, 125, 50, 0.4) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }

    .big-save-button > button:hover {
        background: linear-gradient(135deg, #1b5e20 0%, #388e3c 50%, #66bb6a 100%) !important;
        box-shadow: 0 10px 30px rgba(46, 125, 50, 0.5) !important;
        transform: translateY(-3px) !important;
    }

    /* קלטים - סגנון טבעי */
    .stSelectbox, .stNumberInput, .stDateInput {
        direction: rtl;
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #a5d6a7 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #4caf50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3) !important;
    }

    /* מטריקות */
    [data-testid="stMetricValue"] {
        direction: ltr;
        color: #2e7d32 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #558b2f !important;
    }

    /* Tabs - סגנון טבעי */
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        direction: rtl;
        background-color: transparent !important;
        border-radius: 15px !important;
        color: #2e7d32 !important;
        font-weight: 600 !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4caf50, #81c784) !important;
        color: white !important;
    }

    /* הודעות הצלחה */
    .success-message {
        background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
        border: 2px solid #4caf50;
        color: #1b5e20;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }

    /* כרטיסי מטריקה */
    .metric-card {
        background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
        padding: 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }

    /* פס התקדמות */
    .progress-container {
        background-color: rgba(200, 230, 201, 0.5);
        border-radius: 15px;
        padding: 4px;
        margin: 10px 0;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }

    .progress-bar {
        height: 28px;
        border-radius: 12px;
        text-align: center;
        line-height: 28px;
        color: white;
        font-weight: bold;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    /* קווים מפרידים */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a5d6a7, #4caf50, #a5d6a7, transparent);
        margin: 25px 0;
    }

    /* הודעות מערכת */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
    }

    /* Info boxes */
    [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border-right: 4px solid #4caf50 !important;
    }

    /* Data editor */
    [data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Warning boxes */
    .stWarning {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2) !important;
        border-right: 4px solid #ff9800 !important;
        border-radius: 15px !important;
    }

    /* Footer */
    footer {
        background-color: transparent !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #e8f5e9;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #81c784, #4caf50);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #66bb6a, #388e3c);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# נתיבי קבצים
# =============================================================================
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_FILE = os.path.join(DATA_DIR, "plots.csv")
FERTILIZERS_FILE = os.path.join(DATA_DIR, "fertilizers.csv")
LOGS_FILE = os.path.join(DATA_DIR, "logs.csv")

# =============================================================================
# פונקציות עזר לניהול נתונים
# =============================================================================

def init_csv_files():
    """
    יצירת קבצי CSV עם נתוני דוגמה אם לא קיימים
    נקרא בהרצה ראשונה של האפליקציה
    """

    # יצירת plots.csv
    if not os.path.exists(PLOTS_FILE):
        plots_data = {
            'plot_id': [1, 2, 3],
            'plot_name': ['חלקה א - צפון', 'חלקה ב - דרום', 'חלקה ג - מרכז'],
            'size_dunam': [10.0, 15.0, 8.0],
            'target_n': [50.0, 60.0, 45.0],  # יעד חנקן לדונם
            'target_p': [20.0, 25.0, 18.0],  # יעד זרחן לדונם
            'target_k': [80.0, 90.0, 70.0],  # יעד אשלגן לדונם
            'target_c': [30.0, 35.0, 25.0]   # יעד פחמן לדונם
        }
        pd.DataFrame(plots_data).to_csv(PLOTS_FILE, index=False, encoding='utf-8-sig')

    # יצירת fertilizers.csv
    if not os.path.exists(FERTILIZERS_FILE):
        fert_data = {
            'fert_id': [1, 2, 3, 4, 5],
            'fert_name': ['אוריאה 46%', 'סופר פוספט', 'אשלגן כלורי', 'NPK 20-20-20', 'קומפוסט'],
            'n_percent': [46.0, 0.0, 0.0, 20.0, 2.0],
            'p_percent': [0.0, 20.0, 0.0, 20.0, 1.0],
            'k_percent': [0.0, 0.0, 60.0, 20.0, 1.5],
            'c_percent': [0.0, 0.0, 0.0, 0.0, 25.0]
        }
        pd.DataFrame(fert_data).to_csv(FERTILIZERS_FILE, index=False, encoding='utf-8-sig')

    # יצירת logs.csv
    if not os.path.exists(LOGS_FILE):
        logs_data = {
            'log_id': [],
            'date': [],
            'plot_name': [],
            'fert_name': [],
            'amount_kg': [],
            'created_at': []
        }
        pd.DataFrame(logs_data).to_csv(LOGS_FILE, index=False, encoding='utf-8-sig')


def load_plots():
    """טעינת נתוני חלקות"""
    try:
        return pd.read_csv(PLOTS_FILE, encoding='utf-8-sig')
    except Exception as e:
        st.error(f"שגיאה בטעינת חלקות: {e}")
        return pd.DataFrame()


def load_fertilizers():
    """טעינת נתוני דשנים"""
    try:
        return pd.read_csv(FERTILIZERS_FILE, encoding='utf-8-sig')
    except Exception as e:
        st.error(f"שגיאה בטעינת דשנים: {e}")
        return pd.DataFrame()


def load_logs():
    """טעינת יומן דישון"""
    try:
        df = pd.read_csv(LOGS_FILE, encoding='utf-8-sig')
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת יומן: {e}")
        return pd.DataFrame()


def save_plots(df):
    """שמירת נתוני חלקות"""
    df.to_csv(PLOTS_FILE, index=False, encoding='utf-8-sig')


def save_fertilizers(df):
    """שמירת נתוני דשנים"""
    df.to_csv(FERTILIZERS_FILE, index=False, encoding='utf-8-sig')


def save_log_entry(log_date, plot_name, fert_name, amount_kg):
    """
    שמירת רשומת דישון חדשה ליומן
    מחזיר True אם השמירה הצליחה
    """
    try:
        logs_df = load_logs()

        # יצירת ID חדש
        new_id = 1 if logs_df.empty else logs_df['log_id'].max() + 1

        # יצירת רשומה חדשה
        new_entry = pd.DataFrame({
            'log_id': [new_id],
            'date': [log_date],
            'plot_name': [plot_name],
            'fert_name': [fert_name],
            'amount_kg': [amount_kg],
            'created_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })

        # הוספה לקובץ
        updated_logs = pd.concat([logs_df, new_entry], ignore_index=True)
        updated_logs.to_csv(LOGS_FILE, index=False, encoding='utf-8-sig')

        return True
    except Exception as e:
        st.error(f"שגיאה בשמירה: {e}")
        return False


# =============================================================================
# אתחול קבצי נתונים
# =============================================================================
init_csv_files()

# =============================================================================
# ממשק המשתמש הראשי
# =============================================================================

# כותרת ראשית
st.markdown("# 🥭 ניהול דישון - מטע מנגו")
st.markdown("---")

# יצירת טאבים
tab1, tab2, tab3 = st.tabs(["📝 דיווח דישון", "📊 מצב חלקה", "⚙️ ניהול הגדרות"])

# =============================================================================
# טאב 1: דיווח דישון (Field Worker)
# =============================================================================
with tab1:
    st.markdown("## 📝 דיווח דישון חדש")
    st.markdown("#### מלא את הפרטים ולחץ על שמור")

    # טעינת נתונים לתפריטים נפתחים
    plots_df = load_plots()
    ferts_df = load_fertilizers()

    # בדיקה שיש נתונים
    if plots_df.empty or ferts_df.empty:
        st.error("❌ חסרים נתוני חלקות או דשנים. עבור ללשונית 'ניהול הגדרות' להוספת נתונים.")
    else:
        # יצירת טופס קלט
        col1, col2 = st.columns(2)

        with col1:
            # בחירת תאריך (ברירת מחדל: היום)
            selected_date = st.date_input(
                "📅 תאריך",
                value=date.today(),
                format="DD/MM/YYYY"
            )

            # בחירת חלקה
            plot_names = plots_df['plot_name'].tolist()
            selected_plot = st.selectbox(
                "🌳 בחר חלקה",
                options=plot_names,
                index=0
            )

        with col2:
            # בחירת דשן
            fert_names = ferts_df['fert_name'].tolist()
            selected_fert = st.selectbox(
                "🧪 בחר דשן",
                options=fert_names,
                index=0
            )

            # כמות בק"ג
            amount = st.number_input(
                "⚖️ כמות (ק\"ג)",
                min_value=0.0,
                max_value=10000.0,
                value=0.0,
                step=0.5
            )

        # רווח
        st.markdown("<br>", unsafe_allow_html=True)

        # כפתור שמירה גדול וירוק
        st.markdown('<div class="big-save-button">', unsafe_allow_html=True)
        save_clicked = st.button("💾 שמור דיווח", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

        # לוגיקת שמירה
        if save_clicked:
            # בדיקת תקינות - מניעת כמות 0
            if amount <= 0:
                st.error("❌ שגיאה: יש להזין כמות גדולה מ-0")
            else:
                # שמירת הנתונים
                success = save_log_entry(selected_date, selected_plot, selected_fert, amount)

                if success:
                    # הצגת הודעת הצלחה עם קונפטי
                    st.balloons()
                    st.markdown("""
                    <div class="success-message">
                        ✅ הדיווח נשמר בהצלחה!
                    </div>
                    """, unsafe_allow_html=True)

                    # הצגת סיכום
                    st.info(f"""
                    **סיכום הדיווח:**
                    - תאריך: {selected_date.strftime('%d/%m/%Y')}
                    - חלקה: {selected_plot}
                    - דשן: {selected_fert}
                    - כמות: {amount} ק"ג
                    """)

# =============================================================================
# טאב 2: מצב חלקה (Dashboard)
# =============================================================================
with tab2:
    st.markdown("## 📊 מצב חלקה - דשבורד")

    # טעינת נתונים
    plots_df = load_plots()
    ferts_df = load_fertilizers()
    logs_df = load_logs()

    if plots_df.empty:
        st.warning("אין נתוני חלקות. עבור ללשונית 'ניהול הגדרות' להוספת חלקות.")
    else:
        # בחירת חלקה לתצוגה
        selected_plot_dashboard = st.selectbox(
            "🌳 בחר חלקה לצפייה",
            options=plots_df['plot_name'].tolist(),
            key="dashboard_plot"
        )

        st.markdown("---")

        # קבלת נתוני החלקה הנבחרת
        plot_info = plots_df[plots_df['plot_name'] == selected_plot_dashboard].iloc[0]
        plot_size = plot_info['size_dunam']

        # סינון יומן לחלקה הנבחרת
        plot_logs = logs_df[logs_df['plot_name'] == selected_plot_dashboard]

        if plot_logs.empty:
            st.info(f"📭 אין עדיין דיווחי דישון לחלקה '{selected_plot_dashboard}'")

            # הצגת יעדים בלבד
            st.markdown("### 🎯 יעדי דישון לדונם")
            cols = st.columns(4)
            with cols[0]:
                st.metric("חנקן (N)", f"{plot_info['target_n']:.1f} ק\"ג")
            with cols[1]:
                st.metric("זרחן (P)", f"{plot_info['target_p']:.1f} ק\"ג")
            with cols[2]:
                st.metric("אשלגן (K)", f"{plot_info['target_k']:.1f} ק\"ג")
            with cols[3]:
                st.metric("פחמן (C)", f"{plot_info['target_c']:.1f} ק\"ג")
        else:
            # מיזוג יומן עם נתוני דשנים
            merged = plot_logs.merge(ferts_df, left_on='fert_name', right_on='fert_name', how='left')

            # חישוב כמויות יסודות בפועל
            # הנוסחה: כמות_ק"ג * (אחוז / 100)
            merged['actual_n'] = merged['amount_kg'] * (merged['n_percent'] / 100)
            merged['actual_p'] = merged['amount_kg'] * (merged['p_percent'] / 100)
            merged['actual_k'] = merged['amount_kg'] * (merged['k_percent'] / 100)
            merged['actual_c'] = merged['amount_kg'] * (merged['c_percent'] / 100)

            # סיכום כמויות
            total_n = merged['actual_n'].sum()
            total_p = merged['actual_p'].sum()
            total_k = merged['actual_k'].sum()
            total_c = merged['actual_c'].sum()

            # נרמול לפי גודל החלקה (לדונם)
            n_per_dunam = total_n / plot_size
            p_per_dunam = total_p / plot_size
            k_per_dunam = total_k / plot_size
            c_per_dunam = total_c / plot_size

            # יעדים
            target_n = plot_info['target_n']
            target_p = plot_info['target_p']
            target_k = plot_info['target_k']
            target_c = plot_info['target_c']

            # חישוב אחוזי התקדמות
            pct_n = min((n_per_dunam / target_n * 100) if target_n > 0 else 0, 150)
            pct_p = min((p_per_dunam / target_p * 100) if target_p > 0 else 0, 150)
            pct_k = min((k_per_dunam / target_k * 100) if target_k > 0 else 0, 150)
            pct_c = min((c_per_dunam / target_c * 100) if target_c > 0 else 0, 150)

            # הצגת מטריקות
            st.markdown(f"### 📈 סטטוס דישון - {selected_plot_dashboard}")
            st.markdown(f"**גודל החלקה:** {plot_size} דונם")

            # כרטיסי מטריקה
            cols = st.columns(4)

            elements = [
                ("חנקן (N)", n_per_dunam, target_n, pct_n, "#28a745"),
                ("זרחן (P)", p_per_dunam, target_p, pct_p, "#007bff"),
                ("אשלגן (K)", k_per_dunam, target_k, pct_k, "#fd7e14"),
                ("פחמן (C)", c_per_dunam, target_c, pct_c, "#6f42c1")
            ]

            for i, (name, actual, target, pct, color) in enumerate(elements):
                with cols[i]:
                    delta = actual - target
                    delta_str = f"{delta:+.1f}"
                    st.metric(
                        label=name,
                        value=f"{actual:.1f} ק\"ג/דונם",
                        delta=f"{delta_str} מהיעד ({target:.1f})"
                    )

                    # פס התקדמות
                    bar_color = color if pct <= 100 else "#dc3545"
                    bar_width = min(pct, 100)
                    st.markdown(f"""
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {bar_width}%; background-color: {bar_color};">
                            {pct:.0f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # גרף עמודות - בפועל מול יעד
            st.markdown("### 📊 השוואת בפועל מול יעד")

            chart_data = pd.DataFrame({
                'יסוד': ['חנקן (N)', 'זרחן (P)', 'אשלגן (K)', 'פחמן (C)'],
                'בפועל': [n_per_dunam, p_per_dunam, k_per_dunam, c_per_dunam],
                'יעד': [target_n, target_p, target_k, target_c]
            })

            st.bar_chart(chart_data.set_index('יסוד'))

            st.markdown("---")

            # טבלת דיווחים אחרונים
            st.markdown("### 📋 דיווחים אחרונים")

            display_logs = plot_logs[['date', 'fert_name', 'amount_kg', 'created_at']].copy()
            display_logs.columns = ['תאריך', 'דשן', 'כמות (ק"ג)', 'נוצר ב']
            display_logs = display_logs.sort_values('תאריך', ascending=False).head(10)

            st.dataframe(display_logs, use_container_width=True, hide_index=True)

# =============================================================================
# טאב 3: ניהול הגדרות (Admin)
# =============================================================================
with tab3:
    st.markdown("## ⚙️ ניהול הגדרות")
    st.markdown("#### עריכה ישירה של נתוני המערכת")

    st.warning("⚠️ שים לב: שינויים כאן משפיעים על כל המערכת. ערוך בזהירות!")

    # ניהול חלקות
    st.markdown("### 🌳 ניהול חלקות")
    st.markdown("ערוך, הוסף או מחק חלקות:")

    plots_df = load_plots()

    edited_plots = st.data_editor(
        plots_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "plot_id": st.column_config.NumberColumn("מזהה", disabled=True),
            "plot_name": st.column_config.TextColumn("שם חלקה", required=True),
            "size_dunam": st.column_config.NumberColumn("גודל (דונם)", min_value=0.1, required=True),
            "target_n": st.column_config.NumberColumn("יעד חנקן N", min_value=0),
            "target_p": st.column_config.NumberColumn("יעד זרחן P", min_value=0),
            "target_k": st.column_config.NumberColumn("יעד אשלגן K", min_value=0),
            "target_c": st.column_config.NumberColumn("יעד פחמן C", min_value=0),
        },
        hide_index=True,
        key="plots_editor"
    )

    if st.button("💾 שמור שינויים בחלקות", type="primary"):
        # עדכון מזהים לשורות חדשות
        if edited_plots['plot_id'].isna().any():
            max_id = edited_plots['plot_id'].max()
            max_id = 0 if pd.isna(max_id) else max_id
            for idx in edited_plots[edited_plots['plot_id'].isna()].index:
                max_id += 1
                edited_plots.loc[idx, 'plot_id'] = max_id

        save_plots(edited_plots)
        st.success("✅ חלקות נשמרו בהצלחה!")
        st.rerun()

    st.markdown("---")

    # ניהול דשנים
    st.markdown("### 🧪 ניהול דשנים")
    st.markdown("ערוך, הוסף או מחק דשנים:")

    ferts_df = load_fertilizers()

    edited_ferts = st.data_editor(
        ferts_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "fert_id": st.column_config.NumberColumn("מזהה", disabled=True),
            "fert_name": st.column_config.TextColumn("שם דשן", required=True),
            "n_percent": st.column_config.NumberColumn("% חנקן N", min_value=0, max_value=100),
            "p_percent": st.column_config.NumberColumn("% זרחן P", min_value=0, max_value=100),
            "k_percent": st.column_config.NumberColumn("% אשלגן K", min_value=0, max_value=100),
            "c_percent": st.column_config.NumberColumn("% פחמן C", min_value=0, max_value=100),
        },
        hide_index=True,
        key="ferts_editor"
    )

    if st.button("💾 שמור שינויים בדשנים", type="primary"):
        # עדכון מזהים לשורות חדשות
        if edited_ferts['fert_id'].isna().any():
            max_id = edited_ferts['fert_id'].max()
            max_id = 0 if pd.isna(max_id) else max_id
            for idx in edited_ferts[edited_ferts['fert_id'].isna()].index:
                max_id += 1
                edited_ferts.loc[idx, 'fert_id'] = max_id

        save_fertilizers(edited_ferts)
        st.success("✅ דשנים נשמרו בהצלחה!")
        st.rerun()

    st.markdown("---")

    # צפייה ביומן (קריאה בלבד עם אפשרות מחיקה)
    st.markdown("### 📋 יומן דישון")
    st.markdown("צפייה בכל הדיווחים:")

    logs_df = load_logs()

    if logs_df.empty:
        st.info("📭 היומן ריק - אין דיווחים עדיין")
    else:
        # אפשרות למחיקת רשומות
        logs_display = logs_df.copy()
        logs_display.columns = ['מזהה', 'תאריך', 'חלקה', 'דשן', 'כמות (ק"ג)', 'נוצר ב']

        st.dataframe(logs_display, use_container_width=True, hide_index=True)

        # מחיקת רשומה ספציפית
        st.markdown("#### 🗑️ מחיקת רשומה")
        col1, col2 = st.columns([3, 1])
        with col1:
            delete_id = st.number_input(
                "הזן מזהה רשומה למחיקה",
                min_value=1,
                max_value=int(logs_df['log_id'].max()) if not logs_df.empty else 1,
                step=1
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ מחק", type="secondary"):
                logs_df = logs_df[logs_df['log_id'] != delete_id]
                logs_df.to_csv(LOGS_FILE, index=False, encoding='utf-8-sig')
                st.success(f"✅ רשומה {delete_id} נמחקה!")
                st.rerun()

# =============================================================================
# פוטר
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>🥭 מערכת ניהול דישון | גרסה 1.0</div>",
    unsafe_allow_html=True
)
