from ..api import machine

if machine.get_machine_type() == "laptop":
    controlZone = [
        {'name': 'Instrument', 'x': 198, 'y': 34},
        {'name': 'Polyphony', 'x': 628, 'y': 60},
        {'name': 'Pitchband', 'x': 732, 'y': 60},
        {'name': 'SnapShot', 'x': 807, 'y': 106},
    ]
elif machine.get_machine_type() == "desktop":
    controlZone = [
        {'name': 'Instrument', 'x': 198, 'y': 34},
        {'name': 'Polyphony', 'x': 506, 'y': 48},
        {'name': 'Pitchband', 'x': 586, 'y': 48},
        {'name': 'SnapShot', 'x': 643, 'y': 82},
    ]
