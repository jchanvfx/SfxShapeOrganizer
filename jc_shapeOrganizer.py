# -------------------------------------------------------------------------------
# Shape Organizer v1.0
# (c) 2014 Johnny Chan  - www.picostyle.com
# For bugs please email me at johnny@picostyle.com
# Compatibility: Silhouette v5.1.1 and up, not tested in previous versions
# -------------------------------------------------------------------------------
#
# This Script will organise your roto shapes from one Layer into separate Layers based off each shapes color
#
# -------------------------------------------------------------------------------

import fx

class jc_shapeOrganizer(fx.Action):
    """This Script will organise your roto shapes from one Layer into separate Layers based off each shapes color.
"""

    def __init__(self):
        fx.Action.__init__(self, 'Shape Tools|Shape Organizer' , root='PicoStyle')

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

            fx.beginUndo('jc Shape Organizer')

            # _new cloned parent layer.
            cloneLayer = selection.clone()
            cloneLayer.label = '%s_split 1' %(cloneLayer.label.strip())
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
                    if shapeGroup[object] == color:
                        colorGroup[color].append(object)


            # _add objects with parent into session node.
            newSelection = []
            for grp in colorGroup.keys():
                newLayer = cloneLayer.clone()
                newLayer.label = fx.uniqueLabel(newLayer.label)
                newLayer.color = colorGroup[grp][0].color

                newLayer.property('objects').addObjects(colorGroup[grp])
                node.property('objects').addObjects([newLayer])
                newSelection.append(newLayer)


            # _keep original selection Yes/No
            msg = 'Do you want to delete your original selection?<br/>Delete :: [ <span style="color:#FF00FF"><b>%s</b></span> ]' %(selection.label)
            if (fx.askQuestion(msg, title='Keep Original', okText='Yes', cancelText='No')):
                fx.delete([selection])
            else:
                selection.visible = False

            fx.select(newSelection)
            fx.endUndo()

        else:
            msg = 'The selection must be a Layer.'
            fx.displayError(msg, title='selection error!')

fx.addAction(jc_shapeOrganizer())