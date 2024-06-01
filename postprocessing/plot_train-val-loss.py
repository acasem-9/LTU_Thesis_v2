import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_losses(csv_path):
    # Load data
    data = pd.read_csv(csv_path)
    print(data.columns)
    # Ensure the expected columns are in the DataFrame
    expected_cols = {'                  epoch', '         train/cls_loss', '           val/cls_loss'}
    if not expected_cols.issubset(data.columns):
        print("Error: CSV file does not contain the required columns.")
        return

    # Set the style of seaborn
    sns.set_theme(style="darkgrid")

    # Create a figure and a set of subplots
    plt.figure(figsize=(10, 6))

    # Plot training loss
    sns.lineplot(x='                  epoch', y='         train/cls_loss', data=data, label='Train Loss', color='green')

    # Plot validation loss
    sns.lineplot(x='                  epoch', y='           val/cls_loss', data=data, label='Validation Loss', color='orange')

    # Adding title and labels
    plt.title('20240502_D200') # Training and Validation Loss per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Show the plot
    plt.show()

def main():
    # User input for the CSV file path
    csv_path = input("Enter the path to the CSV file: ").strip('"')

    plot_losses(csv_path)

if __name__ == "__main__":
    main()
