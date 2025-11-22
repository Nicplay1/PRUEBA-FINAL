import threading
from django.core.mail import send_mail

def enviar_correo_async(subject, message, from_email, recipient_list):
    """
    Envía un correo usando un hilo separado para no bloquear la vista.
    """
    thread = threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, recipient_list),
        kwargs={'fail_silently': False}
    )
    thread.start()
