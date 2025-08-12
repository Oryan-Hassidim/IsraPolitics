# import random
# import sys
# from collections import defaultdict
# import matplotlib.pyplot as plt
#
#
# def load_ranks_to_sentences(sentences_file, ranks_file):
#     """
#     Load sentence-to-rank data and organize by rank (1–5).
#     """
#     with open(sentences_file, 'r', encoding='utf-8') as f_sentences, \
#             open(ranks_file, 'r', encoding='utf-8') as f_ranks:
#
#         sentences = [line.strip() for line in f_sentences]
#         ranks = [int(line.strip()) for line in f_ranks]
#
#         if len(sentences) != len(ranks):
#             raise ValueError("Mismatch in number of sentences and ranks")
#
#         rank_dict = defaultdict(list)
#         for sentence, rank in zip(sentences, ranks):
#             if rank < 1 or rank > 5:
#                 raise ValueError(f"Invalid rank: {rank}. Expected 1–5.")
#             rank_dict[rank].append(sentence)
#
#         return dict(rank_dict)
#
#
# def sample_sentences_per_rank(rank_to_sentences, sample_size_per_rank=20):
#     """
#     Randomly sample sentences from each rank.
#     """
#     sampled_pairs = []
#
#     for rank in range(1, 6):
#         sentences = rank_to_sentences.get(rank, [])
#         if len(sentences) < sample_size_per_rank:
#             raise ValueError(
#                 f"Not enough sentences for rank {rank}. Required: {sample_size_per_rank}, Found: {len(sentences)}")
#
#         sampled = random.sample(sentences, sample_size_per_rank)
#         sampled_pairs.extend((sentence, rank) for sentence in sampled)
#
#     return sampled_pairs
#
#
# def collect_user_ranks(sampled_pairs):
#     """
#     Show each sentence, ask user for ranking, and collect triplets.
#     """
#     triplets = []
#     print("Please rate each sentence from 1 (worst) to 5 (best):\n")
#
#     for i, (sentence, original_rank) in enumerate(sampled_pairs, 1):
#         print(f"\n[{i}/{len(sampled_pairs)}] Sentence:\n{sentence}")
#
#         while True:
#             try:
#                 user_input = input("Your rank (1–5): ").strip()
#                 user_rank = int(user_input)
#                 if 1 <= user_rank <= 5:
#                     break
#                 else:
#                     print("❌ Please enter a number between 1 and 5.")
#             except ValueError:
#                 print(
#                     "❌ Invalid input. Please enter a number between 1 and 5.")
#
#         triplets.append((sentence, original_rank, user_rank))
#
#     return triplets
#
#
# # def evaluate_thresholds(triplets):
# #     """
# #     Evaluate model performance across thresholds and plot Recall + FPR.
# #     """
# #     thresholds = range(1, 6)
# #     recalls = []
# #     fprs = []
# #
# #     for T in thresholds:
# #         TP = FP = FN = TN = 0
# #
# #         for sentence, original_rank, user_rank in triplets:
# #             user_positive = user_rank >= T
# #             model_positive = original_rank >= T
# #
# #             if user_positive and model_positive:
# #                 TP += 1
# #             elif user_positive and not model_positive:
# #                 FN += 1
# #             elif not user_positive and model_positive:
# #                 FP += 1
# #             else:
# #                 TN += 1
# #
# #         recall = TP / (TP + FN) if (TP + FN) > 0 else 0
# #         fpr = FP / (FP + TN) if (FP + TN) > 0 else 0
# #
# #         recalls.append(recall)
# #         fprs.append(fpr)
# #
# #     # Plot
# #     plt.figure(figsize=(8, 5))
# #     plt.plot(thresholds, recalls, label='Recall (True Positive Rate)',
# #              marker='o')
# #     plt.plot(thresholds, fprs, label='False Positive Rate (FPR)',
# #              marker='x')
# #     plt.xlabel('Threshold (T)')
# #     plt.ylabel('Rate')
# #     plt.title('Model Evaluation vs Threshold')
# #     plt.xticks(thresholds)
# #     plt.ylim(0, 1)
# #     plt.grid(True)
# #     plt.legend()
# #     plt.tight_layout()
# #     plt.show()
#
# def evaluate_thresholds(triplets):
#     """
#     Evaluate model performance using fixed user labels:
#     - User 4–5 = positive
#     - User 1–3 = negative
#
#     Vary model threshold T from 1 to 5:
#     - Model prediction: original_rank >= T
#     """
#     thresholds = range(1, 6)
#     recalls = []
#     fprs = []
#
#     for T in thresholds:
#         TP = FP = FN = TN = 0
#
#         for sentence, model_rank, user_rank in triplets:
#             user_positive = user_rank >= 4          # Fixed
#             model_positive = model_rank >= T        # Swept threshold
#
#             if user_positive and model_positive:
#                 TP += 1
#             elif user_positive and not model_positive:
#                 FN += 1
#             elif not user_positive and model_positive:
#                 FP += 1
#             else:
#                 TN += 1
#
#         recall = TP / (TP + FN) if (TP + FN) > 0 else 0
#         fpr = FP / (FP + TN) if (FP + TN) > 0 else 0
#
#         recalls.append(recall)
#         fprs.append(fpr)
#
#     # Plot
#     plt.figure(figsize=(8, 5))
#     plt.plot(thresholds, recalls, label='Recall (True Positive Rate)', marker='o')
#     plt.plot(thresholds, fprs, label='False Positive Rate (FPR)', marker='x')
#     plt.xlabel('Model Threshold (T)')
#     plt.ylabel('Rate')
#     plt.title('Fixed User Labels: Recall and FPR vs Model Threshold')
#     plt.xticks(thresholds)
#     plt.ylim(0, 1)
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.show()
#
#
#
# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python script.py <sentences_file> <ranks_file>")
#         sys.exit(1)
#
#     sentences_file = sys.argv[1]
#     ranks_file = sys.argv[2]
#
#     try:
#         rank_dict = load_ranks_to_sentences(sentences_file, ranks_file)
#         sampled_pairs = sample_sentences_per_rank(rank_dict,
#                                                   sample_size_per_rank=20)
#         triplets = collect_user_ranks(sampled_pairs)
#         evaluate_thresholds(triplets)
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         sys.exit(1)
#
#
# if __name__ == "__main__":
#     main()


import random
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def load_ranks_to_sentences(sentences_file, ranks_file, max_score=5):
    """
    Load sentence-to-rank data and organize by rank.
    Assumes ranks_file has one integer per line.
    """
    with open(sentences_file, 'r', encoding='utf-8') as f_sentences, \
         open(ranks_file, 'r', encoding='utf-8') as f_ranks:

        sentences = [line.strip() for line in f_sentences]
        ranks = [int(line.strip()) for line in f_ranks]

        if len(sentences) != len(ranks):
            raise ValueError("Mismatch in number of sentences and ranks")

        rank_dict = defaultdict(list)
        for sentence, rank in zip(sentences, ranks):
            if rank < 1 or rank > max_score:
                raise ValueError(f"Invalid rank: {rank}. Expected 1–{max_score}.")
            rank_dict[rank].append(sentence)

        return dict(rank_dict)

def sample_sentences_per_rank(rank_to_sentences, sample_size_per_rank=20):
    """
    Randomly sample sentences from each rank.
    If fewer sentences than sample_size_per_rank are available,
    use all sentences for that rank instead of raising an error.
    """
    sampled_pairs = []

    for rank in sorted(rank_to_sentences.keys()):
        sentences = rank_to_sentences.get(rank, [])
        if len(sentences) < sample_size_per_rank:
            # Use all sentences if not enough
            sampled = sentences
            print(f"Warning: Only {len(sentences)} sentences available for rank {rank}, using all.")
        else:
            sampled = random.sample(sentences, sample_size_per_rank)
        sampled_pairs.extend((sentence, rank) for sentence in sampled)

    return sampled_pairs

def collect_user_ranks(sampled_pairs, max_score):
    triplets = []
    print(f"Please rate each sentence from 1 (worst) to {max_score} (best):\n")
    for i, (sentence, original_rank) in enumerate(sampled_pairs, 1):
        print(f"\n[{i}/{len(sampled_pairs)}] Sentence:\n{sentence}")
        while True:
            try:
                user_input = input(f"Your rank (1–{max_score}): ").strip()
                user_rank = int(user_input)
                if 1 <= user_rank <= max_score:
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {max_score}.")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number between 1 and {max_score}.")
        triplets.append((sentence, original_rank, user_rank))
    return triplets

def evaluate_filter(triplets):
    """
    Filter mode:
    User positive if rank >=4, negative if 1-3
    Model positive if original_rank >= threshold T
    Plot Recall and FPR vs threshold
    """
    thresholds = range(1, 6)
    recalls = []
    fprs = []

    for T in thresholds:
        TP = FP = FN = TN = 0
        for sentence, model_rank, user_rank in triplets:
            user_positive = user_rank >= 4
            model_positive = model_rank >= T

            if user_positive and model_positive:
                TP += 1
            elif user_positive and not model_positive:
                FN += 1
            elif not user_positive and model_positive:
                FP += 1
            else:
                TN += 1

        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

        recalls.append(recall)
        fprs.append(fpr)

    plt.figure(figsize=(8, 5))
    plt.plot(thresholds, recalls, label='Recall (True Positive Rate)', marker='o')
    plt.plot(thresholds, fprs, label='False Positive Rate (FPR)', marker='x')
    plt.xlabel('Model Threshold (T)')
    plt.ylabel('Rate')
    plt.title('Filter Mode: Recall and FPR vs Model Threshold')
    plt.xticks(thresholds)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def map_to_bucket(score):
    """Map a score 1-10 to buckets: 1=[1-3], 2=[4-6], 3=[7-10]"""
    if 1 <= score <= 3:
        return 1
    elif 4 <= score <= 6:
        return 2
    elif 7 <= score <= 10:
        return 3
    else:
        raise ValueError(f"Score {score} out of bucket range 1-10")

# def evaluate_rank(triplets):
#     """
#     Rank mode:
#     Scores 1-10.
#     Compute MSE and bucketed accuracy.
#     Plot bucketed confusion matrix.
#     """
#
#     true_scores = []
#     pred_scores = []
#
#     for sentence, model_rank, user_rank in triplets:
#         true_scores.append(user_rank)
#         pred_scores.append(model_rank)
#
#     # Mean Squared Error
#     mse = np.mean([(p - t) ** 2 for p, t in zip(pred_scores, true_scores)])
#
#     # Bucketed Accuracy
#     true_buckets = [map_to_bucket(s) for s in true_scores]
#     pred_buckets = [map_to_bucket(s) for s in pred_scores]
#
#     correct = sum(tb == pb for tb, pb in zip(true_buckets, pred_buckets))
#     bucketed_accuracy = correct / len(true_scores)
#
#     print(f"Mean Squared Error (MSE): {mse:.4f}")
#     print(f"Bucketed Accuracy: {bucketed_accuracy:.4f}")
#
#     # Confusion matrix
#     confusion = np.zeros((3, 3), dtype=int)
#     for tb, pb in zip(true_buckets, pred_buckets):
#         confusion[tb - 1][pb - 1] += 1  # zero indexed matrix
#
#     plt.figure(figsize=(6, 5))
#     sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues',
#                 xticklabels=['1-3', '4-6', '7-10'],
#                 yticklabels=['1-3', '4-6', '7-10'])
#     plt.xlabel("Predicted Bucket")
#     plt.ylabel("True Bucket")
#     plt.title("Rank Mode: Bucketed Confusion Matrix")
#     plt.tight_layout()
#     plt.show()

def evaluate_rank(triplets):
    """
    Rank mode:
    Scores 1–10.
    Compute MSE and bucketed accuracy.
    Plot bucketed confusion matrix (percentages).
    """

    true_scores = []
    pred_scores = []

    for sentence, model_rank, user_rank in triplets:
        true_scores.append(user_rank)
        pred_scores.append(model_rank)

    # Mean Squared Error
    mse = np.mean([(p - t) ** 2 for p, t in zip(pred_scores, true_scores)])

    # Bucketed Accuracy
    true_buckets = [map_to_bucket(s) for s in true_scores]
    pred_buckets = [map_to_bucket(s) for s in pred_scores]

    correct = sum(tb == pb for tb, pb in zip(true_buckets, pred_buckets))
    bucketed_accuracy = correct / len(true_scores)

    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Bucketed Accuracy: {bucketed_accuracy:.4f}")

    # Confusion matrix (raw counts)
    confusion = np.zeros((3, 3), dtype=int)
    for tb, pb in zip(true_buckets, pred_buckets):
        confusion[tb - 1][pb - 1] += 1  # zero-indexed

    # Convert to percentage matrix row-wise
    confusion_percent = np.zeros_like(confusion, dtype=float)
    for i in range(3):
        row_sum = np.sum(confusion[i])
        if row_sum > 0:
            confusion_percent[i] = 100.0 * confusion[i] / row_sum

    # Plot as percentages
    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion_percent, annot=True, fmt='.1f', cmap='Blues',
                xticklabels=['1–3', '4–6', '7–10'],
                yticklabels=['1–3', '4–6', '7–10'])
    plt.xlabel("Predicted Bucket")
    plt.ylabel("True Bucket")
    plt.title("Rank Mode: Bucketed Confusion Matrix (%)")
    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <sentences_file> <ranks_file> <mode>")
        print("mode: 'filter' or 'rank'")
        sys.exit(1)

    sentences_file = sys.argv[1]
    ranks_file = sys.argv[2]
    mode = sys.argv[3].lower()

    if mode not in ['filter', 'rank']:
        print("Error: mode must be either 'filter' or 'rank'")
        sys.exit(1)

    max_score = 5 if mode == 'filter' else 10

    try:
        rank_dict = load_ranks_to_sentences(sentences_file, ranks_file, max_score)
        sampled_pairs = sample_sentences_per_rank(rank_dict, sample_size_per_rank=20)
        triplets = collect_user_ranks(sampled_pairs, max_score)

        if mode == 'filter':
            evaluate_filter(triplets)
        else:
            evaluate_rank(triplets)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
