# FastText in Tensorflow

This based on the ideas in Facebook's [FastText](https://github.com/facebookresearch/fastText) but implemented in
Tensorflow. However, it is not an exact replica of fastText. Instead I
only implement the classifier using an embedding layer to classification.
I do not intend to implement heirarchical softmax, instead using nce
loss for training.

I may implement skipgram and cbow training later.

<< Still WIP >>

## Implemented:
- classification of text using word embeddings
- char ngrams, hashed to n bins
- train, test and predict programs

## Not Implemented:
- separate word vector training
- heirarchical softmax (I'm using NCE (sampled) loss instead).
- quantize models

# Usage

The following are examples of how to use the applications. Get full help with
`--help` option on any of the programs.

To transform input data into tensorflow Example format, an example:

    process_input.py --facebook_input=queries.txt --model_dir=. --ngrams=2,3,4

Or, using a text file with one example per line with an extra file for labels:

    process_input.py --text_input=queries.txt --labels=labels.txt --model_dir=.

To train a text classifier:

    classifier.py \
      --train_records=queries.tfrecords \
      --eval_records=queries.tfrecords \
      --label_file=labels.txt \
      --vocab_file=vocab.txt \
      --model_dir=model

To predict classifications for text:

    classifier.py
      --predict_records=queries.tfrecords \
      --label_file=labels.txt \
      --vocab_file=vocab.txt \
      --model_dir=model

# Facebook Examples

You can compare with Facebook's fastText by running similar examples
to what's provided in their repository.

    ./classification_example.sh
    ./classification_results.sh
