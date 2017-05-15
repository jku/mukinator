# Hacking Paulig Muki for fun ~~and profit~~

I got my hands on a IOT-enabled coffee mug, Muki from Paulig. There's an e-ink display on the side and you can use your phone to upload images to the mug. The cool (or rather hot) thing is that this is all powered by the heat of the coffee: there's no battery or power plug.

![Muki](images/muki.png)

I did what one does with new IOT devices: had a look at how it works and tried to reproduce it without the app.

## The Good

Sending images to the mug is pretty easy. Bluez (the bluetooth stack) and ImageMagick (the image manipulation toolkit) do all the heavy lifting I needed on linux.

## The Bad

Anyone within Bluetooth LE distance can send images to my coffee mug :/

## Figuring it out

Muki documentation mentions it uses Bluetooth Low-Energy and I knew Android allows Bluetooth sniffing see [Hpw to enable Bluetooth HCI snoop log](https://developer.android.com/studio/debug/dev-options.html) so I used the Muki app to upload an image to the mug and then moved the log to my laptop via Google Drive.

I had a look at the log with Wireshark: It contained about a thousand frames but scrolling through revealed only one remote MAC address. This is the beginning of the log when filtering with just this MAC as destination:

![Wireshark log](images/bt-log.png)

All of the events are Bluetooth attribute writes to one single handle. First and last write have a payload of a single byte (0x74 and 0x64 respectively). All the other 291 writes are 20 bytes each. Here's an example of a 20 byte payload frame:

![Attribute write](images/bt-frame.png)

At this point I did a bit of math: According to manufacturers Facebook page the screen is 176x264 pixels. At bitdepth 1 that's 46464 bits or 5808 bytes. If you divide 5808 bytes into 20 byte frames you end up with _291_ frames, exactly as many as are sent over Bluetooth. That's unlikely to be a coincidence...

I decided to throw something on the wall and see if it sticks: Googling lead me to gatttool (and hcitool) from Bluez project as the quick-and-dirty options on Linux. After a bit of reading it seemed clear that I only needed the Bluetooth address and a "ATT characteristic handle" to write with gatttool and I already had both from wireshark.

I tried entering the write commands manually with gatttool but that didn't work: I probably type too slowly and the device disconnects to save power. Next I wrote a script that uses the start and stop values from the sniffed log and otherwise just writes a lot of 0xF0 values:

	import pexpect

	console = pexpect.spawn('gatttool -I -t random -b C4:4E:CC:58:F2:08', timeout=3)
	console.sendline('connect')

		console.sendline('char-write-req 0x000d 74')
	for i in range(0,291):
		console.sendline('char-write-cmd 0x000d F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0')
	console.sendline('char-write-req 0x000d 64')

After a few failed attempts and bug fixes the screen flashed and updated to a striped image!

![Stripes!](images/stripes.jpg)

So the 291 frames are indeed for image data and the data seems to be simply binary pixel values one after the other: The data I was writing was 11110000 in binary and the stripes indeed seemed four pixels high.

> Note: At around this time I happened to find some kind of [Android and iOS library](https://github.com/gustavpaulig/Paulig-Muki/) for Muki on Github: it's not an actual source release (even though it claims to be GPL!) but the Android files are easily decompilable. I took a long enough look at the decompiled sources to verify my findings so far but decided not to use the code for anything -- the uploader claims to be Paulig (the manufacturer) but the whole thing seems a little fishy...

# Sending my own pictures with Bluez and Imagemagick

_Working on this..._
