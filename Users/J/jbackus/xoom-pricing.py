import scraperwiki
import json

codes = [
    'AR',
    'AU',
    'BO',
    'BR',
    'CA',
    'CL',
    'CO',
    'CR',
    'DO',
    'EC',
    'SV',
    'FR',
    'DE',
    'GT',
    'HN',
    'IN',
    'IE',
    'IT',
    'JM',
    'MX',
    'NL',
    'NI',
    'PA',
    'PE',
    'PH',
    'PL',
    'ZA',
    'ES',
    'GB',
    'UY'
]

price_points = [100, 200, 500]

def ajax_url(country_code, amount_money):
    return "https://www.xoom.com/ajax/options-xfer-amount-ajax?receiveCountryCode={!s}&sendAmount={!s}".format(country_code,amount_money)

def flatten_response(response_obj):
    res = response_obj['result']
    std = res['standardDisbursementFees']
    val = res['valueDisbursementFees']
    code = res['currencyCode']
    deposit_str = 'DEPOSIT-{!s}'.format(code)
    pickup_str  = 'PICKUP-{!s}'.format(code)
    data = {
        'identifier'    : res['countryCode'] + '-' + str(res['sendAmount']),
        'country code'  : res['countryCode'],
        'currency code' : res['currencyCode'],
        'amount money sent'    : res['sendAmount'],
        'money send limit' : res['sendLimit'],
        'fx rate'       : res['fxRate'],
        'header'        : res['headerMessage'],
        'standard deposit' : std[deposit_str] if deposit_str in std else '',
        'standard deposit original' : std[deposit_str+'-ORIG'] if deposit_str+'-ORIG' in std else '',
        'standard deposit total' : std[deposit_str+'-TOTAL'] if deposit_str+'-TOTAL' in std else '',
        'standard pickup' : std[pickup_str] if pickup_str in std else '',
        'standard pickup original' : std[pickup_str+'-ORIG'] if pickup_str+'-ORIG' in std else '',
        'standard pickup total' : std[pickup_str+'-TOTAL'] if pickup_str+'-TOTAL' in std else '',
        'value deposit' : val[deposit_str] if deposit_str in val else '',
        'value deposit original' : val[deposit_str+'-ORIG'] if deposit_str+'-ORIG' in val else '',
        'value deposit total' : val[deposit_str+'-TOTAL'] if deposit_str+'-TOTAL' in val else '',
        'value pickup' : val[pickup_str] if pickup_str in val else '',
        'value pickup original' : val[pickup_str+'-ORIG'] if pickup_str+'-ORIG' in val else '',
        'value pickup total' : val[pickup_str+'-TOTAL'] if pickup_str+'-TOTAL' in val else ''
    }
    if 'DEPOSIT' in res['disbursementTypes']:
        data['deposit fee'] = res['disbursementTypes']['DEPOSIT']['fee']
    if 'PICKUP' in res['disbursementTypes']:
        data['pickup fee'] = res['disbursementTypes']['PICKUP']['fee']
    return data

for code in codes: 
    for price in price_points: 
        resp = scraperwiki.scrape(ajax_url(code, price))
        json_resp = json.loads(resp)
        normalized = flatten_response(json_resp)
        scraperwiki.sqlite.save(unique_keys=['identifier'], data=normalized)
import scraperwiki
import json

codes = [
    'AR',
    'AU',
    'BO',
    'BR',
    'CA',
    'CL',
    'CO',
    'CR',
    'DO',
    'EC',
    'SV',
    'FR',
    'DE',
    'GT',
    'HN',
    'IN',
    'IE',
    'IT',
    'JM',
    'MX',
    'NL',
    'NI',
    'PA',
    'PE',
    'PH',
    'PL',
    'ZA',
    'ES',
    'GB',
    'UY'
]

price_points = [100, 200, 500]

def ajax_url(country_code, amount_money):
    return "https://www.xoom.com/ajax/options-xfer-amount-ajax?receiveCountryCode={!s}&sendAmount={!s}".format(country_code,amount_money)

def flatten_response(response_obj):
    res = response_obj['result']
    std = res['standardDisbursementFees']
    val = res['valueDisbursementFees']
    code = res['currencyCode']
    deposit_str = 'DEPOSIT-{!s}'.format(code)
    pickup_str  = 'PICKUP-{!s}'.format(code)
    data = {
        'identifier'    : res['countryCode'] + '-' + str(res['sendAmount']),
        'country code'  : res['countryCode'],
        'currency code' : res['currencyCode'],
        'amount money sent'    : res['sendAmount'],
        'money send limit' : res['sendLimit'],
        'fx rate'       : res['fxRate'],
        'header'        : res['headerMessage'],
        'standard deposit' : std[deposit_str] if deposit_str in std else '',
        'standard deposit original' : std[deposit_str+'-ORIG'] if deposit_str+'-ORIG' in std else '',
        'standard deposit total' : std[deposit_str+'-TOTAL'] if deposit_str+'-TOTAL' in std else '',
        'standard pickup' : std[pickup_str] if pickup_str in std else '',
        'standard pickup original' : std[pickup_str+'-ORIG'] if pickup_str+'-ORIG' in std else '',
        'standard pickup total' : std[pickup_str+'-TOTAL'] if pickup_str+'-TOTAL' in std else '',
        'value deposit' : val[deposit_str] if deposit_str in val else '',
        'value deposit original' : val[deposit_str+'-ORIG'] if deposit_str+'-ORIG' in val else '',
        'value deposit total' : val[deposit_str+'-TOTAL'] if deposit_str+'-TOTAL' in val else '',
        'value pickup' : val[pickup_str] if pickup_str in val else '',
        'value pickup original' : val[pickup_str+'-ORIG'] if pickup_str+'-ORIG' in val else '',
        'value pickup total' : val[pickup_str+'-TOTAL'] if pickup_str+'-TOTAL' in val else ''
    }
    if 'DEPOSIT' in res['disbursementTypes']:
        data['deposit fee'] = res['disbursementTypes']['DEPOSIT']['fee']
    if 'PICKUP' in res['disbursementTypes']:
        data['pickup fee'] = res['disbursementTypes']['PICKUP']['fee']
    return data

for code in codes: 
    for price in price_points: 
        resp = scraperwiki.scrape(ajax_url(code, price))
        json_resp = json.loads(resp)
        normalized = flatten_response(json_resp)
        scraperwiki.sqlite.save(unique_keys=['identifier'], data=normalized)
