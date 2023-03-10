import os

import redis
from flask import Flask, request

app = Flask(__name__)
redis = redis.Redis(host=os.environ.get('REDIS', 'localhost'), decode_responses=True)


def to_json(iocs_array):
    objects = []
    for ioc_fields in iocs_array:
        obj = {}
        for i in range(1, len(ioc_fields), 2):
            obj[ioc_fields[i-1]] = ioc_fields[i]
        objects.append(obj)
    return objects


@app.route('/api/iocs/getAll')
def get_all():
    return to_json(redis.fcall('get_all_iocs', 0))


@app.route('/api/iocs/getByYear')
def get_by_year():
    selected_year = int(request.args.get('year') or 0)

    if selected_year is None or selected_year < 1800 or selected_year > 2500:
        return {'error': 'Incorrect year'}

    return redis.fcall('get_by_year', 0, selected_year)


@app.route('/api/iocs/getByYears')
def get_by_years():
    counts_per_year_array = redis.fcall('get_by_years', 0)
    counts = []
    for i in range(1, len(counts_per_year_array), 2):
        counts.append({
            'year': int(counts_per_year_array[i-1]),
            'count': int(counts_per_year_array[i])
        })
    return counts


@app.route('/api/iocs/getByMonth')
def get_by_month():
    available_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    selected_year = int(request.args.get('year') or 0)
    selected_month = int(request.args.get('month') or 0)

    if selected_month < 0 or selected_month > 11:
        return {'error': 'Incorrect month'}

    if selected_month < 10:
        selected_month = '0' + str(selected_month)
    else:
        selected_month = str(selected_month)

    if selected_year is None or selected_year < 1800 or selected_year > 2500:
        return {'error': 'Incorrect year'}

    if selected_month is None or selected_month not in available_months:
        return {'error': 'This month value is incorrect, correct values: ' + ', '.join(available_months)}

    return to_json(redis.fcall('get_by_month', 0, selected_month, selected_year))


@app.route('/api/iocs/getByQuery')
def get_by_query():
    value = str(request.args.get('query'))

    return to_json(redis.fcall('get_by_value', 0, value))


@app.route('/api/iocs/getByType')
def get_by_type():
    available_types = ['Email', 'URL', 'IP', 'Host', 'Filepath', 'Filename', 'Registry', 'MD5', 'SHA1', 'SHA256', 'CVE']
    selected_type = request.args.get('type')

    if selected_type is None or selected_type not in available_types:
        return {'error': 'This type is incorrect, correct types: ' + ', '.join(available_types)}

    return to_json(redis.fcall('get_by_type', 0, selected_type))


@app.route('/api/iocs/getByTypes')
def get_by_types():
    iocs_by_type = redis.fcall('get_by_types', 0)
    counts = []
    for i in range(1, len(iocs_by_type), 2):
        counts.append({
            'type': iocs_by_type[i-1],
            'count': iocs_by_type[i]
        })
    return counts


@app.route('/api/iocs/getById')
def get_by_id():
    ioc_id = request.args.get('id')

    ioc = redis.hgetall('ioc:id:' + ioc_id)
    article = redis.hgetall('articles:' + ioc['article_hash'])
    return {'ioc': ioc, 'article': article}


app.run(debug=True, host='0.0.0.0')
