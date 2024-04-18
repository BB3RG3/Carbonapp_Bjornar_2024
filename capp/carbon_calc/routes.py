from flask import (Blueprint,
    render_template,
    redirect, 
    url_for,
    flash)
from datetime import (timedelta,
    datetime)
from flask_login import (login_required,
    current_user)
from capp.carbon_calc.forms import (BusForm,
    CarForm,
    PlaneForm,
    FerryForm,
    TrainForm,
    MotorbikeForm,
    BicycleForm,
    WalkForm,
    SpecificCarForm)
from capp.carbon_interface.api import CarbonAPI
from capp.models import Transport
from capp import db
import json

carbon_calc = Blueprint('carbon_calc',__name__)
api = CarbonAPI()

# Emissions factor per transport in kg per passemger km
efco2={'Bus':{'Diesel':0.105,'Electric':0.03052,'Hybrid':0.054},
    'Car':{'Gasoline':0.0384,'Diesel':0.0343,'Hybrid':0.0298,'Electric':0.0106,'Hydrogen':0},
    'Plane':{'Short-haul (Buisness)':0.147,
             'Long-haul (Economy)': 0.235, 
             'Long-haul (Premium economy)': 0.427, 
             'Long-haul (First-class)': 0.558, 
             'International (Economy)': 0.140,
             'International (Premium economy)': 0.229,
             'International (Buisness)': 0.406,
             'International (First Class)': 0.560},
    'Ferry':{'Regular':0.226, 'High-speed':0.452},
    'Train':{'Diesel':0.091, 'Electric (Nordic)':0.024, 'Electric (EU)': 0.007},
    'Motorbike':{'≤125cc':0.0415,'125cc to 500cc':0.0505, '>500cc':0.0665,},
    'Bicycle':{'No Fossil Fuel':0},
    'Walk':{'No Fossil Fuel':0}}

# Carbon app, main page
@carbon_calc.route('/carbon_calc')
@login_required
def carbon_calc_home():
    return render_template('carbon_calc/carbon_calc.html', title='carbon_calc')

# New entry bus
@carbon_calc.route('/carbon_calc/new_entry_bus', methods=['GET','POST'])
@login_required
def new_entry_bus():
    form = BusForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data 
        transport = 'Bus'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = (float(kms) * efco2[transport][fuel]) / 70 # Divided by passenger(s)

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_bus.html', title='new entry bus', form=form)

# New entry car
@carbon_calc.route('/carbon_calc/new_entry_car', methods=['GET','POST'])
@login_required
def new_entry_car():
    form = CarForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Car'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = (float(kms) * efco2[transport][fuel]) / 4

        co2 = float("{:.2f}".format(co2))
    
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_car.html', title='new entry car', form=form)    

# New entry specific car
@carbon_calc.route('/carbon_calc/new_entry_specific_car', methods=['GET','POST'])
@login_required
def new_entry_specific_car():
    form = SpecificCarForm()
    if form.validate_on_submit():
        kms = form.kms.data
        model = form.model.data
        transport = "Specified Car"
        fuel = "N/A"
        
        estimate = api.getEstimate(id=model, distance=kms)
        co2 = estimate["data"]["attributes"]["carbon_kg"]
        co2 = int(co2)/4

        co2 = float("{:.2f}".format(co2))
    
        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_specific_car.html', title='new entry specific car', form=form)


# New entry plane
@carbon_calc.route('/carbon_calc/new_entry_plane', methods=['GET','POST'])
@login_required
def new_entry_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Plane'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = (float(kms) * efco2[transport][fuel]) / 100 # average amount of passengers (for all types of flights)

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_plane.html', title='new entry plane', form=form)  

# New entry ferry
@carbon_calc.route('/carbon_calc/new_entry_ferry', methods=['GET','POST'])
@login_required
def new_entry_ferry():
    form = FerryForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Ferry'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = (float(kms) * efco2[transport][fuel]) / 309

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_ferry.html', title='new entry ferry', form=form)     

# New entry motorbike
@carbon_calc.route('/carbon_calc/new_entry_motorbike', methods=['GET','POST'])
@login_required
def new_entry_motorbike():
    form = MotorbikeForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Motorbike'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = float(kms) * efco2[transport][fuel]

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_motorbike.html', title='new entry motorbike', form=form) 

@carbon_calc.route('/carbon_calc/new_entry_train', methods=['GET','POST'])
@login_required
def new_entry_train():
    form = TrainForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Train'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = float(kms) * efco2[transport][fuel]

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_train.html', title='new entry train', form=form) 

# New entry bicycle
@carbon_calc.route('/carbon_calc/new_entry_bicycle', methods=['GET','POST'])
@login_required
def new_entry_bicycle():
    form = BicycleForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Bicycle'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = float(kms) * efco2[transport][fuel]

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_bicycle.html', title='new entry bicycle', form=form)

# New entry walk
@carbon_calc.route('/carbon_calc/new_entry_walk', methods=['GET','POST'])
@login_required
def new_entry_walk():
    form = WalkForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = 'Walk'
        # kms = request.form['kms']
        # fuel = request.form['fuel_type']

        co2 = float(kms) * efco2[transport][fuel]

        co2 = float("{:.2f}".format(co2))

        emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, author=current_user)
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_calc.your_data'))
    return render_template('carbon_calc/new_entry_walk.html', title='new entry walk', form=form)

# Your data
@carbon_calc.route('/carbon_calc/your_data')
@login_required
def your_data():
    # Table
    entries = Transport.query.filter_by(author=current_user). \
        filter(Transport.date> (datetime.now() - timedelta(days=5))).\
        order_by(Transport.date.desc()).order_by(Transport.transport.asc()).all()
    
    # Emissions by category
    emissions_by_transport = db.session.query(db.func.sum(Transport.co2), Transport.transport). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.transport).order_by(Transport.transport.asc()).all()
    emission_transport = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    first_tuple_elements = []
    second_tuple_elements = []
    for a_tuple in emissions_by_transport:
        first_tuple_elements.append(a_tuple[0])
        second_tuple_elements.append(a_tuple[1])

    if 'Bus' in second_tuple_elements:
        index_bus = second_tuple_elements.index('Bus')
        emission_transport[0]=first_tuple_elements[index_bus]
    else:
        emission_transport[0]

    if 'Car' in second_tuple_elements:
        index_car = second_tuple_elements.index('Car')
        emission_transport[1]=first_tuple_elements[index_car]
    else:
        emission_transport[1]
    
    if 'Specified Car' in second_tuple_elements:
        index_specified_car = second_tuple_elements.index('Specified Car')
        emission_transport[2]=first_tuple_elements[index_specified_car]
    else:
        emission_transport[2]

    if 'Ferry' in second_tuple_elements:
        index_ferry = second_tuple_elements.index('Ferry')
        emission_transport[3]=first_tuple_elements[index_ferry]
    else:
        emission_transport[3]

    if 'Motorbike' in second_tuple_elements:
        index_motorbike = second_tuple_elements.index('Motorbike')
        emission_transport[4]=first_tuple_elements[index_motorbike]
    else:
        emission_transport[4]

    if 'Plane' in second_tuple_elements:
        index_plane = second_tuple_elements.index('Plane')
        emission_transport[5]=first_tuple_elements[index_plane]
    else:
        emission_transport[5]

    if 'Train' in second_tuple_elements:
        index_train = second_tuple_elements.index('Train')
        emission_transport[6]=first_tuple_elements[index_train]
    else:
        emission_transport[6]

    # Kilometers by category
    kms_by_transport = db.session.query(db.func.sum(Transport.kms), Transport.transport). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.transport).order_by(Transport.transport.asc()).all()
    kms_transport = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    first_tuple_elements = []
    second_tuple_elements = []
    for a_tuple in kms_by_transport:
        first_tuple_elements.append(a_tuple[0])
        second_tuple_elements.append(a_tuple[1])

    if 'Bicycle' in second_tuple_elements:
        index_bicycle = second_tuple_elements.index('Bicycle')
        kms_transport[0]=first_tuple_elements[index_bicycle]
    else:
        kms_transport[0] 

    if 'Bus' in second_tuple_elements:
        index_bus = second_tuple_elements.index('Bus')
        kms_transport[1]=first_tuple_elements[index_bus]
    else:
        kms_transport[1]

    if 'Car' in second_tuple_elements:
        index_car = second_tuple_elements.index('Car')
        kms_transport[2]=first_tuple_elements[index_car]
    else:
        kms_transport[2]

    if 'Specified Car' in second_tuple_elements:
        index_specified_car = second_tuple_elements.index('Specified Car')
        kms_transport[3]=first_tuple_elements[index_specified_car]
    else:
        kms_transport[3]

    if 'Ferry' in second_tuple_elements:
        index_ferry = second_tuple_elements.index('Ferry')
        kms_transport[4]=first_tuple_elements[index_ferry]
    else:
        kms_transport[4]

    if 'Motorbike' in second_tuple_elements:
        index_motorbike = second_tuple_elements.index('Motorbike')
        kms_transport[5]=first_tuple_elements[index_motorbike]
    else:
        kms_transport[5]

    if 'Plane' in second_tuple_elements:
        index_plane = second_tuple_elements.index('Plane')
        kms_transport[6]=first_tuple_elements[index_plane]
    else:
        kms_transport[6]

    if 'Train' in second_tuple_elements:
        index_train = second_tuple_elements.index('Train')
        kms_transport[7]=first_tuple_elements[index_train]
    else:
        kms_transport[7]     

    if 'Walk' in second_tuple_elements:
        index_walk = second_tuple_elements.index('Walk')
        kms_transport[8]=first_tuple_elements[index_walk]
    else:
        kms_transport[8]    

    # Emissions by date (individual)
    emissions_by_date = db.session.query(db.func.sum(Transport.co2), Transport.date). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.date).order_by(Transport.date.asc()).all()
    over_time_emissions = []
    dates_label = []
    for total, date in emissions_by_date:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_emissions.append(total)    

    # Kms by date (individual)
    kms_by_date = db.session.query(db.func.sum(Transport.kms), Transport.date). \
        filter(Transport.date > (datetime.now() - timedelta(days=5))).filter_by(author=current_user). \
        group_by(Transport.date).order_by(Transport.date.asc()).all()
    over_time_kms = []
    dates_label = []
    for total, date in kms_by_date:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_kms.append(total)      

    return render_template('carbon_calc/your_data.html', title='your_data', entries=entries,
        emissions_by_transport_python_dic=emissions_by_transport,     
        emission_transport_python_list=emission_transport,             
        emissions_by_transport=json.dumps(emission_transport),
        kms_by_transport=json.dumps(kms_transport),
        over_time_emissions=json.dumps(over_time_emissions),
        over_time_kms=json.dumps(over_time_kms),
        dates_label=json.dumps(dates_label))

# Delete emission
@carbon_calc.route('/carbon_calc/delete-emission/<int:entry_id>')
def delete_emission(entry_id):
    entry = Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_calc.your_data'))
    