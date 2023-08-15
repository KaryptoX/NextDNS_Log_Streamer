# NextDNS API Log Streamer / Exporter
A simple Python script for collecting and exporting NextDNS logs as JSON - file or direct output to STDOUT-. Supports crontab mode or "endless" mode. Simple and optimized for the use in SIEM systems e.g. as scripted input.

## Idea
I've searched for an easy way of structured importing my NextDNS logs to the SIEM/Splunk system I use. In best case without tons of 3rd party bibs,tools or plugins. I've searched through the web and already found some interesting projects (e.g. from rhijjawi/NextDNS-API or b0o/nextdns-logs-export). Unfortunately they were either complex (required some 3rd party bibs/tools) or did not work as expected e.g. provided a non structured data format, did not use the official API or in the end were just too much for "just" exporting logs. Also the scripts did not collect historic data in case of failure e.g. when the API has issues. Therefore I decided to write a short script by my own which only uses standard Python bibs and therefore can run on any system with "default" Python installation. 
> Hint: Thy script was designed for Linux like systems, but should also work on Windows systems if the Linux commands/ file paths etc. will be changed.

## Usage
The script contains some comments which should describe the used variables in details. Anyway here a short usage guide:

Before you run the script ensure that you've set the variables according to the run mode you want to perform.

Add your API Key from NextDNS account settings here:
> apikey="APIKEY"

Add your profiles from the individual NextDNS profile pages to the list:
> profiles = ["PROFILE1","PROFILE2","..."]

Define the fetch interval; ensure that you've set the fetch interval to the same interval you've planned the cronjob e.g. if you are using cron "every minute" = 60 ; in "endless" mode the script will run in that interval too. Values below 20 might cause issues with the NextDNS API and resulting duplicates in output!
> fetch_interval = 60

Define if the script should run in crontab mode or "endless" mode:
> crontab_mode = 1

If you choose "crontab_mode = 0" the script will run endless (except cancelled by user or system) based on the interval set in "fetch_interval = XX"

Should the script export the logs to STDOUT via print or write a file?
> "write_file = 0"

> Default location of JSON export: "/tmp/nextdns_log_streamer.json"

Destinations where the files will be written to
> tmp_file_path = "/tmp/"

Used for temporary files.

Ensure the user who runs the script has rights to write to the destination!

> log_file_path = "/var/log/"

Persistent path; e.g. used for keeping the time.

Ensure the user who runs the script has rights to write to the destination!

## Historic Data

The script will notice if there was a gap (higher than "fetch_interval = XX") between the last runtime and the current runtime and than will ONCE collect the historical logs in between (that no logs are missed). Afterwards it will continue with the current timestamp.
> Because of log duplicate reasons etc. the script will only do the "historic collection" once per runtime!!

Hint! In "crontab_mode = 1" the file in (default location) "/tmp/nextdns_log_streamer_startover.log" must be set from "1" to "0" after e.g. reboot or re-run of the script; else the script will not perform the "historic data collection" anymore! The script automatically sets "1" in that location if an historic run already took place in crontab mode. If you use "crontab_mode = 0" that step is not needed!

Hint! Some systems automatically clean the "/tmp/" location after reboot etc. If thats not the case you can set a crontab entry like following:

> @reboot   sed -i 's/1/0/g' /tmp/nextdns_log_streamer_startover.log   # Informs log-streamer that historic events should be collected ONCE

Which will set "0" to the file automatically after reboot. This tells the script that the "historic collection" was not performed yet.

## API Error Case

In case of an API error e.g. HTTP response code "404" the script will save the last timestamp and will continue in the next run there. That process will be repeated until the logs were collected successfully. After successfull collection the script will continue with the current timestamp to avoid duplicate log collection.

## Known Issues & FAQ
- Duplicate Logs


The script ensures that the timeframes sent to the API are not overlapping. Therefore no duplicates should take place. Nevertheless there seems to be a bug in the API processing of NextDNS. Unfortunately I saw that sometimes some logs will be collected twice although the log was not part of the current timestamp sent to the API. I'm still searching for a solution regarding that point.. Fortunately, this does not seem to occur often.

- Logs Missing

The script fetchs the logs available in your defined profiles for your account. Please ensure that the logs will not be deleted from NextDNS side before collection through the script. The setting can be adjusted for every profile in the NextDNS settings. I recommend using at least 1 day that e.g. in error case also historic logs can be fetched from the script (once).

- Change crontab_mode from "0" to "1"

If you change the crontab mode from "0" to "1" ensure that you've set "0" in "nextdns_log_streamer_startover.log" (or delete the whole file); else the "historic data collection" is deactivated for the initial start.
