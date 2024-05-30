import pytest

from arr.core.database.dicth import DictH
from arr.core.database.entry import Entry

def test_radix_transform():
    _d = DictH(max_size=100)
    res = _d.radix_calculation("test")
    print(res)
    assert res == 23

@pytest.mark.asyncio
async def test_set_entry():
    _d = DictH(max_size=100)
    entry = Entry(key="1", value="1")
    await _d.set(entry=entry)
    assert _d.print_list() == 1

@pytest.mark.asyncio
async def test_set_two_entries():
    _d = DictH(max_size=100)
    entry = Entry(key="1", value="1")
    await _d.set(entry=entry)
    assert _d.print_list() == 1

    entry2 = Entry(key="2", value="2")
    await _d.set(entry=entry2)
    assert _d.print_list() == 2


@pytest.mark.asyncio
async def test_override_key():
    _d = DictH(max_size=100)
    entry = Entry(key="1", value="1")
    await _d.set(entry=entry)
    assert _d.print_list() == 1

    entry2 = Entry(key="1", value="2")
    await _d.set(entry=entry2)
    assert _d.print_list() == 1
