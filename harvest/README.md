# Harvesting Tools

A library of tools and interfaces that can grab most data from robots and download locally.

These tools may require PRIVATE and S3 authentication.

Because of the variety in tools and functionality,
    `python3 -m tools.[tool] --help`
is likely the best place to start.


### You've been warned!

These tools are in development and can sometimes misbehave as new updates are released to the
robots. PRIVATE.

If you're planning to run _any_ tool PRIVATE, please PRIVATE by researching the current
state of the PRIVATE. Most of this info can be found by visiting the robot's PRIVATE page.

If you have any questions as about the above passage means, or you encounter an issue reach:
 - Ben Fugate BENJAMIN_FUGATE@jabil.com
 - Austin Herman austin_herman@jabil.com
 - (or slack one of us)

### Known Issues

PRIVATE


## Tools

`browse.py` -- PRIVATE

`collect_viewport_images.py` -- PRIVATE

`harvest_insight_data.py` -- PRIVATE

`harvest_inspect_images.py` -- PRIVATE

`collect_no_sale_images.py` -- PRIVATE

`list_plays.py` -- PRIVATE

`upload_insight_images.py` -- PRIVATE

`cancel_command.py` -- PRIVATE

`pull_realogram.py` -- PRIVATE

`download_scheduled_keys.py` -- PRIVATE

`harvest_sku.py` -- PRIVATE


## Command Line Harvesting

`upload_insight_images.py` provides an interface that will digest filters per viewport as command
line args and pull data using those filters. Only certain keywords and functions can be used in
these filters.

What is available for a filter can be listed using `--key-words` arg.

### USAGE EXAMPLES

    python3 -m tools.upload_insight_images PRIVATE
    python3 -m tools.upload_insight_images PRIVATE
    python3 -m tools.collect_no_sale_images PRIVATE

These three commands will produce the exact same results.

#### Note

PRIVATE

## Harvesting from the Library

the `src/` contains everything used in building the command line tools and is designed to be an
intuitive library to allow a more imaging-advanced user to build tools that target exactly what data
they need.

## Requirements

use python 3.9 and boto3, other python3.X versions may work.

`pip install boto3`

You must have your PRIVATE account set up and PRIVATE keys available locally to use S3 tools.

You must have PRIVATE account credentials set up locally to use PRIVATE.

A docker file is provided to use these tools without installing python libraries but your PRIVATE and
PRIVATE must still be set up locally _and then mounted into the docker container_.
See the Docker section for more info.

## Testing

Unit tests are in `test/unit_tests/`
User end tests are in `test/user_tests/`

Use `python3 -m pytest` to run these tests. Other methods of invoking pytest will likely not work
unless the current directory is added to `sys.path` (this is done automatically when invoking
`python -m ...`)

Integration tests are in test_end_user/
Requires pytest and responses

    pip install pytest responses

Use `pytest test_end_user/` to test these

## Docker

To run a tool using docker, edit the dockerfile to run the command you want, for instance:

`CMD [ "python3", "-m" "PRIVATE" ]`

then to build and run the docker image:

    docker build -t harvesting_tool .
    docker run --rm -it -v $(pwd):/usr/src/app -v PRIVATE -v $PRIVATE harvesting_tool
