# Hacking Paulig Muki for fun and profit

I got my hands on a IOT-enabled coffee mug, Muki from Paulig. There's an e-ink display on the side and you can use your phone to upload images to the mug. The cool (or rather hot) thing is that this is all powered by the heat of the coffee: there's no battery or power plug.

I did what one does with new IOT devices: had a look at how it works and tried to reproduce it without the app.

## The Good

Sending images to the mug is pretty easy. Bluez (the bluetooth stack) and ImageMagick (the image manipulation toolkit) do all the heavy lifting I needed on linux.

## The Bad

Anyone within Bluetooth LE distance can send images to my coffee mug :/

## The Details

Muki documentation mentions it uses Bluetooth Low-Energy and I knew Android allows Bluetooth sniffing see [Hpw to enable Bluetooth HCI snoop log](https://developer.android.com/studio/debug/dev-options.html) so I used the Muki app to upload an image to the mug and then moved the log to my laptop via Google Drive.

I had a look at the log with Wireshark: about a thousand frames but scrolling through revealed only one remote MAC address. This is the beginning of the log when filtering with just this MAC as destination:

![Wireshark log](images/bt-log.png)

