import threading
from unittest.mock import MagicMock, patch

from cema import module_executor


def test_functionExecutor():
    lock = threading.Lock()
    mock_connection = MagicMock()
    mock_module = MagicMock()
    mock_module.test_func.return_value = "success"
    
    with patch("sys.path", []), patch("cema.module_executor.import_module", return_value=mock_module):
        message = {"modulePath": "test_module.py", "function": "test_func", "args": []}
        module_executor.functionExecutor(lock, mock_connection, message)
    
    mock_connection.send.assert_called_once()
    sent_data = mock_connection.send.call_args[0][0]
    assert sent_data["action"] == "execution finished"
    assert sent_data["result"] == "success"


def test_functionExecutor_invalid_function():
    lock = threading.Lock()
    mock_connection = MagicMock()
    mock_module = MagicMock()
    
    del mock_module.non_existent_func  # This ensures the attribute does not exist
    
    with patch("sys.path", []), patch("cema.module_executor.import_module", return_value=mock_module):
        message = {"modulePath": "test_module.py", "function": "non_existent_func", "args": []}
        module_executor.functionExecutor(lock, mock_connection, message)
    
    mock_connection.send.assert_called_once()
    sent_data = mock_connection.send.call_args[0][0]
    assert sent_data["action"] == "error"
    assert "Module test_module.py has no function non_existent_func." in sent_data["exception"]


def test_launchListener():
    with patch("cema.module_executor.Listener") as MockListener, patch("cema.module_executor.getMessage", side_effect=[{"action": "exit"}]):
        mock_listener = MockListener.return_value.__enter__.return_value
        mock_connection = mock_listener.accept.return_value.__enter__.return_value
        
        module_executor.launchListener()
        
        mock_connection.send.assert_called_with({"action": "exited"})
