from flet import TextField, KeyboardType


class CreateInputs(TextField):
    def __init__(
        self,
        placeholder_input,
        text_size_input,
        text_align_input,
        offset_input=None,
        keyboard_type_input=KeyboardType.TEXT,
        autofocus_input=False,
        read_only_input=False,
        value_input=None,
    ):
        self.placeholder_input = placeholder_input
        self.text_size_input = text_size_input
        self.keyboard_type_input = keyboard_type_input
        self.text_align_input = text_align_input
        self.autofocus_input = autofocus_input
        self.read_only_input = read_only_input
        self.offset_input = offset_input
        self.value_input = value_input

    def _build(self):
        return super().__init__(
            hint_text=self.placeholder_input,
            keyboard_type=self.keyboard_type_input,
            autofocus=self.autofocus_input,
            read_only=self.read_only_input,
            text_size=self.text_size_input,
            text_align=self.text_align_input,
            offset=self.offset_input,
            value=self.value_input,
        )

    def change_state(self, page):
        """If the input is activated, it deactivates it and vice versa"""

        if not self.disabled:
            self.disabled = True

        else:
            self.disabled = False

        return page.update(self)

    def change_placeholder(self, new_placeholder):
        """
        This function changes the placeholder text of a widget.
        
        :param new_placeholder: The new text that will replace the current placeholder text in a user interface element, such as a text input field or a search bar
        """

        self.hint_text = new_placeholder

    def set_value(self, new_value):
        """
        This function sets a new value for a given object's attribute.
        
        :param new_value: The new value that will be assigned to the "value" attribute of the object that this method is called on
        """
        
        self.value = new_value
