# LifeLog

A personal life-tracking desktop app built with Python and Tkinter. LifeLog combines to-dos, habits, mood, journaling, goals, and water intake in one dashboard, with all data stored locally in SQLite.

## Features

- **Dashboard**: today's task count, current habit streak, today's mood, and quick links to each section.
- **To-Do List**: add, reorder, complete, and delete tasks.
- **Habit Tracker**: weekly check-ins per habit, with current and best streaks.
- **Mood Tracker**: one mood per day (Awful → Great) and a history view.
- **Journal**: titled entries shown as a card grid; create, edit, and delete.
- **Goals**: short-term, long-term, or untagged goals, each with sub-goals.
- **Health**: daily water intake against an adjustable goal (64 oz default). Sleep, exercise, and supplement logs are planned.

## Tech Stack

- Python 3
- Tkinter / ttk for the GUI
- SQLite (standard-library `sqlite3`) for storage

No third-party packages required.

## Project Structure

```
LifeLog/
├── main.py              # Entry point and page navigation
├── database/            # Data access layer, one module per feature
└── page_guis/           # Tkinter screens, one module per feature
```

Each screen talks to its matching database module, so the UI never writes SQL directly.

## Getting Started

Requires Python 3.8+ with Tkinter (on some Linux distributions, install `python3-tk`).

```bash
git clone https://github.com/spgharpure/LifeLog.git
cd LifeLog
python main.py
```

Run from the project root. On first launch, `lifelog.db` is created in that directory with all tables set up.

## Data Storage

Everything lives in `lifelog.db`: tasks, habits and check-ins, moods, journal entries, goals and sub-goals, and the daily water log. The file is listed in `.gitignore`, so personal data stays out of the repository.

## Roadmap

- Sleep, exercise, and supplement logs
- Historical views for water intake and tasks

## Contributing

Issues and suggestions are welcome. For code changes, please open an issue first to discuss the approach.

## License

No license has been specified yet.
