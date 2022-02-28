# Nentau Police Office - 2

- flag2.txt permission
    - `-r--------   1 root     root       33 Feb 18 07:56 flag2.txt`
- sudoer file
    - `/etc/sudoers.d/sudoers-tsj`:

    ```
    tsjadmin workstation=(ALL:ALL) /bin/cat
    ```

- use sudo `-h` option to bypass host limit
    - `sudo -h workstation /bin/cat /flag*`
    - `TSJ{What_use_of_the_-h_option???}`
