"""
my_packageのテストモジュール

このモジュールでは、my_packageの機能をテストします。

テスト対象:
    - main関数の動作確認
"""

from my_package import main
from pytest_mock import MockerFixture


def test_main(mocker: MockerFixture) -> None:
    """
    main関数のテスト

    期待される動作:
        - "Hello from my-package!"というメッセージが標準出力に出力されること
        - print関数が1回呼び出されること
    """
    # Arrange
    mock_print = mocker.patch("builtins.print")

    # Act
    main()

    # Assert
    mock_print.assert_called_once_with("Hello from my-package!")
