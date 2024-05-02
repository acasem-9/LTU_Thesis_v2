'''
This script evaluates the performance of a text recognition system by calculating various metrics,
including Word Recognition Accuracy (WRA), Character Recognition Accuracy (CRA), Word Error Rate (WER), 
and Character Error Rate (CER). It reads the detection results and the ground truth from text files, 
compares them, and computes the evaluation metrics.
'''

from torchmetrics.text import WordErrorRate, CharErrorRate
from pathlib import Path

def read_file(filepath):
    data = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                data[parts[0]] = parts[1]
    return data

def calculate_metrics(detections, ground_truth):
    wer_metric = WordErrorRate()
    cer_metric = CharErrorRate()

    # Preparing lists for holdiong hypothesis and references
    hypothesis = [detections[k] for k in sorted(detections) if k in ground_truth]
    references = [ground_truth[k] for k in sorted(ground_truth) if k in detections]

    # Update metrics
    wer_metric.update(hypothesis, references)
    cer_metric.update(hypothesis, references)

    # Calculate word and character recognition accuracy
    wra = sum(1 for k in detections if k in ground_truth and detections[k] == ground_truth[k]) / len(ground_truth)
    total_chars = sum(len(ground_truth[k]) for k in ground_truth if k in detections)
    correct_chars = sum(sum(1 for i, c in enumerate(detections[k]) if i < len(ground_truth[k]) and c == ground_truth[k][i])
                        for k in detections if k in ground_truth)
    cra = correct_chars / total_chars

    return wra, cra, wer_metric.compute(), cer_metric.compute()

def main():
    detections_path = input("Enter the path to the detection folder's image_to_word_mapping.txt: ").strip('"')
    test_path = input("Enter the path to the test folder's image_to_word_mapping.txt: ").strip('"')

    detections = read_file(detections_path)
    ground_truth = read_file(test_path)

    wra, cra, wer, cer = calculate_metrics(detections, ground_truth)
    print(f"Word Recognition Accuracy (WRA): {wra:.2%}")
    print(f"Character Recognition Accuracy (CRA): {cra:.2%}")
    print(f"Word Error Rate (WER): {wer:.2%}")
    print(f"Character Error Rate (CER): {cer:.2%}")

    output_file_path = Path(detections_path).parent / "evaluation_metrics.txt"
    with open(output_file_path, 'w') as file:
        file.write(f"Word Recognition Accuracy (WRA): {wra:.2%}\n")
        file.write(f"Character Recognition Accuracy (CRA): {cra:.2%}\n")
        file.write(f"Word Error Rate (WER): {wer:.2%}\n")
        file.write(f"Character Error Rate (CER): {cer:.2%}\n")

    print(f"Metrics saved in {output_file_path}")

if __name__ == "__main__":
    main()
