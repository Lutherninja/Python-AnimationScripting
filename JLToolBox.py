# Toolbox
import maya.cmds as cmds


class Toolbox():
    def __init__(self):
        self.window_name = "jlToolbox"

    def create(self):
        self.delete()

        self.window_name = cmds.window(self.window_name)
        self.m_column = cmds.columnLayout(p=self.window_name, adj=True)
        cmds.button(p=self.m_column,
                    label='Create Control',
                    c=lambda *args: self.createControl())
        self.color = cmds.textField(p=self.m_column)
        cmds.button(p=self.m_column,
                    label='Change Color',
                    command=lambda *args: self.colorBtn())
        self.randPos = cmds.textField(p=self.m_column)
        cmds.button(p=self.m_column,
                    label='Randomize',
                    command=lambda *args: self.randBtn())
        cmds.button(p=self.m_column,
                    label='Spawn Locator in center of selection',
                    command=lambda *args: self.spawnCenterLocator())
        cmds.button(p=self.m_column,
                    label='Spawn Locator in center of each',
                    command=lambda *args: self.spawnIndLocator())

        cmds.showWindow(self.window_name)

    def delete(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

    def colorBtn(self):
        value = cmds.textField(self.color, q=True, text=True)
        self.colorControl(value)
        cmds.textField(self.color, q=True, text='')

    def randBtn(self):
        parameters = cmds.textField(self.randPos, q=True, text=True)
        self.Randomizer(parameters)
        cmds.textField(self.randPos, q=True, text='')

    def colorControl(self, colorname):
        if colorname == 'yellow':
            color = 17
        elif colorname == 'blue':
            color = 6
        elif colorname == 'crimson':
            color = 4
        elif colorname =='dark green':
            color = 7
        elif colorname == 'purple':
            color = 8
        elif colorname == 'pink':
            color = 9
        elif colorname == 'brown':
            color = 10
        elif colorname == 'red':
            color = 13
        elif colorname == 'green':
            color = 14
        else:
            color = 5

        sels = cmds.ls(sl=True)

        for sel in sels:  # iterate through each selection
            shapes = cmds.listRelatives(sel, children=True, shapes=True)

            for shape in shapes:  # iterate through each shape
                cmds.setAttr('%s.overrideEnabled' % shape, True)
                cmds.setAttr('%s.overrideColor' % shape, color)

    def createControl(self):

        sels = cmds.ls(sl=True)

        if len(sels) > 0:
            for sel in sels:
                ctrl = cmds.circle()

                cmds.matchTransform(ctrl, sel)
            else:
                ctrl = cmds.circle()

    def spawnCenterLocator(self):

        sels = cmds.ls(sl=True)
        dups = cmds.duplicate(sels)
        dups = cmds.polyUnite(dups)

        bbox = cmds.exactWorldBoundingBox(dups)
        print bbox
        xMin = bbox[0]
        xMax = bbox[3]
        yMin = bbox[1]
        yMax = bbox[4]

        zMin = bbox[2]
        zMax = bbox[5]

        xMid = (xMin + xMax) / 2
        yMid = (yMin + yMax) / 2
        zMid = (zMin + zMax) / 2
        print xMid, yMid, zMid

        cmds.spaceLocator(p=(xMid, yMid, zMid))
        cmds.delete(dups, ch=True)
        cmds.delet(dups)

    def spawnIndLocator(self):
        sels = cmds.ls(sl=True)
        for comp in sels:
            bbox = cmds.exactWorldBoundingBox(comp)
            print bbox
            xMin = bbox[0]
            xMax = bbox[3]
            yMin = bbox[1]
            yMax = bbox[4]
            zMin = bbox[2]
            zMax = bbox[5]
            xMid = (xMin + xMax) / 2
            yMid = (yMin + yMax) / 2
            zMid = (zMin + zMax) / 2
            cmds.spaceLocator(p=(xMid, yMid, zMid))

    def Randomizer(self, xMax, xMin, yMax, yMin, zMax, zMin, num):
        sels = cmds.ls(sl=True)


        for i in range(num):
            # randomvalues
            dups = cmds.duplicate(sels)

            xRand = random.uniform(xMax, xMin)
            yRand = random.uniform(yMax, yMin)
            zRand = random.uniform(zMax, zMin)

            cmds.move(xRand, yRand, zRand, dups)



myTool = Toolbox()
myTool.create()