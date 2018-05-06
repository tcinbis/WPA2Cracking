import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv", sep=",")
ax = df.plot(kind='barh', colormap='rainbow')
ax.set_xlabel('hashes per second')
ax.set_title('CPU vs. GPU Hashspeed Comparison')
plt.show()