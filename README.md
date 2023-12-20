# BluOS Inky

A simple Python-based script for showing the track information and album cover of the currently playing music from a [BluOS](https://bluos.io/) player to an [InkypHAT](https://github.com/pimoroni/inky-phat) ePaper display.

The script is compatible to the Red/Black/White 250x122 pixels display, but it can be trivially adapted to other colours or dimensions.

The script displays the album cover as a low resolution (122x122 pixels) Red/Black/White image and prints the `title1`, `title2` and `title3` fields of the currently playing track, which typically contain the track title, artist and album title.

You can read more at the [BluOS API](https://content-bluesound-com.s3.amazonaws.com/uploads/2022/07/BluOS-Custom-Integration-API-v1.5.pdf).

## Initial Configuration

Fill in `myconfig-example.py` and rename it to `myconfig.py`.

Update the `BLUOS_IP` with the IP address of your BluOS player. `BLUOS_PORT` is the port number of the service.
A guide on how to find the IP address of your BluOS player is available [here](https://support.bluos.net/hc/en-us/articles/360000463947-How-do-I-find-the-IP-Address-of-my-Player-).

## Execution

The script can be executed as follows:

`$ python3 ./bluos-inky.py`

## Installation as a Service

In a Linux environment, such as a Raspberry Pi, you can install it to run as a service by executing:

`$ ./install-as-service.sh`

You can restart the service:

`$ ./restart.sh`

You can follow the output in the system journal as follows:

`$ ./log.sh`

## Acknowledgements

The `inkyconvert.py` script is based on [inky-conv](https://github.com/RubenLagrouw/inkyconv).
