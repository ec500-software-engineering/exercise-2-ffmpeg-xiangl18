import main_sync
import pytest
import subprocess
import os
import json


@pytest.fixture(scope='session')
def video_path(tmpdir_factory):
    output_path = tmpdir_factory.mktemp(
        'media'
    ).join('test_video.avi')
    cmd = 'ffmpeg -f lavfi -i smptebars -t 10 {}'.format(
        str(output_path)
    )
    subprocess.check_call(
        cmd.split(' ')
    )
    return output_path


class Test(object):
    # def test_run_ffmpeg(self, video_path):
    #     """
    #     test ffmpeg module
    #     """
    #     output_file, output_file2, flist = self.make_input(video_path)
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(main_async.run(flist))
    #     loop.stop()
    #     assert os.path.exists(video_path)
    #     assert os.path.exists(output_file)
    #     assert os.path.exists(output_file2)
    #
    def test_run_ffmpeg_sync(self, video_path):
        output_file, output_file2, flist = self.make_input(video_path)
        main_sync.main(flist)
        assert os.path.exists(video_path)
        assert os.path.exists(output_file)
        assert os.path.exists(output_file2)

    def get_duration(self, filename):
        """
        get video duration for test
        """
        proc_out = subprocess.Popen(
            ['ffprobe', '-print_format', 'json',
             '-show_format', '-show_streams', filename],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE
        )
        json_raw = ''
        for line in proc_out.stdout.readlines():
            json_raw += line.decode('utf-8')
        json_data = json.loads(json_raw)
        duration = int(round(float(json_data['format']['duration'])))
        return duration

    def make_input(self, video_path):
        """
        make input and output for test
        """
        output_file = os.path.join(
            os.path.dirname(
                os.path.realpath(video_path)
            ),
            'video_test_480.mp4'
        )
        output_file2 = os.path.join(
            os.path.dirname(
                os.path.realpath(video_path)
            ),
            'video_test_720.mp4'
        )
        flist = [{'input': video_path, 'output': output_file, 'rate': '1', 'fps': '30', 'res': '480'},
                 {'input': video_path, 'output': output_file2, 'rate': '2', 'fps': '30', 'res': '720'}]
        return output_file, output_file2, flist

    def test_duration(self, video_path):
        """
        test output videos duration
        """
        output_file, output_file2, flist = self.make_input(video_path)
        duration_orig = self.get_duration(str(video_path))
        duration_480 = self.get_duration(str(output_file))
        duration_720 = self.get_duration(str(output_file2))
        assert duration_orig == pytest.approx(duration_480) == pytest.approx(duration_720)

    def test_example_duration(self):
        """
        test given videos duration
        """
        fnin = 'video.avi'
        fnout = 'outputVideo480p.mp4'
        fnout2 = 'outputVideo720p.mp4'
        duration_orig = self.get_duration(fnin)
        duration_480 = self.get_duration(fnout)
        duration_720 = self.get_duration(fnout2)
        assert duration_orig == pytest.approx(duration_480) == pytest.approx(duration_720)


        assert duration_orig == pytest.approx(duration_480) == pytest.approx(duration_720)
