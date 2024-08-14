from cnegng.main import main


def test_main_prints_message(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "hi boss\n"
