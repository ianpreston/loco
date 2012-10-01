# loco

**loco** makes it simple to edit remote files with a local editor. Rather than opening a file with a text-based editor on the server (i.e. `vim`) or `scp`ing it back and forth multiple times, just run `loco filename` and your editor of choice will run on your local box.

## Installation

On every system you wish to use loco with, get a copy of the source tree and run

    $ python setup.py install

## Usage

loco is made up of two components: The server, which runs on your local computer, and the client, which is run from the remote machine.

The optimal way to run loco is to start the daemon on your local machine, then create a reverse SSH tunnel between your machine and the remote machine. Then, connect via SSH. You will be able to run `loco` from the server. Included in the source distribution is a shell script, `locossh`, that automates this process.

Connect via SSH to the remote server:

    local$ locossh remote@remote.host

On the remote server, edit a file:

    remote$ loco /etc/apache2/apache2.conf

## License

Created by [Ian Preston](https://ian-preston.com).

Available under the MIT License.