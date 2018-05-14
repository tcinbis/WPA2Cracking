import matplotlib.pyplot as plt
import pandas as pd

# Create hash comparison of aws instance
df = pd.read_csv("data.csv", sep=",")
ax = df.plot(kind='barh', colormap='rainbow')
ax.set_xlabel('hashes per second')
ax.set_title('CPU vs. GPU Hashspeed Comparison')
plt.show()

# Create hash comparison on own computer
df = pd.read_csv("hash-data-single-i53470-gtx970.csv", sep=",")
ax = df.plot(kind='barh', colormap='rainbow')
ax.set_xlabel('hashes per second')
ax.set_title('CPU i5-3470 vs. GPU GTX970 Hashspeed Comparison')
plt.show()

# Create time comparison on own computer
df = pd.read_csv("time-in-hours-data-single-i53470-gtx970.csv", sep=",")
ax = df.plot(kind='barh', colormap='rainbow')
ax.set_xlabel('hours')
ax.set_title('CPU i5-3470 vs. GPU GTX970 Time Comparison')
plt.show()