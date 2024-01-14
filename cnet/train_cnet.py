import argparse
import subprocess
import os 




def receive_argument(): 
    parser = argparse.ArgumentParser(description='Run YOLO.')
    parser.add_argument('--output', type=str, required=True,
                        help='Output directory')
    parser.add_argument('--network', type=str, required=True,
                        help='Network name (dnet or cnet).')
    parser.add_argument('--model', type=str, required=True,
                        help='Model name (e.g, yolo8s, no .pt extension)')
    parser.add_argument('--dataset', type=str, required=True,
                        help='Name of .yaml file for the dataset.') 
    parser.add_argument('--num_classes', type=str, required=True,
                        help='Number of classes.')
    parser.add_argument('--obj_per_class', type=str, required=True,
                        help='Object instances per class (data per class).')
    parser.add_argument('--epochs', type=str, required=True,
                        help='Number of epochs to run.') 
    parser.add_argument('--batch', type=str, required=True,
                        help='Batch size to use for training.')      
    return parser.parse_args()


def main():
    args = receive_argument()   
    print(args.network)
    print(args.model)
    print(args.dataset)
    print(args.num_classes)
    print(args.obj_per_class)
    print(args.epochs)
    print(args.batch)


if __name__ == "__main__":
    main()