from errno import ENAMETOOLONG

from load import *
from config import *
from analyze import *
from process import *

#process_accident_data(AVIATION_ACCIDENTS)

#process_google_trend(SEARCH_QUERIES)
fatalities_vs_trends_correlation(AVIATION_ACCIDENTS, SEARCH_QUERIES)
#enplanements_plot(ENPLANEMENTS_CSV)