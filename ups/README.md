I kept getting the following error.
```
Error: Data stale
```

Usually with errors you are [not the only one!](https://nmaggioni.xyz/2017/03/14/NUT-CyberPower-UPS/)

So check `ups.conf`
```
[dacyberpower]
        driver = usbhid-ups
        port = auto
        desc = "CyberPower AVRG900LCD"
        pollinterval = 15
```

and `upsd.conf`
```
# This defaults to 15 seconds.  After a UPS driver has stopped updating
# the data for this many seconds, upsd marks it stale and stops making
# that information available to clients.  After all, the only thing worse
# than no data is bad data.
#
# You should only use this if your driver has difficulties keeping
# the data fresh within the normal 15 second interval.  Watch the syslog
# for notifications from upsd about staleness.
MAXAGE 25
```
and `upsmon.conf`
```
# upsmon requires a UPS to provide status information every few seconds
# (see POLLFREQ and POLLFREQALERT) to keep things updated.  If the status
# fetch fails, the UPS is marked stale.  If it stays stale for more than
# DEADTIME seconds, the UPS is marked dead.
#
# A dead UPS that was last known to be on battery is assumed to have gone
# to a low battery condition.  This may force a shutdown if it is providing
# a critical amount of power to your system.
#
# Note: DEADTIME should be a multiple of POLLFREQ and POLLFREQALERT.
# Otherwise you'll have "dead" UPSes simply because upsmon isn't polling
# them quickly enough.  Rule of thumb: take the larger of the two
# POLLFREQ values, and multiply by 3.
DEADTIME 15
```
