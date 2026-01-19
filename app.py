from flask import Flask, render_template, request
from main import main
from car_api import get_car_years, get_car_makes, get_car_models, get_car_submodels

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

if __name__ == '__main__':
    app.run(debug=True)