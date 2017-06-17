"""Process input data into tensorflow examples, to ease training.

Input data is in one of two formats:
- facebook's format used in their fastText library.
- two text files, one with input text per line, the other a label per line.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
import sys
import tensorflow as tf
from itertools import izip
from nltk.tokenize import word_tokenize


tf.flags.DEFINE_string("facebook_input", None,
                       "Input file in facebook train|test format")
tf.flags.DEFINE_string("text_input", None,
                       """Input text file containing one text phrase per line.
                       Must have --labels defined""")
tf.flags.DEFINE_string("labels", None,
                       """Input text file containing one label for
                       classification  per line.
                       Must have --text_input defined.""")
tf.flags.DEFINE_string("output_dir", ".",
                       "Directory to store resulting vector models and checkpoints in")
tf.flags.DEFINE_integer("num_shards", 1,
                        "Number of outputfiles to create")
FLAGS = tf.flags.FLAGS


def CleanText(text):
    return word_tokenise(text.lower())


def ParseFacebookInput(inputfile):
    examples = []
    for line in open(inputfile):
        words = line.split()
        # label is first field with __label__ removed
        match = re.match(r'__label__([0-9]+)', words[0])
        label = int(match.group(1)) if match else None
        # Strip out label and first ,
        words = words[2:]
        examples.append({
            "text": words,
            "label": label
        })
    return examples


def ParseTextInput(textfile, labelsfie):
    examples = []
    with open(textfile) as f1, open(labelsfile) as f2:
        for text, label in izip(f1, f2):
            examples.append({
                "text": CleanText(text),
                "label": int(label),
            })
    return examples


def WriteExamples(examples, outputfile, num_shards):
    """Write examles in TFRecord format.
    Args:
      examples: list of feature dicts.
                {'text': [words], 'label': [labels]}
      outputfile: full pathname of output file
    """
    shard = 0
    num_per_shard = len(examples) / num_shards + 1
    for n, example in enumerate(examples):
        if n % num_per_shard == 0:
            shard += 1
            writer = tf.python_io.TFRecordWriter(outputfile + '-%d-of-%d' % \
                                                 (shard, num_shards))
        record = tf.train.Example()
        record.features.feature["text"].bytes_list.value.extend(example["text"])
        record.features.feature["label"].int64_list.value.append(example["label"])
        if "ngrams" in example:
            records.features.feature["ngrams"].byes_list.value.extend(example["ngrams"])
        writer.write(record.SerializeToString())


def WriteVocab(examples, vocabfile, labelfile):
    words = set()
    labels = set()
    for example in examples:
        words.update(example["text"])
        labels.add(example["label"])
    with open(vocabfile, "w") as f:
        words = sorted(list(words))
        for word in words:
            f.write(word + '\n')
    with open(labelfile, "w") as f:
        labels = sorted(list(labels))
        for label in labels:
            f.write(str(label) + '\n')


def main(_):
    # Check flags
    if not (FLAGS.facebook_input or (FLAGS.text_input and FLAGS.labels)):
        print >>sys.stderr, \
            "Error: You must define either facebook_input or both text_input and labels"
        sys.exit(1)
    if FLAGS.facebook_input:
        inputfile = FLAGS.facebook_input
        examples = ParseFacebookInput(FLAGS.facebook_input)
    else:
        inputfile = FLAGS.text_input
        examples = ParseTextInput(FLAGS.text_input, FLAGS.labels)
    fn, ext = os.path.splitext(inputfile)
    outputfile = os.path.join(FLAGS.output_dir, fn + ".tfrecords")
    WriteExamples(examples, outputfile, FLAGS.num_shards)
    vocabfile = os.path.join(FLAGS.output_dir, fn + ".vocab")
    labelfile = os.path.join(FLAGS.output_dir, fn + ".labels")
    WriteVocab(examples, vocabfile, labelfile)


if __name__ == '__main__':
    tf.app.run()
