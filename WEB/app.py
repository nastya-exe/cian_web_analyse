from flask import Flask, render_template

from utils.info_from_bd import top_five_ads, premises_quantity, histogram_info, all_name_metro, number_ads_today, number_active_ads
from config import database_url

app = Flask(__name__)


@app.route('/')
def start_page():
    name_metro = [name[0] for name in all_name_metro(database_url)]
    metro_max = top_five_ads(database_url, 'max')
    metro_min = top_five_ads(database_url, 'min')

    type_premises = premises_quantity(database_url)

    hist_info = histogram_info(database_url)

    all_active_ads = number_active_ads(database_url)
    ads_today = number_ads_today(database_url)

    return render_template('main.html',
                           metro_max=metro_max,
                           metro_min=metro_min,
                           type_premises=type_premises,
                           hist_info=hist_info,
                           name_metro=name_metro,
                           all_active_ads=all_active_ads,
                           ads_today=ads_today,)

@app.route('/all-ads')
def all_ads_page():
    name_metro = [name[0] for name in all_name_metro(database_url)]
    metro_max = top_five_ads(database_url, 'max')
    metro_min = top_five_ads(database_url, 'min')

    type_premises = premises_quantity(database_url)

    hist_info = histogram_info(database_url)

    all_active_ads = number_active_ads(database_url)
    ads_today = number_ads_today(database_url)
    return render_template('all_ads.html',
                           metro_max=metro_max,
                           metro_min=metro_min,
                           type_premises=type_premises,
                           hist_info=hist_info,
                           name_metro=name_metro,
                           all_active_ads=all_active_ads,
                           ads_today=ads_today, )


# @app.route('/predict')
# def predict_page():
#     return render_template('predict.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
