from sklearn.metrics import accuracy_score

# Suppose these are the true labels
true_labels = [1, 0, 1, 0, 1]  # 1 means plagiarized, 0 means not plagiarized

# Predicted labels from your model
predicted_labels = [1, 0, 1, 0, 0]

accuracy = accuracy_score(true_labels, predicted_labels)
print(f"Accuracy: {accuracy * 100}%")
