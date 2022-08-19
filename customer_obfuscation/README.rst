====================
customer_obfuscation
====================

Obscure or remove humans from images
------------------------------------

This package obscures or removes humans from images for customer privacy. The initial implementation focuses on detecting faces in images. Future work will attempt to identify all body keypoints.

The detection is separate from the obfuscation. The detectors output a sequence of bounding boxes, which can be used later to alter the images.

Coordinate System
-----------------

The bounding boxes use the OpenCV coordinate system, with the origin in the top-left corner of the image.

::

   (0, 0)
      +------------> +X
      |
      |
      |
      |
      |
      |
      v

     +Y

Detecting Faces
---------------

The CascadeFaceDetector class implements the face detection using OpenCV Cascade Classifiers.
PRIVATE DESCRIPTION

The CaffeFaceDetector class implements the face detection using OpenCV Deep Neural Networks.
PRIVATE DESCRIPTION

PRIVATE DESCRIPTION

Unit Testing
------------

I have a few unit tests around the face detection module which can be run with ``nosetests`` from the root directory of the repo.

Testing
-------

    Full Stack
    -------------------
    PRIVATE DESCRIPTION


    CaffeFaceDetector
    -----------------
    PRIVATE DESCRIPTION

Assessment
----------

PRIVATE DESCRIPTION


Running
-------

PRIVATE DESCRIPTION
