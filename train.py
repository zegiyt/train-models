# -*- coding: utf-8 -*-
"""train.py

Automatically generated by Colaboratory.


"""

# Imports
import numpy as np
import os

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

# Confirm TF Version
print("\nTensorflow Version:")
print(tf.__version__)
print()

# Load Dataset
train_data = object_detector.DataLoader.from_pascal_voc(
    'test_30c/train',
    'test_30c/train',
    ['beef', 'shrimp', 'spinach', 'potato', 'springonion', 'fish', 'garlic', 'pork', 'carrot', 'chilli', 'tomato', 'chicken', 'cabbage', 'egg', 'onion', 'radish', 'bell pepper', 'bitter gourd', 'bok choy', 'broccoli', 'cauliflower', 'corn', 'cucumber', 'ginger', 'lettuce', 'pumpkin', 'tofu', 'egg plant', 'chinese cabbage', 'okra']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    'test_30c/valid',
    'test_30c/valid',
    ['beef', 'shrimp', 'spinach', 'potato', 'springonion', 'fish', 'garlic', 'pork', 'carrot', 'chilli', 'tomato', 'chicken', 'cabbage', 'egg', 'onion', 'radish', 'bell pepper', 'bitter gourd', 'bok choy', 'broccoli', 'cauliflower', 'corn', 'cucumber', 'ginger', 'lettuce', 'pumpkin', 'tofu', 'egg plant', 'chinese cabbage', 'okra']
)

# Load model spec
spec = object_detector.EfficientDetSpec(
  model_name='efficientdet-lite0',
  uri='https://tfhub.dev/tensorflow/efficientdet/lite0/feature-vector/1',
  model_dir='/content/checkpoints',
  hparams='')

# Train the model
model = object_detector.create(train_data, model_spec=spec, batch_size=4, train_whole_model=True, epochs=20, validation_data=val_data)

# Evaluate the model
eval_result = model.evaluate(val_data)

# Print COCO metrics
print("mMAP Metrics:")
for label, metric_value in eval_result.items():
    print(f"{label}: {metric_value}")

# Add a line break after all the items have been printed
print()

# Export the model
model.export(export_dir='.', tflite_filename='EfficientDet0.tflite')

# Evaluate the tflite model
tflite_eval_result = model.evaluate_tflite('EfficientDet0.tflite', val_data)

# Print COCO metrics for tflite
print("mMAP metrics tflite")
for label, metric_value in tflite_eval_result.items():
    print(f"{label}: {metric_value}")
