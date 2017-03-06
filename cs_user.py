#!/usr/bin/python2

from GSettingsWidgets import *
import re, random
import gi
gi.require_version('AccountsService', '1.0')
from gi.repository import AccountsService, GLib, Gdk
try:
    import PAM
except:
    import pam as PAM
import pexpect
import time
from random import randint
import shutil
import PIL
import os
import subprocess

class Module:
    name = "user"
    category = "prefs"
    comment = _("Change your user preferences and password")

    def __init__(self, content_box):
        keywords = _("user, account, information, details")
        sidePage = SidePage(_("Account details"), "cs-user", keywords, content_box, module=self)
        self.sidePage = sidePage

    def on_module_selected(self):
        if not self.loaded:
            print "Loading User module"

            page = SettingsPage()
            self.sidePage.add_widget(page)

            settings = page.add_section(_("Account details"))

            self.face_button = PictureChooserButton(num_cols=4, button_picture_size=64, menu_pictures_size=64)
            self.face_button.set_alignment(0.0, 0.5)
            self.face_button.set_tooltip_text(_("Click to change your picture"))

            self.face_photo_menuitem = Gtk.MenuItem.new_with_label(_("Take a photo..."))
            self.face_photo_menuitem.connect('activate', self._on_face_photo_menuitem_activated)

            self.face_browse_menuitem = Gtk.MenuItem.new_with_label(_("Browse for more pictures..."))
            self.face_browse_menuitem.connect('activate', self._on_face_browse_menuitem_activated)

            face_dirs = ["/usr/share/cinnamon/faces"]
            for face_dir in face_dirs:
                if os.path.exists(face_dir):
                    pictures = sorted(os.listdir(face_dir))
                    for picture in pictures:
                        path = os.path.join(face_dir, picture)
                        self.face_button.add_picture(path, self._on_face_menuitem_activated)

            widget = SettingsWidget()
            label = Gtk.Label.new(_("Picture"))
            widget.pack_start(label, False, False, 0)
            widget.pack_end(self.face_button, False, False, 0)
            settings.add_row(widget)

            size_group = Gtk.SizeGroup.new(Gtk.SizeGroupMode.HORIZONTAL)

            widget = SettingsWidget()
            label = Gtk.Label.new(_("Name"))
            widget.pack_start(label, False, False, 0)
            self.realname_entry = EditableEntry()
            size_group.add_widget(self.realname_entry)
            self.realname_entry.connect("changed", self._on_realname_changed)
            self.realname_entry.set_tooltip_text(_("Click to change your name"))
            widget.pack_end(self.realname_entry, False, False, 0)
            settings.add_row(widget)

            widget = SettingsWidget()
            label = Gtk.Label.new(_("Password"))
            widget.pack_start(label, False, False, 0)
            password_mask = Gtk.Label.new(u'\u2022\u2022\u2022\u2022\u2022\u2022')
            password_mask.set_alignment(0.9, 0.5)
            self.password_button = Gtk.Button()
            size_group.add_widget(self.password_button)
            self.password_button.add(password_mask)
            self.password_button.set_relief(Gtk.ReliefStyle.NONE)
            self.password_button.set_tooltip_text(_("Click to change your password"))
            self.password_button.connect('activate', self._on_password_button_clicked)
            self.password_button.connect('released', self._on_password_button_clicked)
            widget.pack_end(self.password_button, False, False, 0)
            settings.add_row(widget)

            current_user = GLib.get_user_name()
            self.accountService = AccountsService.UserManager.get_default().get_user(current_user)
            self.accountService.connect('notify::is-loaded', self.load_user_info)

            self.face_button.add_separator()

            # Video devices assumed to be webcams
            import glob
            webcam_detected = len(glob.glob("/dev/video*")) > 0

            if webcam_detected:
                self.face_button.add_menuitem(self.face_photo_menuitem)

            self.face_button.add_menuitem(self.face_browse_menuitem)

    def update_preview_cb (self, dialog, preview):
        filename = dialog.get_preview_filename()
        dialog.set_preview_widget_active(False)
        if filename is not None and os.path.isfile(filename):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filename, 128, 128)
                if pixbuf is not None:
                    preview.set_from_pixbuf (pixbuf)
                    dialog.set_preview_widget_active(True)
            except:
                pass

    def _on_face_photo_menuitem_activated(self, menuitem):

        # streamer takes -t photos, uses /dev/video0
        if 0 != subprocess.call(["streamer", "-j90", "-t8", "-s800x600", "-o", "/tmp/temp-account-pic00.jpeg"]):
            print "Error: Webcam not available"
            return

        # Use the 8th frame (the webcam takes a few frames to "lighten up")
        path = "/tmp/temp-account-pic07.jpeg"

        # Crop the image to thumbnail size
        image = PIL.Image.open(path)
        width, height = image.size

        if width > height:
            new_width = height
            new_height = height
        elif height > width:
            new_width = width
            new_height = width
        else:
            new_width = width
            new_height = height

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        image = image.crop((left, top, right, bottom))
        image.thumbnail((96, 96), PIL.Image.ANTIALIAS)

        face_path = os.path.join(self.accountService.get_home_dir(), ".face")

        image.save(face_path, "png")
        self.accountService.set_icon_file(face_path)
        self.face_button.set_picture_from_file(face_path)


    def _on_face_browse_menuitem_activated(self, menuitem):
        dialog = Gtk.FileChooserDialog(None, None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(self.accountService.get_home_dir())
        filter = Gtk.FileFilter()
        filter.set_name(_("Images"))
        filter.add_mime_type("image/*")
        dialog.add_filter(filter)

        preview = Gtk.Image()
        dialog.set_preview_widget(preview);
        dialog.connect("update-preview", self.update_preview_cb, preview)
        dialog.set_use_preview_label(False)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            image = PIL.Image.open(path)
            width, height = image.size
            if width > height:
                new_width = height
                new_height = height
            elif height > width:
                new_width = width
                new_height = width
            else:
                new_width = width
                new_height = height
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            image = image.crop((left, top, right, bottom))
            image.thumbnail((96, 96), PIL.Image.ANTIALIAS)
            face_path = os.path.join(self.accountService.get_home_dir(), ".face")
            image.save(face_path, "png")
            self.accountService.set_icon_file(face_path)
            self.face_button.set_picture_from_file(face_path)

        dialog.destroy()

    def _on_face_menuitem_activated(self, path):
        if os.path.exists(path):
            self.accountService.set_icon_file(path)
            shutil.copy(path, os.path.join(self.accountService.get_home_dir(), ".face"))
            return True

    def load_user_info(self, user, param):
        self.realname_entry.set_text(user.get_real_name())
        for path in [os.path.join(self.accountService.get_home_dir(), ".face"), user.get_icon_file(), "/usr/share/cinnamon/faces/user-generic.png"]:
            if os.path.exists(path):
                self.face_button.set_picture_from_file(path)
                break

    def _on_realname_changed(self, widget, text):
        self.accountService.set_real_name(text)

    def _on_password_button_clicked(self, widget):
        dialog = PasswordDialog()
        response = dialog.run()


class PasswordDialog(Gtk.Dialog):

    def __init__ (self):
        super(PasswordDialog, self).__init__()

        self.correct_current_password = False # Flag to remember if the current password is correct or not

        self.set_modal(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_title(_("Change Password"))
        
        self.LOCK_NONE = 0
        self.LOCK_CAPS = 1
        self.mode = self.LOCK_NONE
        self.keymap = Gdk.Keymap.get_for_display(self.get_display())
        self.keymap.connect("state-changed",self._on_keymap_state_changed)

        table = Gtk.Table(8, 4)
        table.set_border_width(6)
        table.set_row_spacings(8)
        table.set_col_spacings(15)

        self.current_label = Gtk.Label.new_with_mnemonic(_("C_urrent password"))
        self.current_label.set_alignment(1, 0.5)
        table.attach(self.current_label, 0, 1, 0, 1)

        label = Gtk.Label.new(_("_New password"))
        label.set_alignment(1, 0.5)
        table.attach(label, 0, 1, 1, 2)

        self.confirm_label = Gtk.Label.new_with_mnemonic(_("Confirm passw_ord"))
        self.confirm_label.set_alignment(1, 0.5)
        table.attach(self.confirm_label, 0, 1, 3, 4)

        self.current_password = Gtk.Entry()
        self.current_password.set_property("caps-lock-warning", False)
        self.current_label.set_mnemonic_widget(self.current_password)
        self.current_password.set_visibility(False)
        self.current_password.connect("focus-out-event", self._on_current_password_changed)
        self.current_password.connect("changed", self._on_current_password_focus)
        table.attach(self.current_password, 1, 3, 0, 1)

        self.gag = Gtk.AccelGroup.new()
        self.add_accel_group(self.gag)

        self.new_password = Gtk.Entry()
        self.new_password.set_property("caps-lock-warning", False)
        self.new_password.add_accelerator("activate",self.gag,Gdk.KEY_n,
                Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)

        self.new_password.set_tooltip_text(_("new password format:\n1.The new "\
                                             "password should not contains Chinese\n2.The length is "\
                                             "8 - 20;\n3.The new password should contains Lowercase "\
                                             "letters;\n4.The new password should contains Capital"\
                                             "\n5.The new password should contains number"))
        self.new_password.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "reload")
        self.new_password.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Generate a password"))
        self.new_password.connect("icon-release", self._on_new_password_icon_released)
        self.new_password.connect("changed", self._on_passwords_changed)
        self.new_password.connect("activate", self._on_new_password_focus_in)
        table.attach(self.new_password, 1, 3, 1, 2)

        self.strengh_indicator = Gtk.ProgressBar()
        self.strengh_indicator.set_tooltip_text(_("Password strength"))
        self.strengh_indicator.set_fraction(0.0)
        table.attach(self.strengh_indicator, 1, 2, 2, 3, xoptions=Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL)
        self.strengh_indicator.set_size_request(-1, 1)

        self.strengh_label = Gtk.Label()
        self.strengh_label.set_justify(Gtk.Justification.LEFT)
        #self.strengh_label.set_tooltip_text(_("Your new password needs to be at least 8 characters long"))
        self.strengh_label.set_alignment(1, 0.5)
        table.attach(self.strengh_label, 0, 3, 6, 7)

        self.confirm_password = Gtk.Entry()
        self.confirm_password.set_property("caps-lock-warning", False)
        self.confirm_label.set_mnemonic_widget(self.confirm_password)
        self.confirm_password.connect("changed", self._on_passwords_changed)
        table.attach(self.confirm_password, 1, 3, 3, 4)

        self.show_password = Gtk.CheckButton.new_with_mnemonic(_("_Show password"))
        self.show_password.connect('toggled', self._on_show_password_toggled)
        table.attach(self.show_password, 1, 3, 4, 5)

        self.capslock_label = Gtk.Label()
        self.capslock_label.set_justify(Gtk.Justification.LEFT)
        self.capslock_label.set_alignment(1, 0.5)
        table.attach(self.capslock_label, 0, 3, 5, 6)

        self.set_border_width(6)

        box = self.get_content_area()
        box.add(table)
        self.show_all()

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.ERROR)
        label = Gtk.Label.new(_("An error occurred. Your password was not changed."))
        content = self.infobar.get_content_area()
        content.add(label)
        table.attach(self.infobar, 0, 1, 7, 8)

        self.infotext = Gtk.Label()
        table.attach(self.infotext, 1, 3, 7, 8)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, _("Chan_ge"), Gtk.ResponseType.OK, )

        self.set_passwords_visibility()
        self.set_response_sensitive(Gtk.ResponseType.OK, False)
        self.infobar.hide()
        self.infotext.hide()
        
        self.username = GLib.get_user_name()
        self.user = AccountsService.UserManager.get_default().get_user(self.username)
        self.realname = self.user.get_real_name()

        self.connect("response", self._on_response)

    def _on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            self.change_password()
        else:
            self.destroy()

    def get_kbd_lock_mode(self):
        self.mode = self.LOCK_NONE
        res = self.keymap.get_caps_lock_state()
        if (res):
            self.mode |= self.LOCK_CAPS

    def kbd_lock_mode_update(self, mode):
        if((mode & self.LOCK_CAPS) != 0):
            self.capslock_label.set_text(_("You have the Caps Lock key on."))
        else:
            self.capslock_label.set_text("")

    def _on_keymap_state_changed(self, widget):
        self.get_kbd_lock_mode()
        self.kbd_lock_mode_update(self.mode)

    def _on_new_password_focus_in(self, widget):
        self.new_password.grab_focus()

    def _on_current_password_focus(self, widget):
        self.infobar.hide()
        self.infotext.hide()
        self.current_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, None)

    def change_password(self):
        oldpass = self.current_password.get_text()
        newpass = self.new_password.get_text()
        passwd = pexpect.spawn("/usr/bin/passwd")
        time.sleep(0.5)
        passwd.sendline(oldpass)
        time.sleep(0.5)
        passwd.sendline(newpass)
        time.sleep(0.5)
        passwd.sendline(newpass)
        time.sleep(0.5)
        passwd.close()

        if passwd.exitstatus is None or passwd.exitstatus > 0:
            self.infobar.show()
            self.infotext.show()
            if self.correct_current_password == False:
                self.infobar.set_tooltip_text(_("The input current password is wrong"))
                self.infotext.set_text(_("The input current password is wrong"))
            elif (oldpass == newpass):
                self.infobar.set_tooltip_text(_("The new password is the same as old."))
                self.infotext.set_text(_("The new password is the same as old."))
        else:
            self.destroy()

    def set_passwords_visibility(self):
        visible = self.show_password.get_active()
        self.new_password.set_visibility(visible)
        self.confirm_password.set_visibility(visible)

    def _on_new_password_icon_released(self, widget, icon_pos, event):
        self.infobar.hide()
        self.infotext.hide()
        self.show_password.set_active(True)

        lowercases = "abcdefghijklmnopqrstuvwxyz"
        uppercases = "ABCDEFGHIGKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        specialChracters = "!@#$%^&*()_-+=~`/ "

        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-+=~`/ "
        newpass = ""
        index_lowcase = randint(0, len(lowercases) -1)
        index_uppercase = randint(0, len(uppercases) -1)
        index_number = randint(0, len(numbers) -1)
        index_special = randint(0, len(specialChracters) -1)

        j = random.randint(8, 20)
        n_list = range(1, j)
        nlist_webld = random.sample(n_list, 4)

        for i in range (j):
            if i == nlist_webld[0]:
                newpass = newpass + lowercases[index_lowcase]
            elif i == nlist_webld[1]:
                newpass = newpass + uppercases[index_uppercase]
            elif i == nlist_webld[2]:
                newpass = newpass + numbers[index_number]
            elif i == nlist_webld[3]:
                newpass = newpass + specialChracters[index_special]
            else:
                index = randint(0, len(characters) -1)
                newpass = newpass + characters[index]

        self.new_password.set_text(newpass)
        self.confirm_password.set_text(newpass)
        self.check_passwords()

    def _on_show_password_toggled(self, widget):
        self.set_passwords_visibility()

    def _on_current_password_changed(self, widget, event):
        self.infobar.hide()
        self.infotext.hide()
        if self.current_password.get_text() != "":
            auth = PAM.pam()
            auth.start('passwd')
            auth.set_item(PAM.PAM_USER, GLib.get_user_name())
            auth.set_item(PAM.PAM_CONV, self.pam_conv)
            try:
                auth.authenticate()
                auth.acct_mgmt()
            except PAM.error, resp:
                self.current_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_DIALOG_WARNING)
                self.current_password.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Wrong password"))
                self.correct_current_password = False
            except:
                print 'Internal error'
            else:
                self.current_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, None)
                self.correct_current_password = True
                #self.check_passwords()
        else:
            self.current_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_DIALOG_WARNING)
            self.current_password.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Wrong password"))
            self.correct_current_password = False

    # Based on setPasswordStrength() in Mozilla Seamonkey, which is tri-licensed under MPL 1.1, GPL 2.0, and LGPL 2.1.
    # Forked from Ubiquity validation.py
    def password_len(self, password):
        return 8 <= len(password) <= 20

    def password_check_contain_upper(self, password):
        pattern = re.compile('[A-Z]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

    def password_check_contain_num(self,password):
        pattern = re.compile('[0-9]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False
    def password_check_contain_zh_cn(self,password):
        for ch in password.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        else:
            return False

    def password_check_contain_lower(self, password):
        pattern = re.compile('[a-z]+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

    def password_check_symbol(self, password):
        pattern = re.compile('([^a-z0-9A-Z])+')
        match = pattern.findall(password)
        if match:
            return True
        else:
            return False

#    def password_check_space(self, password):
#        for i in password:
#            if i.isspace():
#                return True
#            else:
#                continue
#        return False

    def password_check_username(self, password):
        if(self.username == password):
            return True
        else:
            return False
    def password_check_realname(self,password):
        if(self.realname == password):
            return True
        else:
            return False

    def password_strength(self, password):
        upper = lower = digit = symbol = 0
        for char in password:
            if char.isdigit():
                digit += 1
            elif char.islower():
                lower += 1
            elif char.isupper():
                upper += 1
            else:
                symbol += 1
        length = len(password)

        length = min(length,4)
        digit = min(digit,3)
        upper = min(upper,3)
        symbol = min(symbol,3)
        strength = (
            ((length * 0.1) - 0.2) +
            (digit * 0.1) +
            (symbol * 0.15) +
            (upper * 0.1))
        if strength > 1:
            strength = 1
        if strength < 0:
            strength = 0
        return strength

    def _on_passwords_changed(self, widget):
        self.infobar.hide()
        self.infotext.hide()
        new_password = self.new_password.get_text()
        confirm_password = self.confirm_password.get_text()
        current_password = self.current_password.get_text()
        strength = self.password_strength(new_password)
        if new_password != confirm_password:
            self.confirm_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_DIALOG_WARNING)
            self.confirm_password.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Passwords do not match"))
            self.set_response_sensitive(Gtk.ResponseType.OK, False)
        else:
            self.confirm_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, None)

        if self.password_check_contain_zh_cn(new_password) == True:
            self.new_password.set_text("")
            self.strengh_label.set_text(_("Your password should not contain Chinese"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_contain_zh_cn(confirm_password) == True:
            self.confirm_password.set_text("")
            self.strengh_label.set_text(_("Your password should not contain Chinese"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

#        elif self.password_check_space(new_password) == True:
#            self.strengh_label.set_text(_("Your password should not contain space"))
#            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
#            self.strengh_indicator.set_fraction(0)
#            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_len(new_password) != True:
            self.strengh_label.set_text(_("The length of your password should neither longer than 20 nor less than 8"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0.0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_username(new_password) == True:
            self.strengh_label.set_text(_("Your password should not be the same as your user name"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_realname(new_password) == True:
            self.strengh_label.set_text(_("Your password should not be the same as your user full name"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_contain_lower(new_password) != True:
            self.strengh_label.set_text(_("Your password is too easy, it should contain lowercase"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_contain_upper(new_password) != True:
            self.strengh_label.set_text(_("Your password is too easy, it should contain uppercase"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        elif self.password_check_contain_num(new_password) != True:
            self.strengh_label.set_text(_("Your password is too easy, it should contain number"))
            self.strengh_indicator.set_tooltip_text(_("Password is not available"))
            self.strengh_indicator.set_fraction(0)
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

        else:
            if strength < 0.6:
                self.strengh_indicator.set_tooltip_text(_("Password strength") + ": " + _("Weak"))
                self.strengh_indicator.set_fraction(0.2)
            elif strength < 0.75:
                self.strengh_indicator.set_tooltip_text(_("Password strength") + ": " + _("Fair"))
                self.strengh_indicator.set_fraction(0.4)
            elif strength < 0.9:
                self.strengh_indicator.set_tooltip_text(_("Password strength") + ": " + _("Good"))
                self.strengh_indicator.set_fraction(0.6)
            else:
                self.strengh_indicator.set_tooltip_text(_("Password strength") + ": " + _("Strong"))
                self.strengh_indicator.set_fraction(1.0)
            if ((new_password == current_password) or (confirm_password == current_password)):
                self.strengh_label.set_text(_("The new password is the same as old."))
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            elif ((new_password.lower() == current_password.lower()) or (confirm_password.lower() == current_password.lower())):
                self.strengh_label.set_text(_("new and old password must differ by more than just case"))
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            elif new_password != confirm_password:
                self.confirm_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_DIALOG_WARNING)
                self.confirm_password.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Passwords do not match"))
                self.strengh_label.set_text(_("Newpassword is ok, but the confirmation password is not the same as Newpassword"))
                self.set_response_sensitive(Gtk.ResponseType.OK, False)
            else:
                self.confirm_password.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, None)
                self.strengh_label.set_text(_("Your password is great"))
                self.check_passwords()

    def check_passwords(self):
        new_password = self.new_password.get_text()
        confirm_password = self.confirm_password.get_text()
        if new_password == confirm_password:
            self.set_response_sensitive(Gtk.ResponseType.OK, True)
        else:
            self.set_response_sensitive(Gtk.ResponseType.OK, False)

    def pam_conv(self, auth, query_list, userData):
        resp = []
        for i in range(len(query_list)):
            query, type = query_list[i]
            val = self.current_password.get_text()
            resp.append((val, 0))
        return resp
