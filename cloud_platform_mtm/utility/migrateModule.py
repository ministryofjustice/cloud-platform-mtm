from cloud_platform_mtm.utility import destination, source, utility

def migrateModuleResources(module: str, destinationState, sourceState):
    moduleName = "module." + module
    moduleState = destination.getModuleState(sourceState, moduleName)

    destinationNewState = destination.mergeModuleState(destinationState, moduleState, module)
    utility.saveState("core", destinationNewState)

    sourceNewState = source.deleteModuleState(sourceState, moduleName)
    utility.saveState("components", sourceNewState)
