# Path Tools

Scripts specifically used to inspect, modify, and extract PRIVATE data

## inspection/ tools

scripts that specifically aid in inspecting PRIVATE data

### filter_viewports.py

extract PRIVATE or specific pieces PRIVATE that match the given filter(s) from a `PRIVATE.json`

    ./filter_viewports.py PRIVATE.json --include "PRIVATE" --extract "{PRIVATE: PRIVATE}"

### filter_scan_event.py

extract PRIVATE or specific pieces of a PRIVATE that match the given filter(s) from a `PRIVATE.json`

    ./filter_scan_event.py PRIVATE.json --include "PRIVATE" --extract "{PRIVATE : [PRIVATE, PRIVATE, PRIVATE]}"

### get_viewport_images.py

Find all PRIVATE results and print out some PRIVATE.

## modification/ tools

scripts that specifically aid in modifying PRIVATE data

### add_image_dimensions_to_keypoints.py

Add image dimension to PRIVATE keypoint files
