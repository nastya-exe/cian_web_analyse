from flask import Flask, render_template, request

from utils.info_from_bd import InfoBd
from config import database_url

app = Flask(__name__)


def variables_start(active):
    info = InfoBd(database_url, is_active=active)

    name_metro = [name[0] for name in info.all_name_metro()]
    metro_max = info.top_five_ads(max_min='max')
    metro_min = info.top_five_ads(max_min='min')

    type_premises = info.premises_quantity()

    hist_info = info.histogram_info()

    all_active_ads = info.all_ads()
    ads_today = info.number_ads_today()
    total = InfoBd(database_url).all_ads()

    return {
        'name_metro': name_metro,
        'metro_max': metro_max,
        'metro_min': metro_min,
        'type_premises': type_premises,
        'hist_info': hist_info,
        'ads_today': ads_today,
        'all_active_ads': all_active_ads,
        'total': total
    }


@app.route('/')
def start_page():
    variable = variables_start('yes')

    return render_template('start.html', **variable)


@app.route('/all-ads')
def all_ads_page():
    variable = variables_start('no')

    return render_template('all_ads.html', **variable)


@app.route('/request')
def request_page_active():
    metro = request.args.get('metro')
    price = request.args.get('price')
    rooms = request.args.get('rooms')
    typ = request.args.get('type_premises').lower()
    active = request.args.get('active', 'yes')

    is_active = active == 'yes'

    info = InfoBd(database_url, active, metro, price, rooms, typ)

    hist_info = info.histogram_info()
    metro_max = info.top_five_ads('max')
    metro_min = info.top_five_ads('min')
    ads_today = info.number_ads_today()
    all_active_ads = info.all_ads()
    type_premises = info.premises_quantity()
    html = 'request.html' if is_active else 'request_all_ads.html'

    return render_template(html,
                           metro_max=metro_max,
                           metro_min=metro_min,
                           type_premises=type_premises,
                           hist_info=hist_info,
                           ads_today=ads_today,
                           all_active_ads=all_active_ads)


@app.route('/predict')
def predict_page():
    return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
