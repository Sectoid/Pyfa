# Used by:
# Implants named like: Halo (18 of 18)
# Implants named like: Low grade Halo (12 of 12)
runTime = "early"
type = "passive"
def handler(fit, implant, context):
    fit.implants.filteredItemMultiply(
        lambda implant: "signatureRadiusBonus" in implant.itemModifiedAttributes and "implantSetAngel" in implant.itemModifiedAttributes,
        "signatureRadiusBonus",
        implant.getModifiedItemAttr("implantSetAngel"))