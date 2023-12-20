from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(api_key='')
from codecarbon import EmissionsTracker



app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_code = request.form['code_input']

        # Calculate CO2 Emissions for Original Code
        tracker = EmissionsTracker()
        tracker.start()
        execute_user_code(user_code)  # Execute user's original code
        emissions_original = tracker.stop()

        # Optimize and execute the optimized code
        optimized_code = optimize_code(user_code)
        tracker.start()
        execute_user_code(optimized_code)  # Execute optimized code
        emissions_optimized = tracker.stop()

        # Format emissions data as a string in kg
        emissions_original_str = "{:.11f} kg".format(emissions_original)
        emissions_optimized_str = "{:.11f} kg".format(emissions_optimized)

        return render_template('index.html', 
                               original_code=user_code, 
                               optimized_code=optimized_code, 
                               emissions_original=emissions_original_str, 
                               emissions_optimized=emissions_optimized_str)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)