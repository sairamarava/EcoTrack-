from flask import Flask, render_template, request
app = Flask(__name__)

# Emission factors
EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal
        "Waste": 0.1   # kgCO2/kg
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate')
def calculator():
    return render_template('calculate.html')

@app.route('/result', methods=['POST'])
def calculate():
    # Retrieve input from the form
    country = request.form.get('country', 'India')
    waste = float(request.form.get('waste', 0))
    commute = float(request.form.get('commute', 0))
    meals = int(request.form.get('meals', 0))
    electricity = float(request.form.get('electricity', 0))
    
    # Calculate emissions
    factors = EMISSION_FACTORS.get(country, EMISSION_FACTORS["India"])
    waste_emissions = waste * factors["Waste"]
    commute_emissions = commute * factors["Transportation"]
    diet_emissions = meals * factors["Diet"]
    electricity_emissions = electricity * factors["Electricity"]

    total_emissions = waste_emissions + commute_emissions + diet_emissions + electricity_emissions

    # Pass the data to the result page
    return render_template(
        'result.html',
        country=country,
        waste_emissions=waste_emissions,
        commute_emissions=commute_emissions,
        diet_emissions=diet_emissions,
        electricity_emissions=electricity_emissions,
        total_emissions=total_emissions
    )

if __name__ == '__main__':
    app.run(debug=True)
