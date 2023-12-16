import pandas as pd
import json
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
# Assuming 'your_file.json' is the name of your JSON file
with open('work_dirs/mouse/20231130_095049/vis_data/20231130_095049.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

df = df.iloc[20:]

# Drop rows with NaN values in the 'coco/AP (L)' column and reset the index
df1 = df.dropna(subset=['epoch']).reset_index(drop=True)

df2 = df.dropna(subset=['coco/AP (L)']).reset_index(drop=True)




fig, ax1 = plt.subplots()
# ax1.plot(df2['step'], df2['EPE'], color='blue', label='Series 1')
ax1.plot(df2['step'], df2['EPE'], label='End-point error', color='blue', marker='o')
ax1.set_xlabel('Epochs')
ax1.set_ylabel('End-point error', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a twin Axes sharing the xaxis
ax2 = ax1.twinx()

# Plot the second series on the twin Axes
# ax2.plot(df2['step'], df2['PCK'], color='red', label='Series 2')


ax2.plot(df1['epoch'], df1['acc_pose'], label='Train Accuracy')
# Plot validation accuracy
ax2.plot(df2['step'], df2['coco/AP (L)'], label='COCO Average Precision', marker='o')
ax2.plot(df2['step'], df2['PCK'], label='Procentage correct points', marker='o')

ax2.set_ylabel('Accuracy')
ax2.tick_params(axis='y')






# # Display the DataFrame
# plt.figure()

# # Plot training accuracy
# line1 = plt.plot(df1['epoch'], df1['acc_pose'], label='Train Accuracy')

# # Plot validation accuracy
# plt.plot(df2['step'], df2['coco/AP (L)'], label='Validation Accuracy', marker='o')
# plt.plot(df2['step'], df2['PCK'], label='Procentage correct points', marker='o')
# plt.plot(df2['step'], df2['EPE'], label='End-point error', marker='o')

# # Set labels and title
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.title('Training and Validation Accuracy Over Epochs')

# # Display legend
ax1.legend()
ax2.legend()
# # # datacursor()

# Show the plot
plt.savefig("accuracy.pdf", bbox_inches='tight', pad_inches=0)
plt.show()
print(df2['step'], df2['coco/AP (L)'])