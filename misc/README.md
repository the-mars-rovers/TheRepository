# Miscellaneous

Useful scripts and other bits and bobs.

## Eduroam on rPi

Add to `/etc/wpa_supplicant/wpa_supplicant.conf`:

```text
network={
        ssid="eduroam"
        scan_ssid=1
        key_mgmt=WPA-EAP
        eap=PEAP
        identity="<r-nr>@kuleuven.be"
        password=hash:<passwdhash>
        phase1="peaplabel=0"
        phase2="auth=MSCHAPV2"
}
```

Replace `<r-nr>` with your user ID ("r-nummer", not username).
Replace `<passwdhash>` with the output of `echo -n plaintext_password_here | iconv -t utf16le | openssl md4`.

Don't forget to remove the command history, so your password doesn't end up in there for everyone to see.
Run `history` and then `history -d <nr>` to delete a single line.   

## `showip`

Shows the IPv4 address on an OLED display (up to 2 with 14pt font on 128x32)

Requires installing the Adafruit library (it's a git submodule).

This script updates on it's own every 4 seconds and slightly moves the text to prevent burn-in.

## `postip`

Pushes some data (including the date/time, IP address, wifi status) to a particular [ix.io](http://ix.io) file.
The service file only works if your systemd has been setup to use the proper `network-online.target`.

Don't forget to setup your ix.io "account" via a `~/.netrc` entry, for example:

```text
machine ix.io
    login my_raspberry_pi
    password a_random_string_dont_use_a_real_password_its_unsecured
```

Then publish something to get an ID: `date | ix`, and use that ID in the script.
