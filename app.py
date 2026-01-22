from flask import Flask, render_template, request
from main import main
from car_api import get_car_years, get_car_makes, get_car_models, get_car_submodels, get_car_details
from maps_api import get_directions_and_map

app = Flask(__name__)

@app.route('/')
def index():
    main_test = main()
    return render_template('index.html', main=main_test)

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
    details = get_car_details(year_chosen, make_chosen, model_chosen, submodel_chosen)
    return render_template('car_details.html', details=details, year=year_chosen, make=make_chosen, model=model_chosen, submodel=submodel_chosen)

@app.route('/trip-input', methods=['GET'])
def trip_input_form():
    return render_template('trip_input.html')

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
    print(f"Pickup: {pickup}, Dropoff: {dropoff}, Stop1: {stop1}, Stop2: {stop2}, Stop3: {stop3}, Passengers: {passengers}")

    leg_info, total_distance, total_duration, map_file, distances, durations = get_directions_and_map(
        pickup,
        dropoff,
        waypoints=[stop for stop in [stop1, stop2, stop3] if stop]
    ) if pickup and dropoff else (None, None, None, None, None, None)

    return render_template('distance.html', leg_info=leg_info, total_distance=total_distance, total_duration=total_duration, map_file=map_file, pickup=pickup, dropoff=dropoff, stop1=stop1, stop2=stop2, stop3=stop3, passengers=passengers)

@app.route('/passengers', methods=['GET'])
def passengers():
    return render_template('passengers.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)