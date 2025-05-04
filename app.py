from pydbus import SystemBus, SessionBus

# Connect to the IBus D-Bus session bus
bus = SystemBus()

# Get the IBus service
ibus = bus.get("org.freedesktop.IBus", "/org/freedesktop/IBus")

# Get the current input method engine
current_engine = ibus.GetEngine()
print(f"Current input engine: {current_engine}")

# List all available input engines
engines = ibus.ListEngines()
print("Available input engines:")
for engine in engines:
    print(engine)
