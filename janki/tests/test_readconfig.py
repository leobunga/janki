from os.path import join as opj, dirname as opd
from pytest import raises
from janki.core.config import readconfig
from janki.common.exceptions import ConfigError

def test_readgood():
    ret = readconfig(opj(opd(__file__),'fixtures','goodconf'), _test=True)
    assert ret['a'] == 1
    assert ret['b'] == '2'
    assert ret['c'] == [1,2,3]
    assert ret['d'] == {1:1, 2:2, 3:3}
    assert 'e' not in ret
    assert ret['f'](2) == 4

def test_readbad():
    with raises(ConfigError):
        ret = readconfig(opj(opd(__file__),'fixtures','badconf'), _test=True)
