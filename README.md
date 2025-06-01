
# 🎬 Movies_Project

The **Movies_Project** is a Python-based tool that allows you to explore and render a visual movie catalog by pulling movie data from a local SQLite database and generating an HTML movie gallery. It's organized with a clear data/backend and web/frontend separation.

---

## 📌 Project Description

This app lets you load movies from a local database and visually present them in a styled HTML file. Movie information such as title, release year, IMDb rating, and poster URL is displayed in a responsive grid layout using a template system.

---

## 🧩 Features

- Query or load movie data from a local database (`movies.db`)
- HTML movie grid generation triggered by menu option 11
- Custom HTML template with placeholders
- Built-in CSS styling for visual layout
- Modular code structure for data access and external API

---

## 🚀 How to Use

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Dependencies

Create a `.env` file in the root directory and add your API key:

```env
API_KEY='your_api_key_here'
```

### 3. Run the App

From the root of the project:

```bash
python app.py
```

You will be presented with a menu. Select option `11` to generate the HTML movie gallery.

### 4. View the Output

Open the generated `website/index.html` in your browser to view the movie showcase.

---

## 🗂️ Project Structure

```
Movies_Project/
├── .env                       # Your api key
├── app.py                     # Main script with menu and logic
├── movie_api.py               # Optional: API access and lookups
├── data/
│   ├── __init__.py
│   ├── movie_storage_sql.py   # Handles database operations
│   └── movies.db              # SQLite database with movie data
│
├── website/
│   ├── index_template.html    # HTML template with placeholders
│   ├── index.html             # Generated HTML (output)
│   └── style.css              # CSS styling
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🛠️ Technologies Used

| Purpose              | Library             |
|----------------------|---------------------|
| Database ORM         | `SQLAlchemy`        |
| Fuzzy Search Matching| `fuzzywuzzy`        |
| API Requests         | `requests`          |
| HTML Generation      | Template injection  |

---

## 👨‍💻 Example Imports

```python
from data import movie_storage_sql as storage
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import requests
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
