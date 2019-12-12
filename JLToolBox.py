# Toolbox
import maya.cmds as cmds
import random as random


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

        cmds.text('xMax')
        self.xMax = cmds.floatField(p=self.m_column)
        cmds.text('xMin')
        self.xMin = cmds.floatField(p=self.m_column)
        cmds.text('yMax')
        self.yMax = cmds.floatField(p=self.m_column)
        cmds.text('yMin')
        self.yMin = cmds.floatField(p=self.m_column)
        cmds.text('zMax')
        self.zMax = cmds.floatField(p=self.m_column)
        cmds.text('zMin')
        self.zMin = cmds.floatField(p=self.m_column)
        cmds.text('Number of Duplicates')
        self.num = cmds.intField(p=self.m_column)

        cmds.button(p=self.m_column,
                    label='Randomize',
                    command=lambda *args: self.randBtn())
        cmds.text('Name')
        self.a_name = cmds.textField(p=self.m_column)
        cmds.text('Padding')
        self.padding = cmds.intField(p=self.m_column)
        cmds.text('Suffix')
        self.a_suffix = cmds.textField(p=self.m_column)
        cmds.button(p=self.m_column,
                    label='Rename',
                    command=lambda *args: self.renameBtn())
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
        self.Randomizer(cmds.floatField(self.xMax, q=True, value=True),
                        cmds.floatField(self.xMin, q=True, value=True),
                        cmds.floatField(self.yMax, q=True, value=True),
                        cmds.floatField(self.yMin, q=True, value=True),
                        cmds.floatField(self.zMax, q=True, value=True),
                        cmds.floatField(self.zMin, q=True, value=True),
                        cmds.intField(self.num, q=True, value=True))
    def renameBtn(self):
        self.renameFunc(cmds.textField(self.a_name, q=True, text=True),
                        cmds.intField(self.padding, q=True, value=True),
                        cmds.textField(self.a_suffix, q=True, text=True))

    def colorControl(self, colorname):
        if colorname == 'yellow':
            color = 17
        elif colorname == 'blue':
            color = 6
        elif colorname == 'crimson':
            color = 4
        elif colorname == 'dark green':
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

    def renameFunc(self, a_name, a_padding, a_suffix):
        listObj = cmds.ls(sl=True)
        for count, obj in enumerate(listObj):
            cmds.rename(obj, a_name + "_" + str(count + 1).zfill(a_padding) + "_" + a_suffix)


myTool = Toolbox()
myTool.create()