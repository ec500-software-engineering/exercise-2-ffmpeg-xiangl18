from ffprobe import ffprobe_sync
from pytest import approx


def test_duration():
    fnin = 'video.avi'
    fnout = 'outputVideo480p.mp4'
    fnout2 = 'outputVideo720p.mp4'
    orig_meta = ffprobe_sync(fnin)
    orig_duration = float(orig_meta['streams'][0]['duration'])
    meta_480 = ffprobe_sync(fnout)
    duration_480 = float(meta_480['streams'][0]['duration'])
    meta_720 = ffprobe_sync(fnout2)
    duration_720 = float(meta_720['streams'][0]['duration'])
    assert orig_duration == approx(duration_480) == approx(duration_720)

