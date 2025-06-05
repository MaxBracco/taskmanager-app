import streamlit as st
import datetime
import json
import os
import pandas as pd
from collections import defaultdict # Für Gruppierungen
import plotly.express as px # Für einfache Visualisierungen

# --- Konfiguration ---
DATA_FILE = "tasks.json"

# --- Datenmodell (für Tasks) ---
class Task:
    def __init__(self, id, title, description, due_date, priority, status, assigned_to=None, tags=None, notes=None, created_at=None, completed_at=None, recurrence=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority # Low, Medium, High, Urgent
        self.status = status     # To Do, In Progress, On Hold, Completed, Cancelled
        self.assigned_to = assigned_to
        self.tags = tags if tags is not None else []
        self.notes = notes if notes is not None else []
        self.created_at = created_at if created_at else datetime.datetime.now().isoformat()
        self.completed_at = completed_at
        self.recurrence = recurrence # z.B. {'type': 'daily', 'interval': 1} oder None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if isinstance(self.due_date, datetime.date) else self.due_date,
            "priority": self.priority,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "tags": self.tags,
            "notes": self.notes,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "recurrence": self.recurrence
        }

    @staticmethod
    def from_dict(data):
        due_date = data.get("due_date")
        if due_date and isinstance(due_date, str):
            try:
                due_date = datetime.date.fromisoformat(due_date)
            except ValueError:
                due_date = None # Falls das Datum ungültig ist
        else:
            due_date = None

        # NEU: Fehlerbehandlung für 'recurrence'
        recurrence_data = data.get("recurrence")
        if isinstance(recurrence_data, str) and recurrence_data.lower() == "none":
            recurrence_data = None
        elif isinstance(recurrence_data, dict):
            # Sicherstellen, dass 'interval' ein int ist
            if 'interval' in recurrence_data and not isinstance(recurrence_data['interval'], int):
                try:
                    recurrence_data['interval'] = int(recurrence_data['interval'])
                except (ValueError, TypeError):
                    recurrence_data['interval'] = 1 # Standardwert, falls Konvertierung fehlschlägt
        else:
            recurrence_data = None


        return Task(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""), # Standardwert, falls fehlt
            due_date=due_date,
            priority=data.get("priority", "Medium"), # Standardwert, falls fehlt
            status=data.get("status", "To Do"),     # Standardwert, falls fehlt
            assigned_to=data.get("assigned_to"),
            tags=data.get("tags"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at"),
            recurrence=recurrence_data # Hier die korrigierten Daten verwenden
        )

# --- Hilfsfunktionen für Datenhandling (JSON) ---
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return [Task.from_dict(d) for d in data]
            except json.JSONDecodeError:
                return [] # Leere Liste, falls JSON fehlerhaft ist
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4, ensure_ascii=False)

# --- Initialisierung des Session State ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = max([t.id for t in st.session_state.tasks] + [0]) + 1
if "confirm_delete_completed" not in st.session_state:
    st.session_state.confirm_delete_completed = False
if "confirm_delete_all" not in st.session_state: # NEU: Für "Alle Aufgaben löschen" Bestätigung
    st.session_state.confirm_delete_all = False
if "page" not in st.session_state: # Initialize page state
    st.session_state.page = "Dashboard"

# --- Funktionen für Task-Management ---
def add_task(title, description, due_date, priority, status, assigned_to, tags, recurrence):
    new_task = Task(st.session_state.next_task_id, title, description, due_date, priority, status, assigned_to, tags, recurrence=recurrence)
    st.session_state.tasks.append(new_task)
    st.session_state.next_task_id += 1
    save_tasks(st.session_state.tasks)
    st.success("Aufgabe erfolgreich hinzugefügt!")

def update_task(task_id, new_title, new_description, new_due_date, new_priority, new_status, new_assigned_to, new_tags, new_recurrence):
    for i, task in enumerate(st.session_state.tasks):
        if task.id == task_id:
            st.session_state.tasks[i].title = new_title
            st.session_state.tasks[i].description = new_description
            st.session_state.tasks[i].due_date = new_due_date
            st.session_state.tasks[i].priority = new_priority
            st.session_state.tasks[i].status = new_status
            st.session_state.tasks[i].assigned_to = new_assigned_to
            st.session_state.tasks[i].tags = new_tags
            st.session_state.tasks[i].recurrence = new_recurrence
            if new_status == "Completed" and st.session_state.tasks[i].completed_at is None:
                st.session_state.tasks[i].completed_at = datetime.datetime.now().isoformat()
            elif new_status != "Completed" and st.session_state.tasks[i].completed_at is not None:
                st.session_state.tasks[i].completed_at = None
            save_tasks(st.session_state.tasks)
            st.success(f"Aufgabe '{new_title}' erfolgreich aktualisiert!")
            return
    st.error("Aufgabe nicht gefunden.")

def delete_task(task_id):
    st.session_state.tasks = [task for task in st.session_state.tasks if task.id != task_id]
    save_tasks(st.session_state.tasks)
    st.success("Aufgabe erfolgreich gelöscht!")

def add_note_to_task(task_id, note_content):
    for task in st.session_state.tasks:
        if task.id == task_id:
            task.notes.append({"timestamp": datetime.datetime.now().isoformat(), "content": note_content})
            save_tasks(st.session_state.tasks)
            st.success("Notiz hinzugefügt!")
            return
    st.error("Aufgabe nicht gefunden.")

def mark_task_as_completed(task_id):
    for i, task in enumerate(st.session_state.tasks):
        if task.id == task_id:
            if task.status != "Completed":
                st.session_state.tasks[i].status = "Completed"
                st.session_state.tasks[i].completed_at = datetime.datetime.now().isoformat()
                save_tasks(st.session_state.tasks)
                st.success(f"Aufgabe '{task.title}' als 'Erledigt' markiert! 🎉")
            else:
                st.info(f"Aufgabe '{task.title}' ist bereits als 'Erledigt' markiert.")
            return
    st.error("Aufgabe nicht gefunden.")

def delete_completed_tasks():
    tasks_before_delete = len(st.session_state.tasks)
    st.session_state.tasks = [task for task in st.session_state.tasks if task.status != "Completed"]
    tasks_after_delete = len(st.session_state.tasks)
    deleted_count = tasks_before_delete - tasks_after_delete
    save_tasks(st.session_state.tasks)
    st.success(f"{deleted_count} erledigte Aufgaben erfolgreich gelöscht!")
    st.session_state.confirm_delete_completed = False # Reset confirmation
    st.rerun() # Reload UI

def delete_all_tasks_confirmed():
    st.session_state.tasks = []
    st.session_state.next_task_id = 1
    save_tasks(st.session_state.tasks)
    st.success("Alle Aufgaben wurden gelöscht.")
    st.session_state.confirm_delete_all = False # Reset confirmation
    st.rerun()

def get_filtered_and_sorted_tasks(tasks, filter_status=None, filter_priority=None, filter_assigned_to=None, filter_tag=None, sort_by="Due Date", sort_order="Ascending"):
    filtered_tasks = tasks
    if filter_status and filter_status != "All":
        filtered_tasks = [task for task in filtered_tasks if task.status == filter_status]
    if filter_priority and filter_priority != "All":
        filtered_tasks = [task for task in filtered_tasks if task.priority == filter_priority]
    if filter_assigned_to and filter_assigned_to != "All":
        filtered_tasks = [task for task in filtered_tasks if task.assigned_to == filter_assigned_to]
    if filter_tag and filter_tag != "All":
        filtered_tasks = [task for task in filtered_tasks if filter_tag in task.tags]

    # Sortierung
    if sort_by == "Due Date":
        filtered_tasks.sort(key=lambda x: x.due_date if x.due_date else datetime.date(9999, 12, 31), reverse=(sort_order == "Descending"))
    elif sort_by == "Priority":
        priority_order = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
        filtered_tasks.sort(key=lambda x: priority_order.get(x.priority, 99), reverse=(sort_order == "Descending"))
    elif sort_by == "Status":
        status_order = {"To Do": 0, "In Progress": 1, "On Hold": 2, "Completed": 3, "Cancelled": 4}
        filtered_tasks.sort(key=lambda x: status_order.get(x.status, 99), reverse=(sort_order == "Descending"))
    elif sort_by == "Created At":
        filtered_tasks.sort(key=lambda x: x.created_at, reverse=(sort_order == "Descending"))
    elif sort_by == "Title":
        filtered_tasks.sort(key=lambda x: x.title.lower(), reverse=(sort_order == "Descending"))

    return filtered_tasks

def generate_recurring_tasks():
    today = datetime.date.today()
    for task in st.session_state.tasks:
        if task.recurrence and task.status == "Completed" and task.due_date:
            last_due_date = task.due_date
            if task.recurrence['type'] == 'daily':
                next_due_date = last_due_date + datetime.timedelta(days=task.recurrence.get('interval', 1))
            elif task.recurrence['type'] == 'weekly':
                next_due_date = last_due_date + datetime.timedelta(weeks=task.recurrence.get('interval', 1))
            elif task.recurrence['type'] == 'monthly':
                # Einfache Monats-Logik, kann komplexer werden (z.B. Monatsende)
                try:
                    next_month = last_due_date.month + task.recurrence.get('interval', 1)
                    next_year = last_due_date.year + (next_month - 1) // 12
                    next_month = (next_month - 1) % 12 + 1
                    next_due_date = datetime.date(next_year, next_month, last_due_date.day)
                except ValueError: # Tag gibt es im nächsten Monat nicht (z.g. 31. Feb)
                    # Dies sollte den letzten Tag des Monats ergeben, wenn der ursprüngliche Tag ungültig ist
                    temp_date = datetime.date(last_due_date.year, last_due_date.month, 1) + datetime.timedelta(days=32 * task.recurrence.get('interval', 1))
                    next_due_date = datetime.date(temp_date.year, temp_date.month, 1) - datetime.timedelta(days=1)


            elif task.recurrence['type'] == 'yearly':
                next_due_date = datetime.date(last_due_date.year + task.recurrence.get('interval', 1), last_due_date.month, last_due_date.day)
            else:
                next_due_date = None

            if next_due_date and next_due_date > today:
                # Prüfen, ob die Aufgabe bereits generiert wurde
                existing_next_task = any(
                    t.title == task.title and
                    t.description == task.description and
                    t.due_date == next_due_date and
                    t.status != "Completed" # Vermeiden, abgeschlossene Aufgaben erneut zu erstellen
                    for t in st.session_state.tasks
                )
                if not existing_next_task:
                    new_recurring_task = Task(
                        id=st.session_state.next_task_id,
                        title=task.title,
                        description=task.description,
                        due_date=next_due_date,
                        priority=task.priority,
                        status="To Do", # Neue Instanz ist "To Do"
                        assigned_to=task.assigned_to,
                        tags=task.tags,
                        notes=[], # Keine alten Notizen übernehmen
                        recurrence=task.recurrence # Rekurrenz beibehalten
                    )
                    st.session_state.tasks.append(new_recurring_task)
                    st.session_state.next_task_id += 1
                    st.success(f"Wiederkehrende Aufgabe '{task.title}' für {next_due_date.isoformat()} generiert.")
                    save_tasks(st.session_state.tasks) # Sofort speichern

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Task Manager")
st.title("📋 Task Manager")

# --- CSS Styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        font-size: 3em;
        font-weight: 800;
        color: #4A00B7;
        text-align: center;
        margin-bottom: 1.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #5A189A;
        margin-top: 2em;
        margin-bottom: 1em;
        border-bottom: 2px solid #E0BBE4;
        padding-bottom: 0.5em;
    }
    /* Allgemeiner Stil für alle Streamlit Buttons (falls nicht überschrieben) */
    .stButton>button {
        background-color: #7B2CBF;
        color: white;
        padding: 10px 20px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        display: inline-flex; /* Für Icon-Text Ausrichtung */
        align-items: center;
        gap: 8px; /* Abstand zwischen Icon und Text */
    }
    .stButton>button:hover {
        background-color: #9D4EDD;
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    /* Spezifischer Stil für den Bearbeiten-Button */
    .stButton button[key^="edit_"] {
        background-color: #DBEAFE; /* Hellblau */
        color: #2563EB; /* Dunkelblau */
        border: 1px solid #2563EB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 8px 12px; /* Etwas kleiner als Standard */
        font-size: 0.9em;
    }
    .stButton button[key^="edit_"]:hover {
        background-color: #BFDBFE;
        transform: translateY(-1px);
    }

    /* Spezifischer Stil für den Löschen-Button */
    .stButton button[key^="delete_"] {
        background-color: #FEE2E2; /* Hellrot */
        color: #DC2626; /* Dunkelrot */
        border: 1px solid #DC2626;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 8px 12px; /* Etwas kleiner als Standard */
        font-size: 0.9em;
    }
    .stButton button[key^="delete_"]:hover {
        background-color: #FECACA;
        transform: translateY(-1px);
    }

    /* NEU: Stil für den "Als Erledigt markieren" Button */
    .stButton button[key^="complete_task_"] {
        background-color: #D1FAE5; /* Hellgrün */
        color: #047857; /* Dunkelgrün */
        border: 1px solid #047857;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 8px 12px;
        font-size: 0.9em;
    }
    .stButton button[key^="complete_task_"]:hover {
        background-color: #A7F3D0;
        transform: translateY(-1px);
    }
    /* NEU: Stil für den "Erledigte Aufgaben löschen" Button */
    .stButton button[key="delete_completed_tasks_button"] {
        background-color: #FFDEB4; /* Orange-ähnlich */
        color: #D97706; /* Dunkelorange */
        border: 1px solid #D97706;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 10px 15px;
        font-weight: 600;
    }
    .stButton button[key="delete_completed_tasks_button"]:hover {
        background-color: #FFCC80;
        transform: translateY(-1px);
    }
    /* NEU: Stil für die Bestätigungsbuttons (Löschen) */
    .stButton button[key^="confirm_delete_"] {
        background-color: #EF4444; /* Hellrot */
        color: white;
        border: 1px solid #EF4444;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 10px 15px;
        font-weight: 600;
    }
    .stButton button[key^="confirm_delete_"]:hover {
        background-color: #DC2626;
        transform: translateY(-1px);
    }
     /* NEU: Stil für Abbrechen-Buttons */
    .stButton button[key^="cancel_delete_"] {
        background-color: #E5E7EB; /* Hellgrau */
        color: #4B5563; /* Dunkelgrau */
        border: 1px solid #9CA3AF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 10px 15px;
        font-weight: 600;
    }
    .stButton button[key^="cancel_delete_"]:hover {
        background-color: #D1D5DB;
        transform: translateY(-1px);
    }


    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stDateInput>div>div>input, .stTimeInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #D0B3E4;
        padding: 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stDateInput>div>div>input:focus, .stTimeInput>div>div>input:focus {
        border-color: #9D4EDD;
        box-shadow: 0 0 0 3px rgba(157, 78, 221, 0.3);
        outline: none;
    }
    .task-item {
        background-color: #fff;
        border: 1px solid #E0BBE4;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex; /* Für bessere Layout-Kontrolle der Task-Elemente */
        align-items: center;
    }
    .task-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    .task-complete {
        background-color: #E6FFFA;
        border-left: 6px solid #38A169;
        opacity: 0.9;
    }
    .task-name-complete {
        text-decoration: line-through;
        color: #6B7280;
        font-style: italic;
    }
    .priority-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: 700;
        margin-left: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .priority-5 { background-color: #FEE2E2; color: #DC2626; } /* Rot */
    .priority-4 { background-color: #FFEDD5; color: #F59E0B; } /* Orange */
    .priority-3 { background-color: #FEF3C7; color: #D97706; } /* Gold */
    .priority-2 { background-color: #DBEAFE; color: #2563EB; } /* Blau */
    .priority-1 { background-color: #E5E7EB; color: #4B5563; } /* Grau */
    
    /* Custom styles for sidebar buttons */
    .sidebar-button button {
        width: 100%;
        text-align: left;
        background-color: #f0f2f6; /* Light gray for inactive */
        color: #4B5563; /* Dark gray text */
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 8px;
        font-weight: 600;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .sidebar-button button:hover {
        background-color: #e2e4e8;
        color: #2D3748;
    }
    .sidebar-button button.active {
        background-color: #7B2CBF; /* Primary purple for active */
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar Navigation
st.sidebar.header("Navigation")

# Custom navigation buttons
if st.sidebar.button("Dashboard", key="nav_dashboard"):
    st.session_state.page = "Dashboard"
if st.sidebar.button("Aufgaben verwalten", key="nav_manage_tasks"):
    st.session_state.page = "Aufgaben verwalten"
if st.sidebar.button("Berichte & Analyse", key="nav_reports_analysis"):
    st.session_state.page = "Berichte & Analyse"
if st.sidebar.button("Einstellungen", key="nav_settings"):
    st.session_state.page = "Einstellungen"

# --- Dashboard ---
if st.session_state.page == "Dashboard":
    st.header("Übersicht")

    # Schnell-Statistiken
    col1, col2, col3, col4 = st.columns(4)
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t.status == "Completed"])
    overdue_tasks = len([t for t in st.session_state.tasks if t.due_date and t.due_date < datetime.date.today() and t.status not in ["Completed", "Cancelled"]])
    today_due_tasks = len([t for t in st.session_state.tasks if t.due_date == datetime.date.today() and t.status not in ["Completed", "Cancelled"]])

    with col1:
        st.metric(label="Gesamtaufgaben", value=total_tasks)
    with col2:
        st.metric(label="Abgeschlossen", value=completed_tasks)
    with col3:
        st.metric(label="Überfällig", value=overdue_tasks)
    with col4:
        st.metric(label="Fällig heute", value=today_due_tasks)

    st.subheader("Aktuelle Aufgaben (To Do & In Progress)")
    current_tasks = [t for t in st.session_state.tasks if t.status in ["To Do", "In Progress"]]

    if current_tasks:
        st.write("Wähle eine Aufgabe zum Erledigen:")
        
        # Sortiere Aufgaben, z.B. nach Fälligkeitsdatum und Priorität
        current_tasks.sort(key=lambda x: (x.due_date if x.due_date else datetime.date(9999,12,31), 
                                          {"Urgent":0, "High":1, "Medium":2, "Low":3}.get(x.priority, 99)))

        headers = ["Titel", "Fällig", "Priorität", "Status", "Aktion"]
        cols_widths = [4, 2, 1, 1, 1.5] # Anpassbare Spaltenbreiten

        # Header-Zeile
        cols_header = st.columns(cols_widths)
        for col_idx, header_text in enumerate(headers):
            cols_header[col_idx].markdown(f"**{header_text}**")
        st.markdown("---") # Trennlinie unter dem Header

        for task in current_tasks:
            # Erstelle Spalten für jede Zeile
            cols = st.columns(cols_widths)
            with cols[0]:
                st.write(task.title)
            with cols[1]:
                st.write(task.due_date.isoformat() if task.due_date else 'N/A')
            with cols[2]:
                st.write(task.priority)
            with cols[3]:
                st.write(task.status)
            with cols[4]:
                if st.button("✅ Erledigt", key=f"complete_task_{task.id}", help=f"Markiere '{task.title}' als erledigt"):
                    mark_task_as_completed(task.id)
                    st.rerun() # Seite neu laden, um Änderungen anzuzeigen

    else:
        st.info("Keine aktuellen Aufgaben vorhanden, die erledigt werden können.")

    st.subheader("Aufgaben nach Priorität")
    priority_counts = defaultdict(int)
    for task in st.session_state.tasks:
        priority_counts[task.priority] += 1
    priority_df = pd.DataFrame(priority_counts.items(), columns=['Priority', 'Count'])
    if not priority_df.empty:
        fig_priority = px.pie(priority_df, values='Count', names='Priority', title='Aufgabenverteilung nach Priorität')
        st.plotly_chart(fig_priority, use_container_width=True)
    else:
        st.info("Keine Aufgaben zur Anzeige der Prioritätsverteilung.")

    st.subheader("Aufgaben nach Status")
    status_counts = defaultdict(int)
    for task in st.session_state.tasks:
        status_counts[task.status] += 1
    status_df = pd.DataFrame(status_counts.items(), columns=['Status', 'Count'])
    if not status_df.empty:
        fig_status = px.bar(status_df, x='Status', y='Count', title='Aufgaben nach Status', color='Status')
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("Keine Aufgaben zur Anzeige der Statusverteilung.")


# --- Aufgaben verwalten ---
elif st.session_state.page == "Aufgaben verwalten":
    st.header("Aufgaben verwalten")

    # --- Neue Aufgabe hinzufügen ---
    st.subheader("Neue Aufgabe hinzufügen")
    with st.form("add_task_form"):
        title = st.text_input("Titel der Aufgabe *", placeholder="Task-Management-App entwickeln")
        description = st.text_area("Beschreibung", placeholder="Implementierung der Frontend- und Backend-Logik...")
        col_add_1, col_add_2 = st.columns(2)
        with col_add_1:
            due_date = st.date_input("Fälligkeitsdatum", min_value=datetime.date.today(), value=datetime.date.today())
            priority = st.selectbox("Priorität", ["Low", "Medium", "High", "Urgent"], index=1)
        with col_add_2:
            status = st.selectbox("Status", ["To Do", "In Progress", "On Hold", "Completed", "Cancelled"])
            assigned_to = st.text_input("Zugewiesen an (optional)", placeholder="Max Mustermann")
        
        # Tags
        tags_input = st.text_input("Tags (durch Komma getrennt)", placeholder="Development, Streamlit, Python")
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]

        # Rekurrenz
        st.markdown("---")
        st.write("Wiederkehrende Aufgabe?")
        recurrence_type = st.selectbox("Typ der Wiederholung", ["None", "daily", "weekly", "monthly", "yearly"])
        recurrence_interval = None
        if recurrence_type != "None":
            recurrence_interval = st.number_input("Intervall (alle X Tage/Wochen/Monate/Jahre)", min_value=1, value=1)
        
        # Removed key from here as it's inside a form
        submitted = st.form_submit_button("Aufgabe hinzufügen")
        if submitted:
            if not title:
                st.error("Titel der Aufgabe ist erforderlich!")
            else:
                recurrence_data = {'type': recurrence_type, 'interval': int(recurrence_interval)} if recurrence_type != "None" else None
                add_task(title, description, due_date, priority, status, assigned_to, tags, recurrence_data)

    st.markdown("---")

    # --- Aufgaben filtern und sortieren ---
    st.subheader("Aufgabenliste")
    col_filter_1, col_filter_2, col_filter_3 = st.columns(3)
    
    all_statuses = ["All"] + list(set(t.status for t in st.session_state.tasks))
    all_priorities = ["All", "Urgent", "High", "Medium", "Low"]
    all_assignees = ["All"] + list(set(t.assigned_to for t in st.session_state.tasks if t.assigned_to))
    all_tags = ["All"] + list(set(tag for t in st.session_state.tasks for tag in t.tags))

    with col_filter_1:
        filter_status = st.selectbox("Filter nach Status", all_statuses)
        filter_priority = st.selectbox("Filter nach Priorität", all_priorities)
    with col_filter_2:
        filter_assigned_to = st.selectbox("Filter nach Zugewiesen an", all_assignees)
        filter_tag = st.selectbox("Filter nach Tag", all_tags)
    with col_filter_3:
        sort_by = st.selectbox("Sortieren nach", ["Due Date", "Priority", "Status", "Created At", "Title"])
        sort_order = st.radio("Sortierreihenfolge", ["Ascending", "Descending"], horizontal=True)

    filtered_and_sorted_tasks = get_filtered_and_sorted_tasks(
        st.session_state.tasks,
        filter_status,
        filter_priority,
        filter_assigned_to,
        filter_tag,
        sort_by,
        sort_order
    )

    if filtered_and_sorted_tasks:
        # Anzeigen der Aufgaben in erweiterbaren Abschnitten
        for task in filtered_and_sorted_tasks:
            with st.expander(f"**{task.title}** (Fällig: {task.due_date.isoformat() if task.due_date else 'N/A'}) - Status: {task.status} - Priorität: {task.priority}"):
                st.write(f"**ID:** {task.id}")
                st.write(f"**Beschreibung:** {task.description}")
                st.write(f"**Fälligkeitsdatum:** {task.due_date.isoformat() if task.due_date else 'Nicht gesetzt'}")
                st.write(f"**Priorität:** {task.priority}")
                st.write(f"**Status:** {task.status}")
                st.write(f"**Zugewiesen an:** {task.assigned_to if task.assigned_to else 'Niemand'}")
                st.write(f"**Tags:** {', '.join(task.tags) if task.tags else 'Keine'}")
                st.write(f"**Erstellt am:** {datetime.datetime.fromisoformat(task.created_at).strftime('%d.%m.%Y %H:%M')}")
                if task.completed_at:
                    st.write(f"**Abgeschlossen am:** {datetime.datetime.fromisoformat(task.completed_at).strftime('%d.%m.%Y %H:%M')}")
                
                # Check added here to prevent error if recurrence is None or not a dict
                if task.recurrence and isinstance(task.recurrence, dict):
                    st.write(f"**Wiederholung:** {task.recurrence.get('type', '').capitalize()} (alle {task.recurrence.get('interval', '')})")
                else:
                    st.write("**Wiederholung:** Keine")

                # Notizen
                st.subheader("Notizen")
                if task.notes:
                    for note in task.notes:
                        st.text_area(f"Notiz vom {datetime.datetime.fromisoformat(note['timestamp']).strftime('%d.%m.%Y %H:%M')}", value=note['content'], height=70, disabled=True)
                new_note = st.text_area(f"Neue Notiz für '{task.title}'", key=f"note_{task.id}")
                if st.button("Notiz hinzufügen", key=f"add_note_{task.id}"):
                    if new_note:
                        add_note_to_task(task.id, new_note)
                        st.rerun() # UI aktualisieren
                    else:
                        st.warning("Notiz kann nicht leer sein.")

                st.markdown("---")
                st.subheader("Aufgabe bearbeiten")
                with st.form(f"edit_task_form_{task.id}"):
                    new_title = st.text_input("Neuer Titel", value=task.title, key=f"edit_title_{task.id}")
                    new_description = st.text_area("Neue Beschreibung", value=task.description, key=f"edit_desc_{task.id}")
                    col_edit_1, col_edit_2 = st.columns(2)
                    with col_edit_1:
                        new_due_date = st.date_input("Neues Fälligkeitsdatum", value=task.due_date if task.due_date else datetime.date.today(), key=f"edit_due_{task.id}")
                        new_priority = st.selectbox("Neue Priorität", ["Low", "Medium", "High", "Urgent"], index=["Low", "Medium", "High", "Urgent"].index(task.priority), key=f"edit_prio_{task.id}")
                    with col_edit_2:
                        # Corrected: Handle cases where task.status might not be in the predefined list
                        status_options = ["To Do", "In Progress", "On Hold", "Completed", "Cancelled"]
                        try:
                            current_status_index = status_options.index(task.status)
                        except ValueError:
                            current_status_index = 0  # Default to "To Do" if status is not recognized

                        new_status = st.selectbox("Neuer Status", status_options, index=current_status_index, key=f"edit_status_{task.id}")
                        new_assigned_to = st.text_input("Neu zugewiesen an", value=task.assigned_to if task.assigned_to else "", key=f"edit_assigned_{task.id}")

                    # Tags bearbeiten
                    current_tags_str = ", ".join(task.tags)
                    new_tags_input = st.text_input("Neue Tags (durch Komma getrennt)", value=current_tags_str, key=f"edit_tags_{task.id}")
                    new_tags = [t.strip() for t in new_tags_input.split(',') if t.strip()]

                    # Rekurrenz bearbeiten
                    st.markdown("---")
                    st.write("Wiederkehrende Aufgabe bearbeiten")
                    current_recurrence_type = task.recurrence['type'] if task.recurrence and isinstance(task.recurrence, dict) and 'type' in task.recurrence else "None"
                    current_recurrence_interval = task.recurrence['interval'] if task.recurrence and isinstance(task.recurrence, dict) and 'interval' in task.recurrence else 1
                    
                    edit_recurrence_type = st.selectbox("Typ der Wiederholung", ["None", "daily", "weekly", "monthly", "yearly"], index=["None", "daily", "weekly", "monthly", "yearly"].index(current_recurrence_type), key=f"edit_recur_type_{task.id}")
                    edit_recurrence_interval = None
                    if edit_recurrence_type != "None":
                        edit_recurrence_interval = st.number_input("Intervall (alle X Tage/Wochen/Monate/Jahre)", min_value=1, value=current_recurrence_interval, key=f"edit_recur_interval_{task.id}")
                    
                    edit_recurrence_data = {'type': edit_recurrence_type, 'interval': int(edit_recurrence_interval)} if edit_recurrence_type != "None" else None

                    col_actions_edit, col_actions_delete = st.columns(2)
                    with col_actions_edit:
                        # Removed key from here
                        if st.form_submit_button("Aufgabe aktualisieren"):
                            if not new_title:
                                st.error("Titel der Aufgabe ist erforderlich!")
                            else:
                                update_task(task.id, new_title, new_description, new_due_date, new_priority, new_status, new_assigned_to, new_tags, edit_recurrence_data)
                                st.rerun() # UI aktualisieren
                    with col_actions_delete:
                        # Removed key from here
                        if st.form_submit_button("Aufgabe löschen"):
                            delete_task(task.id)
                            st.rerun() # UI aktualisieren
    else:
        st.info("Keine Aufgaben gefunden, die den Filtern entsprechen.")

    st.markdown("---")
    st.subheader("Wartungsaktionen")
    # Verschieben des "Erledigte Aufgaben löschen" Buttons in die linke Spalte
    col_maintenance_1, col_maintenance_2 = st.columns(2)
    with col_maintenance_1: # Jetzt in col_maintenance_1
        if st.button("Erledigte Aufgaben löschen", key="delete_completed_tasks_button"):
            st.session_state.confirm_delete_completed = True
        
        if st.session_state.confirm_delete_completed:
            st.warning("Sind Sie sicher, dass Sie ALLE erledigten Aufgaben löschen möchten? Dies kann nicht rückgängig gemacht werden.")
            col_confirm_del, col_cancel_del = st.columns(2)
            with col_confirm_del:
                if st.button("Ja, erledigte Aufgaben löschen", key="confirm_delete_completed_action"):
                    delete_completed_tasks()
            with col_cancel_del:
                if st.button("Abbrechen", key="cancel_delete_completed_action"):
                    st.session_state.confirm_delete_completed = False
                    st.rerun()
    
    st.markdown("---")
    # NEU: "Alle Aufgaben löschen" Bereich
    st.subheader("Gefahrenbereich: Alle Aufgaben löschen")
    if st.button("ALLE Aufgaben löschen", key="delete_all_tasks_button", type="secondary"):
        st.session_state.confirm_delete_all = True
    
    if st.session_state.confirm_delete_all:
        st.warning("Sind Sie absolut sicher, dass Sie ALLE Aufgaben löschen möchten? Dies kann NICHT rückgängig gemacht werden.")
        col_confirm_all, col_cancel_all = st.columns(2)
        with col_confirm_all:
            if st.button("JA, ALLE Aufgaben unwiderruflich löschen", key="confirm_delete_all_action"):
                delete_all_tasks_confirmed()
        with col_cancel_all:
            if st.button("Abbrechen", key="cancel_delete_all_action"):
                st.session_state.confirm_delete_all = False
                st.rerun()


# --- Berichte & Analyse ---
elif st.session_state.page == "Berichte & Analyse":
    st.header("Berichte & Analyse")

    if not st.session_state.tasks:
        st.info("Keine Aufgaben zum Erstellen von Berichten vorhanden.")
    else:
        df_tasks = pd.DataFrame([task.to_dict() for task in st.session_state.tasks])
        
        # Konvertiere due_date und created_at zu datetime Objekten
        df_tasks['due_date'] = pd.to_datetime(df_tasks['due_date'], errors='coerce')
        df_tasks['created_at'] = pd.to_datetime(df_tasks['created_at'], errors='coerce')
        df_tasks['completed_at'] = pd.to_datetime(df_tasks['completed_at'], errors='coerce')

        st.subheader("Aufgabenstatus-Verteilung")
        status_counts = df_tasks['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Anzahl']
        fig_status_pie = px.pie(status_counts, values='Anzahl', names='Status', title='Verteilung der Aufgaben nach Status')
        st.plotly_chart(fig_status_pie, use_container_width=True)

        st.subheader("Aufgaben nach Priorität")
        priority_counts = df_tasks['priority'].value_counts().reset_index()
        priority_counts.columns = ['Priorität', 'Anzahl']
        # Sortiere nach der gewünschten Prioritätsreihenfolge
        priority_order_list = ["Urgent", "High", "Medium", "Low"]
        priority_counts['Priorität'] = pd.Categorical(priority_counts['Priorität'], categories=priority_order_list, ordered=True)
        priority_counts = priority_counts.sort_values('Priorität')
        fig_priority_bar = px.bar(priority_counts, x='Priorität', y='Anzahl', title='Anzahl der Aufgaben nach Priorität', color='Priorität')
        st.plotly_chart(fig_priority_bar, use_container_width=True)

        st.subheader("Aufgaben-Erstellung über die Zeit")
        df_tasks['creation_date'] = df_tasks['created_at'].dt.to_period('D') # Gruppierung nach Tag
        daily_creations = df_tasks['creation_date'].value_counts().sort_index().reset_index()
        daily_creations.columns = ['Datum', 'Anzahl']
        daily_creations['Datum'] = daily_creations['Datum'].astype(str) # Für Plotly X-Achse
        fig_time_series = px.line(daily_creations, x='Datum', y='Anzahl', title='Anzahl der täglich erstellten Aufgaben')
        st.plotly_chart(fig_time_series, use_container_width=True)

        st.subheader("Durchschnittliche Erledigungszeit (für abgeschlossene Aufgaben)")
        completed_df = df_tasks[df_tasks['status'] == 'Completed'].copy()
        if not completed_df.empty:
            completed_df['time_to_complete'] = (completed_df['completed_at'] - completed_df['created_at']).dt.days
            avg_completion_time = completed_df['time_to_complete'].mean()
            if not pd.isna(avg_completion_time):
                st.info(f"Die durchschnittliche Zeit bis zur Erledigung einer Aufgabe beträgt: **{avg_completion_time:.2f} Tage**")
            else:
                st.info("Es gibt nicht genügend Daten, um die durchschnittliche Erledigungszeit zu berechnen (Stellen Sie sicher, dass sowohl Erstellungs- als auch Abschlussdaten vorhanden sind).")
            
            # Histogramm der Erledigungszeiten
            fig_completion_hist = px.histogram(completed_df, x='time_to_complete', nbins=10, title='Verteilung der Erledigungszeiten (in Tagen)')
            st.plotly_chart(fig_completion_hist, use_container_width=True)

        else:
            st.info("Keine abgeschlossenen Aufgaben zum Analysieren der Erledigungszeit vorhanden.")

        st.subheader("Aufgaben nach zugewiesener Person")
        assigned_to_counts = df_tasks['assigned_to'].value_counts().reset_index()
        assigned_to_counts.columns = ['Zugewiesen an', 'Anzahl']
        if not assigned_to_counts.empty:
            fig_assigned_to = px.bar(assigned_to_counts, x='Zugewiesen an', y='Anzahl', title='Anzahl der Aufgaben pro zugewiesener Person', color='Zugewiesen an')
            st.plotly_chart(fig_assigned_to, use_container_width=True)
        else:
            st.info("Keine Aufgaben mit Zuweisungen gefunden.")

        st.subheader("Aufgaben nach Tags")
        all_tags_flat = [tag for sublist in df_tasks['tags'].dropna() for tag in sublist]
        if all_tags_flat:
            tag_counts = pd.Series(all_tags_flat).value_counts().reset_index()
            tag_counts.columns = ['Tag', 'Anzahl']
            fig_tags = px.bar(tag_counts, x='Tag', y='Anzahl', title='Anzahl der Aufgaben pro Tag', color='Tag')
            st.plotly_chart(fig_tags, use_container_width=True)
        else:
            st.info("Keine Tags für Aufgaben gefunden.")


# --- Einstellungen ---
elif st.session_state.page == "Einstellungen":
    st.header("Einstellungen")
    st.write("Hier können Sie allgemeine Einstellungen für den Task Manager vornehmen.")

    # Option zur manuellen Auslösung der wiederkehrenden Aufgaben
    st.subheader("Manuelle Generierung wiederkehrender Aufgaben")
    st.write("Klicken Sie hier, um aus abgeschlossenen Aufgaben neue, wiederkehrende Aufgabeninstanzen zu generieren.")
    if st.button("Jetzt wiederkehrende Aufgaben generieren"):
        generate_recurring_tasks()

    st.subheader("Datenmanagement")
    st.write("Hier können Sie Ihre Aufgabenliste exportieren oder importieren.")

    # Exportieren der Aufgaben
    tasks_data_for_export = [task.to_dict() for task in st.session_state.tasks]
    json_export_str = json.dumps(tasks_data_for_export, indent=4, ensure_ascii=False)
    st.download_button(
        label="Aufgaben als JSON exportieren",
        data=json_export_str,
        file_name="tasks_export.json",
        mime="application/json"
    )

    # Importieren von Aufgaben
    st.markdown("---")
    st.subheader("Aufgaben importieren")
    uploaded_file = st.file_uploader("Wählen Sie eine JSON-Datei mit Aufgaben zum Import", type="json")
    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            if isinstance(imported_data, list):
                new_tasks = []
                for task_data in imported_data:
                    # Um Konflikte zu vermeiden, vergeben wir neue IDs für importierte Aufgaben
                    task_data["id"] = st.session_state.next_task_id
                    new_task = Task.from_dict(task_data)
                    new_tasks.append(new_task)
                    st.session_state.next_task_id += 1
                
                st.session_state.tasks.extend(new_tasks)
                save_tasks(st.session_state.tasks)
                st.success(f"{len(new_tasks)} Aufgaben erfolgreich importiert!")
                st.rerun()
            else:
                st.error("Die importierte JSON-Datei sollte eine Liste von Aufgabenobjekten enthalten.")
        except json.JSONDecodeError:
            st.error("Fehler beim Dekodieren der JSON-Datei. Bitte stellen Sie sicher, dass es sich um eine gültige JSON-Datei handelt.")
        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    st.markdown("---")
    st.subheader("Alle Aufgaben löschen")
    st.warning("⚠️ Achtung: Diese Aktion löscht unwiderruflich ALLE Ihre Aufgaben. Gehen Sie mit Vorsicht vor.")
    if st.button("ALLE Aufgaben löschen (Bestätigung erforderlich!)", key="delete_all_tasks_settings_button"):
        st.session_state.confirm_delete_all = True
    
    if st.session_state.confirm_delete_all:
        st.error("Bestätigen Sie: Sind Sie sicher, dass Sie ALLE Aufgaben dauerhaft löschen möchten?")
        col_confirm_all_settings, col_cancel_all_settings = st.columns(2)
        with col_confirm_all_settings:
            if st.button("Ja, alle Aufgaben löschen", key="confirm_delete_all_settings_action"):
                delete_all_tasks_confirmed()
        with col_cancel_all_settings:
            if st.button("Nein, abbrechen", key="cancel_delete_all_settings_action"):
                st.session_state.confirm_delete_all = False
                st.rerun()