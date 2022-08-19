import os
import tarfile
import time
import numpy as np
import tensorflow as tf
from six.moves import urllib
from PIL import Image


class DeepLabModel(object):
    def __init__(self, input_size=513, use_gpu=True):
        self._input_size = input_size
        self._model_url_path = "models/PRIVATE.tar.gz"
        self._model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        self._model_url_path)
        self._fetch_models()
        self._benchmark_times = []
        self.num_gpus = 0
        if use_gpu:
            self.num_gpus = len(tf.config.experimental.list_physical_devices('GPU'))
            print(f"Num GPUs Available: {self.num_gpus}")
        self._graph_def = self._get_graph_def()
        self._graph = tf.compat.v1.Graph()
        with self._graph.as_default():
            tf.import_graph_def(self._graph_def, name='')

        if use_gpu:
            self._sess = tf.compat.v1.Session(graph=self._graph,
                                              config=tf.compat.v1.ConfigProto(
                                                  allow_soft_placement=True,
                                                  log_device_placement=False))
        else:
            self._sess = tf.compat.v1.Session(graph=self._graph,
                                              config=tf.compat.v1.ConfigProto(
                                                  device_count={"GPU": 0}))

    def blur_from_disk(self, image_path, save_mask=False):
        image_name = os.path.basename(image_path)
        print(f"Blurring {image_name}")

        image = Image.open("%s.jpg" % image_path)
        occluded_image, mask = self.blur(image)

        image_dir = os.path.dirname(image_path)
        image_name = image_name.split('.')[0]

        if save_mask:
            mask.save(os.path.join(image_dir, image_name + '_mask.png'))

        occluded_image.save(os.path.join(image_dir, image_name + '_blur.png'))

    def blur(self, image):
        seg_map, blur_image = self._segment(image)
        if blur_image:
            mask = self._segment_map_to_mask(seg_map, self._create_mask_colormap())
            mask = mask.resize(image.size, Image.NEAREST)
            return Image.alpha_composite(image.convert("RGBA"), mask), mask, blur_image

        return None, None, blur_image

    def _fetch_models(self):
        if not os.path.exists(self._model_path):
            print(f"Downloading model: {self._model_path}")
            urllib.request.urlretrieve("http://download.tensorflow.org/" + self._model_url_path,
                                       self._model_path)

    def _get_graph_def(self):
        graph_def = None
        tar_file = tarfile.open(self._model_path)
        for tar_info in tar_file.getmembers():
            if "frozen_inference_graph" in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.compat.v1.GraphDef.FromString(file_handle.read())
                break
        tar_file.close()
        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')
        return graph_def

    def _segment(self, image):
        width, height = image.size
        resize_ratio = 1.0 * self._input_size / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert("RGB").resize(target_size, Image.ANTIALIAS)
        start = time.time()
        seg_map = self._sess.run("SemanticPredictions:0",
                                 feed_dict={"ImageTensor:0": [np.asarray(resized_image)]})[0]
        self._benchmark_times.append(time.time() - start)

        if 15 not in seg_map:
            # nothing we care about was detected so return nothing
            return seg_map, False

        # floor all values != 15 to 0 (functionally this will only segment people)
        seg_map[seg_map != 15] = 0

        return seg_map, True

    @staticmethod
    def _create_mask_colormap():
        mask_colormap = np.full((256, 4), (128, 128, 128, 255), dtype=int)
        mask_colormap[0] = (0, 0, 0, 0)
        return mask_colormap

    @staticmethod
    def _segment_map_to_mask(seg_map, colormap):
        return Image.fromarray(colormap[seg_map].astype(np.uint8))

    def get_average_time(self):
        return sum(self._benchmark_times) / len(self._benchmark_times)


if __name__ == "__main__":
    model_path = "models/PRIVATE.tar.gz"
    images_path = "../../tests/data/"
    images = []

    for i in range(5):
        images.append(os.path.join(images_path, 'image' + str(i + 1)))

    model = DeepLabModel()
    for image_path in images:
        model.blur_from_disk(image_path)
