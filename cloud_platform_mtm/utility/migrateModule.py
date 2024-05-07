from cloud_platform_mtm.utility import destination, source, utility

def migrateModuleResources(module: str, destination_path, source_path):
    module_name = "module." + module
    module_state = destination.getModuleState(source_path, module_name)

    destination_new_state = destination.mergeModuleState(destination_path, module_state, module)
    utility.save_state("core", destination_new_state)

    source_new_state = source.deleteModuleState(source_path, module_name)
    utility.save_state("components", source_new_state)
