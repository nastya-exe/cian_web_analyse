from flask import Flask, render_template, request

from utils.info_from_bd import top_five_ads, premises_quantity, histogram_info, all_name_metro, number_ads_today, \
    all_ads
from config import database_url

app = Flask(__name__)


def variables_start(active):
    name_metro = [name[0] for name in all_name_metro(database_url)]
    metro_max = top_five_ads(database_url, 'max', active)
    metro_min = top_five_ads(database_url, 'min', active)

    type_premises = premises_quantity(database_url, active)

    hist_info = histogram_info(database_url, active)

    all_active_ads = all_ads(database_url, active)
    ads_today = number_ads_today(database_url)
    total = all_ads(database_url, active)

    return {
        'name_metro': name_metro,
        'metro_max': metro_max,
        'metro_min': metro_min,
        'type_premises': type_premises,
        'hist_info': hist_info,
        'ads_today': ads_today,
        'all_active_ads': all_active_ads,
        'total': total}


@app.route('/')
def start_page():
    variable = variables_start(True)

    return render_template('start.html', **variable)


@app.route('/all-ads')
def all_ads_page():
    variable = variables_start(False)

    return render_template('all_ads.html', **variable)


@app.route('/request')
def request_page_active():
    metro = request.args.get('metro')
    price = request.args.get('price')
    rooms = request.args.get('rooms')
    typ = request.args.get('type_premises').lower()
    active = request.args.get('active', 'yes')

    is_active = active == 'yes'

    hist_info = histogram_info(database_url, is_active, metro, price, rooms, typ)
    metro_max = top_five_ads(database_url, 'max', is_active)
    metro_min = top_five_ads(database_url, 'min', is_active)
    ads_today = number_ads_today(database_url, metro, price, rooms, typ)
    all_active_ads = all_ads(database_url, is_active, metro, price, rooms, typ)
    type_premises = premises_quantity(database_url, is_active, metro, price, rooms, typ)
    html = 'request.html' if is_active else 'request_all_ads.html'

    return render_template(html,
                           metro_max=metro_max,
                           metro_min=metro_min,
                           type_premises=type_premises,
                           hist_info=hist_info,
                           ads_today=ads_today,
                           all_active_ads=all_active_ads)


# @app.route('/predict')
# def predict_page():
#     return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
