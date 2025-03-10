import nfc

def write_to_mifare(tag):
    # Authenticate with key A (or B, if needed) for block 0x2A
    key = bytes([0xFF]*6)  # Default key (FFFFFFFFFFFF)

    # Block address you want to write to
    block_address = 0x2A
    
    # Data to write (must be 16 bytes long)
    data = b"BALANCE:1500$80c"  # Ensure it's 16 bytes long

    # Authenticate and write the data
    if tag.authenticate(block_address, key):
        tag.write(block_address, data)
        print("Data written successfully to block 0x2A!")
    else:
        print("Failed to authenticate.")

# Connect to NFC reader
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': write_to_mifare})