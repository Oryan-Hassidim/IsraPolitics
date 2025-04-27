import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer
from torch.utils.data import random_split
from typing import List, Tuple


###########################################################################
# Constants

KNESSET_DICTA_BERT: str = "GiliGold/Knesset-DictaBERT"
ALPHA_BERT_BASE: str = "onlplab/alephbert-base"
ALPHA_BERT_GIMMEL: str = "./alephbertgimmel-base/ckpt_73780--Max512Seq"
"""Path to the locally cloned AlephBERT-Gimmel model. 
Must clone from: https://github.com/Dicta-Israel-Center-for-Text-Analysis/
alephbertgimmel.git"""

SENTIMENT_SIZE: int = 5
BATCH_SIZE: int = 8
EPOCHS: int = 5
LR: float = 2e-5
MAX_LENGTH: int = 512

###########################################################################


class CustomBERTregression(nn.Module):
    """Custom BERT model for regression tasks."""

    def __init__(self, bert_model_name: str) -> None:
        """Initializes the model with a pre-trained BERT and a linear
        output layer.
        Args:
            bert_model_name (str): Name or path of the pre-trained BERT.
        """
        super(CustomBERTregression, self).__init__()

        # Load the pre-trained BERT model without the classification head
        self.bert = AutoModel.from_pretrained(bert_model_name)

        # Get the hidden size of the BERT model
        bert_hidden_size = self.bert.config.hidden_size

        # Fully connected layer
        self.fc = nn.Linear(bert_hidden_size, 1)

    def forward(self, input_ids: torch.Tensor,
                attention_mask: torch.Tensor) -> torch.Tensor:
        """Forward pass of the model.

        Args:
            input_ids (torch.Tensor): Tokenized input IDs.
            attention_mask (torch.Tensor): Attention mask for input IDs.

        Returns:
            torch.Tensor: Model output tensor.
        """
        outputs = self.bert(
            input_ids=input_ids, attention_mask=attention_mask)

        # Extract hidden state of the [CLS] token (batch_size, hidden_dim)
        cls_hidden_state = outputs.last_hidden_state[:, 0, :]

        # Pass through the fully connected layer
        output = self.fc(cls_hidden_state)
        return output


###########################################################################


class SentimentDataset(Dataset):
    """Dataset class for handling text and sentiment labels."""

    def __init__(self, texts: List[str], labels: List[float],
                 tokenizer: AutoTokenizer,
                 max_length: int = MAX_LENGTH) -> None:
        """Initializes the dataset.

        Args:
            texts (List[str]): List of input texts.
            labels (List[float]): Corresponding sentiment labels.
            tokenizer (AutoTokenizer): Tokenizer for processing texts.
            max_length (int, optional): Maximum sequence length. Defaults
             to MAX_LENGTH.
        """
        self.texts = texts
        self.labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(
            1)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        """Returns the number of samples in the dataset."""
        return len(self.texts)

    def __getitem__(self, idx: int) -> Tuple[
            torch.Tensor, torch.Tensor, torch.Tensor]:
        """Gets a single sample from the dataset.
        Args:
            idx (int): Index of the sample.
        Returns:
            Tuple[torch.Tensor, torch.Tensor, torch.Tensor]: Tokenized
            input IDs, attention mask, and label.
        """
        encoding = self.tokenizer(
            self.texts[idx],
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt"
        )
        return encoding['input_ids'].squeeze(0), \
               encoding['attention_mask'].squeeze(0), \
               self.labels[idx]


###########################################################################

def train_one_epoch(
        model: nn.Module,
        train_loader: DataLoader,
        criterion: nn.Module,
        optimizer: optim.Optimizer,
        device: torch.device
) -> float:
    """Trains the model for one epoch.

    Args:
        model (nn.Module): The model to train.
        train_loader (DataLoader): DataLoader for training data.
        criterion (nn.Module): Loss function.
        optimizer (optim.Optimizer): Optimizer.
        device (torch.device): Device to use (CPU or GPU).

    Returns:
        float: Average training loss.
    """
    model.train()
    total_loss = 0

    for input_ids, attention_mask, labels in train_loader:
        input_ids, attention_mask, labels = (
            input_ids.to(device),
            attention_mask.to(device),
            labels.to(device)
        )

        optimizer.zero_grad()
        predictions = model(input_ids, attention_mask)
        loss = criterion(predictions, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)  # Average loss


def train_model(model, train_loader, val_loader, epochs=EPOCHS, lr=LR):
    """Main training loop."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr)

    train_losses = []
    val_losses = []

    for epoch in range(epochs):
        avg_train_loss = train_one_epoch(
            model, train_loader, criterion, optimizer, device)
        train_losses.append(avg_train_loss)

        val_loss = evaluate_model(model, val_loader, criterion, device)
        val_losses.append(val_loss)

        # Save model checkpoint
        save_model(model, epoch, f"model_epoch_{epoch + 1}.pth")

        print(
            f"Epoch {epoch + 1}/{epochs}: Train Loss = "
            f"{avg_train_loss:.4f}, Val Loss = {val_loss:.4f}"
        )

    plot_training(train_losses, val_losses)


def evaluate_model(model: nn.Module, val_loader: DataLoader,
                   criterion: nn.Module, device: torch.device) -> float:
    """Evaluates the model on validation data.

    Args:
        model (nn.Module): The model to evaluate.
        val_loader (DataLoader): DataLoader for validation data.
        criterion (nn.Module): Loss function.
        device (torch.device): Device to use (CPU or GPU).

    Returns:
        float: Average validation loss.
    """
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for input_ids, attention_mask, labels in val_loader:
            input_ids, attention_mask, labels = input_ids.to(
                device), attention_mask.to(device), labels.to(device)

            predictions = model(input_ids, attention_mask)
            loss = criterion(predictions, labels)
            total_loss += loss.item()

    return total_loss / len(val_loader)


def plot_training(train_losses: List[float],
                  val_losses: List[float]) -> None:
    """Plots training and validation loss.

    Args:
        train_losses (List[float]): Training loss per epoch.
        val_losses (List[float]): Validation loss per epoch.
    """
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Training and Validation Loss')
    plt.show()


def save_model(model: nn.Module, epoch: int,
               path: str = "model_checkpoint.pth") -> None:
    """Saves model state.

    Args:
        model (nn.Module): Model to save.
        epoch (int): Current epoch.
        path (str, optional): Path to save the model.
         Defaults to "model_checkpoint.pth".
    """
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict()
    }, path)
    print(f"Model saved at epoch {epoch} -> {path}")


def load_model(model: nn.Module,
               path: str = "model_checkpoint.pth") -> int:
    """Loads model state.

    Args:
        model (nn.Module): Model to load state into.
        path (str, optional): Path to model checkpoint.
        Defaults to "model_checkpoint.pth".

    Returns:
        int: Last trained epoch.
    """
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    print(f"Model loaded from {path} (Epoch {checkpoint['epoch']})")
    return checkpoint['epoch']  # Return last trained epoch


def example_usage():
    """
    Example usage
    """
    bert_model_name = KNESSET_DICTA_BERT
    tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
    model = CustomBERTregression(bert_model_name)

    # Example sentences
    sentences = ["הספר היה ממש טוב", "השירות היה גרוע מאוד"]
    labels = [5.0, 1.0]

    dataset = SentimentDataset(sentences, labels, tokenizer)

    # Split dataset into 80% train, 20% validation
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset,
                                              [train_size, val_size])

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE,
                              shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE,
                            shuffle=False)

    train_model(model, train_loader, val_loader)
