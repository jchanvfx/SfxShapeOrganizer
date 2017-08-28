# Shape Organizer v1.1
# Compatibility: Silhouette v5.2 and up

# This Script will organise your roto shapes from one Layer into separate Layers
# based off each shapes color

# (c) 2016, Johnny Chan
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.

# * Neither the name of the Johnny Chan nor the names of its contributors
#   may be used to endorse or promote products derived from this software without
#   specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ------------------------------------------------------------------------------

import fx


class ShapeOrganizer(fx.Action):
    """
    This Script will organise your roto shapes from one Layer into
    separate Layers based off the shape colors.
    """

    def __init__(self):
        fx.Action.__init__(
            self, 'Shape Organizer', menu='Shape Tools', root='ChantasticVFX'
        )

    def available(self):
        session = fx.activeSession()
        assert session, "Select a Session"
        node = session.node(type="RotoNode")
        assert node, "The session does not contain a Roto Node"
        selection = fx.selection()
        assert len(selection) == 1, "There must be more than one selection."

    def execute(self):
        node = fx.activeNode()
        selection = fx.selection()[0]

        if selection.type == 'Layer':
            children = selection.children

            colorList = []
            colorGroup = {}
            shapeGroup = {}

            fx.beginUndo('Shape Organizer')

            # _new cloned parent layer.
            cloneLayer = selection.clone()
            cloneLayer.label = '{}_split 1'.format(cloneLayer.label.strip())
            fx.delete(cloneLayer.children)

            # _make color groups.
            for child in children:
                colorList.append(str(child.color))
                shapeGroup[child] = str(child.color)

            colorList = list(set(colorList))

            # _assign objects to sorted color group.
            for color in colorList:
                colorGroup[color] = []
                for object in shapeGroup.keys():
                    object.link = None
                    if shapeGroup[object] == color:
                        colorGroup[color].append(object)

            # _add objects with parent into session node.
            newSelection = []
            for grp in colorGroup.keys():
                newLayer = cloneLayer.clone()
                newLayer.label = fx.uniqueLabel(newLayer.label)
                newLayer.color = colorGroup[grp][0].color
                index = selection.parent.children.index(selection)

                newLayer.property('objects').addObjects(colorGroup[grp])
                node.property('objects').addObjects([newLayer], index + 1)
                newSelection.append(newLayer)

            # _keep original selection Yes/No
            msg = (
                'Keep Original Selection?<br/>'
                'Delete :: [ <span style="color:#FF00FF"><b>{}</b></span> ]'
                .format(selection.label)
            )

            if (fx.askQuestion(
                    msg, title='Keep Original', okText='Yes', cancelText='No')):
                selection.visible = False
            else:
                fx.delete([selection])

            fx.select(newSelection)
            fx.endUndo()
        else:
            msg = 'The selection must be a Layer.'
            fx.displayError(msg, title='selection error!')

fx.addAction(ShapeOrganizer())
