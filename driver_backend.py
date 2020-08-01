import usb.core
import usb.util


class Driver(object):
    def __init__(self):
        self.x9_vendorid = 0x18f8  # vendorid
        self.x9_productid = 0x1086  # productid
        self.bmRequestType = 0x21  # bmRequestType
        self.bRequest = 0x09  # bRequest
        self.wValue = 0x0307  # wValue
        self.wIndex = 0x0001  # wIndex

        self.conquered = False
        self.device_busy = bool()

        self.profile_states = [1, 1, 1, 1, 1, 1]
        self.current_active_profile = 1
        self.cyclic_colors = {"White": 1, "Cyan": 1, "Red": 1, "Lightgreen": 1, "Pink": 1, "Blue": 1, "Yellow": 1}

        self.supported_dpis = [200, 400, 600, 800, 1000, 1200, 1600, 2000, 2400, 3200, 4000, 4800]

    def initPayload(self, instruction_code):
        payload = [0x07]
        payload.append(instruction_code)
        return payload

    def find_device(self):
        print("Trying to find device...")
        self.mouse = usb.core.find(idVendor=self.x9_vendorid, idProduct=self.x9_productid)

    def device_state(self):
        try:
            self.device_busy = self.mouse.is_kernel_driver_active(self.wIndex)
        except usb.core.USBError as exception:
            print(exception.strerror)
            if exception.errno == 13:
                # usb.backend.libusb1.LIBUSB_ERROR_ACCESS as e
                print("Try adding a udev rule for your mouse, follow the guide here https://wiki.archlinux.org/index.php/udev#Accessing_firmware_programmers_and_USB_virtual_comm_devicesrunning. Running as root will probably work too but not recommended")
            return -1
        except AttributeError:
            print("Device not found. Try replugging")
            return -2
        print("Device is ready to be configured")
        return 1

    def conquer(self):
        if self.device_busy and not self.conquered:
            self.mouse.detach_kernel_driver(self.wIndex)
            usb.util.claim_interface(self.mouse, self.wIndex)
            self.conquered = True

    def liberate(self):
        self.conquered
        if self.conquered:
            try:
                usb.util.release_interface(self.mouse, self.wIndex)
                self.mouse.attach_kernel_driver(self.wIndex)
                self.conquered = False
            except:
                print("Failed to release device back to kernel")

    def addzerobytes(self, list, number_of_bytes):
        for i in range(number_of_bytes):
            list.append(0x00)

    def create_rgb_lights_config(self, changing_scheme, time_duration):
        payload = self.initPayload(0x13)
        payload.append(self.set_cyclic_colors())

        if changing_scheme == "Fixed":
            payload.append(0x86 - time_duration)
        elif changing_scheme == "Cyclic":
            payload.append(0x96 - time_duration)
        elif changing_scheme == "Static":
            payload.append(0x86)
        elif changing_scheme == "Off":
            payload.append(0x87)

        self.addzerobytes(payload, 4)
        return payload

    def create_scrollwheel_config(self, state):
        payload = self.initPayload(0x11)
        if state == "Volume":
            payload.append(0x01)
        else:
            payload.append(0x00)
        self.addzerobytes(payload, 5)
        return(payload)

    def create_dpi_profile_config(self, DPI, profile_to_modify):
        payload = self.initPayload(0x09)
        payload.append(0x40 - 1 + self.current_active_profile)
        payload.append(self.set_dpi_this_profile(DPI, profile_to_modify))
        payload.append(self.set_active_profiles())

        self.addzerobytes(payload, 3)

        return payload

    def create_color_profile_config(self, profile, red, green, blue):
        payload = self.initPayload(0x14)
        internal_profile = (profile - 1) * 2
        internal_red = int((255 - red) / 16)
        internal_green = int((255 - green) / 16)
        internal_blue = int((255 - blue) / 16)

        byte = internal_profile * 16 + internal_green
        payload.append(byte)
        byte = internal_red * 16 + internal_blue
        payload.append(byte)

        payload.append(self.set_active_profiles())

        self.addzerobytes(payload, 3)

        return payload

    def set_active_profiles(self):
        byte = 0
        for i in range(6):
            byte += self.profile_states[i] * 2**i

        return byte

    def set_dpi_this_profile(self, DPI, profile_to_modify):
        '''DPI is set to the value that is closest to one of the mouse's supported values'''
        internal_dpi = 0
        best_match_dpi = self.find_closest_dpi(DPI)
        if best_match_dpi >= 200 and best_match_dpi <= 1200:
            internal_dpi = int(best_match_dpi / 200)
        elif best_match_dpi == 1600:
            internal_dpi = 0x7
        elif best_match_dpi == 2000:
            internal_dpi = 0x9
        elif best_match_dpi == 2400:
            internal_dpi = 0xb
        elif best_match_dpi == 3200:
            internal_dpi = 0xd
        elif best_match_dpi == 4000:
            internal_dpi = 0xe
        elif best_match_dpi == 4800:
            internal_dpi = 0xf
        else:
            print("DPI out of supported range (200-4800).")

        internal_profile = profile_to_modify + 7
        byte = (internal_dpi * 16) + internal_profile

        return byte

    def set_cyclic_colors(self):
        colors = self.cyclic_colors["White"] * (2**6)
        colors += self.cyclic_colors["Cyan"] * (2**5)
        colors += self.cyclic_colors["Red"] * (2**4)
        colors += self.cyclic_colors["Lightgreen"] * (2**3)
        colors += self.cyclic_colors["Pink"] * (2**2)
        colors += self.cyclic_colors["Blue"] * (2**1)
        colors += self.cyclic_colors["Yellow"] * (2**0)

        return colors

    def send_payload(self, payload):
        self.mouse.ctrl_transfer(self.bmRequestType, self.bRequest, self.wValue, self.wIndex, payload)
        # print([hex(i) for i in payload])

    def find_closest_dpi(self, DPI):
        if DPI in self.supported_dpis:
            return DPI

        difference = 4800
        best_match = int()
        for supported in self.supported_dpis:
            temp_diff = DPI - supported
            # print(temp_diff if temp_diff > 0 else temp_diff * -1)
            if (difference >= (temp_diff if temp_diff > 0 else temp_diff * -1)):
                best_match = supported
                difference = temp_diff
        return best_match


class Driver_API(Driver):
    '''The sole purpose of this class is to give the frontend access to the Driver
    class. Unless present the super().__init__ call defaults to the Gtk.Wondow
    class according to the MRO'''
    def __init__():
        super().__init__()


# driver = Driver()
# for i in range(200, 4801, 200):
#     print(i, driver.find_closest_dpi(i))
# driver.find_device()
# driver.device_state()
# payload = driver.create_color_profile_config(3, 255, 255, 255)
# print(payload)
# driver.send_payload(payload)
#
# payload = driver.create_rgb_lights_config("Cyclic", 1)
# print(payload)
# driver.send_payload(payload)
#
# # driver.set_active_profiles(1, 1, 1, 1, 1, 1)
# driver.send_payload(driver.create_dpi_profile_config(6, 600, 6))
