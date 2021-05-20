from Controllers import email_controller, log_sales_controller
class_email = email_controller.MailControl()

log_sales_controller.automatic_get_sales_from_yesterday()
class_email.send_email_to_user()
