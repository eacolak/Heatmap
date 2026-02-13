from sdks.novavision.src.helper.package import PackageHelper
from components.Heatmap.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    OutputImage,
    HeatmapOutputs,
    HeatmapResponse,
    HeatmapExecutor,
    OutputData,
)


def build_response(context):
    outputImage = OutputImage(value=context.image)
    outputData = OutputData(value=context.image)
    Outputs = HeatmapOutputs(outputImage=outputImage, outputData=outputData)
    packageResponse = HeatmapResponse(outputs=Outputs)
    packageExecutor = HeatmapExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
