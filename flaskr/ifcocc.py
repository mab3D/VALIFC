# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
import ifcopenshell
import ifcopenshell.geom


#def show():
#    settings = geom.settings()
#    #settings.set(settings.USE_PYTHON_OPENCASCADE, True)
#
#    # Initialize a graphical display window
#    occ_display = geom.occ_utils.initialize_display()
#    ifc_file = ifcopenshell.open("G:/Flask/Ondersteunend/TeUploade/IFC Schependomlaan.ifc")
#
#
#    products = ifc_file.by_type("IfcProduct")
#    for product in products:
#        if product.is_a("IfcOpeningElement"): continue
#        if product.Representation:
#            shape = geom.create_shape(settings, product).geometry
#            display_shape = geom.utils.display_shape(shape)
#            if product.is_a("IfcPlate"):
#                # Plates are the transparent parts of the window assembly
#                # in the IfcOpenHouse model
#                geom.utils.set_shape_transparency(display_shape, 0.8)
#
#    #It will disappear soon, so let's loop here
#    ifcopenshell.geom.utils.main_loop()


def show(m):
    f = ifcopenshell.open(m)
    ifcopenshell.geom.utils.initialize_display()
    #settings = ifcopenshell.geom.settings()
    # settings = ifcopenshell.geom.settings(USE_PYTHON_OPENCASCADE=True)
    settings = settings.set(settings.use_python_opencascade, true)
    for item in ifcopenshell.geom.iterate(
        settings, f, exclude=["IfcSpace", "IfcOpeningElement"]
    ):
        ifcopenshell.geom.utils.display_shape(item)
    ifcopenshell.geom.utils.main_loop()
