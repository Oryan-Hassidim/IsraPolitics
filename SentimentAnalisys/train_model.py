import sys
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from model import (CustomBERTregression, SentimentDataset, train_model,
                   evaluate_model, KNESSET_DICTA_BERT, ALPHA_BERT_BASE,
                   ALPHA_BERT_GIMMEL,
                   BATCH_SIZE, EPOCHS, LR, MAX_LENGTH)


def load_data(train_file: str, rank_file: str, tokenizer, max_length: int):
    """Loads text and rank data from files and tokenizes it."""
    with open(train_file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f.readlines()]

    with open(rank_file, 'r', encoding='utf-8') as f:
        labels = [float(line.strip()) for line in f.readlines()]

    return SentimentDataset(texts, labels, tokenizer, max_length)


def train(train_data: SentimentDataset, dev_data: SentimentDataset,
          model_name: str, epochs: int, batch_size: int, lr: float):
    """Trains the model using the training and development dataset."""
    model = CustomBERTregression(model_name)

    train_loader = DataLoader(train_data, batch_size=batch_size,
                              shuffle=True)
    val_loader = DataLoader(dev_data, batch_size=batch_size)

    train_model(model, train_loader, val_loader, epochs, lr)
    return model


def test(model: CustomBERTregression, test_data: SentimentDataset,
         batch_size: int):
    """Evaluates the model on the test dataset."""
    test_loader = DataLoader(test_data, batch_size=batch_size)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    criterion = torch.nn.MSELoss()
    test_loss = evaluate_model(model, test_loader, criterion, device)
    print(f"Final Test Loss: {test_loss:.4f}")


def main():
    """
    Main function to handle command-line arguments and
    execute training/testing.
    """
    if len(sys.argv) != 8:
        print("Usage: python train_model.py sentences_train.txt "
              "ranks_train.txt \"\n\
              sentences_dev.txt ranks_dev.txt sentences_test.txt "
              "ranks_test.txt model_option(1/2/3)")
        sys.exit(1)

    train_texts, train_ranks, dev_texts, dev_ranks, test_texts, \
        test_ranks, model_option = sys.argv[1:]

    model_option = int(model_option)
    if model_option == 1:
        model_name = KNESSET_DICTA_BERT
    elif model_option == 2:
        model_name = ALPHA_BERT_BASE
    elif model_option == 3:
        model_name = ALPHA_BERT_GIMMEL
    else:
        print("Invalid model option. Choose 1, 2, or 3.")
        sys.exit(1)

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load datasets
    train_data = load_data(train_texts, train_ranks, tokenizer, MAX_LENGTH)
    dev_data = load_data(dev_texts, dev_ranks, tokenizer, MAX_LENGTH)
    test_data = load_data(test_texts, test_ranks, tokenizer, MAX_LENGTH)

    # Train model
    model = train(train_data, dev_data, model_name, EPOCHS, BATCH_SIZE, LR)

    # Evaluate model
    test(model, test_data, BATCH_SIZE)


if __name__ == "__main__":
    """Usage: python train_model.py sentences_train.txt 
    ranks_train.txt sentences_dev.txt ranks_dev.txt sentences_test.txt 
    ranks_test.txt model_option(1/2/3)"""
    main()
