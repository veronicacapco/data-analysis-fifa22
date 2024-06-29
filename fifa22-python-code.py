import pandas as pd
import numpy as np
import altair as alt

# importing the dataset
data = pd.read_csv('data/players-22.csv')

# tidying the data
raw_data = pd.read_csv('data/players-22.csv')

data_mod1 = raw_data[['long_name', 'nationality_name', 'age', 
                      'height_cm', 'weight_kg', 'overall', 'wage_eur', 
                      'international_reputation', 'shooting',
                      'passing', 'dribbling', 'defending']]
data_mod1.head()
data_mod1.to_csv('tidy-data.csv')

# load tidied data and print rows
tidy_data = pd.read_csv('data/tidy-fifa22-data.csv')

tidy_data.drop('Unnamed: 0', axis = 1).head()

# heat map
# melt corr_mx
data_corr = data_mod2.loc[:, ['shooting','passing', 'dribbling',
   'defending','overall']].corr()

data_long = data_corr.reset_index().rename(
    columns = {'index': 'row'}
).melt(
       id_vars = 'row',
       var_name = 'col',
       value_name = 'Correlation'
)

# construct plot
alt.Chart(data_long).mark_rect().encode(
  x = alt.X('col', title = '', sort = {'field': 'Correlation',
                                       'order': 'ascending'}),
  y = alt.Y('row', title = '', sort = {'field': 'Correlation',
                                       'order': 'ascending'}),
  color = alt.Color('Correlation', 
                    scale = alt.Scale(scheme = 'greenblue', # diverging gradient
                                      domain = (-1, 1), # ensure white = 0
                                      type = 'sqrt'), # adjust gradient scale
                    legend = alt.Legend(tickCount = 5)) # add ticks to colorbar at 0.5 for reference
).properties(width = 300, height = 300)

# linear regression
data_mod2 = data_mod1.dropna() # drop missing rows

response = data_mod2.loc[:, ['wage_eur']] # response variable

data = data_mod2.loc[:, ['shooting','passing', 'dribbling',
   'defending']] # the variables

data = add_dummy_feature(data, value = 1) # add intercept column
linreg = LinearRegression(fit_intercept = False)

# fit linear model
linreg.fit(data,response)

# predicting data
fitted = linreg.predict(data)

# R^2
R_2 = r2_score(response,linreg.predict(data))
R_2

# residuals
residuals = ((response - fitted)**2).sum()
residuals

# scatter plot
scatter = alt.Chart(data_mod1).mark_point(point=True).encode(
       x = alt.X('overall',title='Overall Score',scale=alt.Scale(domain=[45,95])),
       y = alt.Y('wage_eur',title='Player Weekly Wage')
)

# regression line
regression =
   scatter.transform_regression('overall','wage_eur').mark_line(color='black', trokeWidth=4)

# layer
   scatter + regression

# can we fit a polynomial?

x = np.array(data_mod2['overall']).reshape((-1,1))
y = np.array(data_mod2['wage_eur']).reshape((-1,1))

coefficients = np.polyfit(data_mod2['overall'],data_mod2['wage_eur'],deg=4)

poly = np.poly1d(coefficients)
fitted_x = np.linspace(x[0], x[-1])
fitted_y = poly(fitted_x)

fitted_x = [item for sublist in fitted_x for item in sublist]
fitted_y = [item for sublist in fitted_y for item in sublist]

fitted_values = pd.DataFrame()
fitted_values['fitted_x'] = fitted_x
fitted_values['fitted_y'] = fitted_y

scatter = alt.Chart(data_mod1).mark_point(point=True).encode(
    x = alt.X('overall',title='Overall
Score',scale=alt.Scale(domain=[45,95])),
    y = alt.Y('wage_eur',title='Player Weekly Wage')
)
   
polyfit =
alt.Chart(fitted_values).mark_line(color='black',strokeWidth=3).encode(
       x = alt.X('fitted_x',scale=alt.Scale(domain=[45,95])),
       y = alt.Y('fitted_y')
)

scatter+polyfit

# KDE of age
hist = alt.Chart(data_mod1).transform_bin(
    as_ = 'Age',
    field ='age', # name to give binned variable
    bin = alt.Bin(step = 5)
).transform_aggregate(
    Count = 'count()',
    groupby = ['Age']
).transform_calculate(
    Density = 'datum.Count/(5*19239)' # divide counts by samplesize x binwidth
).mark_bar(size = 20).encode(
    x = alt.X('Age:Q',scale=alt.Scale(domain=[10, 55])),
    y = 'Density:Q',
)

smooth = alt.Chart(data_mod1).transform_density(
    density = 'age',
    as_ = ['Age', 'Density'],
    extent=[10, 55],
    bandwidth = 2,
).mark_line(color = 'black',strokeWidth=3).encode(
    x = alt.X('Age:Q'),
    y = 'Density:Q',
)

hist + smooth

# KDE of weight
hist = alt.Chart(data_mod1).transform_bin(
    as_ = 'Weight',
    field ='weight_kg', # name to give binned variable
    bin = alt.Bin(step = 5)
).transform_aggregate(
    Count = 'count()',
    groupby = ['Weight']
).transform_calculate(
    Density = 'datum.Count/(5*19239)' # divide counts by sample
size x binwidth
).mark_bar(size = 20).encode(
    x = alt.X('Weight:Q',title='Weight (kg)',
scale=alt.Scale(domain=[45, 115])),
    y = 'Density:Q',
)

smooth = alt.Chart(data_mod1).transform_density(
    density = 'weight_kg',
    as_ = ['Weight', 'Density'],
    extent=[45, 115],
    bandwidth = 3,
).mark_line(color = 'black',strokeWidth=3).encode(
    x = alt.X('Weight:Q'),
    y = 'Density:Q',
)

hist + smooth
  
