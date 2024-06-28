Python 3.11.1 (v3.11.1:a7a450f84a, Dec  6 2022, 15:24:06) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> # load tidied data and print rows
>>> tidy_data = pd.read_csv('data/tidy-fifa22-data.csv')
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    tidy_data = pd.read_csv('data/tidy-fifa22-data.csv')
NameError: name 'pd' is not defined. Did you mean: 'id'?
>>> tidy_data.drop('Unnamed: 0', axis = 1).head()
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    tidy_data.drop('Unnamed: 0', axis = 1).head()
NameError: name 'tidy_data' is not defined
