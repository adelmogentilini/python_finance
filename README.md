# Strategy trade skeleton

This is a project that can serve as a basic skeleton for developing applications to test trading strategies. It uses data taken from YAHOO FINANCE with the limitations of the library itself. For example, data related to 15-minute intervals may be limited to the last 60 (59 to avoid time-related issues) days of quotes.

## Customization of the simulation

The simulation can be conducted on multiple assets simultaneously, but the provided result will be cumulative, as if we had invested simultaneously in all the assets.
