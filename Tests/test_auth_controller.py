from unittest import TestCase, mock
from Controllers import auth_controller as ac


class TestAuthController(TestCase):

    @mock.patch("Controllers.auth_controller.Fernet")
    def test_encrypt_works(self, mock_Fernet):
        mock_Fernet.return_value = mock.MagicMock()
        mock_Fernet().encrypt.return_value = bytes("gAAAAABgpp7PY73eDDYNTqpP8tCptsZQoeG2IgDZ132a8K_uZV3u7ACsi0XjpUD4HZ66fD-Ta5wve7Y81u3llcifO1PIdvwS1A==".encode())
        content = "testing..."
        key = "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="
        encrypt = ac.encrypt(content, key)
        self.assertEqual(encrypt, "gAAAAABgpp7PY73eDDYNTqpP8tCptsZQoeG2IgDZ132a8K_uZV3u7ACsi0XjpUD4HZ66fD-Ta5wve7Y81u3llcifO1PIdvwS1A==")

    def test_is_encrypted_works(self):
        self.assertTrue(ac.is_encrypted("gAAAAABgpp7PY73eDDYNTqpP8tCptsZQoeG2IgDZ132a8K_uZV3u7ACsi0XjpUD4HZ66fD-Ta5wve7Y81u3llcifO1PIdvwS1A==", "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="))
        self.assertFalse(ac.is_encrypted("test", "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="))

    @mock.patch("Controllers.auth_controller.Fernet")
    def test_decrypt_works(self, mock_Fernet):
        content_encrypted = "kjzgBRBJMOP6d4fQhzqcr4Poheiona"
        mock_Fernet.return_value = mock.MagicMock()
        mock_Fernet().decrypt.return_value = bytes("kjzgBRBJMOP6d4fQhzqcr4Poheiona".encode())
        key = "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="
        self.assertEqual(ac.decrypt(content_encrypted, key), "kjzgBRBJMOP6d4fQhzqcr4Poheiona")