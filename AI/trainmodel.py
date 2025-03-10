import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from model import NeuralNetwork
from model import INPUT_LENGTH

# Assuming your provided NeuralNetwork class is already defined as `NeuralNetwork`

# Step 1: Create a synthetic dataset
# This is just for demonstration, you can replace it with your actual data
class SyntheticDataset(torch.utils.data.Dataset):
    def __init__(self, size=1000, input_length=INPUT_LENGTH):
        self.size = size
        self.data = torch.randn(size, input_length)  # Random input data
        self.targets = torch.randn(size, input_length)  # Random target data
    
    def __len__(self):
        return self.size
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

# Step 2: Initialize model, loss function, and optimizer
model = NeuralNetwork()

# Define Mean Squared Error loss (you can choose another one based on your problem)
criterion = nn.MSELoss()

# Use an optimizer, here using Adam
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Step 3: Create a DataLoader for the synthetic dataset
train_dataset = SyntheticDataset(size=1000)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)

# Step 4: Training loop
num_epochs = 10

for epoch in range(num_epochs):
    model.train()  # Set model to training mode
    running_loss = 0.0

    for inputs, targets in train_loader:
        optimizer.zero_grad()  # Zero the gradients
        outputs = model(inputs)  # Forward pass
        loss = criterion(outputs, targets)  # Compute loss
        loss.backward()  # Backward pass
        optimizer.step()  # Update weights
        
        running_loss += loss.item() * inputs.size(0)  # Accumulate the loss

    avg_loss = running_loss / len(train_loader.dataset)  # Average loss for this epoch
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

# Step 5: Save the model
torch.save(model.state_dict(), 'trained_model.pth')

print("Training completed and model saved as 'trained_model.pth'.")
