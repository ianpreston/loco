#!/usr/bin/python
import SocketServer
import tempfile
import subprocess
import os
import json

LOCO_HOST = 'localhost'
LOCO_PORT = 4206
LOCO_FALLBACK_EDITOR = 'gedit'
LOCO_HEADER_DELIMITER = '\n'


class LocoServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class LocoHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.request_headers = None
        self.response_headers = None
        self.raw_request = None
        self.request_file_contents = None

    def determine_editor(self):
        if self.request_headers.get('editor', None):
            return self.request_headers['editor']
        if os.environ.get('LOCO_EDITOR', None):
            return os.environ['LOCO_EDITOR']
        if os.environ.get('EDITOR', None):
            return os.environ['EDITOR']
        
        return LOCO_FALLBACK_EDITOR

    def respond_success(self, new_file_contents):
        self.response_headers = {
            'success': True
        }
        self.request.sendall(json.dumps(self.response_headers) +
            LOCO_HEADER_DELIMITER +
            new_file_contents)

    def respond_error(self, error_code, error_text):
        self.response_headers = {
            'success': False,
            'error_code': error_code,
            'error_text': error_text
        }
        self.request.sendall(json.dumps(self.response_headers) + LOCO_HEADER_DELIMITER + '\n')

    def parse_request(self):
        s = self.raw_request.split(LOCO_HEADER_DELIMITER)
        self.request_headers = json.loads(s[0])
        self.request_file_contents = '\n'.join(s[1:])
        
    def handle(self):
        self.raw_request = self.request.recv(65536)
        temp_filename = tempfile.mkstemp()[1]

        self.parse_request()

        with open(temp_filename, 'wb') as f:
            f.write(self.request_file_contents)
            f.flush()
        
        with open('/dev/null', 'rwb') as devnull:
            try:
                subprocess.check_call(self.determine_editor() + ' ' + temp_filename,
                                      shell=True,
                                      stdin=devnull,
                                      stdout=devnull,
                                      stderr=devnull)
            except OSError, e:
                self.respond_error(0, 'spawning editor failed: ' + str(e))
                return
            except subprocess.CalledProcessError, e:
                self.respond_error(0, 'editor exited with status code: ' + str(e.returncode))
                return
            except:
                self.respond_error(0, 'spawning editor child process failed')
                return

        with open(temp_filename, 'r') as f:
            self.respond_success(f.read(65536))