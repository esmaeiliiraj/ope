#! python3

import numpy as np
import pandas as pd
import sklearn

import System
import clr

# Import RevitAPI
# clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
# clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = __revit__.ActiveUIDocument.Document

link_collector = FilteredElementCollector(doc).OfClass(RevitLinkInstance)

links = []
for link in link_collector:
	links.append(link.GetLinkDocument())



gen_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel).WhereElementIsNotElementType().ToElements()

workset_table = doc.GetWorksetTable()

opes = [ope for ope in gen_collector if "BMS_OPE" in ope.Symbol.FamilyName]

ope_data = []
for ope in opes[200:250]:
	params = []
	
	ope_id = ope.Id.IntegerValue
	
	try:
		ope_code = ope.LookupParameter("OPE Code").AsString()
	except:
		ope_code = None


	try:
		ope_description = ope.LookupParameter("OPE Description").AsString()
	except:
		ope_description = None
		

	try:
		ope_service = ope.LookupParameter("OPE Service Type").AsString()
	except:
		ope_service = None
	
	try:
		ope_workset = workset_table.GetWorkset(ope.WorksetId).Name
	except:
		ope_workset = None
		
	try:
		arch_walls_collector = FilteredElementCollector(links[0]).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
		intersect_filter = ElementIntersectsElementFilter(ope)
		clashing_wall = arch_walls_collector.WherePasses(intersect_filter).ToElements()
		
		if clashing_wall:
			wall_name = clashing_wall[0].Name
		
		else:
			struct_walls_collector = FilteredElementCollector(links[1]).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
			clashing_wall = struct_walls_collector.WherePasses(intersect_filter).ToElements()
			wall_name = clashing_wall[0].Name
	except:
		wall_name = None
	
	ope_data.append((ope_id, ope_code, ope_description, ope_service, ope_workset, wall_name))


data = pd.DataFrame(ope_data, columns=["Id", "Code", "Description", "Service", "Workset", "Wall"])
data.set_index("Id")
#data.to_csv("C:\\Users\\irajesmaeili\\Desktop\\MyExtensions\\MyFirstExtension.extension\\MyTools.tab\\MyTools.panel\\MyFirstCommand.pushbutton\\ope.csv", index=False)
print(data)