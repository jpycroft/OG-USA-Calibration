'''
This script locates the data required for macro_parameters for the OG-UK model,
and calculates the values. 

The script is based on macro_params_FRED.py for OG-USA-Calibration.
'''
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import datetime
import statsmodels.api as sm
from pandas_datareader import data
import eurostat

###### USER ENTRY: country and year ########
Country = 'UK'
Year = 2018
############################################
StartPeriod = Year
EndPeriod = Year
filter_pars = {'GEO': [Country]}

# USEFUL WEB SITES
# Eurostat Data Navigation Tree available here: 
# https://ec.europa.eu/dgs/eurostat/contingency/table_of_contents_en.pdf
# for panda_datareader see: 
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#eurostat

##############################################################################
########### for initial_debt_ratio - START ###################################
df_gdp = eurostat.get_sdmx_data_df('nama_10_gdp', StartPeriod, EndPeriod, 
                                    filter_pars, flags = True, verbose=True)
print('df_gdp: ', df_gdp)
# df_gdp2 = eurostat.get_sdmx_data_df('ei_namq_10_ma', StartPeriod, EndPeriod, 
#                                   filter_pars, flags = True, verbose=True)
df_debt = eurostat.get_sdmx_data_df('gov_10dd_edpt1', StartPeriod, EndPeriod, 
                                    filter_pars, flags = True, verbose=True)
print('df_debt: ', df_debt)
########### for initial_debt_ratio - END #####################################
##############################################################################

##############################################################################
########### for ALPHA_T & ALPHA_G - START ####################################
df_gov = eurostat.get_sdmx_data_df('gov_10a_main', StartPeriod, EndPeriod, 
                                    filter_pars, flags = True, verbose=True)
print('df_gov: ', df_gov)
########### for ALPHA_T & ALPHA_G - END ######################################
##############################################################################

##############################################################################
########### for gamma = capital_share = 1 - labour_share - START #############
# previously used EU-KLEMS as in this report: 
# https://ec.europa.eu/economy_finance/publications/pages/publication15147_en.pdf
# https://euklems.eu/
# This OECD report gives the labour share as 0.7 (Figure 4)
# https://www.oecd.org/g20/topics/employment-and-social-policy/The-Labour-Share-in-G20-Economies.pdf
# This Office of National Statistics chart give labour share in 2016 as 54.44
# https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/adhocs/006610labourshareofgdpandprivatenonfinancialcorporationgrossoperatingsurpluscorporateprofitabilitycurrentpricesquarter1jantomar1997toquarter3julytosept2016
# According to this report (Figure 2):
# https://bankunderground.co.uk/2019/08/07/is-there-really-a-global-decline-in-the-non-housing-labour-share/
# Values depends on whether you are dealing with 
# - the "unadjusted corporate sector" (around 60% labour share) versus
# - the "adjusted business sector (using KLEMS)" (around 70% labour share)
gamma = 1 - 0.7
print('gamma: ', gamma)
########### for gamma = capital_share = 1 - labour_share - END ###############
##############################################################################

##############################################################################
### for g_y (Exogenous growth rate of labor augmenting tech change) - START ##
# use real_GDP_growth rate as proxy. Needs to be averaged over time periods.
df_growth = eurostat.get_sdmx_data_df('tec00115', StartPeriod, EndPeriod, 
                                    filter_pars, flags = True, verbose=True)
print('df_growth: ', df_growth)
### for g_y (Exogenous growth rate of labor augmenting tech change) - END ####
##############################################################################

##############################################################################
########### for r_gov_shift & r_gov_scale - START ############################
# need to regress: gov_bond_yields = f(corporate_bond_yields)
gbond = data.DataReader("irt_lt_mcby_d", 
                       start='1986-1-1', 
                       end='2020-12-31', 
                       data_source='eurostat')
# gbond.shape = (9132, 29)
# note column format:
gbond_UK = gbond.loc[:, ('EMU convergence criterion bond yields', 
                         'United Kingdom', 'Daily')]
print('gbond_UK:', gbond_UK)
# UK corporate bond yield not readily available; global value may be more
# appropriate; use US values for now:
start_fred = datetime.datetime(1986, 1, 1)
end_fred = datetime.datetime(2020, 12, 31)  # go through today
fred_cbond = web.DataReader('DBAA', 'fred', start_fred, end_fred)
print('fred_cbond: ', fred_cbond)

# # estimate r_gov_shift and r_gov_scale
# rate_data = fred_data_d[['10 year treasury rate',
#                          'BAA Corp Bond Rates']].dropna()
# rate_data['constant'] = np.ones(len(rate_data.index))
# # mod = PanelOLS(fred_data['10 year treasury rate'],
# #                fred_data[['constant', 'BAA Corp Bond Rates']])
# mod = sm.OLS(rate_data['10 year treasury rate'],
#                rate_data[['constant', 'BAA Corp Bond Rates']])
# res = mod.fit()
########### for r_gov_shift & r_gov_scale - END ##############################
##############################################################################

##############################################################################
########### collect key values as macro_parameters - START ###################
# # initialize a dictionary of parameters
macro_parameters = {}
# TO DO:
# macro_parameters['initial_debt_ratio'] =
# macro_parameters['alpha_T'] =
# macro_parameters['alpha_G'] = 
# macro_parameters['gamma'] =
macro_parameters['gamma'] = gamma
# macro_parameters['g_y'] =
# macro_parameters['r_gov_shift'] = 
# macro_parameters['r_gov_scale'] = 
print('macro_parameters: ', macro_parameters)
########### collect key values as macro_parameters - END #####################
##############################################################################