import re

def is_crop_key(s3_url):
    return s3_url.find('crop-') >= 0

def get_key(s3_url, no_full_res=False, crop=False):
    # URL can be URL or just the key
    if no_full_res:
        assert not crop, 'Robot currently does not support crop + low res'
        return pluck_key(s3_url, crop)
    return re.sub(r'-Q(\d{3})-S(\d\.\d{3})', '-Q095-S1.000', pluck_key(s3_url, crop))

def is_crop_key(s3_url):
    return s3_url.find('crop-') >= 0


def get_key(s3_url, no_full_res=False, crop=False):
    # URL can be URL or just the key
    if no_full_res:
        assert not crop, 'Robot currently does not support crop + low res'
        return pluck_key(s3_url, crop)
    return re.sub(r'-Q(\d{3})-S(\d\.\d{3})', '-Q095-S1.000', pluck_key(s3_url, crop))


def get_key_bucket(s3_url, no_full_res=False, vp_id="", crop=False):
    if not s3_url:
        return {'bucket': "", 'key': "", 'vp_id': ""}

    key = get_key(s3_url, no_full_res=no_full_res, crop=crop)

    key = {'bucket': pluck_bucket(s3_url),
           'key': key,
           'vp_id': vp_id}
    return key


def pluck_bucket(s3_url):
    if s3_url.startswith('s3:'):
        return re.search(r's3:\/\/([\-\w\d]+)\/', s3_url).group(1)
    return re.search(r'https:\/\/([\-\w\d\/]+)', s3_url).group(1)


def pluck_key(s3_url, crop=False):
    if crop:
        try:
            return re.search(r':\/\/([\-\w\d]+)\/(.+)', s3_url).group(2)
        except: # Old way
            return re.search(r'(PRIVATE\/[\-\.\w\d\/\~]+)', s3_url).group(0)
    try:
        key = re.search(r':\/\/([\-\w\d]+)\/(.+)', s3_url).group(2)
    except: # Old way:
        key = re.search(r'(PRIVATE\/[\-\.\w\d\/]+)', s3_url).group(0)
    if is_crop_key(s3_url):
        key = key.replace('crop-', 'full-') + '-Q095-S1.000.jpg'
    return key

def pluck_play(PRIVATE):
    return PRIVATE


def pluck_path(PRIVATE):
    return PRIVATE


def pluck_sequence(PRIVATE):
    return PRIVATE

def get_cam_name(PRIVATE):
    return PRIVATE

def get_key_crop(PRIVATE):
    return PRIVATE
