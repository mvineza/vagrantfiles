## My personal Vagrant environments

Feel free to add or update.

## Quick Demo

[![asciicast](https://asciinema.org/a/yvo8siITBYRy1R4OfjUcQOwNn.svg)](https://asciinema.org/a/yvo8siITBYRy1R4OfjUcQOwNn)

## Detailed Tutorial

1. Ensure ansible and vagrant are installed.

2. Go to target environment. Some of the environments might be still in
   progress (no provisioner, Vagrantfile don't have enough details, etc.) so
   pick another one.

   ```
   cd environments/jenkins
   ```

3. Open `Vagrantfile` and update number of nodes by editing `N` if you want.
   Else, you can just leave the default value.

4. Bootstrap environment. This will bring up "N" VMs and run ansible provisioner
   at the end. The provisioner creates a user on the vagrant machine(s) with
   full sudo access and can do paswordless SSH to the machines.. The username
   that will be created is the same username who ran this command below.

   ```
   vagrant up
   ```
