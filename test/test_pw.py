import re
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
from pathlib import Path

import pytest

spec = spec_from_loader("pw", SourceFileLoader("pw", str(Path(__file__).parent.parent.joinpath('pw'))))
pw = module_from_spec(spec)
spec.loader.exec_module(pw)


def test_toml_wraptor_value():
    toml = Path(__file__).with_name('test.toml')
    assert pw.toml_wraptor_value(toml, 'tool1') == 'tool1 pip'
    assert pw.toml_wraptor_value(toml, 'tool2') == 'tool2 pip'
    assert pw.toml_wraptor_value(toml, 'tool3').split() == ['a', 'b', 'c']
    assert pw.toml_wraptor_value(toml, 'tool4').split() == ['d', 'e']
    assert pw.toml_wraptor_value(toml, 'tool5') == 'tool5 pip'
    assert pw.toml_wraptor_value(toml, 'tool6') == 'tool6 pip'


def test_toml_aliases():
    toml = Path(__file__).with_name('test.toml')
    assert pw.toml_aliases(toml) == {'run': 'tool1 start', 'test': 'tool2 run test'}


def test_parse_args():
    cmd, args, upgrade, clean_install = pw.parse_args(['pw', 'command'])
    assert cmd == 'command' and args == [] and not upgrade and not clean_install

    cmd, args, upgrade, clean_install = pw.parse_args(['pw', 'command', 'arg1', 'arg2'])
    assert cmd == 'command' and args == ['arg1', 'arg2'] and not upgrade and not clean_install

    cmd, args, upgrade, clean_install = pw.parse_args(['pw', '--upgrade', 'command', 'arg1'])
    assert cmd == 'command' and args == ['arg1'] and upgrade and not clean_install

    cmd, args, upgrade, clean_install = pw.parse_args(['pw', '--clean-install', 'command'])
    assert cmd == 'command' and args == [] and not upgrade and clean_install

    with pytest.raises(Warning, match=f'Python Wraptor version {pw.VERSION}'):
        pw.parse_args(['pw', '--version', 'command'])

    with pytest.raises(Warning, match=re.escape(pw.HELP)):
        pw.parse_args(['pw'])


def test_parse_args_with_alias():
    toml = Path(__file__).with_name('test.toml')
    aliases = pw.toml_aliases(toml)
    cmd, args, upgrade, clean_install = pw.parse_args(['pw', 'run'], aliases)
    assert cmd == 'tool1' and args == ['start'] and not upgrade and not clean_install
    cmd, args, upgrade, clean_install = pw.parse_args(['pw', '--clean-install', 'test', 'my-test'], aliases)
    assert cmd == 'tool2' and args == ['run', 'test', 'my-test'] and not upgrade and clean_install
