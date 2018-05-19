import loggging

LOG_FORMATTER = '%(asctime)s [%(levelname)s] %(name)s %(filename)s:%(lineno)d %(message)s'

LOG_STREAM_HANDLER = loggging.StreamHandler()
LOG_STREAM_HANDLER.setFormatter(LOG_FORMATTER)
LOG_STREAM_HANDLER.setLevel(loggging.DEBUG)

loggging.root.addHandler(LOG_STREAM_HANDLER)
