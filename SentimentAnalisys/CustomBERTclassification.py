import torch.nn as nn
from transformers import AutoModel


class CustomBERTclassification(nn.Module):
    def __init__(self, bert_model_name, output_dim):
        super(CustomBERTclassification, self).__init__()

        # Load the pre-trained BERT model without the classification head
        self.bert = AutoModel.from_pretrained(bert_model_name)

        # Get the hidden size of the BERT model
        bert_hidden_size = self.bert.config.hidden_size

        # Fully connected layer
        self.fc = nn.Linear(bert_hidden_size, output_dim)

        # Optional: do we want a hyperparameter for min probability?
        self.activation = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        # Get hidden states from BERT
        outputs = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask)

        # Extract hidden state of the [CLS] token (batch_size, hidden_dim)
        cls_hidden_state = outputs.last_hidden_state[:, 0, :]

        # Pass through the fully connected layer
        logits = self.fc(cls_hidden_state)

        # Apply activation function
        return self.activation(logits)
