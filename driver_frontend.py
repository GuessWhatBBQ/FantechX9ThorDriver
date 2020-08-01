import driver_backend
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

driver_api = driver_backend.Driver_API


class driver_frontend(Gtk.Window, driver_api):
    def __init__(self):
        super(driver_frontend, self).__init__()
        super(driver_api, self).__init__()
        self.set_title("FantechX9Thor")
        self.set_default_size(500, 600)
        self.startup()

        ########################################################################
        # Default Configs
        self.profile_dpi_configs = [200, 600, 1000, 1600, 2400, 4000]
        self.profile_states = [1, 1, 1, 1, 1, 1]
        self.profile_color_configs = ["rgb(255,255,0)", "rgb(0,0,255)", "rgb(255,0,255)", "rgb(0,255,0)", "rgb(255,0,0)", "rgb(0,255,255)"]
        self.current_active_profile = 3
        self.rgb_color_change_scheme = "Cyclic"
        self.current_scheme_timer = 1
        self.cyclic_colors = {"White": 1, "Cyan": 1, "Red": 1, "Lightgreen": 1, "Pink": 1, "Blue": 1, "Yellow": 1}
        self.config_file_avail = False
        ########################################################################

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        self.profiles = [Gtk.VBox(spacing=6) for i in range(6)]

        self.profile_color_container = [Gdk.RGBA() for i in range(6)]
        self.set_default_colors(self.config_file_avail)
        self.colors = [Gtk.ColorButton() for i in range(6)]
        for i in range(6):
            self.colors[i].connect("color-set", self.on_color_changed, i)
            self.colors[i].set_rgba(self.profile_color_container[i])

        self.dpis = [Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, 200, 4800, 200) for i in range(6)]
        for i in range(6):
            self.dpis[i].set_inverted(True)
            self.dpis[i].set_value(self.profile_dpi_configs[i])
            self.dpis[i].connect("value-changed", self.on_dpi_changed, i)
            for j in self.supported_dpis:
                self.dpis[i].add_mark(j, Gtk.PositionType.LEFT)

        self.active_profiles = [Gtk.RadioButton() for i in range(6)]
        for i in range(6):
            self.active_profiles[i].join_group(self.active_profiles[0])
            self.active_profiles[i].set_halign(Gtk.Align.CENTER)
            self.active_profiles[i].connect("toggled", self.on_active_profile_toggled, i)
        self.active_profiles[self.current_active_profile - 1].set_active(True)

        self.profile_name = [Gtk.Label() for i in range(6)]
        for i in range(6):
            label = "Profile " + str(i + 1)
            self.profile_name[i].set_label(label)

        self.profile_state = [Gtk.CheckButton() for i in range(6)]
        for i in range(6):
            self.profile_state[i].set_active(True if self.profile_states[i] == 1 else False)
            self.profile_state[i].connect("toggled", self.on_state_toggled, i)
            self.profile_state[i].set_halign(Gtk.Align.CENTER)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox.pack_start(self.hbox, True, True, 0)

        for i in range(6):
            self.hbox.pack_start(self.profiles[i], True, True, 0)
            self.profiles[i].pack_start(self.dpis[i], True, True, 10)
            self.profiles[i].pack_start(self.profile_state[i], False, True, 0)
            self.profiles[i].pack_start(self.profile_name[i], False, True, 0)
            self.profiles[i].pack_start(self.active_profiles[i], False, True, 0)
            self.profiles[i].pack_start(self.colors[i], False, False, 0)

        self.schemes = ["Fixed", "Cyclic", "Static", "Off"]
        self.color_schemes = Gtk.ListStore(str)
        for scheme in self.schemes:
            self.color_schemes.append([scheme])

        self.scheme_timers = [1, 2, 3, 4, 5, 6]
        self.color_scheme_timers = Gtk.ListStore(int)
        for timer in self.scheme_timers:
            self.color_scheme_timers.append([timer])

        self.hbox_color_scheme = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox.pack_start(self.hbox_color_scheme, False, False, 20)

        self.scheme_combo_label = Gtk.Label()
        self.scheme_combo_label.set_label("Color Scheme:")
        self.hbox_color_scheme.pack_start(self.scheme_combo_label, False, False, 0)
        self.scheme_combo = Gtk.ComboBox()
        self.scheme_combo.set_model(self.color_schemes)
        self.scheme_combo.set_active(self.schemes.index(self.rgb_color_change_scheme))
        self.scheme_combo.connect("changed", self.on_scheme_changed)
        self.hbox_color_scheme.pack_start(self.scheme_combo, True, True, 0)
        self.renderer_text = Gtk.CellRendererText()
        self.scheme_combo.pack_start(self.renderer_text, True)
        self.scheme_combo.add_attribute(self.renderer_text, "text", 0)

        self.scheme_timer_label = Gtk.Label()
        self.scheme_timer_label.set_label("Scheme Timer:")
        self.hbox_color_scheme.pack_start(self.scheme_timer_label, False, False, 0)
        self.scheme_timer_combo = Gtk.ComboBox()
        self.scheme_timer_combo.set_model(self.color_scheme_timers)
        self.scheme_timer_combo.connect("changed", self.on_current_scheme_timer_changed)
        self.scheme_timer_combo.set_active(self.scheme_timers.index(self.current_scheme_timer))
        self.hbox_color_scheme.pack_start(self.scheme_timer_combo, True, True, 0)
        self.renderer_text = Gtk.CellRendererText()
        self.scheme_timer_combo.pack_start(self.renderer_text, True)
        self.scheme_timer_combo.add_attribute(self.renderer_text, "text", 0)

        self.cyclic_colors_label = Gtk.Label()
        self.cyclic_colors_label.set_label("Colors active during cyclic color change:")
        self.cyclic_colors_label.set_halign(Gtk.Align.START)
        self.vbox.pack_start(self.cyclic_colors_label, False, True, 0)

        self.hbox_cyclic_color_state = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.vbox.pack_start(self.hbox_cyclic_color_state, False, True, 0)
        self.cyclic_colors_state = [Gtk.CheckButton() for i in range(len(self.cyclic_colors))]
        prof = 0
        for colorname in self.cyclic_colors.keys():
            self.cyclic_colors_state[prof].set_label(colorname)
            self.cyclic_colors_state[prof].set_active(True if self.cyclic_colors[colorname] == 1 else False)
            self.cyclic_colors_state[prof].connect("toggled", self.on_cyclic_color_changed)
            self.hbox_cyclic_color_state.pack_start(self.cyclic_colors_state[prof], True, True, 0)
            prof += 1

        self.action_bar = Gtk.ActionBar()
        self.vbox.pack_end(self.action_bar, False, False, 0)
        self.apply_button = Gtk.Button()
        self.apply_button.set_label("Apply")
        self.apply_button.connect("clicked", self.on_apply_button_clicked)
        self.action_bar.pack_end(self.apply_button)
        self.reconfigure_button = Gtk.Button()
        self.reconfigure_button.set_label("Reconfigure Device")
        self.action_bar.pack_start(self.reconfigure_button)
        self.reconfigure_button.connect("clicked", self.reconfigure_button_clicked)

    def on_scheme_changed(self, combo):
        tree_iter = combo.get_active_iter()
        model = combo.get_model()
        self.rgb_color_change_scheme = model[tree_iter][0]

        time_not_req = ["Static", "Off"]

        if self.rgb_color_change_scheme in time_not_req:
            self.scheme_timer_combo.set_model()
        else:
            self.scheme_timer_combo.set_model(self.color_scheme_timers)
            self.scheme_timer_combo.set_active(self.scheme_timers.index(self.current_scheme_timer))

    def reconfigure_button_clicked(self, button):
        print(self.profile_color_configs)
        self.startup()

    def startup(self):
        self.find_device()
        state = self.device_state()
        alert = Gtk.MessageDialog()
        alert.add_button("Close", Gtk.ResponseType.CLOSE)
        alert.props.use_markup = True
        if state == -1:
            alert.set_markup('''Insufficient Permissions! Try adding a udev rule for your mouse, follow the guide <a href="https://wiki.archlinux.org/index.php/udev#Accessing_firmware_programmers_and_USB_virtual_comm_devicesrunning" title="Arch Wiki Guide">here</a>. Running as root will probably work too but not recommended''')
            alert.run()
            alert.destroy()
        elif state == -2:
            alert.set_markup("Device not found! Try Replugging.")
            alert.run()
            alert.destroy()

    def on_state_toggled(self, button, profile):
        state = button.get_active()
        if state:
            self.profile_states[profile] = 1
        else:
            self.profile_states[profile] = 0

    def on_active_profile_toggled(self, button, profile):
        if button.get_active():
            self.current_active_profile = profile + 1

    def on_current_scheme_timer_changed(self, radio):
        timer = radio.get_active()
        self.current_scheme_timer = timer + 1

    def on_apply_button_clicked(self, button):
        self.conquer()

        profile = 1
        for dpi in self.profile_dpi_configs:
            config = self.create_dpi_profile_config(dpi, profile)
            self.send_payload(config)
            profile += 1
        profile = 1
        for color in self.profile_color_container:
            red = int(color.red * 255)
            green = int(color.green * 255)
            blue = int(color.blue * 255)
            config = self.create_color_profile_config(profile, red, green, blue)
            self.send_payload(config)
            profile += 1
        config = self.create_rgb_lights_config(self.rgb_color_change_scheme, self.current_scheme_timer)
        self.send_payload(config)

        self.liberate()

    def on_dpi_changed(self, scale, profile):
        value = int(scale.get_value())
        value = self.find_closest_dpi(value)
        scale.set_value(value)
        self.profile_dpi_configs[profile] = value

    def on_color_changed(self, color, profile):
        self.profile_color_container[profile] = color.get_rgba()
        self.profile_color_configs[profile] = color.get_rgba().to_string()

    def on_cyclic_color_changed(self, button):
        label = button.get_label()
        state = button.get_active()
        if state:
            self.cyclic_colors[label] = 1
        else:
            self.cyclic_colors[label] = 0

    def set_default_colors(self, config_state):
        if not config_state:
            for i in range(6):
                self.profile_color_container[i].parse(self.profile_color_configs[i])


ui = driver_frontend()
ui.show_all()
ui.connect("destroy", Gtk.main_quit)
Gtk.main()
