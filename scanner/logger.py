import structlog


def configure_logging():
    structlog.configure(
        processors=[
            structlog.processors.EventRenamer("msg"),
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", key="ts"),
            structlog.processors.LogfmtRenderer(
                key_order=["ts", "level", "msg"],
                bool_as_flag=False,
            ),
        ],
    )
