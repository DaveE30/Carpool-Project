from flask import Flask, render_template, request, send_file
import io
from main import main
from car_api import get_car_years, get_car_makes, get_car_models, get_car_submodels, get_car_details
from maps_api import get_directions_and_map

app = Flask(__name__)

@app.route('/')
def index():
    main_test = main()
    return render_template('index.html', main=main_test)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/car-choice', methods=['GET'])
def car_choice():
    years_list = get_car_years()
    makes_list = get_car_makes()
    year_chosen = request.form.get('year')
    make_chosen = request.form.get('make')
    return render_template('car_choice.html', years=years_list, makes=makes_list, year_selected=year_chosen, make_selected=make_chosen)

@app.route('/car-choice/model', methods=['GET'])
def car_model_choice():
    year_chosen = request.args.get('year')
    make_chosen = request.args.get('make')
    models_list = get_car_models(year_chosen, make_chosen)
    model_chosen = request.args.get('model')
    return render_template('model.html', models=models_list, selected_year=year_chosen, selected_make=make_chosen, selected_model=model_chosen)  # Pass year, make, and model

@app.route('/car-choice/submodel', methods=['GET'])
def car_submodel_choice():
    year_chosen = request.args.get('year')
    make_chosen = request.args.get('make')
    model_chosen = request.args.get('model')
    submodel_chosen = request.args.get('submodel')
    submodels_list = get_car_submodels(year_chosen, make_chosen, model_chosen)
    print(submodels_list)
    return render_template('submodel.html', submodels=submodels_list, selected_year=year_chosen, selected_make=make_chosen, selected_model=model_chosen, selected_submodel=submodel_chosen)

@app.route('/car-details', methods=['GET', 'POST'])
def car_details():
    year_chosen = request.args.get('year')
    make_chosen = request.args.get('make')
    model_chosen = request.args.get('model')
    submodel_chosen = request.args.get('submodel')
    combined_mpg = request.form.get('combined_mpg')
    details = get_car_details(year_chosen, make_chosen, model_chosen, submodel_chosen)
    return render_template('car_details.html', details=details, year=year_chosen, make=make_chosen, model=model_chosen, submodel=submodel_chosen, combined_mpg=combined_mpg)

@app.route('/trip-input', methods=['GET'])
def trip_input_form():
    combined_mpg = request.args.get('combined_mpg')
    return render_template('trip_input.html', combined_mpg=combined_mpg)

@app.route('/calculate-trip', methods=['GET', 'POST'])
def trip_output():
    pickup = request.form.get('pickup')
    dropoff = request.form.get('destination')
    if stop1 := request.form.get('stop1'):
       stop1 = request.form.get('stop1')
    if stop2 := request.form.get('stop2'):
       stop2 = request.form.get('stop2')
    if stop3 := request.form.get('stop3'):
       stop3 = request.form.get('stop3')
    passengers = request.form.get('passengers')
    # combined_mpg = request.form.get('combined_mpg')
    print(f"Pickup: {pickup}, Dropoff: {dropoff}, Stop1: {stop1}, Stop2: {stop2}, Stop3: {stop3}, Passengers: {passengers}")
    combined_mpg = 27
    leg_info, total_distance, total_duration, map_file, distances, durations = get_directions_and_map(
        pickup,
        dropoff,
        waypoints=[stop for stop in [stop1, stop2, stop3] if stop]
    ) if pickup and dropoff else (None, None, None, None, None, None)

    def calculate_cost(total_distance, combined_mpg, passengers):
        gas_price_per_gallon = 2.83
        
        gas_used = total_distance / combined_mpg
        total_gas_cost = gas_used * gas_price_per_gallon
        cost_per_person = total_gas_cost / int(passengers)
        return round(cost_per_person, 2), total_gas_cost
    
    cost_per_person, total_gas_cost = calculate_cost(total_distance, combined_mpg , passengers)

    def save_report(total_distance, total_duration, leg_info, cost_per_person):
        with open("trip_report.txt", "w") as f:
            f.write("Trip Report\n")
            f.write("===========\n\n")
            f.write(f"Total Distance: {total_distance} miles\n")
            f.write(f"Total Duration: {total_duration} minutes\n\n")
            
            f.write(f"Estimated Cost Per Person: ${cost_per_person}\n")
        print("Report saved as trip_report.txt")

    save_report=save_report(total_distance, total_duration, leg_info, cost_per_person)
    


    return render_template('distance.html', leg_info=leg_info, total_distance=total_distance, total_duration=total_duration, map_file=map_file, pickup=pickup, dropoff=dropoff, stop1=stop1, stop2=stop2, stop3=stop3, passengers=passengers, cost_per_person=cost_per_person, total_gas_cost=total_gas_cost, save_report=save_report)

@app.route('/download-report', methods=['POST'])
def download_report():
    total_distance = request.form.get('total_distance')
    total_duration = request.form.get('total_duration')
    cost_per_person = request.form.get('cost_per_person')
    total_gas_cost = request.form.get('total_gas_cost')
    pickup = request.form.get('pickup')
    dropoff = request.form.get('dropoff')
    passengers = request.form.get('passengers')
  
    
    import json
 
    
    # Create the report text
    report = f"""Trip Report
=============

Pickup: {pickup}
Dropoff: {dropoff}
Passengers: {passengers}

Total Distance: {total_distance} miles
Total Duration: {total_duration} minutes
Total Gas Cost: ${total_gas_cost}
Cost Per Person: ${cost_per_person}
"""

    
    # Create a file-like object
    buffer = io.BytesIO()
    buffer.write(report.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='trip_report.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)