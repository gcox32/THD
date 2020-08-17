
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# predefined style set
plt.style.use('ggplot')

# set vars
SEED = 15
count = 100

# import Faker for generating names
from faker import Faker
Faker.seed(SEED)
np.random.seed(SEED)

fake = Faker()

names = []
salaries = []
for _ in range(count):
    names.append(fake.name())

    salary = np.random.randint(1000,2500)
    salaries.append(salary)

# dataframe
df = pd.DataFrame(
    {'Name':names,
     'Salary':salaries,
     }
)

print(df.head())