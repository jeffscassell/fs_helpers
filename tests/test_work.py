from fs_helpers.work import cleanFilename



def test_convertFilename():
    filename = "here-is a name"
    assert cleanFilename(filename) == "here_is_a_name"
    
    filename = "some illegal (':'^') characters"
    assert cleanFilename(filename) == "some_illegal_(''')_characters"