# loco

**loco** makes it simple to edit remote files with a local editor. Rather than opening a file with a text-based editor on the server (i.e. `vim`) or `scp`ing it back and forth multiple times, just run `loco filename` and your editor of choice will run on your local box.

## Installation

On your local machine (the client you will be SSHing from) and any servers you intend to use `loco` with, install via:

    $ python setup.py install

## Usage

loco is made up of two components: The server, which runs on your local computer, and the client, which is run from the remote machine.

The included `locossh` script automates starting an instance of `locod` locally, then opening an SSH session and remote tunnel to the specified host.

Connect via SSH to the remote server:

    local$ locossh remote@remote.host

On the remote server, edit a file:

    remote$ loco /etc/apache2/apache2.conf

## License

Created by [Ian Preston](https://ian-preston.com).

Available under the MIT License.