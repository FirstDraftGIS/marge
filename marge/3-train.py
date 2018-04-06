import csv
import georefdata
from pandas import read_csv
import tensorflow as tf
from tensorflow import decode_csv
from tensorflow import estimator
from tensorflow.contrib.layers import bucketized_column, crossed_column, embedding_column, sparse_column_with_keys, sparse_column_with_hash_bucket, real_valued_column

from config import KEEPING, PROCESSED_TRAINING_FILE


MODEL_DIR = "/tmp/marge_model"
TRAIN_DATA = PROCESSED_TRAINING_FILE
TRAIN_EPOCHS = 40
EPOCHS_BETWEEN_EVALS = 2
BATCH_SIZE = 40

_NUM_EXAMPLES = {
    'train': 32561,
    'validation': 16281,
}


_CSV_COLUMNS = KEEPING

# should probably get these based on fieldnames matching with columns
_CSV_COLUMN_DEFAULTS = [ [""], [""], [""], [float(0)], [""], ["n"] ]
print("_CSV_COLUMN_DEFAULTS:", _CSV_COLUMN_DEFAULTS)

base_column_dict = {
    "country_code": sparse_column_with_keys("country_code", keys=georefdata.get_country_codes()),
    "geonames_feature_class": sparse_column_with_keys("geonames_feature_class", keys=georefdata.get_geonames_feature_classes()),
    "geonames_feature_code": sparse_column_with_keys("geonames_feature_code", keys=georefdata.get_geonames_feature_codes()),
    "importance": real_valued_column("importance"),
    "place_type": sparse_column_with_keys("place_type", keys=["B", "N", "P", "T"])
}

base_columns = list(base_column_dict.values())

crossed_columns = []

deep_columns = []

model = estimator.DNNLinearCombinedClassifier(
    model_dir=MODEL_DIR,
    linear_feature_columns=base_columns + crossed_columns,
    dnn_feature_columns=deep_columns,
    dnn_hidden_units=[100, 50])
print("model:", type(model))

def input_fn(data_file, num_epochs=2, shuffle=False, batch_size=40):
    def parse_csv(value):
        columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
        features = dict(zip(_CSV_COLUMNS, columns))
        labels = features.pop("correct")
        return features, tf.equal(labels, 'y')

    dataset = tf.data.TextLineDataset(data_file)

    if shuffle:
        dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

    dataset = dataset.map(parse_csv, num_parallel_calls=5)

    # We call repeat after shuffling, rather than before, to prevent separate
    # epochs from blending together.
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset

train_input_fn =lambda: input_fn(TRAIN_DATA, EPOCHS_BETWEEN_EVALS, False, BATCH_SIZE)

for n in range(TRAIN_EPOCHS // EPOCHS_BETWEEN_EVALS):
  model.train(input_fn=train_input_fn)
