import numpy as np
import os
import pytest
import tarfile
from urllib.request import urlretrieve

from pysigproc import SigprocFile
from pysigproc.candidate import Candidate


@pytest.fixture(scope="session", autouse=True)
def fil_file(tmpdir_factory):
    temp_dir_path = tmpdir_factory.mktemp("data")
    download_path = str(temp_dir_path) + '/askap_frb_180417.tgz'
    url = 'http://astro.phys.wvu.edu/files/askap_frb_180417.tgz'
    urlretrieve(url, download_path)
    frb_tar = tarfile.open(download_path)
    frb_tar.extractall(path=os.path.dirname(download_path))
    return temp_dir_path.join('28.fil')


def test_pysigproc_obj(fil_file):
    fil_obj = SigprocFile(fil_file)
    assert fil_obj.nchans == 336


def test_get_data(fil_file):
    fil_obj = SigprocFile(fil_file)
    data = fil_obj.get_data(0, 10)
    assert np.isclose(np.mean(data), 128, atol=1)


def test_Candidate(fil_file):
    cand = Candidate(fp=fil_file, dm=475.28400, tcand=2.0288800, width=2, label=-1, snr=16.8128, min_samp=256, device=0)
    assert np.isclose(cand.dispersion_delay(), 0.6254989199749227, atol=1e-3)
