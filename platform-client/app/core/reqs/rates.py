import requests

from core.models import enums, models, schemas


# -- -- Get candle
def get_candle(url: str, currency_id : enums.CurrencyId, cookies : dict, type : enums.Type = enums.Type.CURRENT) -> schemas.Candle:
    # Query params
    params = {
        'currencyId' : currency_id.value,
        'type' : type.value
    }
    params_str = '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
    
    # Perform request
    print('        [$] REQUEST (GET): ' + url + params_str, end=' | ')
    response = requests.get(
        url=url,
        params=params,
        cookies=cookies,
        verify=False
    )
    
    # Check response code
    if response.status_code == 200:
        print('OK')
        data : dict = response.json()["rates"]

        # Build response code structure
        rates : models.Rates = models.Rates(
            ticker=models.Ticker(
                ticker              = data["ticker"]["ticker"],
                todaysChangePerc    = data["ticker"]["todaysChangePerc"],
                todaysChange        = data["ticker"]["todaysChange"],
                updated             = data["ticker"]["updated"],
                day                 = models.Day(
                    o   = data["ticker"]["day"]["o"],
                    h   = data["ticker"]["day"]["h"],
                    l   = data["ticker"]["day"]["l"],
                    c   = data["ticker"]["day"]["c"],
                    v   = data["ticker"]["day"]["v"],
                    vw  = data["ticker"]["day"]["vw"]
                    ),
                lastTrade           = models.LastTrade(
                    c   = data["ticker"]["lastTrade"]["c"],
                    i   = data["ticker"]["lastTrade"]["i"],
                    p   = data["ticker"]["lastTrade"]["p"],
                    s   = data["ticker"]["lastTrade"]["s"],
                    t   = data["ticker"]["lastTrade"]["t"],
                    x   = data["ticker"]["lastTrade"]["x"]
                    ),
                min                 = models.Min(
                    t   = data["ticker"]["min"]["t"],
                    n   = data["ticker"]["min"]["n"],
                    o   = data["ticker"]["min"]["o"],
                    h   = data["ticker"]["min"]["h"],
                    l   = data["ticker"]["min"]["l"],
                    c   = data["ticker"]["min"]["c"],
                    v   = data["ticker"]["min"]["v"],
                    vw  = data["ticker"]["min"]["vw"],
                    ),
                prevDay             = models.PrevDay(
                    o   = data["ticker"]["prevDay"]["o"],
                    h   = data["ticker"]["prevDay"]["h"],
                    l   = data["ticker"]["prevDay"]["l"],
                    c   = data["ticker"]["prevDay"]["c"],
                    v   = data["ticker"]["prevDay"]["v"],
                    vw  = data["ticker"]["prevDay"]["vw"]
                    )
            ),
            status=data["status"],
            request_id=data["request_id"]
        )
        
        # Retrieve appropriate schema
        candle = schemas.Candle(
            time    = rates.ticker.min.t,
            open    = rates.ticker.min.o,
            high    = rates.ticker.min.h,
            low     = rates.ticker.min.l,
            close   = rates.ticker.min.c
        )
        
        # Return candle schema
        return candle
        
    else:
        # HTTP exception
        print('ERROR - ' + str(response.status_code))
        print(f'ERROR ({str(response.status_code)})')
        raise Exception("Error response code: " + str(response.status_code))
