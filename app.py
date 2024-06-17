from flask import Flask, render_template, request
from openai import OpenAI
import time
from codecarbon import EmissionsTracker
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

client = OpenAI(api_key='')

app = Flask(__name__)

metrics = {
    "code_samples": [],
    "emissions_original": [],
    "emissions_optimized": [],
    "execution_time_original": [],
    "execution_time_optimized": [],
    "emissions_gpt_optimize": [],
    "time_gpt_optimize": []
}

def analyze_code(code):
    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Check this code for errors: \n{code}"}
        ])
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
    
def optimize_code(code):
    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Optimize this code for better efficiency and lower energy consumption: \n{code}"}
        ])
        optimized_response = response.choices[0].message.content
        return optimized_response
    except Exception as e:
        return str(e)

def execute_user_code(code):
    # IMPORTANT: Implement a secure method to execute user code
    # The following is a simplified example and should not be used in production
    try:
        exec(code)
    except Exception as e:
        return str(e)

def measure_gpt_metrics(code, function):
    tracker = EmissionsTracker()
    tracker.start()
    start_time = time.time()
    result = function(code)
    end_time = time.time()
    emissions = tracker.stop()
    execution_time = end_time - start_time
    return emissions, execution_time, result

def plot_metrics():
    x = list(range(1, len(metrics["code_samples"]) + 1))

    fig = make_subplots(rows=2, cols=2, subplot_titles=("CO2 Emissions", "Execution Time", "GPT Optimization Emissions", "GPT Optimization Time"))

    fig.add_trace(go.Scatter(x=x, y=metrics["emissions_original"], mode='lines+markers', name='Original Code Emissions'), row=1, col=1)
    fig.add_trace(go.Scatter(x=x, y=metrics["emissions_optimized"], mode='lines+markers', name='Optimized Code Emissions'), row=1, col=1)
    fig.update_xaxes(title_text="Code Sample", row=1, col=1)
    fig.update_yaxes(title_text="Emissions (kg)", row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=metrics["execution_time_original"], mode='lines+markers', name='Original Code Time'), row=1, col=2)
    fig.add_trace(go.Scatter(x=x, y=metrics["execution_time_optimized"], mode='lines+markers', name='Optimized Code Time'), row=1, col=2)
    fig.update_xaxes(title_text="Code Sample", row=1, col=2)
    fig.update_yaxes(title_text="Time (seconds)", row=1, col=2)

    fig.add_trace(go.Scatter(x=x, y=metrics["emissions_gpt_optimize"], mode='lines+markers', name='GPT Optimization Emissions'), row=2, col=1)
    fig.update_xaxes(title_text="Code Sample", row=2, col=1)
    fig.update_yaxes(title_text="Emissions (kg)", row=2, col=1)

    fig.add_trace(go.Scatter(x=x, y=metrics["time_gpt_optimize"], mode='lines+markers', name='GPT Optimization Time'), row=2, col=2)
    fig.update_xaxes(title_text="Code Sample", row=2, col=2)
    fig.update_yaxes(title_text="Time (seconds)", row=2, col=2)

    fig.update_layout(height=800, width=1000, title_text="Performance Metrics")

    return pio.to_html(fig, full_html=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_code = request.form['code_input']

        # Track emissions and execution time for original code
        tracker_original = EmissionsTracker()
        tracker_original.start()
        start_time_original = time.time()
        execute_user_code(user_code)  # Execute user's original code
        end_time_original = time.time()
        emissions_original = tracker_original.stop()

        # Optimize the code
        emissions_gpt_optimize, time_gpt_optimize, optimized_code = measure_gpt_metrics(user_code, optimize_code)

        # Track emissions and execution time for optimized code
        tracker_optimized = EmissionsTracker()
        tracker_optimized.start()
        start_time_optimized = time.time()
        execute_user_code(optimized_code)  # Execute optimized code
        end_time_optimized = time.time()
        emissions_optimized = tracker_optimized.stop()

        # Calculate compile and execution times
        execution_time_original = end_time_original - start_time_original
        execution_time_optimized = end_time_optimized - start_time_optimized

        # Store metrics
        metrics["code_samples"].append(user_code)
        metrics["emissions_original"].append(emissions_original)
        metrics["emissions_optimized"].append(emissions_optimized)
        metrics["execution_time_original"].append(execution_time_original)
        metrics["execution_time_optimized"].append(execution_time_optimized)
        metrics["emissions_gpt_optimize"].append(emissions_gpt_optimize)
        metrics["time_gpt_optimize"].append(time_gpt_optimize)

        # Format emissions data as a string in kg
        emissions_original_str = "{:.11f} kg".format(emissions_original)
        emissions_optimized_str = "{:.11f} kg".format(emissions_optimized)
        emissions_gpt_optimize_str = "{:.11f} kg".format(emissions_gpt_optimize)

        # Generate plot
        plot_html = plot_metrics()

        return render_template('index.html', 
                               original_code=user_code, 
                               optimized_code=optimized_code, 
                               emissions_original=emissions_original_str, 
                               emissions_optimized=emissions_optimized_str,
                               execution_time_original="{:.4f} seconds".format(execution_time_original),
                               execution_time_optimized="{:.4f} seconds".format(execution_time_optimized),
                               emissions_gpt_optimize=emissions_gpt_optimize_str,
                               time_gpt_optimize="{:.4f} seconds".format(time_gpt_optimize),
                               plot_html=plot_html)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

