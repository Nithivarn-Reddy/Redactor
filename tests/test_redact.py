from project1 import *


def test_readFiles(pattern=['*.text','otherfiles/*.md']):
    assert readFiles(pattern) is not None

def test_redact_names():
    data,count=redact_names(["Martin Luther king."])
    assert len(data) != 0 and count[0] == 2

def test_redact_dates():
    data,count = redact_dates(['09/09/2020','05/25/1995'])
    assert len(data) !=0 and len(count) == 2

def test_redact_genders():
    data,count=redact_genders(['he she man woman.'])
    assert len(data) != 0 and count[0] == 4

def test_redact_concept():
    data,sentences,count=redact_concept(['study school university post graduate.'],'study')
    assert len(data)!=0 and len(sentences)!=0 and len(count)!=0

def test_redact_stats(capsys):
    stats('stdout')
    captured=capsys.readouterr()
    assert '' in captured.out




