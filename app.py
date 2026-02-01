"""
אפליקציית ניהול דישון למטע מנגו - גרסה 3.0
Mango Orchard Fertilization Management System

גרסה זו שומרת נתונים ב-Google Sheets לאחסון קבוע ומאובטח
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import io
import json
import gspread
from google.oauth2.service_account import Credentials

# =============================================================================
# הגדרות עמוד ו-RTL
# =============================================================================
st.set_page_config(
    page_title="ניהול דישון - מטע מנגו",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# סיסמת מנהל (שנה לסיסמה שלך!)
# =============================================================================
ADMIN_PASSWORD = "mango2024"

# =============================================================================
# CSS מותאם לעברית ו-RTL - עיצוב טבעי/חקלאי
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 25%, #fff8e1 50%, #f1f8e9 75%, #e8f5e9 100%);
        background-attachment: fixed;
    }

    .main, .block-container {
        direction: rtl;
        text-align: right;
    }

    * {
        font-family: 'Calibri', 'Assistant', 'Arial', sans-serif !important;
    }

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

    .dataframe {
        direction: rtl;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px;
    }

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

    .delete-button > button {
        background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%) !important;
    }

    .delete-button > button:hover {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%) !important;
    }

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

    [data-testid="stMetricValue"] {
        direction: ltr;
        color: #2e7d32 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #558b2f !important;
    }

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

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a5d6a7, #4caf50, #a5d6a7, transparent);
        margin: 25px 0;
    }

    .stAlert {
        border-radius: 15px !important;
        border: none !important;
    }

    [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border-right: 4px solid #4caf50 !important;
    }

    [data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .stWarning {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2) !important;
        border-right: 4px solid #ff9800 !important;
        border-radius: 15px !important;
    }

    footer {
        background-color: transparent !important;
    }

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

    @media (max-width: 768px) {
        h1 {
            font-size: 1.8rem !important;
        }
        .big-save-button > button {
            font-size: 18px !important;
            padding: 15px 20px !important;
        }
    }

    .connection-status {
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-weight: 600;
    }

    .connected {
        background: linear-gradient(135deg, #c8e6c9, #a5d6a7);
        color: #1b5e20;
    }

    .disconnected {
        background: linear-gradient(135deg, #ffcdd2, #ef9a9a);
        color: #b71c1c;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# אתחול Session State
# =============================================================================
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'delete_confirm' not in st.session_state:
    st.session_state.delete_confirm = None
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0
if 'gsheet_client' not in st.session_state:
    st.session_state.gsheet_client = None

# =============================================================================
# פונקציות Google Sheets
# =============================================================================

@st.cache_resource
def get_google_client():
    """יצירת חיבור ל-Google Sheets"""
    try:
        # קריאת credentials מ-Streamlit Secrets
        # תומך בשתי שיטות: JSON כמחרוזת או כ-TOML section

        if "gcp_service_account_json" in st.secrets:
            # שיטה 1: JSON כמחרוזת (מומלץ)
            credentials_dict = json.loads(st.secrets["gcp_service_account_json"])
        elif "gcp_service_account" in st.secrets:
            # שיטה 2: TOML section
            credentials_dict = dict(st.secrets["gcp_service_account"])
        else:
            st.error("חסרים פרטי התחברות ל-Google Sheets")
            return None

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=scopes
        )

        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"שגיאה בחיבור ל-Google Sheets: {e}")
        return None


def get_spreadsheet():
    """קבלת הגיליון"""
    try:
        client = get_google_client()
        if client is None:
            return None

        spreadsheet_url = st.secrets["spreadsheet_url"]
        spreadsheet = client.open_by_url(spreadsheet_url)
        return spreadsheet
    except Exception as e:
        st.error(f"שגיאה בפתיחת הגיליון: {e}")
        return None


def init_sheets():
    """אתחול גיליונות עם נתוני דוגמה אם ריקים"""
    try:
        spreadsheet = get_spreadsheet()
        if spreadsheet is None:
            return False

        # בדיקה ויצירת גיליון חלקות
        try:
            plots_sheet = spreadsheet.worksheet("plots")
            if plots_sheet.row_count <= 1:
                raise Exception("Empty sheet")
        except:
            try:
                plots_sheet = spreadsheet.add_worksheet(title="plots", rows=100, cols=10)
            except:
                plots_sheet = spreadsheet.worksheet("plots")

            plots_data = [
                ['plot_id', 'plot_name', 'size_dunam', 'target_n', 'target_p', 'target_k', 'target_c'],
                [1, 'חלקה א - צפון', 10.0, 50.0, 20.0, 80.0, 30.0],
                [2, 'חלקה ב - דרום', 15.0, 60.0, 25.0, 90.0, 35.0],
                [3, 'חלקה ג - מרכז', 8.0, 45.0, 18.0, 70.0, 25.0]
            ]
            plots_sheet.clear()
            plots_sheet.update('A1', plots_data)

        # בדיקה ויצירת גיליון דשנים
        try:
            ferts_sheet = spreadsheet.worksheet("fertilizers")
            if ferts_sheet.row_count <= 1:
                raise Exception("Empty sheet")
        except:
            try:
                ferts_sheet = spreadsheet.add_worksheet(title="fertilizers", rows=100, cols=10)
            except:
                ferts_sheet = spreadsheet.worksheet("fertilizers")

            ferts_data = [
                ['fert_id', 'fert_name', 'n_percent', 'p_percent', 'k_percent', 'c_percent'],
                [1, 'אוריאה 46%', 46.0, 0.0, 0.0, 0.0],
                [2, 'סופר פוספט', 0.0, 20.0, 0.0, 0.0],
                [3, 'אשלגן כלורי', 0.0, 0.0, 60.0, 0.0],
                [4, 'NPK 20-20-20', 20.0, 20.0, 20.0, 0.0],
                [5, 'קומפוסט', 2.0, 1.0, 1.5, 25.0]
            ]
            ferts_sheet.clear()
            ferts_sheet.update('A1', ferts_data)

        # בדיקה ויצירת גיליון יומן
        try:
            logs_sheet = spreadsheet.worksheet("logs")
        except:
            logs_sheet = spreadsheet.add_worksheet(title="logs", rows=1000, cols=10)
            logs_data = [['log_id', 'date', 'plot_name', 'fert_name', 'amount_kg', 'created_at']]
            logs_sheet.update('A1', logs_data)

        return True
    except Exception as e:
        st.error(f"שגיאה באתחול: {e}")
        return False


@st.cache_data(ttl=30)
def load_plots():
    """טעינת נתוני חלקות"""
    try:
        spreadsheet = get_spreadsheet()
        if spreadsheet is None:
            return pd.DataFrame()

        sheet = spreadsheet.worksheet("plots")
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"שגיאה בטעינת חלקות: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=30)
def load_fertilizers():
    """טעינת נתוני דשנים"""
    try:
        spreadsheet = get_spreadsheet()
        if spreadsheet is None:
            return pd.DataFrame()

        sheet = spreadsheet.worksheet("fertilizers")
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"שגיאה בטעינת דשנים: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=15)
def load_logs():
    """טעינת יומן דישון"""
    try:
        spreadsheet = get_spreadsheet()
        if spreadsheet is None:
            return pd.DataFrame()

        sheet = spreadsheet.worksheet("logs")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date

        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת יומן: {e}")
        return pd.DataFrame()


def clear_cache():
    """ניקוי cache"""
    load_plots.clear()
    load_fertilizers.clear()
    load_logs.clear()


def save_plots(df):
    """שמירת חלקות"""
    try:
        spreadsheet = get_spreadsheet()
        sheet = spreadsheet.worksheet("plots")

        sheet.clear()
        data = [df.columns.tolist()] + df.values.tolist()
        sheet.update('A1', data)

        clear_cache()
        return True
    except Exception as e:
        st.error(f"שגיאה בשמירה: {e}")
        return False


def save_fertilizers(df):
    """שמירת דשנים"""
    try:
        spreadsheet = get_spreadsheet()
        sheet = spreadsheet.worksheet("fertilizers")

        sheet.clear()
        data = [df.columns.tolist()] + df.values.tolist()
        sheet.update('A1', data)

        clear_cache()
        return True
    except Exception as e:
        st.error(f"שגיאה בשמירה: {e}")
        return False


def save_log_entry(log_date, plot_name, fert_name, amount_kg):
    """שמירת רשומת דישון חדשה"""
    try:
        spreadsheet = get_spreadsheet()
        sheet = spreadsheet.worksheet("logs")

        # קבלת כל הנתונים לחישוב ID חדש
        all_data = sheet.get_all_records()
        new_id = 1 if len(all_data) == 0 else max([r.get('log_id', 0) for r in all_data]) + 1

        # הוספת שורה חדשה
        new_row = [
            new_id,
            str(log_date),
            plot_name,
            fert_name,
            amount_kg,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]

        sheet.append_row(new_row)
        clear_cache()
        return True
    except Exception as e:
        st.error(f"שגיאה בשמירה: {e}")
        return False


def delete_log_entry(log_id):
    """מחיקת רשומה מהיומן"""
    try:
        spreadsheet = get_spreadsheet()
        sheet = spreadsheet.worksheet("logs")

        # מציאת השורה למחיקה
        all_data = sheet.get_all_values()
        for i, row in enumerate(all_data):
            if i > 0 and len(row) > 0 and str(row[0]) == str(log_id):
                sheet.delete_rows(i + 1)
                clear_cache()
                return True

        return False
    except Exception as e:
        st.error(f"שגיאה במחיקה: {e}")
        return False


def export_to_excel(df, filename):
    """ייצוא ל-Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='נתונים')
    return output.getvalue()


# =============================================================================
# בדיקת חיבור
# =============================================================================
def check_connection():
    """בדיקה האם יש חיבור תקין"""
    try:
        has_credentials = "gcp_service_account" in st.secrets or "gcp_service_account_json" in st.secrets
        has_url = "spreadsheet_url" in st.secrets

        if not has_credentials or not has_url:
            return False

        spreadsheet = get_spreadsheet()
        return spreadsheet is not None
    except:
        return False


# =============================================================================
# ממשק המשתמש הראשי
# =============================================================================

# כותרת ראשית
st.markdown("# 🥭 ניהול דישון - מטע מנגו")

# בדיקת חיבור
is_connected = check_connection()

if is_connected:
    st.markdown("""
    <div class="connection-status connected">
        ✅ מחובר ל-Google Sheets - הנתונים נשמרים אוטומטית בענן
    </div>
    """, unsafe_allow_html=True)

    # אתחול גיליונות
    init_sheets()
else:
    st.markdown("""
    <div class="connection-status disconnected">
        ❌ לא מחובר ל-Google Sheets - נדרשת הגדרה
    </div>
    """, unsafe_allow_html=True)

    st.error("""
    ## הגדרת Google Sheets

    כדי להשתמש באפליקציה, יש להגדיר חיבור ל-Google Sheets.

    פנה למנהל המערכת להשלמת ההגדרה.
    """)
    st.stop()

st.markdown("---")

# יצירת טאבים
tab1, tab2, tab3 = st.tabs(["📝 דיווח דישון", "📊 מצב חלקה", "🔐 ניהול הגדרות"])

# =============================================================================
# טאב 1: דיווח דישון
# =============================================================================
with tab1:
    st.markdown("## 📝 דיווח דישון חדש")
    st.markdown("#### מלא את הפרטים ולחץ על שמור")

    plots_df = load_plots()
    ferts_df = load_fertilizers()

    if plots_df.empty or ferts_df.empty:
        st.error("❌ חסרים נתוני חלקות או דשנים. פנה למנהל להוספת נתונים.")
    else:
        if st.session_state.form_submitted:
            st.balloons()
            st.markdown("""
            <div class="success-message">
                ✅ הדיווח נשמר בהצלחה!
            </div>
            """, unsafe_allow_html=True)

            if st.button("➕ הוסף דיווח נוסף"):
                st.session_state.form_submitted = False
                st.session_state.form_key += 1
                st.rerun()
        else:
            col1, col2 = st.columns([1, 1])

            with col1:
                selected_date = st.date_input(
                    "📅 תאריך",
                    value=date.today(),
                    format="DD/MM/YYYY",
                    key=f"date_{st.session_state.form_key}"
                )

                plot_names = plots_df['plot_name'].tolist()
                selected_plot = st.selectbox(
                    "🌳 בחר חלקה",
                    options=plot_names,
                    index=0,
                    key=f"plot_{st.session_state.form_key}"
                )

            with col2:
                fert_names = ferts_df['fert_name'].tolist()
                selected_fert = st.selectbox(
                    "🧪 בחר דשן",
                    options=fert_names,
                    index=0,
                    key=f"fert_{st.session_state.form_key}"
                )

                amount = st.number_input(
                    "⚖️ כמות (ק\"ג)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=0.0,
                    step=0.5,
                    key=f"amount_{st.session_state.form_key}"
                )

            selected_fert_info = ferts_df[ferts_df['fert_name'] == selected_fert].iloc[0]
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.8); padding: 10px; border-radius: 10px; margin: 10px 0;">
                <strong>הרכב הדשן:</strong> N: {selected_fert_info['n_percent']}% |
                P: {selected_fert_info['p_percent']}% |
                K: {selected_fert_info['k_percent']}% |
                C: {selected_fert_info['c_percent']}%
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="big-save-button">', unsafe_allow_html=True)
            save_clicked = st.button("💾 שמור דיווח", use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

            if save_clicked:
                if amount <= 0:
                    st.error("❌ שגיאה: יש להזין כמות גדולה מ-0")
                else:
                    with st.spinner("שומר ב-Google Sheets..."):
                        success = save_log_entry(selected_date, selected_plot, selected_fert, amount)
                        if success:
                            st.session_state.form_submitted = True
                            st.rerun()

# =============================================================================
# טאב 2: מצב חלקה (Dashboard)
# =============================================================================
with tab2:
    st.markdown("## 📊 מצב חלקה - דשבורד")

    plots_df = load_plots()
    ferts_df = load_fertilizers()
    logs_df = load_logs()

    if plots_df.empty:
        st.warning("אין נתוני חלקות. פנה למנהל להוספת חלקות.")
    else:
        col_filter1, col_filter2, col_filter3 = st.columns([2, 1, 1])

        with col_filter1:
            selected_plot_dashboard = st.selectbox(
                "🌳 בחר חלקה",
                options=plots_df['plot_name'].tolist(),
                key="dashboard_plot"
            )

        with col_filter2:
            min_date = date.today() - timedelta(days=365)
            start_date = st.date_input(
                "📅 מתאריך",
                value=min_date,
                format="DD/MM/YYYY",
                key="start_date"
            )

        with col_filter3:
            end_date = st.date_input(
                "📅 עד תאריך",
                value=date.today(),
                format="DD/MM/YYYY",
                key="end_date"
            )

        st.markdown("---")

        plot_info = plots_df[plots_df['plot_name'] == selected_plot_dashboard].iloc[0]
        plot_size = plot_info['size_dunam']

        plot_logs = logs_df[logs_df['plot_name'] == selected_plot_dashboard].copy() if not logs_df.empty else pd.DataFrame()

        if not plot_logs.empty:
            plot_logs = plot_logs[
                (plot_logs['date'] >= start_date) &
                (plot_logs['date'] <= end_date)
            ]

        if plot_logs.empty:
            st.info(f"📭 אין דיווחי דישון לחלקה '{selected_plot_dashboard}' בטווח התאריכים שנבחר")

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
            merged = plot_logs.merge(ferts_df, left_on='fert_name', right_on='fert_name', how='left')

            merged['actual_n'] = merged['amount_kg'] * (merged['n_percent'] / 100)
            merged['actual_p'] = merged['amount_kg'] * (merged['p_percent'] / 100)
            merged['actual_k'] = merged['amount_kg'] * (merged['k_percent'] / 100)
            merged['actual_c'] = merged['amount_kg'] * (merged['c_percent'] / 100)

            total_n = merged['actual_n'].sum()
            total_p = merged['actual_p'].sum()
            total_k = merged['actual_k'].sum()
            total_c = merged['actual_c'].sum()

            n_per_dunam = total_n / plot_size
            p_per_dunam = total_p / plot_size
            k_per_dunam = total_k / plot_size
            c_per_dunam = total_c / plot_size

            target_n = plot_info['target_n']
            target_p = plot_info['target_p']
            target_k = plot_info['target_k']
            target_c = plot_info['target_c']

            pct_n = (n_per_dunam / target_n * 100) if target_n > 0 else 0
            pct_p = (p_per_dunam / target_p * 100) if target_p > 0 else 0
            pct_k = (k_per_dunam / target_k * 100) if target_k > 0 else 0
            pct_c = (c_per_dunam / target_c * 100) if target_c > 0 else 0

            st.markdown(f"### 📈 סטטוס דישון - {selected_plot_dashboard}")
            st.markdown(f"**גודל החלקה:** {plot_size} דונם | **סה\"כ דיווחים:** {len(plot_logs)}")

            cols = st.columns(4)

            elements = [
                ("חנקן (N)", n_per_dunam, target_n, pct_n, "#2e7d32"),
                ("זרחן (P)", p_per_dunam, target_p, pct_p, "#1565c0"),
                ("אשלגן (K)", k_per_dunam, target_k, pct_k, "#ef6c00"),
                ("פחמן (C)", c_per_dunam, target_c, pct_c, "#6a1b9a")
            ]

            for i, (name, actual, target, pct, color) in enumerate(elements):
                with cols[i]:
                    delta = actual - target
                    delta_str = f"{delta:+.1f}"
                    st.metric(
                        label=name,
                        value=f"{actual:.1f}",
                        delta=f"{delta_str} ({pct:.0f}%)"
                    )

                    if pct > 100:
                        bar_color = "#d32f2f"
                    elif pct >= 80:
                        bar_color = color
                    else:
                        bar_color = "#ffa726"

                    bar_width = min(pct, 100)
                    st.markdown(f"""
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {bar_width}%; background-color: {bar_color};">
                            {pct:.0f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("### 📊 השוואת בפועל מול יעד (ק\"ג לדונם)")

            chart_data = pd.DataFrame({
                'יסוד': ['חנקן (N)', 'זרחן (P)', 'אשלגן (K)', 'פחמן (C)'],
                'בפועל': [n_per_dunam, p_per_dunam, k_per_dunam, c_per_dunam],
                'יעד': [target_n, target_p, target_k, target_c]
            })

            st.bar_chart(chart_data.set_index('יסוד'))

            st.markdown("---")

            col_table_header, col_export = st.columns([3, 1])

            with col_table_header:
                st.markdown("### 📋 דיווחים אחרונים")

            with col_export:
                display_logs = plot_logs[['date', 'fert_name', 'amount_kg', 'created_at']].copy()
                display_logs.columns = ['תאריך', 'דשן', 'כמות (ק"ג)', 'נוצר ב']

                excel_data = export_to_excel(display_logs, "דיווחים")
                st.download_button(
                    label="📥 ייצוא Excel",
                    data=excel_data,
                    file_name=f"דיווחים_{selected_plot_dashboard}_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            display_logs_sorted = display_logs.sort_values('תאריך', ascending=False).head(20)
            st.dataframe(display_logs_sorted, use_container_width=True, hide_index=True)

# =============================================================================
# טאב 3: ניהול הגדרות
# =============================================================================
with tab3:
    st.markdown("## 🔐 ניהול הגדרות")

    if not st.session_state.admin_authenticated:
        st.markdown("#### הזן סיסמת מנהל להמשך")

        password = st.text_input("סיסמה", type="password", key="admin_password")

        if st.button("🔓 כניסה"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ סיסמה שגויה")
    else:
        col_title, col_logout = st.columns([4, 1])
        with col_title:
            st.markdown("#### עריכה ישירה של נתוני המערכת")
        with col_logout:
            if st.button("🚪 התנתק"):
                st.session_state.admin_authenticated = False
                st.rerun()

        st.warning("⚠️ שים לב: שינויים כאן משפיעים על כל המערכת!")

        st.markdown("### 🌳 ניהול חלקות")

        plots_df = load_plots()

        edited_plots = st.data_editor(
            plots_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "plot_id": st.column_config.NumberColumn("מזהה", disabled=True),
                "plot_name": st.column_config.TextColumn("שם חלקה", required=True),
                "size_dunam": st.column_config.NumberColumn("גודל (דונם)", min_value=0.1, required=True),
                "target_n": st.column_config.NumberColumn("יעד N", min_value=0),
                "target_p": st.column_config.NumberColumn("יעד P", min_value=0),
                "target_k": st.column_config.NumberColumn("יעד K", min_value=0),
                "target_c": st.column_config.NumberColumn("יעד C", min_value=0),
            },
            hide_index=True,
            key="plots_editor"
        )

        if st.button("💾 שמור חלקות", type="primary", key="save_plots"):
            if edited_plots['plot_id'].isna().any():
                max_id = edited_plots['plot_id'].max()
                max_id = 0 if pd.isna(max_id) else max_id
                for idx in edited_plots[edited_plots['plot_id'].isna()].index:
                    max_id += 1
                    edited_plots.loc[idx, 'plot_id'] = max_id

            if save_plots(edited_plots):
                st.success("✅ חלקות נשמרו!")
                st.rerun()

        st.markdown("---")

        st.markdown("### 🧪 ניהול דשנים")

        ferts_df = load_fertilizers()

        edited_ferts = st.data_editor(
            ferts_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "fert_id": st.column_config.NumberColumn("מזהה", disabled=True),
                "fert_name": st.column_config.TextColumn("שם דשן", required=True),
                "n_percent": st.column_config.NumberColumn("% N", min_value=0, max_value=100),
                "p_percent": st.column_config.NumberColumn("% P", min_value=0, max_value=100),
                "k_percent": st.column_config.NumberColumn("% K", min_value=0, max_value=100),
                "c_percent": st.column_config.NumberColumn("% C", min_value=0, max_value=100),
            },
            hide_index=True,
            key="ferts_editor"
        )

        if st.button("💾 שמור דשנים", type="primary", key="save_ferts"):
            if edited_ferts['fert_id'].isna().any():
                max_id = edited_ferts['fert_id'].max()
                max_id = 0 if pd.isna(max_id) else max_id
                for idx in edited_ferts[edited_ferts['fert_id'].isna()].index:
                    max_id += 1
                    edited_ferts.loc[idx, 'fert_id'] = max_id

            if save_fertilizers(edited_ferts):
                st.success("✅ דשנים נשמרו!")
                st.rerun()

        st.markdown("---")

        st.markdown("### 📋 יומן דישון")

        logs_df = load_logs()

        if logs_df.empty:
            st.info("📭 היומן ריק")
        else:
            col_log_title, col_log_export = st.columns([3, 1])
            with col_log_export:
                logs_export = logs_df.copy()
                logs_export.columns = ['מזהה', 'תאריך', 'חלקה', 'דשן', 'כמות (ק"ג)', 'נוצר ב']
                excel_logs = export_to_excel(logs_export, "יומן_מלא")
                st.download_button(
                    label="📥 ייצוא הכל",
                    data=excel_logs,
                    file_name=f"יומן_דישון_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            logs_display = logs_df.copy()
            logs_display.columns = ['מזהה', 'תאריך', 'חלקה', 'דשן', 'כמות (ק"ג)', 'נוצר ב']
            st.dataframe(logs_display.sort_values('מזהה', ascending=False), use_container_width=True, hide_index=True)

            st.markdown("#### 🗑️ מחיקת רשומה")

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                delete_id = st.number_input(
                    "מזהה למחיקה",
                    min_value=1,
                    max_value=int(logs_df['log_id'].max()) if not logs_df.empty else 1,
                    step=1,
                    key="delete_id"
                )

            with col2:
                if st.button("🗑️ מחק", key="delete_btn"):
                    st.session_state.delete_confirm = delete_id

            with col3:
                if st.session_state.delete_confirm == delete_id:
                    st.markdown('<div class="delete-button">', unsafe_allow_html=True)
                    if st.button("⚠️ אישור מחיקה", key="confirm_delete"):
                        if delete_log_entry(delete_id):
                            st.success(f"✅ רשומה {delete_id} נמחקה!")
                            st.session_state.delete_confirm = None
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.delete_confirm:
                st.warning(f"⚠️ האם אתה בטוח שברצונך למחוק רשומה {st.session_state.delete_confirm}?")

# =============================================================================
# פוטר
# =============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>🥭 מערכת ניהול דישון | גרסה 3.0 | מחובר ל-Google Sheets</div>",
    unsafe_allow_html=True
)
