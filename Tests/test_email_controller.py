# from unittest import mock, TestCase
# from Controllers import email_controller
# mc = email_controller.MailControl()
#
#
# class TestMailController(TestCase):
#
#     @mock.patch("Controllers.email_controller.smtplib")
#     @mock.patch("Controllers.email_controller.MIMEMultipart")
#     def test_build_email(self, mock_MIMEMultipart, mock_smtplib):
#         receiver = "email@email.com"
#         title = "test"
#         message = "message..."
#         mock_MIMEMultipart.return_value = None
#         self.assertFalse(mc.build_email(receiver, title, message))
#
#         mock_MIMEMultipart.return_value = mock.MagicMock()
#         mock_MIMEMultipart.__getitem__.return_value = ""
#         self.assertTrue(mc.build_email(receiver, title, message))
