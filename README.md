# MS Teams Status LED

The user's current availability in Microsoft Teams is indicated by
*user presence states*:

- Available
- Busy
- OnThePhone
- InAMeeting
- DoNotDisturb
- Presenting
- Away
- BeRightBack
- Offline

This tool accesses this information and maps it to a color which is then
displayed by a RGB-LED. The current implementation uses
[BlinkStick Square](https://www.blinkstick.com/products/blinkstick-square).

## MS Teams

MS Teams logs extensively to `%APPDATA%/Microsoft/Teams/logs.txt`. Every change
of the *user presence state* can be found there as well. The script simply
opens the file on regular basis searching for the latest change starting from
the end of the file.

A log entry of interest looks like this:

```text
Thu Jul 13 2023 18:07:10 GMT+0200 (Central European Summer Time) <12116> -- info -- StatusIndicatorStateService: Added Available (current state: Away -> Available)| profileType: AAD
```

A regular expression is used to extract the state.

## Libraries

- BlinkStick library for Python 3.x
  - <https://pypi.org/project/BlinkStick310/1.0.1/>
- file_read_backwards
  - <https://pypi.org/project/file-read-backwards/>
