import bluetooth
nearby_devices = bluetooth.discover_devices(duration=4, lookup_names=True, flush_cache=True, lookup_class=False)