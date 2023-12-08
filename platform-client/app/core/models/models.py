from typing import NamedTuple

# ---------------------------------------------------
# -- Data GET responses
# -- -- Ticker's day
class Day(NamedTuple):
    o   : float
    h   : float
    l   : float
    c   : float
    v   : float
    vw  : float

# -- -- Ticker's last trade
class LastTrade(NamedTuple):
    c   : list[int]
    i   : str
    p   : float
    s   : float
    t   : float
    x   : float

# -- -- Ticker's 
class Min(NamedTuple):
    t   : int
    n   : float
    o   : float
    h   : float
    l   : float
    c   : float
    v   : float
    vw  : float

# -- -- Ticker's 
class PrevDay(NamedTuple):
    o   : float
    h   : float
    l   : float
    c   : float
    v   : float
    vw  : float

# -- -- Rates' ticker
class Ticker(NamedTuple):
    ticker              : str
    todaysChangePerc    : float
    todaysChange        : float
    updated             : int
    day                 : Day
    lastTrade           : LastTrade
    min                 : Min
    prevDay             : PrevDay
    
# -- Rates
class Rates(NamedTuple):
    ticker      : Ticker
    status      : str
    request_id  : str
