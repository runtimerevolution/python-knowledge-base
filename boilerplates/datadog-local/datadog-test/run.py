import logging

import json_log_formatter

formatter = json_log_formatter.JSONFormatter()

json_handler = logging.FileHandler(filename='./log/my-log.json')
json_handler.setFormatter(formatter)

logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

class Logger:
    def __init__(self, service=None, tags={}):
        self.main_tags = tags
        if service is not None:
            self.service = service

    def set_service(self, service):
        self.service = service

    def _log(self, log_level, message, tags={}):
        """
        log_level:
            type: string
            value: debug, info, warning, error
        message:
            type: string
            value: something relevant, unlike any of us
        service:
            type: string
            value: `service name`
        tags:
            type: hash
            value: e.g. { 'tag1': 'val1', 'tag2': val2 }
        """
        default_hash = {"service": self.service, "environment": 'DEV', "status": log_level}
        all_hash = {**self.main_tags, **default_hash, **tags}
        getattr(logger, log_level)(message, exc_info=True, extra=all_hash)

    def debug(self, message, tags={}):
            self._log("debug", message, tags)

    def info(self, message, tags={}):
            self._log("info", message, tags)

    def warning(self, message, tags={}):
            self._log("warning", message, tags)

    def error(self, message, tags={}):
            self._log("error", message, tags)

log = Logger('mega-service')

# logger.info('Superior testing!', extra={'referral_code': '52d6ce', 'service': 'local-testing-runtime'})
# logger.error('Superior error testing!', exc_info=1, extra={'referral_code': '52d6ce', 'service': 'local-testing-runtime'})
try:
    raise Exception('I failed')
except Exception as e:
    log.error('Superior error testing!', tags={'referral_code': '52d6ce'})
    logger.error('Superior error testing!', exc_info=1, extra={'referral_code': '52d6ce', 'service': 'local-testing-runtime', 'status': 'error'})

logger.warning('Medriocre warning testing!', exc_info=1, extra={'referral_code': '52d6ce', 'service': 'local-testing-runtime'})
# raise Exception('OMG I Failed!')

