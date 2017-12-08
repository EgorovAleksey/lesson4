from flask import Flask, request, redirect
import requests
import os


app = Flask(__name__)


def get_newborns_names():
    api_key = os.getenv('MOS_API', None)
    request_data = requests.get(
        'http://api.data.mos.ru/v1/datasets/2009/rows?api_key={}'.format(api_key)
    )
    return request_data.json()


def create_html_table(data, year_filter):
    if not data:
        return

    cell_headers = [
        {'Name': 'Имя'},
        {'NumberOfPersons': 'Количество человек'},
        {'Year': 'Год'},
        {'Month': 'Месяц'},
    ]

    html_table = '<!DOCTYPE html><table border=1px cellspacing = "1"><tr>'
    for cell_header in cell_headers:
        html_table += '<th align="left">{}</th>'.format(list(cell_header.values())[0])
    html_table += '</tr>'

    for newborns_name in data:
        if year_filter != newborns_name['Cells']['Year'] and year_filter:
            continue

        html_table += '<tr>'
        for cell_header in cell_headers:
            cell_data = newborns_name['Cells'][list(cell_header.keys())[0]]
            html_table += '<td>{}</td>'.format(cell_data)
        html_table += '</tr>'
    html_table += '</table>'
    return html_table


@app.route('/')
def root_index():
    return redirect('/names?year=2017')


@app.route('/names')
def names_index():
    try:
        year_filter = int(request.args.get('year', None))
    except ValueError:
        year_filter = None
    newborns_names = get_newborns_names()
    return create_html_table(newborns_names, year_filter)


if __name__ == '__main__':
    app.run()
