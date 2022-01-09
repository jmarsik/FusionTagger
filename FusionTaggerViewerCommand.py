import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


# Class for a Fusion 360 Command
# Place your program logic here
# Delete the line that says "pass" for any method you want to use
class FusionTaggerViewerCommand(Fusion360CommandBase):

    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command, inputs, args, input_values):
        pass

    # Run after the command is finished.
    # Can be used to launch another command automatically or do other clean up.
    def on_destroy(self, command, inputs, reason, input_values):
        pass

    # Run when any input is changed.
    # Can be used to check a value and then update the add-in UI accordingly
    def on_input_changed(self, command_, command_inputs, changed_input, input_values):
        pass

    # Run when the user presses OK
    # This is typically where your main program logic would go
    def on_execute(self, command, inputs, args, input_values):

        ao = get_app_objects()

        attributes = ao['design'].findAttributes(input_values['attribute_group'], input_values['attribute_name'])
        selectedEntities = [s.entity for s in ao['ui'].activeSelections]

        if (len(selectedEntities) == 0):
            message_string = 'Found attributes in ALL entities:\n\n'
        else:
            message_string = 'Found attributes in SELECTED entities:\n\n'

        num_attrs = 0

        for attribute in attributes:
            if (len(selectedEntities) != 0 and not attribute.parent in selectedEntities):
                continue;

            message_string += attribute.groupName
            message_string += ' , '
            message_string += attribute.name
            message_string += ' , '
            message_string += attribute.value
            message_string += ' , '
            # SketchPoint for example does not have a name
            if hasattr(attribute.parent, 'name'):
                message_string += attribute.parent.name
                message_string += '\n'
            elif hasattr(attribute.parent, 'objectType'):
                message_string += '[' + str(attribute.parent.objectType) + ']\n'
            else:
                message_string += '[' + str(type(attribute.parent)) + ']\n'

            num_attrs = num_attrs + 1

        if (num_attrs == 0): message_string += 'No attributes found'            

        ao['ui'].messageBox(message_string)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI
    def on_create(self, command, command_inputs):

        command_inputs.addStringValueInput('attribute_group', 'Group', '')
        command_inputs.addStringValueInput('attribute_name', 'Name', '')
