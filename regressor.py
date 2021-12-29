import math

import numpy
import pandas
import statsmodels.api as sm
from sklearn import linear_model

# Reading the CSV
heart_data = pandas.read_csv("./heart.csv")

# Start data setup
heart_data['Sex'] = (heart_data['Sex'] == 'M').astype(int)

chest_pain_types = {'ATA': 0, 'NAP': 1, 'ASY': 2, 'TA': 3}
heart_data['ChestPainType'].replace(chest_pain_types, inplace=True)

heart_data['ExerciseAngina'] = (
    heart_data['ExerciseAngina'] == 'Y').astype(int)
# End data setup

# Regression model with all fields except the ECG related ones
x_train = numpy.array(heart_data[['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol',
                                  'FastingBS', 'MaxHR', 'ExerciseAngina', 'Oldpeak']])
y_train = numpy.array(heart_data['HeartDisease'])

regressor = linear_model.LinearRegression()
regressor.fit(x_train, y_train)


def logisticPredication(x, regressor: linear_model.LinearRegression) -> int():
    return (1 / (1 + math.exp(-(-regressor.intercept_ + x)))) > 0.5


def predict(data: list) -> int():
    predict = regressor.predict([data])
    return logisticPredication(x=predict, regressor=regressor)


result = sm.OLS(y_train,  sm.add_constant(x_train)).fit()
