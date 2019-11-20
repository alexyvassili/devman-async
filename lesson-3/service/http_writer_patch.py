import logging


def _write_no_exception(self, chunk: bytes) -> None:
    try:
        self.original_write(chunk)
    except ConnectionResetError as exc:
        logging.debug('ConnectionResetError exception suppressed')


def patch_streamwriter(http_writer):
    http_writer.StreamWriter.original_write = http_writer.StreamWriter._write
    http_writer.StreamWriter._write = _write_no_exception
    # logging.warning('StreamWriter patched to suppress ConnectionResetError\'s')
