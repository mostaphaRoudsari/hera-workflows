from pydantic import ValidationError
import pytest

from hera.v1.existing_volume import ExistingVolume
from hera.v1.resources import Resources
from hera.v1.volume import Volume


def test_init_raises_on_invalid_mem():
    with pytest.raises(ValidationError):
        Resources(min_mem='4')
    with pytest.raises(ValidationError):
        Resources(max_mem='4')


def test_init_raises_on_invalid_cpu():
    with pytest.raises(ValidationError):
        Resources(max_cpu=-1)
    with pytest.raises(ValidationError):
        Resources(min_cpu=2, max_cpu=1)


def test_init_volume_error_propagates():
    with pytest.raises(ValidationError):
        Resources(volume=Volume(size='1', mount_path='/path'))


def test_init_passes():
    r = Resources(
        min_cpu=1,
        max_cpu=2,
        min_mem='2Gi',
        max_mem='3Gi',
        gpus=1,
        volume=Volume(size='10Gi', mount_path='/path'),
        existing_volume=ExistingVolume(name='test', mount_path='/path2'),
    )
    assert r.min_cpu == 1
    assert r.max_cpu == 2
    assert r.min_mem == '2Gi'
    assert r.max_mem == '3Gi'
    assert r.gpus == 1
    assert r.volume.size == '10Gi'
    assert r.volume.mount_path == '/path'
    assert r.existing_volume.mount_path == '/path2'
