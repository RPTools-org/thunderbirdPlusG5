#-*- coding:utf-8 -*
import controlTypes
import globalVars
import api
import winUser

# def isTBWindow() :
	# hwFG = winUser.getForegroundWindow()
	# title = winUser.getWindowText(hwFG)
	# return True if title.endswith("Thunderbird") else False
	
def getIA2Attr(obj,attribute_value=False,attribute_name ="id"):
	r= hasattr (obj,"IA2Attributes") and attribute_name in obj.IA2Attributes.keys ()
	if not r :return False
	r =obj.IA2Attributes[attribute_name]
	return r if not attribute_value  else r ==attribute_value

def getChildByRoleIDName(oParent, role, ID, name, idx=0) : # attention : controlTypes roles
	if not oParent    : 
		return None
	# ID can be the n first chars of the searched 
	try :  # except
		if idx > 0 : o = oParent.getChild(idx)
		else : o = oParent.firstChild
	except :
		# sharedVars.log(o, "Exception in getChildByRoleIDName")
		o = oParent.firstChild
		pass
	result = None
	while o:
		# sharedVars.log(o, "Loop begin")
		if o.role == role :
			# sharedVars.log(o, "Role matched")
			if ID == "" and name == ""  : 
				# sharedVars.log(o, "returned o Empty ID and name matched")
				return o
			if ID :
				objID = str(getIA2Attr(o))
				if objID.startswith(ID) : 
					# sharedVars.log(o, "returned o  ID matched")
					return o
			elif name and hasattr(o, "name") and o.name.startswith(name) :
				# sharedVars.log(o, "Name matched")
				return  o
			else :
				# sharedVars.log(o, "returned o Only Role matched")
				return o
		o = o.next
		idx += 1
		# end while
		# sharedVars.logte("Not found in getChildByRoleIDName : role={}, ID={}, name={}".format(role.name, ID, name))
	return None

def getPropertyPage(force=False) :
	if not force and globalVars.TBPropertyPage :
			return globalVars.TBPropertyPage
	# else search propertypage
	o = api.getForegroundObject()
	# IA2ID = tabpanelcontainer in , Role.GROUPING
	if o : o = getChildByRoleIDName(o, controlTypes.Role.GROUPING, ID="tabpanelcontainer", name="", idx=36)
	# IA2ID = mail3PaneTab1 in , Role.PROPERTYPAGE
	if o : globalVars.TBPropertyPage = getChildByRoleIDName(o, controlTypes.Role.PROPERTYPAGE, ID="mail3PaneTab1", name="", idx=2)
	# sharedVars.log(globalVars.TBPropertyPage, "gETPropertyPage globalVars.TBPropertyPage")
	return globalVars.TBPropertyPage