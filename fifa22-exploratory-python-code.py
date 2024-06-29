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

# overall score
player_sample = data_mod1.sample(5000)  # max number of rows that Altair can use is 5000
fig_1 = alt.Chart(player_sample).mark_point(point=True).encode(
    x = alt.X('overall',title='Overall Score'),
    y = alt.Y('wage_eur',title='Player Weekly Wage')
) 
fig_1

# player heights
fig_2 = alt.Chart(player_sample,title='Player Heights').mark_bar(point=True).encode(
    x = alt.X('height_cm',title='Height (cm)'), 
    y = alt.Y('count()',title='count')
)
fig_2

# allows more rows to be used in altair
alt.data_transformers.enable('default', max_rows = None)

# player wage and player age
alt.Chart(data_mod1, title = 'Player Age With Regards to Their Weekly Wage').mark_bar().encode(
   x = alt.X('age', title = 'Age of Player'),
   y = alt.Y('wage_eur', title = 'Weekly Wage of Player'),
   color = 'international_reputation:N'
)

# faceting
# overall level
overall_labels = ['1_low', '2_medium', '3_high']
data_mod2 = data_mod1.copy()
data_mod2['overall_fac'] = pd.qcut(data_mod1.overall, q = 3, labels = overall_labels)

data_mod2 = data_mod2.drop(columns = {'nationality_name', 'age', 'height_cm', 'weight_kg', 'body_type','wage_eur',
   'release_clause_eur', 'international_reputation', 'shooting', 'passing', 'dribbling', 'defending'})

# game stats
avg_skill = data_mod1[['shooting', 'passing', 'dribbling', 'defending']].mean(axis = 1)
data_mod2['avg_skill'] = avg_skill
data_mod2.head()

# player overall ability and player game stats
alt.Chart(data_mod2).mark_circle().encode(
    x = alt.X('avg_skill',
    axis = alt.Axis(title = 'Average Skill of Player'),
    scale = alt.Scale(zero = False, type = 'pow', exponent = 0.1)),
    y = alt.Y('overall', axis = alt.Axis(title = 'Overall Ability'), 
              scale = alt.Scale(zero = False, type = 'pow', exponent = 0.1)),
    color = 'overall_fac:O'
).facet(column = 'overall_fac')
