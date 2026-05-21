import sqlite3
from flask import Flask, render_template, jsonify, request
from moead_engine import MOEAD_MEC
import numpy as np
import threading
import time


app = Flask(__name__)
DB_NAME = "mec_history.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS history 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             tasks INTEGER,
             congestion REAL,
             avg_latency REAL,
             avg_energy REAL,
             solutions_found INTEGER)''')
    conn.close()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/run-optimization', methods=['POST'])
def run_optimization():
    tasks = int(request.form.get('tasks', 10))
    congestion = float(request.form.get('congestion', 0.5))
    
    # Initialize Engine
    engine = MOEAD_MEC(num_tasks=tasks)
    engine.weights = np.linspace(congestion, 1.0, engine.n_subproblems)
    
    pareto_solutions = engine.run()
    
    # Process valid solutions
    valid_data = []
    for ind in pareto_solutions:
        if ind.fitness.values[0] < 9000:
            valid_data.append({
                "latency": round(ind.fitness.values[0], 2),
                "energy": round(ind.fitness.values[1], 2)
            })
    
    # Calculate Averages for History
    if valid_data:
        avg_lat = sum(d['latency'] for d in valid_data) / len(valid_data)
        avg_eng = sum(d['energy'] for d in valid_data) / len(valid_data)
        
        # Store in SQLite
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''INSERT INTO history (tasks, congestion, avg_latency, avg_energy, solutions_found)
                            VALUES (?, ?, ?, ?, ?)''', 
                         (tasks, congestion, avg_lat, avg_eng, len(valid_data)))
    
    return jsonify(valid_data)

@app.route('/history', methods=['GET'])
def get_history():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        return jsonify([dict(row) for row in rows])


is_auto_running = False

def background_optimizer():
    """Background task that runs when toggle is ON"""
    global is_auto_running
    while True:
        if is_auto_running:
            # Simulate an auto-run with random congestion
            tasks = 10
            congestion = np.random.uniform(0.1, 0.9)
            
            engine = MOEAD_MEC(num_tasks=tasks)
            # Logic to run and save to DB (Reuse your existing logic here)
            # ... (Algorithm 1 and 2 execution) ...
            
            print(f"Auto-Optimization complete: Congestion {congestion:.2f}")
        time.sleep(5) # Run every 5 seconds

@app.route('/toggle-auto', methods=['POST'])
def toggle_auto():
    global is_auto_running
    is_auto_running = not is_auto_running
    return jsonify({"status": "success", "auto_mode": is_auto_running})

# ... (keep existing /history and /run-optimization routes)

if __name__ == '__main__':
    init_db()
    # Start the background thread
    threading.Thread(target=background_optimizer, daemon=True).start()
    app.run(debug=True)
    