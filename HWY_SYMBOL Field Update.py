#Maps

fc = 'Highways'
fields = arcpy.ListFields(fc)
fieldName = 'HWY_SYMBOL'

#When skiping an optional parameter or keep its default setting, exclude it from the Python syntax, add an empty pair of quotation marks (""), or add a hashtag enclosed by quotation marks ("#"). In this case, you excluded text for several optional parameters (expression type, code_block, field_type, and enforce_domains) in order to use default settings for these parameters. 

for field in fields:
    if field.name == fieldName:
        arcpy.management.CalculateField(fc, fieldName, "'Highway ' + !HWY_SYMBOL!")
    else:
        pass


