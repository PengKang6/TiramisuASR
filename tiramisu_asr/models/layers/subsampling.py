# Copyright 2020 Huy Le Nguyen (@usimarit)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tensorflow as tf

from ...utils.utils import merge_two_last_dims


class VGG2L(tf.keras.layers.Layer):
    def __init__(self,
                 filters: tuple or list = (32, 64),
                 kernel_size: int or list or tuple = 3,
                 strides: int or list or tuple = 2,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 name="vgg2lsubsampling",
                 **kwargs):
        super(VGG2L, self).__init__(name=name, **kwargs)
        self.conv1 = tf.keras.layers.Conv2D(
            filters=filters[0], kernel_size=kernel_size, strides=1,
            padding="same", name=f"{name}_conv_1",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.conv2 = tf.keras.layers.Conv2D(
            filters=filters[0], kernel_size=kernel_size, strides=1,
            padding="same", name=f"{name}_conv_2",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.maxpool1 = tf.keras.layers.MaxPool2D(
            pool_size=strides,
            padding="same", name=f"{name}_maxpool_1"
        )
        self.conv3 = tf.keras.layers.Conv2D(
            filters=filters[1], kernel_size=kernel_size, strides=1,
            padding="same", name=f"{name}_conv_3",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.conv4 = tf.keras.layers.Conv2D(
            filters=filters[1], kernel_size=kernel_size, strides=1,
            padding="same", name=f"{name}_conv_4",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.maxpool2 = tf.keras.layers.MaxPool2D(
            pool_size=strides,
            padding="same", name=f"{name}_maxpool_2"
        )
        self.time_reduction_factor = self.maxpool1.pool_size[0] + self.maxpool2.pool_size[0]

    def call(self, inputs, training=False, **kwargs):
        outputs = self.conv1(inputs, training=training)
        outputs = tf.nn.relu(outputs)
        outputs = self.conv2(outputs, training=training)
        outputs = tf.nn.relu(outputs)
        outputs = self.maxpool1(outputs, training=training)

        outputs = self.conv3(inputs, training=training)
        outputs = tf.nn.relu(outputs)
        outputs = self.conv4(outputs, training=training)
        outputs = tf.nn.relu(outputs)
        outputs = self.maxpool2(outputs, training=training)

        return merge_two_last_dims(outputs)

    def get_config(self):
        conf = super(VGG2L, self).get_config()
        conf.update(self.conv1.get_config())
        conf.update(self.conv2.get_config())
        conf.update(self.maxpool1.get_config())
        conf.update(self.conv3.get_config())
        conf.update(self.conv4.get_config())
        conf.update(self.maxpool2.get_config())
        return conf


class Conv2dSubsampling2(tf.keras.layers.Layer):
    def __init__(self,
                 filters: int,
                 strides: list or tuple or int = 2,
                 kernel_size: int or list or tuple = 3,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 name="conv2dsubsampling2",
                 **kwargs):
        super(Conv2dSubsampling2, self).__init__(name=name, **kwargs)
        self.conv1 = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size,
            strides=strides, padding="same", name=f"{name}_1",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.conv2 = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size,
            strides=strides, padding="same", name=f"{name}_2",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.time_reduction_factor = self.conv1.strides[0] + self.conv2.strides[0]

    def call(self, inputs, training=False, **kwargs):
        outputs = self.conv1(inputs, training=training)
        outputs = tf.nn.relu(outputs)
        outputs = self.conv2(outputs, training=training)
        outputs = tf.nn.relu(outputs)
        return merge_two_last_dims(outputs)

    def get_config(self):
        conf = super(Conv2dSubsampling2, self).get_config()
        conf.update(self.conv1.get_config())
        conf.update(self.conv2.get_config())
        return conf


class Conv2dSubsampling(tf.keras.layers.Layer):
    def __init__(self,
                 filters: int,
                 strides: list or tuple or int = 2,
                 kernel_size: int or list or tuple = 3,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 name="conv2dsubsampling",
                 **kwargs):
        super(Conv2dSubsampling, self).__init__(name=name, **kwargs)
        self.conv = tf.keras.layers.Conv2D(
            filters=filters, kernel_size=kernel_size,
            strides=strides, padding="same", name=f"{name}_1",
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer
        )
        self.time_reduction_factor = self.conv.strides[0]

    def call(self, inputs, training=False, **kwargs):
        outputs = self.conv(inputs, training=training)
        outputs = tf.nn.relu(outputs)
        return merge_two_last_dims(outputs)

    def get_config(self):
        conf = super(Conv2dSubsampling, self).get_config()
        conf.update(self.conv.get_config())
        return conf
