import logging

from api.core.config import get_settings

logger = logging.getLogger(__name__)


async def send_email(subject: str, recipients: list[str], body: str) -> None:
    settings = get_settings()
    if not settings.mail_configured:
        logger.info("Email not configured; skipping '%s' to %s", subject, recipients)
        return

    recipients = [email for email in recipients if email]
    if not recipients:
        return

    from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

    config = ConnectionConfig(
        MailStartTLS=settings.mail_starttls,
        MailSSL=settings.mail_ssl_tls,
        MailUsername=settings.mail_username,
        MailPassword=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_FROM_NAME=settings.app_name,
        USE_CREDENTIALS=settings.use_credentials,
        VALIDATE_CERTS=True,
    )

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="plain",
    )

    try:
        await FastMail(config).send_message(message)
    except Exception:
        logger.exception("Failed to send email '%s' to %s", subject, recipients)
