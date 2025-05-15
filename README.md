# 🧬 MySQL CSV Seeder Project

This project contains a Python script that:
- Connects to a MySQL database
- Creates a database called `ALX_prodev` (if it doesn't exist)
- Creates a table called `user_data` (if it doesn't exist)
- Reads a CSV file (`user_data.csv`) with user information (name, email, age)
- Generates a unique `user_id` for each user
- Inserts the user data into the table

---

## 📦 Folder Structure

python generator project/
│
├── seed.py # Python script that handles DB setup and data seeding
├── user_data.csv # Your input data file (name, email, age)
├── README.md # This readme file


---

## 🛠️ Requirements

- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) (optional GUI)
- Python 3.x
- Python package: `mysql-connector-python`

### ✅ Install mysql-connector-python

```bash
pip install mysql-connector-python
