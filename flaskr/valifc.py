import ifcopenshell
from ifcopenshell import geom


from flask import jsonify

from datetime import datetime



### IFC

def openifc(path):
# Open ifc into script
    m = ifcopenshell.open(path)
    return m

###
# DOES NOT WORK PROPERLY
def saveasbrep(model):
    settings = geom.settings()
    settings.set(settings.USE_BREP_DATA, True)
    spaces = (model.by_type('IfcWall'))
    for space in spaces:
        try:
            shape = geom.create_shape(settings, space)
            occ_shape = shape.geometry.brep_data
            with open("G:/Flask/Ondersteunend/cad/brep_dataavvas.brep", "a") as file:
                file.write(occ_shape)
        except:
            pass

    #shape = ifcopenshell.geom.create_shape(settings, spaces).geometry
    pp = 'pp'


    return pp
# DOES NOT WORK PROPERLY
def savetoifc(model):
    modelex = model.by_type('IfcWall')
    #modelex = model
    modelex.write('G:/Flask/Ondersteunend/cad/lol.ifc')

def read_geom(path):
    ifc_file = ifcopenshell.open(path)
    settings = geom.settings()
    for ifc_entity in ifc_file.by_type("IfcWall"):
        shape = geom.create_shape(settings, ifc_entity)
        # ios stands for IfcOpenShell
        ios_vertices = shape.geometry.verts
        ios_edges = shape.geometry.edges
        ios_faces = shape.geometry.faces
        # IfcOpenShell store vertices in a single tuple, same for edges and faces
        res = str(ios_vertices) + str(ios_edges) + str(ios_faces)

        return res



def validate(filefolder, filename):
    start = datetime.now()
    start_string = start.strftime("%d/%m/%Y %H:%M:%S")
    # Read ifc
    toread = filefolder + '/' + filename
    try:
        m = openifc(toread)
    except:
        return 'Error - could not read file'

    # Iniate dictionary for jsonify
    reportdict = {}

#==# 00 META
    reportdict['00_filename'] = filename
    projectname = str((m.by_type('IfcProject')[0])[2])
    reportdict['00_projectname'] = projectname
    reportdict['00_starttime'] = start_string

#==# 01 Validate IfcSpace
    ## DEV test for no space
    spacecount = len(m.by_type('IfcSpace'))
    if spacecount > 0:
        space = True
    else:
        space = False
    reportdict['01_IfcSpace'] = space
    reportdict['01_IfcSpace_count'] = spacecount

    temp = read_geom(toread)
    reportdict['02_rep'] = temp



    end = datetime.now()
    end_string = end.strftime("%d/%m/%Y %H:%M:%S")
    reportdict['00_endtime'] = end_string

    # returnfile = jsonify(reportdict)

    return reportdict

## VERVALLEN

#def validate(filefolder, filename):
#    # Create empty report txt
#    txtname = filename[:-4]
#    try:
#        create_rep(filefolder, txtname)
#    except:
#        return 'Could not create report'
#    # load ifc
#    toread = filefolder + '/' + filename
#    try:
#        m = openifc(toread)
#    except:
#        return 'Could not create report'
#    # Iniate lines, which is to write the report
#    lines = []
#    lines.append('Writing report for ' + filename)
#    lines.append('Start time:')
#    pa = (m.by_type('IfcSite')[0])[13]
#    sitepa = str(pa)
#
#    write_rep(filefolder, txtname, lines)
#    #returnfile = '/report/' + str(txtname) + '.txt'
#    reportdict = {}
#    returnfile = jsonify({"message": "messag", "severity": "danger"})
#    return returnfile



#def create_rep(filefolder, txtname):
#    n = filefolder + '/report/' + str(txtname) + '.txt'
#    f = open(n, 'w+')

#def write_rep(filefolder, txtname, lines):
#    n = filefolder + '/report/' + str(txtname) + '.txt'
#    with open(n, 'w') as f:
#        for line in lines:
#            f.writelines(line)
#            f.writelines("\n")
